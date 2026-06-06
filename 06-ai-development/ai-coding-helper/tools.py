"""
tools.py —— 「码小安」的工具集 + 权限审计关卡(对标教程的 Tools / function calling）。

两个工具刻意覆盖两种风险等级,用来演示「Agent 调工具时如何做安全控制」:
    search_knowledge_base  只读检索知识库      -> 放行(ALLOW)
    save_learning_note     写本地笔记文件      -> 敏感动作,需人工确认(APPROVAL)

安全核心:工具执行前先过权限审计(复用 03 tool-permission-audit),
而不是依赖模型自觉。未注册的工具按最小权限默认拒绝。
"""

import json
import os
import sys

# 复用 03 的权限审计器(AI 开发 × AI 安全)
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "tool-permission-audit"))
import policy as pol          # noqa: E402
from auditor import audit     # noqa: E402

from knowledge_base import DOCUMENTS  # noqa: E402

# 注册本助手工具的权限策略(未注册的工具 -> 审计器默认拒绝)
pol.POLICY["search_knowledge_base"] = {"action": pol.ALLOW}
pol.POLICY["save_learning_note"] = {"action": pol.APPROVAL}

NOTES_FILE = os.path.join(_HERE, "notes.md")


# —— 工具实现 ——
def search_knowledge_base(keyword: str) -> str:
    """在知识库里按关键词检索条目(只读)。"""
    kw = (keyword or "").lower()
    hits = [d for d in DOCUMENTS
            if kw in d["title"].lower() or kw in d["content"].lower()]
    if not hits:
        return f"知识库中未找到与『{keyword}』相关的条目。"
    return "\n".join(f"[{d['id']}] {d['title']}:{d['content']}" for d in hits[:3])


def save_learning_note(content: str) -> str:
    """把一条学习笔记追加保存到本地 notes.md(写操作,敏感)。"""
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"- {content}\n")
    return f"已保存学习笔记到 {os.path.basename(NOTES_FILE)}。"


_IMPL = {
    "search_knowledge_base": search_knowledge_base,
    "save_learning_note": save_learning_note,
}

# 工具 schema(交给 DeepSeek 让它决定何时调用)
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "在编程/面试知识库中按关键词检索资料,用于回答事实性问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "检索关键词,如『二分查找』『RAG』"}
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_learning_note",
            "description": "当用户明确要求『记下来/保存笔记』时,把一条学习笔记保存到本地文件。",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "要保存的笔记内容"}
                },
                "required": ["content"],
            },
        },
    },
]


def _default_confirm(name: str, args: dict, reason: str) -> bool:
    """默认人工确认:命令行下询问 y/n。"""
    print(f"\n  [需人工确认] {reason}")
    print(f"  即将执行:{name}({args})")
    try:
        return input("  确认执行?(y/N): ").strip().lower() == "y"
    except (EOFError, KeyboardInterrupt):
        return False


def dispatch(name: str, arguments, confirm=_default_confirm) -> str:
    """
    统一工具入口:解析参数 -> 过权限审计 -> (敏感则人工确认) -> 执行。
    confirm 为 (name, args, reason) -> bool 的回调,APPROVAL 时调用。
    """
    try:
        args = json.loads(arguments) if isinstance(arguments, str) else (arguments or {})
    except json.JSONDecodeError:
        args = {}

    decision, reason = audit(name, args)
    if decision == pol.DENY:
        return f"[审计拒绝] {reason}"
    if decision == pol.APPROVAL:
        if not confirm(name, args, reason):
            return f"[已取消] 敏感操作未获人工确认:{reason}"

    fn = _IMPL.get(name)
    if fn is None:
        return f"[错误] 未知工具:{name}"
    try:
        return fn(**args)
    except TypeError as e:
        return f"[错误] 工具参数不匹配:{e}"


def _self_test():
    """离线自测:不调模型,直接验证审计关卡。"""
    # 只读工具放行
    r1 = dispatch("search_knowledge_base", {"keyword": "二分查找"})
    assert "二分查找" in r1, r1
    # 敏感写工具:确认通过则执行
    r2 = dispatch("save_learning_note", {"content": "自测笔记"}, confirm=lambda *a: True)
    assert "已保存" in r2, r2
    # 敏感写工具:拒绝确认则取消
    r3 = dispatch("save_learning_note", {"content": "x"}, confirm=lambda *a: False)
    assert "已取消" in r3, r3
    # 未注册工具:默认拒绝
    r4 = dispatch("rm_rf", {})
    assert "审计拒绝" in r4, r4
    print("tools 自测通过:只读放行 / 敏感需确认 / 未注册默认拒绝 均正确")


if __name__ == "__main__":
    _self_test()
