"""
ai_coding_helper.py —— AI 编程小助手 MVP(对标 LangChain4j 教程,用 Python 复刻)。

对标教程的核心能力(本项目已落地的部分):
    ChatModel      -> DeepSeek 对话模型(OpenAI 兼容,设 base_url)
    SystemMessage  -> SYSTEM_PROMPT,定义"编程学习导师"的人设与边界
    AI Service     -> AiCodingHelper 类,把"模型 + 记忆 + 系统提示 + 检索"封装成一个服务
    ChatMemory     -> ChatMemory 滑动窗口记忆,按 session_id 多会话隔离(对标 @MemoryId)
    RAG            -> 可选挂载 Retriever,检索知识库后把资料拼进提示(检索/生成解耦)
    Tools          -> --tools 走 function calling,工具执行前过权限审计
    Guardrail      -> --safe 输入拦提示注入 + 输出 DLP 脱敏(复用 02 安全模块)
    流式输出        -> stream=True,逐字打印(对标教程的 SSE 流式)

教程里更进阶的 Web 前端,见 README 的「下一步路线图」,后续迭代加入。

运行:
    python ai_coding_helper.py                 # 交互式对话(默认会话)
    python ai_coding_helper.py "你的问题"       # 单轮提问后退出
    python ai_coding_helper.py --rag           # 开启 RAG
    python ai_coding_helper.py --tools         # 开启工具调用
    python ai_coding_helper.py --safe          # 开启安全护栏(输入/输出)
    # 开关可组合,如: python ai_coding_helper.py --rag --safe "你的问题"

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
MAX_TOOL_STEPS = 5  # 工具调用循环最大步数,防止无限循环

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
    """AI 服务:把『模型 + 系统提示 + 会话记忆 + (可选)检索』封装成一个可复用的服务对象。"""

    def __init__(self, retriever=None, use_tools=False, guardrails=False, trace=False):
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise SystemExit(
                "未找到 DEEPSEEK_API_KEY。请在本目录创建 .env 并填入 key(见 .env.example)。"
            )
        self.client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
        self.memory = ChatMemory()
        self.retriever = retriever  # 传入则启用 RAG;为 None 则纯对话
        self.use_tools = use_tools  # 开启则走 function calling 工具调用循环
        self.guardrails = guardrails  # 开启则启用输入/输出安全护栏
        self.trace = trace  # 开启则把每轮指标也打印到控制台

    def _mode_str(self) -> str:
        """当前模式串,写进日志便于分组统计。"""
        parts = []
        if self.retriever is not None:
            parts.append("rag")
        if self.use_tools:
            parts.append("tools")
        if self.guardrails:
            parts.append("safe")
        return "+".join(parts) if parts else "chat"

    @staticmethod
    def _usage_dict(usage):
        """把 SDK 的 usage 对象规整成 dict;拿不到返回 None。"""
        if not usage:
            return None
        return {
            "prompt_tokens": getattr(usage, "prompt_tokens", 0) or 0,
            "completion_tokens": getattr(usage, "completion_tokens", 0) or 0,
            "total_tokens": getattr(usage, "total_tokens", 0) or 0,
        }

    def _record(self, session_id, user_input, answer, usage, latency_s,
                rag_hits=0, tool_calls=0, blocked=False):
        """落一条可观测性记录:延迟 + token + 成本 + 模式 + RAG/工具计数。"""
        import observability as obs
        if usage:
            pt, ct = usage["prompt_tokens"], usage["completion_tokens"]
            tt = usage.get("total_tokens", pt + ct)
            estimated = False
        else:  # 流式拿不到 usage 时用字符启发式估算
            pt = obs.estimate_tokens(user_input)
            ct = obs.estimate_tokens(answer)
            tt = pt + ct
            estimated = True
        rec = obs.log_turn({
            "session_id": session_id, "mode": self._mode_str(),
            "latency_s": latency_s, "prompt_tokens": pt, "completion_tokens": ct,
            "total_tokens": tt, "estimated": estimated,
            "rag_hits": rag_hits, "tool_calls": tool_calls, "blocked": blocked,
        })
        if self.trace:
            print(obs.console_line(rec))
        return rec

    def _guard_input(self, user_input: str):
        """输入护栏:命中提示注入则返回拦截语,否则返回 None。"""
        if not self.guardrails:
            return None
        from guardrails import check_input
        ok, matched = check_input(user_input)
        if not ok:
            return f"【输入护栏拦截】检测到疑似提示注入,已拒绝。命中特征数:{len(matched)}"
        return None

    def _guard_output(self, text: str) -> str:
        """输出护栏:对模型输出做 DLP 脱敏。"""
        if not self.guardrails:
            return text
        from guardrails import filter_output
        safe, hits = filter_output(text)
        if hits:
            safe += f"\n(输出护栏:已脱敏 {', '.join(hits)})"
        return safe

    def chat(self, session_id: str, user_input: str, stream: bool = True) -> str:
        """
        一轮对话:系统提示 +(可选)检索资料 + 该会话历史 + 本次输入 -> 模型作答 -> 写回记忆。
        开启工具时走工具调用循环;否则按 stream 流式/非流式直接作答。
        """
        import observability as obs

        # 输入护栏:疑似提示注入直接拦截,根本不喂给模型
        blocked = self._guard_input(user_input)
        if blocked is not None:
            print(blocked)
            self._record(session_id, user_input, blocked, None, 0.0, blocked=True)
            return blocked

        if self.use_tools:
            return self._chat_with_tools(session_id, user_input)

        messages, rag_hits = self._build_messages(session_id, user_input)

        usage = None
        with obs.Timer() as t:
            # 开启输出护栏时改用非流式:拿到完整输出后做 DLP 脱敏再打印
            if self.guardrails:
                resp = self.client.chat.completions.create(
                    model=CHAT_MODEL, messages=messages, temperature=0.3
                )
                usage = self._usage_dict(resp.usage)
                answer = self._guard_output(resp.choices[0].message.content)
                print(answer)
            elif stream:
                answer, usage = self._chat_stream(messages)
            else:
                resp = self.client.chat.completions.create(
                    model=CHAT_MODEL, messages=messages, temperature=0.3
                )
                usage = self._usage_dict(resp.usage)
                answer = resp.choices[0].message.content

        # 写回记忆:本轮的提问和回答都进入该会话的窗口
        self.memory.add(session_id, "user", user_input)
        self.memory.add(session_id, "assistant", answer)
        self._record(session_id, user_input, answer, usage, t.seconds, rag_hits=rag_hits)
        return answer

    def _build_messages(self, session_id: str, user_input: str):
        """
        拼装本轮 messages:系统提示 + 会话历史 +(可选 RAG 检索资料 +)本次输入。
        返回 (messages, rag_hits);rag_hits 供可观测性记录命中数。
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.memory.history(session_id))

        # RAG:检索知识库,把相关资料作为本轮的额外上下文(检索/生成解耦)
        rag_hits = 0
        if self.retriever is not None:
            context, rag_hits = self.retriever.build_context(user_input)
            if context:
                turn = (
                    "请优先依据下面的【知识库资料】回答;资料不足时再用你自己的知识补充,"
                    f"不要编造。\n知识库资料:\n{context}\n\n我的问题:{user_input}"
                )
            else:
                turn = user_input
            messages.append({"role": "user", "content": turn})
        else:
            messages.append({"role": "user", "content": user_input})
        return messages, rag_hits

    def stream_reply(self, session_id: str, user_input: str):
        """
        Web 用的流式生成器:逐段 yield 文本增量(给 SSE 接口推送)。
        先过输入护栏;若开启输出护栏则改为整段脱敏后一次性 yield。
        """
        import observability as obs

        blocked = self._guard_input(user_input)
        if blocked is not None:
            self._record(session_id, user_input, blocked, None, 0.0, blocked=True)
            yield blocked
            return

        messages, rag_hits = self._build_messages(session_id, user_input)

        usage = None
        with obs.Timer() as t:
            if self.guardrails:
                # 输出护栏需要完整文本才能脱敏,故非流式取全量再 yield
                resp = self.client.chat.completions.create(
                    model=CHAT_MODEL, messages=messages, temperature=0.3
                )
                usage = self._usage_dict(resp.usage)
                answer = self._guard_output(resp.choices[0].message.content)
                yield answer
            else:
                chunks = []
                resp = self.client.chat.completions.create(
                    model=CHAT_MODEL, messages=messages, temperature=0.3,
                    stream=True, stream_options={"include_usage": True},
                )
                for piece in resp:
                    if getattr(piece, "usage", None):  # 末尾带 usage 的块
                        usage = self._usage_dict(piece.usage)
                    if piece.choices:
                        delta = piece.choices[0].delta.content
                        if delta:
                            chunks.append(delta)
                            yield delta
                answer = "".join(chunks)

        self.memory.add(session_id, "user", user_input)
        self.memory.add(session_id, "assistant", answer)
        self._record(session_id, user_input, answer, usage, t.seconds, rag_hits=rag_hits)

    def _chat_stream(self, messages: list):
        """流式调用:逐 chunk 打印并拼接出完整答案。返回 (answer, usage)。"""
        chunks = []
        usage = None
        resp = self.client.chat.completions.create(
            model=CHAT_MODEL, messages=messages, temperature=0.3,
            stream=True, stream_options={"include_usage": True},
        )
        for piece in resp:
            if getattr(piece, "usage", None):  # 末尾带 usage 的块,choices 可能为空
                usage = self._usage_dict(piece.usage)
            if piece.choices:
                delta = piece.choices[0].delta.content
                if delta:
                    print(delta, end="", flush=True)
                    chunks.append(delta)
        print()  # 换行收尾
        return "".join(chunks), usage

    def _chat_with_tools(self, session_id: str, user_input: str) -> str:
        """
        工具调用循环(ReAct 核心,对标教程的 Tools):
        模型自主决定是否调工具 -> 工具先过权限审计再执行 -> 结果回填 -> 直到最终答案。
        """
        import observability as obs
        from tools import TOOL_SCHEMAS, dispatch  # 延迟导入:不开 tools 就不加载

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.memory.history(session_id))
        messages.append({"role": "user", "content": user_input})

        answer = "(已达到最大步数,未得到最终答案)"
        tool_calls = 0
        agg = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        with obs.Timer() as t:
            for step in range(1, MAX_TOOL_STEPS + 1):
                resp = self.client.chat.completions.create(
                    model=CHAT_MODEL, messages=messages,
                    tools=TOOL_SCHEMAS, tool_choice="auto", temperature=0.3,
                )
                u = self._usage_dict(resp.usage)  # 累加每一步的 token
                if u:
                    for k in agg:
                        agg[k] += u.get(k, 0)
                msg = resp.choices[0].message

                if not msg.tool_calls:          # 没有要调工具 -> 最终答案
                    answer = self._guard_output(msg.content)  # 输出护栏:最终答案脱敏
                    print(answer)
                    break

                messages.append(msg)            # 把"要调工具"的消息加入历史
                for tc in msg.tool_calls:
                    tool_calls += 1
                    name = tc.function.name
                    raw_args = tc.function.arguments
                    print(f"  [第{step}步] 模型请求调用工具:{name}({raw_args})")
                    result = dispatch(name, raw_args)   # 工具内部已过权限审计
                    print(f"  -> {result}")
                    messages.append({
                        "role": "tool", "tool_call_id": tc.id, "content": result,
                    })

        # 写回记忆:只存原始问答(不污染上下文)
        self.memory.add(session_id, "user", user_input)
        self.memory.add(session_id, "assistant", answer)
        self._record(session_id, user_input, answer, agg, t.seconds, tool_calls=tool_calls)
        return answer


