"""
observability.py —— 「码小安」的日志与可观测性(对标教程「日志和可观测性」章节)。

提供三件事,让线上 AI 服务"看得见":
    1) 结构化日志:每轮对话落一条 JSON 行到 logs/coding_helper.jsonl(可被 ELK/Loki 采集)
    2) 关键指标:延迟、prompt/completion/总 token、预估成本、模式、RAG 命中数、工具调用数
    3) 聚合统计:summarize() 读日志算出 总轮次/平均延迟/总 token/总成本(给 /api/metrics)

token 用量优先取模型返回的 usage;流式拿不到时用字符启发式估算(标注 estimated=True)。
"""

import json
import os
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(_HERE, "logs")
LOG_FILE = os.path.join(LOG_DIR, "coding_helper.jsonl")

# DeepSeek 计费(元/百万 token)。示例值,请以官网最新价为准。
PRICE_INPUT_PER_M = 2.0
PRICE_OUTPUT_PER_M = 8.0


def estimate_tokens(text: str) -> int:
    """字符启发式估算 token(CJK 约 1 字 1 token,其他约 4 字符 1 token)。"""
    text = text or ""
    cjk = sum(1 for ch in text if "一" <= ch <= "鿿")
    other = len(text) - cjk
    return cjk + max(0, other // 4)


def estimate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    """按 token 估算成本(元),保留 6 位小数。"""
    cost = (prompt_tokens / 1_000_000) * PRICE_INPUT_PER_M \
        + (completion_tokens / 1_000_000) * PRICE_OUTPUT_PER_M
    return round(cost, 6)


def log_turn(record: dict) -> dict:
    """把一条对话指标记录追加为 JSON 行;并补上成本字段。"""
    record.setdefault("cost_cny", estimate_cost(
        record.get("prompt_tokens", 0), record.get("completion_tokens", 0)))
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def console_line(record: dict) -> str:
    """一行人类可读的指标摘要(给 --trace 在控制台打印)。"""
    return (f"[trace] mode={record.get('mode')} "
            f"latency={record.get('latency_s')}s "
            f"tokens={record.get('total_tokens')}"
            f"(in {record.get('prompt_tokens')}/out {record.get('completion_tokens')}"
            f"{' est' if record.get('estimated') else ''}) "
            f"cost={record.get('cost_cny')}元 "
            f"rag_hits={record.get('rag_hits')} tool_calls={record.get('tool_calls')}")


class Timer:
    """上下文管理器:计时,退出后 .seconds 可读。"""

    def __enter__(self):
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.seconds = round(time.perf_counter() - self._t0, 3)


def summarize(limit: int = 1000) -> dict:
    """读取日志做聚合统计(给 /api/metrics 或离线分析)。"""
    if not os.path.exists(LOG_FILE):
        return {"turns": 0}
    rows = []
    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    rows = rows[-limit:]
    n = len(rows)
    if n == 0:
        return {"turns": 0}
    return {
        "turns": n,
        "avg_latency_s": round(sum(r.get("latency_s", 0) for r in rows) / n, 3),
        "total_tokens": sum(r.get("total_tokens", 0) for r in rows),
        "total_cost_cny": round(sum(r.get("cost_cny", 0) for r in rows), 6),
        "blocked_turns": sum(1 for r in rows if r.get("blocked")),
    }


def _self_test():
    """离线自测:不调模型,验证估算/记账/聚合。"""
    assert estimate_tokens("你好world") >= 2
    assert estimate_cost(1_000_000, 0) == PRICE_INPUT_PER_M
    rec = log_turn({"mode": "test", "latency_s": 0.1, "prompt_tokens": 10,
                    "completion_tokens": 5, "total_tokens": 15})
    assert rec["cost_cny"] >= 0
    s = summarize()
    assert s["turns"] >= 1
    print("observability 自测通过:token 估算 / 成本记账 / 日志聚合 均正确")


if __name__ == "__main__":
    _self_test()
