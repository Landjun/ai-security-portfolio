"""
ai_audit.py —— AI 辅助代码审计(回应 JD:"用 AI 提升代码审计效率")。

混合方案:先用静态扫描器(agent-code-audit/audit_scan.py)快速定位危险点,
再把代码交给大模型做语义级审计(解释成因、补充扫描器漏掉的逻辑漏洞、给修复)。
人 + 静态 + AI 三者结合,比纯人工快、比纯工具准。

运行:  python ai_audit.py <代码文件>
       python ai_audit.py    # 默认审计 agent-code-audit/vulnerable_agent.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
_ENV = os.path.join(_ROOT, "06-ai-development", "real-rag-system", ".env")
_DEFAULT = os.path.join(_ROOT, "03-agent-rag-security", "agent-code-audit", "vulnerable_agent.py")
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "agent-code-audit"))

PROMPT = """你是资深代码审计专家。审计下面的 Python 代码,找出安全漏洞。
对每个漏洞输出:行号(估计)、漏洞类型、风险说明、修复建议。按风险从高到低排序,简洁。
代码:
```python
%s
```"""


def static_findings(path):
    """先跑静态扫描器,拿到快速定位结果。"""
    try:
        from audit_scan import scan
        return scan(path)
    except Exception:
        return []


def ai_audit(path):
    try:
        from dotenv import load_dotenv
        load_dotenv(_ENV)
        key = os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            return None
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
        with open(path, encoding="utf-8") as f:
            code = f.read()
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": PROMPT % code}],
            temperature=0.1,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"(AI 审计未执行:{e})"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else _DEFAULT
    print("=" * 64)
    print(f"AI 辅助代码审计:{os.path.basename(path)}")
    print("=" * 64)

    print("\n[1/2] 静态扫描快速定位:")
    sf = static_findings(path)
    for ln, sev, cat, desc, code in sf:
        print(f"  L{ln} ({sev}) {cat}")
    print(f"  小计 {len(sf)} 处")

    print("\n[2/2] AI 语义审计(补充成因/逻辑漏洞/修复):")
    out = ai_audit(path)
    if out is None:
        print("  未检测到 DEEPSEEK_API_KEY,跳过 AI 审计(静态结果已给出)。")
    else:
        print(out)

    print("\n结论:静态扫描定位入口 + AI 语义审计补充,组合提升代码审计效率与覆盖。")


if __name__ == "__main__":
    main()
