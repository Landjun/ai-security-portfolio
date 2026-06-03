"""
agent.py —— 真实 Agent:DeepSeek function calling 工具调用循环。

运行:  python agent.py
       python agent.py "查一下订单 A1001"

循环逻辑(ReAct 的核心):
    用户提问
      -> 把问题 + 工具清单发给 DeepSeek
      -> 模型决定:要么直接回答,要么"请求调用某个工具"
      -> 若请求调工具:本地执行该工具,把结果回填
      -> 再发给模型 -> 直到模型给出最终自然语言答案

需要:06 的 real-rag-system/.env 里有 DEEPSEEK_API_KEY(本项目复用同一个 key)。
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOL_SCHEMAS, dispatch

CHAT_MODEL = "deepseek-chat"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MAX_STEPS = 5   # 防止无限循环

SYSTEM = (
    "你是电商客服 Agent。可以使用提供的工具来查询订单、查政策、发起退款。"
    "需要数据时请调用工具,不要编造;最终用简洁中文回答用户。"
)


def _client():
    # 复用 real-rag-system 目录下的 .env(同一个 DeepSeek key)
    here = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(here), "real-rag-system", ".env")
    load_dotenv(env_path)
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        raise SystemExit(f"未找到 DEEPSEEK_API_KEY,请确认 {env_path} 中已配置。")
    return OpenAI(api_key=key, base_url=DEEPSEEK_BASE_URL)


def run_agent(question: str) -> str:
    client = _client()
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]

    for step in range(1, MAX_STEPS + 1):
        resp = client.chat.completions.create(
            model=CHAT_MODEL, messages=messages,
            tools=TOOL_SCHEMAS, tool_choice="auto", temperature=0.2,
        )
        msg = resp.choices[0].message

        # 模型没有要求调工具 -> 已经是最终答案
        if not msg.tool_calls:
            return msg.content

        # 把模型这条"要调工具"的消息原样加入对话历史
        messages.append(msg)

        # 逐个执行模型请求的工具,并回填结果
        for tc in msg.tool_calls:
            name = tc.function.name
            args = tc.function.arguments
            result = dispatch(name, args)
            print(f"  [第{step}步] 模型决定调用工具: {name}({args}) -> {result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })

    return "(已达到最大步数,未得到最终答案)"


def main():
    if len(sys.argv) > 1:
        questions = [" ".join(sys.argv[1:])]
    else:
        questions = [
            "帮我查一下订单 A1001 的状态",
            "订单 A1001 我想退款 50 元,帮我办一下",
            "你们的退货政策是怎样的?",
        ]

    for q in questions:
        print("=" * 64)
        print(f"用户: {q}")
        print("-" * 64)
        answer = run_agent(q)
        print(f"\nAgent 最终回答: {answer}\n")


if __name__ == "__main__":
    main()
