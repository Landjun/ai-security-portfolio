"""
ai_coding_helper.py —— AI 编程小助手 MVP(对标 LangChain4j 教程,用 Python 复刻)。

对标教程的核心能力(本 MVP 已落地的部分):
    ChatModel      -> DeepSeek 对话模型(OpenAI 兼容,设 base_url)
    SystemMessage  -> SYSTEM_PROMPT,定义"编程学习导师"的人设与边界
    AI Service     -> AiCodingHelper 类,把"模型 + 记忆 + 系统提示"封装成一个服务
    ChatMemory     -> ChatMemory 滑动窗口记忆,按 session_id 多会话隔离(对标 @MemoryId)
    流式输出        -> stream=True,逐字打印(对标教程的 SSE 流式)

教程里更进阶的 RAG / 工具调用 / 护栏 / Web 前端,见 README 的「下一步路线图」,后续迭代加入。

运行:
    python ai_coding_helper.py            # 进入交互式对话(默认会话)
    python ai_coding_helper.py "你的问题"  # 单轮提问后退出

需要:本目录放一个 .env,内含 DEEPSEEK_API_KEY(见 .env.example)。
"""

import os
import sys
from collections import defaultdict, deque

from dotenv import load_dotenv
from openai import OpenAI

# —— 配置 ——
CHAT_MODEL = "deepseek-chat"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MEMORY_WINDOW = 20  # 每个会话最多记住最近 N 条消息(对标 MessageWindowChatMemory)

# 系统提示词:定义编程小助手的人设、风格与边界(对标教程的 SystemMessage)
SYSTEM_PROMPT = (
    "你是一名资深编程学习导师,名叫『码小安』,专长是带零基础的人入门编程与 AI 开发。"
    "回答要求:1) 先给最小可运行的思路或代码,再解释原理;"
    "2) 代码要简短、带注释、能直接跑;3) 主动指出常见坑和下一步该学什么;"
    "4) 只回答编程、计算机、AI 开发与求职相关的问题,无关问题礼貌拒绝并引导回正题。"
)


class ChatMemory:
    """
    滑动窗口会话记忆:按 session_id 隔离多个会话,每个会话只保留最近 N 条消息。
    对标 LangChain4j 的 MessageWindowChatMemory + @MemoryId 多会话能力。
    """

    def __init__(self, window: int = MEMORY_WINDOW):
        self.window = window
        self._store = defaultdict(lambda: deque(maxlen=window))

    def add(self, session_id: str, role: str, content: str) -> None:
        self._store[session_id].append({"role": role, "content": content})

    def history(self, session_id: str) -> list:
        return list(self._store[session_id])

    def clear(self, session_id: str) -> None:
        self._store.pop(session_id, None)


class AiCodingHelper:
    """AI 服务:把『模型 + 系统提示 + 会话记忆』封装成一个可复用的服务对象。"""

    def __init__(self):
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise SystemExit(
                "未找到 DEEPSEEK_API_KEY。请在本目录创建 .env 并填入 key(见 .env.example)。"
            )
        self.client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
        self.memory = ChatMemory()

    def chat(self, session_id: str, user_input: str, stream: bool = True) -> str:
        """
        一轮对话:系统提示 + 该会话历史 + 本次输入 -> 模型作答 -> 把问答写回记忆。
        stream=True 时逐字打印(流式),返回拼好的完整答案。
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.memory.history(session_id))
        messages.append({"role": "user", "content": user_input})

        if stream:
            answer = self._chat_stream(messages)
        else:
            resp = self.client.chat.completions.create(
                model=CHAT_MODEL, messages=messages, temperature=0.3
            )
            answer = resp.choices[0].message.content

        # 写回记忆:本轮的提问和回答都进入该会话的窗口
        self.memory.add(session_id, "user", user_input)
        self.memory.add(session_id, "assistant", answer)
        return answer

    def _chat_stream(self, messages: list) -> str:
        """流式调用:逐 chunk 打印并拼接出完整答案。"""
        chunks = []
        resp = self.client.chat.completions.create(
            model=CHAT_MODEL, messages=messages, temperature=0.3, stream=True
        )
        for piece in resp:
            delta = piece.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                chunks.append(delta)
        print()  # 换行收尾
        return "".join(chunks)


def interactive(helper: AiCodingHelper) -> None:
    """交互式对话循环。输入 exit/quit 退出,输入 /clear 清空当前会话记忆。"""
    session_id = "cli-default"
    print("码小安 已就绪。输入问题开始对话;exit 退出,/clear 清空记忆。")
    print("-" * 60)
    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            return
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("再见。")
            return
        if user_input == "/clear":
            helper.memory.clear(session_id)
            print("(已清空当前会话记忆)")
            continue
        print("码小安: ", end="", flush=True)
        helper.chat(session_id, user_input, stream=True)
        print("-" * 60)


def main():
    load_dotenv()  # 从当前目录的 .env 读取 DEEPSEEK_API_KEY
    helper = AiCodingHelper()

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(f"你: {question}")
        print("码小安: ", end="", flush=True)
        helper.chat("cli-oneshot", question, stream=True)
    else:
        interactive(helper)


if __name__ == "__main__":
    main()