def interactive(helper: AiCodingHelper) -> None:
    """交互式对话循环。输入 exit/quit 退出,输入 /clear 清空当前会话记忆。"""
    session_id = "cli-default"
    parts = []
    if helper.retriever is not None:
        parts.append("RAG")
    if helper.use_tools:
        parts.append("工具")
    if helper.guardrails:
        parts.append("护栏")
    mode = "+".join(parts) if parts else "纯对话"
    print(f"码小安 已就绪(模式:{mode})。输入问题开始对话;exit 退出,/clear 清空记忆。")
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
        if helper.use_tools or helper.guardrails:
            print("码小安:")  # 工具/护栏模式答案在内部整段打印
        else:
            print("码小安: ", end="", flush=True)
        helper.chat(session_id, user_input, stream=True)
        print("-" * 60)


def main():
    load_dotenv()  # 从当前目录的 .env 读取 DEEPSEEK_API_KEY

    # 解析开关:--rag 内存检索,--vectordb Chroma 持久化向量库,--tools 工具,--safe 护栏,--trace 指标
    args = sys.argv[1:]
    use_rag = "--rag" in args
    use_vectordb = "--vectordb" in args
    use_tools = "--tools" in args
    guardrails = "--safe" in args
    trace = "--trace" in args
    args = [a for a in args
            if a not in ("--rag", "--vectordb", "--tools", "--safe", "--trace")]

    retriever = None
    if use_vectordb:
        from retriever_chroma import ChromaRetriever  # 真实向量库(持久化)
        retriever = ChromaRetriever()
    elif use_rag:
        from retriever import Retriever  # 延迟导入:不开 RAG 就不加载 fastembed
        retriever = Retriever()
    helper = AiCodingHelper(retriever=retriever, use_tools=use_tools,
                            guardrails=guardrails, trace=trace)

    if args:
        question = " ".join(args)
        print(f"你: {question}")
        if use_tools or guardrails:
            print("码小安:")
        else:
            print("码小安: ", end="", flush=True)
        helper.chat("cli-oneshot", question, stream=True)
    else:
        interactive(helper)


if __name__ == "__main__":
    main()
