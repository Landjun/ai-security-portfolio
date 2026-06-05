# 项目:LangChain Agent(DeepSeek + 工具调用 + 权限审计)

> 用 **LangChain** 搭建的工具调用 Agent,回应岗位 JD 点名的技术栈(LangChain / Agent / 工具调用),
> 并接入权限审计,体现「LangChain 开发 × AI 安全」。

## 为什么做这个

JD 要求"掌握主流 AI Native 技术栈,具备 Agent 开发能力(LangChain/ReAct 等)"。
之前我用原生 SDK 实现过 function-calling Agent(见 [06 real-agent](../real-agent/)),
这里用 **LangChain** 再实现一遍,证明对主流框架的掌握。

## 用到的 LangChain 能力

- `langchain_openai.ChatOpenAI`:接 DeepSeek(OpenAI 兼容,设 base_url)。
- `@tool` 装饰器:把普通函数声明为 LangChain 工具(自动从 docstring/类型注解生成 schema)。
- `llm.bind_tools(tools)`:把工具绑定到模型。
- LangChain 消息类型:`SystemMessage / HumanMessage / AIMessage / ToolMessage`。
- 工具调用循环:模型返回 `.tool_calls` → 执行 → 回填 `ToolMessage` → 直到自然语言答案。

## 安全加固(LangChain × 安全)

工具执行前接入 [03 权限审计器](../../03-agent-rag-security/tool-permission-audit/):
- `query_order` / `get_policy`:只读,放行。
- `issue_refund`:敏感动作,需人工确认;金额超上限(1000)直接拦截。

> 这正是 JD 关心的"Agent 调用高危工具时如何做权限控制"——把安全审计作为工具调用的统一关卡。

## 运行 & 验证

```powershell
pip install langchain langchain-openai
cd 06-ai-development\langchain-agent
python agent_langchain.py
```
预期:Agent 通过 LangChain 调用工具查询订单/政策并作答;退款类工具会过权限审计。

## 实测说明

- "查订单 A1001" → LangChain 调 `query_order` 作答。
- "退款 50 元" → 模型先查订单与政策(多工具),敏感退款经审计需人工确认。
- "退款 99999 元" → 模型自身也会质疑;即便发起,审计器按金额上限拦截。

## 面试表达

> "我用 LangChain 实现了一个工具调用 Agent:ChatOpenAI 接 DeepSeek、@tool 定义工具、bind_tools 绑定,
> 走 LangChain 的消息与 tool_calls 循环。关键是我在工具执行前接了一道权限审计——只读工具放行、
> 退款这类敏感动作需人工确认、超额直接拦截。这回应了'Agent 调高危工具怎么做权限控制':
> 把审计做成工具调用的统一关卡,而不是依赖模型自觉。"

## 安全边界
工具均为模拟(退款不涉及真实资金);本地与自有环境;密钥走 .env 不提交。
