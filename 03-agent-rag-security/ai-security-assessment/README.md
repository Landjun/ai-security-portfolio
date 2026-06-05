# 工具:AI 系统安全评测体系 (AI Security Assessment Framework)

> 把作品集里所有攻防实验,收口成一套「**资产 → 威胁 → 测试用例库 → 风险评级 → 报告**」的可复用评测方法论 + 工具。
> 直接对应岗位 P0 能力:**"基于实战视角构建 AI 系统安全评测及漏洞挖掘体系"**。

## 为什么做这个

会单点攻击只是"会测",能把测试**成体系、可规模化、可交付**才是评测工程师的核心。
本框架解决:评测一个 AI 系统时,**测什么、怎么测、用哪个用例、怎么评级、怎么出报告**。

## 评测方法论(闭环)

```
① 资产枚举  → 盘点 AI 系统的攻击面(模型/系统提示词/输入/RAG知识库/Agent工具/训练数据/输出/供应链)
② 威胁建模  → 对每个资产面映射威胁(OWASP LLM Top 10 / MITRE ATLAS)
③ 用例库    → 每个威胁对应可执行测试用例(关联本作品集的可运行 demo)
④ 执行评级  → 逐项测试,按高/中/低评级,留证据
⑤ 报告交付  → 风险汇总 + 整改建议 + 复测(自动化红队回归)
```

## 内容

```
ai-security-assessment/
├── checklist.py   # 评测用例库:13 条用例,关联 OWASP + 可运行 demo + 缓解措施
├── assess.py      # 为目标系统生成结构化评测报告骨架(可填写)
├── scanner.py     # 【可执行】自动跑攻击载荷、打分、出报告(评测体系落地为工具)
└── README.md
```

## 从"清单"到"可运行扫描器"(scanner.py)

`checklist.py` 回答"该测什么";`scanner.py` 直接"自动测完给分数":
对被测系统的安全护栏跑一批攻击载荷(注入/越狱/工具越权/机密泄露 + 误报检查),
逐条判定 blocked/controlled/allowed,算出**安全得分**并生成报告。

```powershell
python scanner.py            # 护栏组件打分(示例:10/10 = 100%)
python scanner.py --report   # 额外生成 SCAN-REPORT.md
python scan_realrag.py       # 【端到端】把载荷打进真实 DeepSeek RAG(实测 6/6)
```
> 把它纳入回归:每次改护栏后重跑,确保安全得分不下降;再配 auto-redteam 量化绕过率。
> `scan_realrag.py` 评测的是**真实 AI 系统**的整体行为(拦截注入/越狱、合规引导、超纲拒答、正常作答),而非只测组件。

## 用例库覆盖(13 条,关联作品集 demo)

| 维度 | 用例 | 对应 demo |
|------|------|-----------|
| 输入/提示层 | 直接注入 / 越狱 / RAG 间接注入 | prompt-injection · jailbreak · real-rag-injection |
| 输出层 | 机密泄露 / 不安全输出处理 | llm-security-gateway · xss |
| Agent/工具层 | 工具越权 / 未授权工具·SSRF | real-agent-audit · tool-permission-audit |
| 数据/训练层 | 数据投毒 / 后门木马 | data-poisoning · backdoor-attack |
| 模型内生层 | 对抗样本 / 成员推断 / 模型窃取 | text-adversarial · membership-inference · model-extraction |
| 鲁棒性/红队 | 防护绕过率基准 | auto-redteam |

> 这把"我做了一堆攻防 demo"升级成"我有一套带用例库的 AI 安全评测体系",每条用例都能现场跑给面试官看。

## 运行 & 验证

```powershell
cd 03-agent-rag-security\ai-security-assessment
python checklist.py            # 打印评测清单 + 统计(13 条用例)
python checklist.py --md       # 输出 Markdown 清单(贴进文档)
python assess.py "企业知识库问答系统" > REPORT.md   # 生成可填写的评测报告骨架
```

## 面试表达

> "我把做过的 AI 攻防,收口成了一套安全评测体系:先枚举 AI 系统的资产面(模型、系统提示词、输入、RAG 知识库、Agent 工具、训练数据、输出、供应链),对每个资产面映射 OWASP LLM Top 10 / ATLAS 的威胁,落成一个 13 条的测试用例库——每条用例都关联一个我能现场跑的 demo、默认风险等级和缓解措施;再用一个脚本为目标系统自动生成可填写的评测报告骨架。比如评测一个企业 RAG 问答系统,我会从'知识库间接注入、检索越权、输出泄露、工具越权'这几个面逐项测、评级、出报告,整改后再用自动化红队基准复测绕过率。这就是从单点测试到体系化交付的闭环。"

## 与岗位 JD 的对应

- P0 能力5「构建 AI 系统安全评测及漏洞挖掘体系」→ 本框架。
- P0 能力1「AI 安全攻防实战」→ 用例库每条都有可跑 demo。
- 能力6「安全自动化」→ 报告骨架自动生成。
- 能力8「报告撰写」→ 标准化报告模板与评级。

## 安全边界

仅用于对**自有/授权**的 AI 系统做防御性评测;不针对任何未授权的第三方系统。
