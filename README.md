# AI 安全作品集 (AI Security Portfolio)

> 一个从传统安全到 AI 安全的转型作品集：把每一次学习都沉淀成**代码、文档、可复现环境与面试表达**。

## 🎯 目标

半年到一年内转型 **AI 安全 / AI Agent 工程师**，长期深耕传统安全、AI 安全、区块链安全。
所有产出遵循一条原则：**学到的东西，必须变成可展示的成果。**

## 🧱 能力三层总览(会造 · 会防应用 · 会攻防模型)

```
第三层 · AI 内生安全   对抗样本 / 数据投毒 / 后门 / 成员推断 / 模型窃取 / 自动化红队
第二层 · AI 应用安全   提示注入 / 越狱 / RAG 注入检测 / Agent 权限审计 / 纵深防御 / 真实LLM验证
第一层 · AI 开发       真实 RAG(embedding+检索+生成) / 真实 Agent(function calling)
```

> 全部纯 Python、可本地复现;模型层实验零 GPU(scikit-learn)。
> 📌 [项目地图 + STAR 故事集](05-resume-interview/project-map.md) · [成长路线 ROADMAP](ROADMAP.md)

## 📂 模块导航

| 模块 | 方向 | 状态 |
|------|------|------|
| [01 传统安全](01-traditional-security/) | Web/系统漏洞原理、复现、防护、检测 | ✅ 4 个案例 |
| [02 AI 安全](02-ai-security/) | 提示注入、越狱、模型滥用等案例研究 | ✅ 2 个案例 |
| [03 Agent / RAG 安全](03-agent-rag-security/) | AI Agent / RAG 系统的安全工具与防护 | ✅ 7 个工具 |
| [04 运营 AI 提效](04-ops-ai-efficiency/) | 教学运营场景的 AI 自动化案例 | ✅ 2 个案例 |
| [05 简历与面试](05-resume-interview/) | 简历项目描述、面试表达、作品集话术 | ✅ 进行中 |
| [06 AI 开发](06-ai-development/) | 真实 LLM 应用 / RAG / Agent / 微调 | ✅ 2 个项目 |
| [07 AI 内生安全](07-ai-intrinsic-security/) | 对抗样本 / 投毒 / 后门 / 隐私 / 模型窃取 | ✅ 7 个实验 |

> 📌 完整成长路线见 **[ROADMAP.md](ROADMAP.md)**（求职导向 · 分阶段 · 持续打勾）。

## ✅ 已完成案例（可运行）

| 案例 | 方向 | 看点 |
|------|------|------|
| [提示注入 Prompt Injection](02-ai-security/prompt-injection/) | AI 安全 | 模型被"忽略指令"劫持泄露系统提示词 → 输入护栏拦截 |
| [越狱 Jailbreak](02-ai-security/jailbreak/) | AI 安全 | 角色扮演/DAN 绕过安全护栏 → 越狱检测+拒答加固 |
| [RAG 注入检测器](03-agent-rag-security/rag-injection-detector/) | Agent/RAG 安全 | 知识库投毒劫持模型 → 可扫描文件的注入检测工具 |
| [Agent 工具调用权限审计](03-agent-rag-security/tool-permission-audit/) | Agent/RAG 安全 | 被劫持 Agent 越权转账/删库 → 最小权限审计拦截(LLM06) |
| [端到端安全 Agent 管线](03-agent-rag-security/secure-agent-pipeline/) | Agent/RAG 安全 | 复用上两个工具 → 纵深防御:任一层失守另一层兜底(LLM01+06) |
| [真实 RAG 系统](06-ai-development/real-rag-system/) | AI 开发 | 本地 embedding 语义检索 + DeepSeek 生成,真实可用的 RAG |
| [真实 LLM 注入攻防验证](03-agent-rag-security/real-rag-injection/) | AI 开发 × 安全 | 真实 DeepSeek 被投毒文档劫持 → 检测器源头剔除(含 v1 被绕过→v2 加固) |
| [真实 Agent](06-ai-development/real-agent/) | AI 开发 | DeepSeek function calling 自主调用工具,完整 ReAct 循环 |
| [文本对抗样本](07-ai-intrinsic-security/text-adversarial/) | AI 内生安全 | 形近字+拆字让分类器判错 → 对抗训练加固模型本身(ATLAS) |
| [数据投毒](07-ai-intrinsic-security/data-poisoning/) | AI 内生安全 | 6 条毒样本让准确率 100%→62% → kNN 检测清洗恢复(LLM03) |
| [后门/木马攻击](07-ai-intrinsic-security/backdoor-attack/) | AI 内生安全 | 秘密触发器隐蔽埋后门(干净100%)→ 翻转测试自动揪出(ATLAS) |
| [成员推断攻击](07-ai-intrinsic-security/membership-inference/) | AI 内生安全·隐私 | 靠自信度判断样本是否被训练过 AUC 0.93 → 正则化降到 0.56 |
| [差分隐私训练 DP-SGD](07-ai-intrinsic-security/dp-sgd/) | AI 内生安全·隐私 | 手写DP-SGD裁剪+加噪,成员推断 AUC 0.58→0.51,量化隐私-效用权衡 |
| [模型窃取](07-ai-intrinsic-security/model-extraction/) | AI 内生安全 | 黑盒查询蒸馏复制模型(保真度 95%)→ 限流/输出扰动防御 |
| [自动化红队](07-ai-intrinsic-security/auto-redteam/) | AI 内生安全 | 批量变体轰炸自有检测器,量化绕过率 31% 定位致命弱点(ATLAS) |
| [ML 语义注入检测器](03-agent-rag-security/ml-injection-detector/) | AI 开发 × 安全 | 语义 embedding+LR 把红队绕过率 53%→0%、零误报(Roadmap 3.1 闭环) |
| [真实 Agent 越权攻防](03-agent-rag-security/real-agent-audit/) | AI 开发 × 安全 | 真实 DeepSeek Agent 被劫持越权退款 → 审计器执行前拦截(LLM06) |
| [LLM 安全网关](03-agent-rag-security/llm-security-gateway/) | 工程化收口 | 输入/动作/输出三关卡封装成统一中间件 + HTTP API(Roadmap 3.2) |

> 全部纯 Python、零依赖、无需 API Key，本地一条命令即可复现攻击与防御。

## ✍️ 文章与表达输出

- [当 AI Agent 被劫持：用纵深防御守住"会动手的模型"](articles/agent-security-defense-in-depth.md) — 技术博客文章（📤 待发布，见[发布指南](articles/PUBLISH-GUIDE.md)）
- [纯 Python 复现 AI 内生安全的六大攻击面](articles/ai-intrinsic-security-six-attacks.md) — 内生安全长文（📤 待发布）
- [项目地图 + STAR 面试故事集](05-resume-interview/project-map.md) — 三层能力总览与面试故事
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
