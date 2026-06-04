# 可直接粘贴的简历「项目经历」段落

> 从 20 条话术里精选浓缩,直接复制进简历即可。提供「精简版(2 条)」「标准版(3 条)」「完整版(4 条)」三档,按简历篇幅选用。
> 记得把 GitHub 链接保留:https://github.com/Landjun/ai-security-portfolio

---

## ⭐ 标准版(推荐,3 条,适合大多数简历)

**AI 安全作品集（个人开源项目） | Python · DeepSeek · scikit-learn · fastembed**
**GitHub: github.com/Landjun/ai-security-portfolio**

- **AI 内生安全攻防(核心)**:独立复现并防御模型层六大攻击面——对抗样本(对抗训练)、数据投毒(kNN 检测,准确率 100%→62%→100%)、后门木马(秘密触发器+翻转测试自动定位)、成员推断(AUC 0.93)、模型窃取(黑盒查询保真度 95%)、自动化红队(量化绕过率);并手写 DP-SGD 量化隐私-效用权衡。对应 OWASP ML/LLM Top 10、MITRE ATLAS。
- **LLM/Agent 应用安全**:在真实 DeepSeek 上复现并防御提示注入、越狱、RAG 间接注入与 Agent 越权;将正则检测器升级为语义 ML 检测器,在 36 个红队变体上把绕过率从 53% 降到 0%、零误报;并把全部检测器封装成统一「LLM 安全网关」中间件 + HTTP API。
- **AI 开发能力**:用本地 embedding + DeepSeek 搭建真实 RAG 问答系统与 function-calling Agent,打通向量化→检索→增强→生成与工具调用闭环——"会造才会防"。

---

## 精简版(2 条,适合一页纸简历)

**AI 安全作品集(开源,github.com/Landjun/ai-security-portfolio) | Python**

- 独立完成 AI 内生安全六大攻击面的可复现攻防(对抗样本/投毒/后门/成员推断/模型窃取/自动化红队)+ 手写 DP-SGD,每个含量化指标与防御,对应 OWASP ML/LLM Top 10、MITRE ATLAS。
- 在真实 DeepSeek 上做 LLM/Agent 攻防(注入/越狱/RAG 注入/Agent 越权),将正则检测器升级为语义 ML 检测(红队绕过率 53%→0%),并封装为统一 LLM 安全网关(中间件 + HTTP API)。

---

## 完整版(4 条,作品集是简历主项时用)

**AI 安全作品集(个人开源,约 19 个可运行项目) | Python · DeepSeek · scikit-learn · fastembed · numpy**
**GitHub: github.com/Landjun/ai-security-portfolio**

- **AI 内生安全**:复现并防御模型层六大攻击面 + DP-SGD 差分隐私训练,每个有量化结果(如成员推断 AUC 0.93→正则化 0.56;模型窃取保真度 95%;后门干净准确率 100% 仍可被触发器激活)。对应 OWASP ML/LLM Top 10、MITRE ATLAS。
- **应用/Agent 安全**:真实 DeepSeek 上验证提示注入/越狱/RAG 注入/Agent 越权攻防;自动化红队量化检测器绕过率,并用语义 ML 检测把绕过率从 53% 降到 0%、零误报。
- **工程化**:将所有检测器封装为统一「LLM 安全网关」(输入护栏 + 动作审计 + 输出扫描 + 审计日志),提供库与零依赖 HTTP API,安全能力可插拔接入。
- **AI 开发 + 传统安全**:真实 RAG 与 function-calling Agent;并以本地靶场复现 SQL 注入/XSS/命令注入/路径穿越(OWASP A01/A03),支撑从传统安全到 AI 安全的转型叙事。

---

## 一句话「项目亮点」(放简历技能栏或自我评价)

> 系统化 AI 安全作品集,覆盖 AI 开发、应用/Agent 安全、AI 内生安全三层,均为可复现代码 + 量化结果;具备"发现问题→量化→定位根因→根治"的安全研究方法论。

## 投递小贴士

- 简历里 GitHub 链接做成超链接,确保可点击。
- 不同岗位可微调侧重:**内生安全岗**突出第 1 条;**Agent 工程/安全岗**突出第 2、3 条。
- 面试前对照 [project-map.md](project-map.md) 的 STAR 故事,挑 2-3 个能讲深。
