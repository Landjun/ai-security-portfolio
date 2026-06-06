# 02 · AI 安全 (AI Security)

针对大模型 / AI 应用的安全案例研究。对应 OWASP Top 10 for LLM Applications。

## 已完成案例(可运行)

| 案例 | 风险 | 看点 |
|------|------|------|
| [提示注入 Prompt Injection](prompt-injection/) | LLM01 | "忽略指令"劫持泄露系统提示词 → 输入护栏拦截 |
| [越狱 Jailbreak](jailbreak/) | LLM01 | 角色扮演/DAN 绕过安全护栏 → 越狱检测 + 拒答加固 |

## 相关案例(在其他模块,同属 AI 应用安全)

- [RAG 注入检测器](../03-agent-rag-security/rag-injection-detector/) · [真实 LLM 注入攻防](../03-agent-rag-security/real-rag-injection/)(间接注入 LLM01)
- [Agent 工具调用权限审计](../03-agent-rag-security/tool-permission-audit/) · [真实 Agent 越权攻防](../03-agent-rag-security/real-agent-audit/)(过度授权 LLM06)
- [LLM 安全网关](../03-agent-rag-security/llm-security-gateway/)(含输出泄露扫描 LLM02)
- [ML 语义注入检测器](../03-agent-rag-security/ml-injection-detector/)(自动化红队绕过率 53%→0%)

> AI 应用安全的攻防大多落在 `03 Agent/RAG 安全`,本模块聚焦最基础的提示层(注入/越狱)。

## 运行

```powershell
cd 02-ai-security\<案例名>
python demo.py
```

## 约定与安全边界

每个案例:`案例名/demo.py`(攻击 vs 防御对比)+ `README.md`(原理→复现→防护→检测→面试表达)。
全部本地模拟、纯防御研究,不针对任何真实第三方系统;模型被攻破后仅输出占位符,不产出真实有害内容。
