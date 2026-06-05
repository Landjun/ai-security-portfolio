# AI 攻防 / CTF 比赛准备

> 对应岗位能力:**"参加高水平 AI 攻防及漏洞挖掘赛事"**。
> 诚实说明:这是**准备清单与方法**,真实名次需实际参赛积累(见 jd-gap-analysis)。

## 一、AI 安全 / 攻防赛常见题型

| 题型 | 内容 | 我的对应储备 |
|------|------|--------------|
| Prompt Injection / 越狱 | 套出系统提示词、绕过限制拿 flag | prompt-injection · jailbreak |
| RAG / 知识库注入 | 投毒文档劫持问答系统 | real-rag-injection |
| Agent 越权 | 诱导 Agent 调用危险工具 | real-agent-audit · tool-permission-audit |
| 模型层(对抗/投毒/后门) | 构造对抗样本、检测后门 | text-adversarial · backdoor-attack |
| 隐私(成员推断/窃取) | 判断训练成员、复制模型 | membership-inference · model-extraction |
| 传统 Web(注入/SSRF/反序列化) | 经典漏洞拿 shell | 01 传统安全 8 靶场 |
| 代码审计 | 审计给定代码找漏洞 | agent-code-audit |

> 作品集已覆盖大多数 AI 攻防赛题型的**原理与复现**,可作为赛前知识底座。

## 二、参赛准备路径

1. 平台:CTF(攻防世界/BUUCTF/CTFtime)、AI 安全专项赛、各厂商 SRC 众测。
2. 节奏:每周固定刷题 + 复现一个新手法(写进 research-notes)。
3. 组队:补齐 Web/Pwn/Crypto/AI 各方向,明确分工。
4. 复盘:每场赛后写 writeup(用下方模板),沉淀题型与解法。

## 三、Writeup 模板

```
# 题目名(分类 / 分值)
## 题目描述
## 解题思路(侦察→定位→利用→拿flag)
## 关键步骤 / payload(合规、仅赛题环境)
## flag
## 知识点与复盘
```

## 四、诚实定位

> 我目前的优势是 **AI 攻防题型的知识与复现储备**;**真实名次/题解需要实际参赛积累**。
> 计划:带作品集投递的同时,参加 AI 安全/攻防赛,把"准备"变成"成果"。
