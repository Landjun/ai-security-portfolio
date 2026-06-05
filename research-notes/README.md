# 前沿研究复现笔记

> 对应岗位能力:**"跟踪全球 AI 安全前沿攻防手法,并能落地复现和转化"**。
> 这里把"读到的攻击手法/论文 → 我的可运行复现 → 转化为工具/方法"组织成笔记体系。

## 已复现(均有可运行代码)

| 攻击手法 | 出处/类别 | 我的复现 | 转化 |
|----------|-----------|----------|------|
| 间接提示注入(RAG 投毒) | OWASP LLM01 | [real-rag-injection](../03-agent-rag-security/real-rag-injection/) | 注入检测器 + ML 语义检测 |
| 后门/触发器(BadNets 思想) | 数据投毒/后门 | [backdoor-attack](../07-ai-intrinsic-security/backdoor-attack/) | 翻转测试自动找触发器 |
| 成员推断(Shokri 思想) | 隐私攻击 | [membership-inference](../07-ai-intrinsic-security/membership-inference/) | 量化 AUC + 正则化防御 |
| 差分隐私训练(Abadi DP-SGD) | 隐私防御 | [dp-sgd](../07-ai-intrinsic-security/dp-sgd/) | 隐私-效用权衡曲线 |
| 模型窃取(查询蒸馏) | 模型 IP | [model-extraction](../07-ai-intrinsic-security/model-extraction/) | 限流/扰动/水印防御 |
| 文本对抗样本 | 对抗 ML | [text-adversarial](../07-ai-intrinsic-security/text-adversarial/) | 对抗训练 |

## 复现方法论

> **读懂手法 → 最小复现 → 量化效果 → 定位根因 → 给出防御 → 转化为工具/方法。**

这套"发现→量化→定位→根治"的闭环,是把前沿手法落地的核心,贯穿本作品集每个实验。

## 前沿手法笔记(跟踪 + 关联我的复现)

| 手法 | 笔记 | 我的关联复现 |
|------|------|--------------|
| Many-shot 越狱(长上下文) | [many-shot-jailbreak](many-shot-jailbreak.md) | 越狱实验 / 自动化红队 |
| 对抗后缀 GCG(梯度搜索越狱) | [adversarial-suffix-gcg](adversarial-suffix-gcg.md) | 文本对抗样本 / 对抗训练 |
| 间接注入数据外泄 | [indirect-injection-data-exfiltration](indirect-injection-data-exfiltration.md) | 真实 RAG 注入 / 多智能体 / 安全网关 |

## 新增笔记

照 [`_template.md`](_template.md) 新建笔记:每读到一个新手法,写一篇"原理+我的复现+防御+转化"。
持续更新即体现"持续跟踪前沿"的能力。
