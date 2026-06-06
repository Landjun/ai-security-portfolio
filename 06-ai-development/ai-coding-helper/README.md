# 项目:AI 编程小助手「码小安」(对标 LangChain4j 教程,Python 复刻)

> 参考编程导航《LangChain4j 实战 · AI 编程助手》教程,用 **Python(DeepSeek + openai SDK)** 复刻同一套能力。
> 教程原版是 Java/Spring Boot,本机无 JDK/Maven 且整个作品集是 Python,故用 Python 复刻——
> 关注点一致:**ChatModel → 系统提示 → 多会话记忆 → 流式输出 →（路线图）RAG / 工具 / 护栏 / Web**。

## 为什么做这个

- 回应「AI Agent / AI 应用开发」岗位的核心技能:**会话式 AI 服务、上下文记忆、流式交互**。
- 与 06 其它项目互补:`real-rag-system`(检索)、`langchain-agent`(工具调用)、本项目(对话式 AI 服务封装)。
- 教程能力逐项对标,证明「换语言也能把同一套工程能力落地」。

## 能力对标(教程 → 本 MVP）

| 教程概念（LangChain4j） | 本项目实现 | 状态 |
|---|---|---|
| ChatModel | `OpenAI` 客户端接 DeepSeek（OpenAI 兼容，设 `base_url`） | ✅ |
| SystemMessage | `SYSTEM_PROMPT` 定义「码小安」人设、风格与边界 | ✅ |
| AI Service | `AiCodingHelper` 把「模型+记忆+系统提示」封装成服务 | ✅ |
| ChatMemory + @MemoryId | `ChatMemory` 滑动窗口 + 按 `session_id` 多会话隔离 | ✅ |
| SSE 流式 | `stream=True` 逐字打印 | ✅ |
| RAG（检索增强） | `retriever.py` fastembed 本地检索 + 资料拼进提示，检索/生成解耦 | ✅ |
| Tools（工具调用） | 复用 06 `langchain-agent` 思路 | ⏳ 路线图 |
| Guardrail（护栏） | 复用 02/03 的输入/输出校验与权限审计 | ⏳ 路线图 |
| Web 前端 + SSE 接口 | FastAPI `/chat` SSE + 简易前端 | ⏳ 路线图 |

## 运行 & 验证

```powershell
pip install -r requirements.txt
cd 06-ai-development\ai-coding-helper
copy .env.example .env   # 然后编辑 .env 填入 DEEPSEEK_API_KEY
python ai_coding_helper.py              # 纯对话:交互式
python ai_coding_helper.py "用python写个二分查找"   # 纯对话:单轮
python ai_coding_helper.py --rag        # RAG:基于知识库作答(交互式)
python ai_coding_helper.py --rag "二分查找有哪些坑"   # RAG:单轮
```

**离线自测**（不消耗 key）：

```powershell
# 1) 多会话记忆/滑动窗口逻辑
python -c "import ai_coding_helper as m; mem=m.ChatMemory(window=4); [mem.add('a','user',str(i)) for i in range(10)]; print('窗口裁剪正确' if len(mem.history('a'))==4 else '错误')"
# 2) RAG 检索(fastembed 本地,无需 key;首次自动下载小模型)
python -c "from retriever import Retriever; r=Retriever(); print(r.retrieve('二分查找有什么坑')[0][1]['title'])"
```

预期：纯对话下问「上一题再优化一下」能记住上下文；`--rag` 下问知识库内问题会基于资料作答(更准、可溯源)；
答案逐字流式输出；`/clear` 清空会话记忆；非编程问题被礼貌拒绝（系统提示边界生效）。

## 下一步路线图（MVP → 完整体）

1. ~~**RAG**:把编程学习资料/面试题做成知识库,检索后拼进上下文~~ ✅ 已完成(`knowledge_base.py` + `retriever.py`)。
2. **工具调用**：加「查面试题 / 搜文档」等工具，走 function calling（复用 `langchain-agent`）。
3. **护栏**：输入侧拦提示注入、输出侧过敏感信息（复用 `02/03` 安全模块）。
4. **Web 化**：FastAPI 暴露 SSE `/chat` 接口 + 一个极简前端聊天页。

## 面试表达

> "我用 Python 复刻了一个对话式 AI 编程助手:把 DeepSeek 对话模型、系统提示、会话记忆和检索封装成一个
> AI 服务对象;会话记忆用滑动窗口并按 session_id 多会话隔离(对应 LangChain4j 的 ChatMemory 和
> @MemoryId);接了 RAG——fastembed 本地向量化做语义检索,把知识库资料拼进提示让模型基于资料作答,
> 检索与生成解耦,减少幻觉、可溯源;回答走流式输出提升体感。骨架还可平滑接工具调用和安全护栏——
> 这正是把『AI 应用开发』和『AI 安全』接到一起的地方。"

## 安全边界

仅本地/自有环境;API Key 走 `.env`(已 gitignore,绝不提交);系统提示限定话题范围,
后续护栏会进一步拦截提示注入与敏感信息泄露。
