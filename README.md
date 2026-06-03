# AI 安全作品集 (AI Security Portfolio)

> 一个从传统安全到 AI 安全的转型作品集：把每一次学习都沉淀成**代码、文档、可复现环境与面试表达**。

## 🎯 目标

半年到一年内转型 **AI 安全 / AI Agent 工程师**，长期深耕传统安全、AI 安全、区块链安全。
所有产出遵循一条原则：**学到的东西，必须变成可展示的成果。**

## 📂 模块导航

| 模块 | 方向 | 状态 |
|------|------|------|
| [01 传统安全](01-traditional-security/) | Web/系统漏洞原理、复现、防护、检测 | 🚧 搭建中 |
| [02 AI 安全](02-ai-security/) | 提示注入、越狱、模型滥用等案例研究 | ✅ 2 个案例 |
| [03 Agent / RAG 安全](03-agent-rag-security/) | AI Agent / RAG 系统的安全工具与防护 | ✅ 3 个工具 |
| [04 运营 AI 提效](04-ops-ai-efficiency/) | 教学运营场景的 AI 自动化案例 | 🚧 搭建中 |
| [05 简历与面试](05-resume-interview/) | 简历项目描述、面试表达、作品集话术 | 🚧 搭建中 |

## ✅ 已完成案例（可运行）

| 案例 | 方向 | 看点 |
|------|------|------|
| [提示注入 Prompt Injection](02-ai-security/prompt-injection/) | AI 安全 | 模型被"忽略指令"劫持泄露系统提示词 → 输入护栏拦截 |
| [越狱 Jailbreak](02-ai-security/jailbreak/) | AI 安全 | 角色扮演/DAN 绕过安全护栏 → 越狱检测+拒答加固 |
| [RAG 注入检测器](03-agent-rag-security/rag-injection-detector/) | Agent/RAG 安全 | 知识库投毒劫持模型 → 可扫描文件的注入检测工具 |
| [Agent 工具调用权限审计](03-agent-rag-security/tool-permission-audit/) | Agent/RAG 安全 | 被劫持 Agent 越权转账/删库 → 最小权限审计拦截(LLM06) |
| [端到端安全 Agent 管线](03-agent-rag-security/secure-agent-pipeline/) | Agent/RAG 安全 | 复用上两个工具 → 纵深防御:任一层失守另一层兜底(LLM01+06) |

> 全部纯 Python、零依赖、无需 API Key，本地一条命令即可复现攻击与防御。

## ✍️ 文章与表达输出

- [当 AI Agent 被劫持：用纵深防御守住"会动手的模型"](articles/agent-security-defense-in-depth.md) — 技术博客文章
- [PPT 大纲 + 5 分钟面试口播稿](05-resume-interview/talk-deck-outline.md) — 面试/分享用
- [简历项目话术](05-resume-interview/resume-bullets.md) — 5 条可直接写进简历的要点

## 🧭 每个模块的统一结构

每个案例/工具尽量包含：
1. **原理** —— 这是什么，为什么会出问题
2. **复现环境** —— 本地靶场 / 授权环境，可一键跑起来
3. **防护方案** —— 怎么防
4. **修复建议** —— 怎么改
5. **检测清单** —— 怎么发现
6. **面试表达** —— 一句话讲清楚

## ⚠️ 安全边界

本仓库所有内容**仅用于本地靶场、授权环境、学习与防御研究**，不包含针对真实第三方目标的攻击脚本。

## 🛠️ 工作方式

MVP 优先 · 每一步都可运行可验证 · 每个产出对应一句简历话术。
