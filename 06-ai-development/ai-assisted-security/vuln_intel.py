"""
vuln_intel.py —— AI 辅助漏洞情报分析(回应 JD:"批量分析漏洞公告并生成验证思路")。

把漏洞公告/CVE 描述交给大模型,结构化提取:受影响组件/版本、漏洞类型、利用前提、
危害、修复建议、以及【合规的验证思路】(只给授权环境下的验证方向,不给攻击 PoC)。

运行:  python vuln_intel.py
依赖:复用 06/real-rag-system/.env 的 DEEPSEEK_API_KEY;无 key 时给出离线提示。
"""

import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
_ENV = os.path.join(_ROOT, "06-ai-development", "real-rag-system", ".env")

# 示例漏洞公告(可换成真实公告文本批量处理)
ADVISORIES = [
    "某开源 Web 框架 X 1.2.0-1.4.3 版本存在反序列化漏洞,攻击者向 /api/import 接口"
    "提交构造的序列化数据可导致远程代码执行。已在 1.4.4 修复。",
    "某 AI Agent 框架 Y 的工具调用模块未对用户提供的 URL 做校验,存在 SSRF,"
    "可访问内网与云元数据。建议升级到最新版并启用 URL 白名单。",
]

PROMPT = """你是漏洞情报分析助手。请把下面的漏洞公告结构化,只输出 JSON,字段:
component(受影响组件)、versions(受影响版本)、vuln_type(漏洞类型)、
precondition(利用前提)、impact(危害)、fix(修复建议)、
verify_idea(在【授权测试环境】下的合规验证方向,只给方向不给攻击代码)。
公告:%s"""


def _client():
    try:
        from dotenv import load_dotenv
        load_dotenv(_ENV)
        key = os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            return None
        from openai import OpenAI
        return OpenAI(api_key=key, base_url="https://api.deepseek.com")
    except Exception:
        return None


def analyze(client, text):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": PROMPT % text}],
        temperature=0.1,
    )
    return resp.choices[0].message.content.strip()


def main():
    client = _client()
    print("=" * 64)
    print("AI 辅助漏洞情报分析" + ("" if client else "(未检测到 API Key,仅展示流程)"))
    print("=" * 64)
    if client is None:
        print("\n配置 06/real-rag-system/.env 的 DEEPSEEK_API_KEY 后,可对每条公告自动产出:")
        print("  component / versions / vuln_type / precondition / impact / fix / verify_idea")
        return
    for i, adv in enumerate(ADVISORIES, 1):
        print(f"\n--- 公告 {i} ---\n{adv}\n结构化结果:")
        out = analyze(client, adv)
        print(out)


if __name__ == "__main__":
    main()
