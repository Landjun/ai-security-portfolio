# 03 · Agent / RAG 安全 (Agent & RAG Security)

面向 AI Agent 与 RAG 系统的安全工具与防护——本作品集**最核心的差异化模块**,最贴近 AI 安全岗位。

## 已完成(工具 / 案例)

| 子项目 | 方向 | 看点 |
|--------|------|------|
| [RAG 注入检测器](rag-injection-detector/) | 输入防护 | 知识库投毒劫持模型 → 可扫描文件的注入检测工具 |
| [工具调用权限审计](tool-permission-audit/) | 动作防护 | 被劫持 Agent 越权转账/删库 → 最小权限审计(LLM06) |
| [端到端安全 Agent 管线](secure-agent-pipeline/) | 纵深防御 | 复用上两者 → 任一层失守另一层兜底(LLM01+06) |
| [真实 LLM 注入攻防验证](real-rag-injection/) | 真实环境 | 真实 DeepSeek 被投毒劫持 → 检测器 v1 被绕过→v2 加固 |
| [真实 Agent 越权攻防](real-agent-audit/) | 真实环境 | 真实 DeepSeek Agent 越权退款 → 审计执行前拦截 |
| [ML 语义注入检测器](ml-injection-detector/) | 工程化 | 红队绕过率 53%→0%、零误报(Roadmap 3.1) |
| [LLM 安全网关](llm-security-gateway/) | 产品化 | 输入/动作/输出 三关卡中间件 + HTTP API + 限速/ML可插拔 |
| [AI 系统安全评测体系](ai-security-assessment/) | 评测体系 | 资产→威胁→13用例库→评级→报告 + 可运行扫描器(组件+端到端) |
| [AI Agent 代码审计](agent-code-audit/) | 代码审计 | 7类漏洞 + 扫描器 + 审计报告 + 修复闭环(8→0) |
| [多智能体安全](multi-agent-security/) | 前沿 | 跨智能体提示注入传播(混淆代理)→ 智能体边界纵深防御 |
| [MCP 安全](mcp-security/) | 前沿 | 工具描述投毒/不可信服务器/rug-pull 检测 |

## 主线叙事

```
单点工具(检测器/审计器) → 组合管线(纵深防御) → 真实 LLM 验证 → ML 根治 → 统一网关 → 评测体系
                                            → 代码审计 / 多Agent / MCP(前沿)
```

## 运行

```powershell
cd 03-agent-rag-security\<子项目>
python demo.py   # 或对应脚本,见各子项目 README
```

## 安全边界

全部本地模拟 / 自有授权环境,纯防御研究;密钥走 .env 不提交,机密均为演示占位符。
