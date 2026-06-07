# 06 · AI 开发 (AI Development)

> "会造才会防"。本模块沉淀**真实的 AI 开发能力**——调用真实大模型、做真实 RAG、搭真实 Agent、跑通微调。
> 这是支撑 AI 内生安全研究(模块 07)的地基。

## 已完成(阶段 1 全部落地)

| 项目 | 阶段 | 看点 |
|------|------|------|
| [真实 RAG 系统](real-rag-system/) | 1.1/1.2 | 本地 fastembed 语义检索 + DeepSeek 生成,检索/生成解耦 |
| [真实 Agent](real-agent/) | 1.3 | DeepSeek function calling 自主调用工具,完整 ReAct 循环 |
| [LangChain Agent](langchain-agent/) | 1.3 | LangChain(ChatOpenAI+@tool+bind_tools)+ 工具执行前权限审计 |
| [LoRA 微调](lora-finetune/) | 1.4 | numpy 手写机制(6%参数)+ peft 真实微调 bert-tiny(0.19%参数,测试100%) |
| [AI 赋能安全自动化](ai-assisted-security/) | 拓展 | AI 辅助漏洞情报分析 + AI 辅助代码审计(静态+语义混合) |
| [AI 编程小助手「码小安」](ai-coding-helper/) | 拓展 | 对标 LangChain4j 教程的 Python 复刻:对话/记忆/RAG/工具+审计/护栏/SSE Web/可观测/评测/MCP/多模态/向量库 |
| [TS Agent Guard](ts-agent-guard/) | 拓展 | TypeScript 复刻 Agent 工具调用 + 输入护栏 + 权限审计(回应 JD 的 TS 技术栈) |

## 与安全模块的关系

- 模块 `02/03` 的攻防把"模拟模型"换成这里的**真实模型**后,更有说服力(见真实 RAG 注入、真实 Agent 越权)。
- 模块 `07` 的内生安全实验依赖真实可训练/可调用模型;本模块的 LoRA 也呼应内生安全的训练阶段。

## 运行

```powershell
cd 06-ai-development\<项目>
python <脚本>.py   # 见各项目 README;需 DeepSeek 的走 real-rag-system/.env
```

## 约定与安全边界

每个项目独立子目录,含 `README.md` + 可运行代码。API Key 一律走环境变量(.env),**绝不提交密钥**;
下载的模型/缓存已 gitignore。
