# 工具:AI 赋能安全自动化

> 用 AI 提升传统安全作业效率。直接对应岗位 P1 能力:**"探索 AI 在传统安全方向的自动化能力,提升作业效率和交付质量"**。

## 两个工具

### 1. AI 辅助漏洞情报分析 `vuln_intel.py`
回应 JD "**批量分析漏洞公告并生成验证思路**"。把漏洞公告/CVE 描述交给大模型,结构化提取:
受影响组件、版本、漏洞类型、利用前提、危害、修复建议、**合规验证思路**(只给授权环境下的验证方向)。

```powershell
python vuln_intel.py
```
输出:每条公告 → JSON 结构化情报(component/versions/vuln_type/precondition/impact/fix/verify_idea)。

### 2. AI 辅助代码审计 `ai_audit.py`
回应 JD "**用 AI 提升代码审计效率**"。混合方案:
- 先用静态扫描器(`agent-code-audit/audit_scan.py`)快速定位危险点;
- 再把代码交给大模型做语义级审计(解释成因、补充逻辑漏洞、给修复)。

```powershell
python ai_audit.py            # 默认审计 vulnerable_agent.py
python ai_audit.py 某文件.py
```
输出:静态定位结果 + AI 语义审计(漏洞类型/风险/修复)。

## 为什么是"混合"而不是纯 AI

- **静态扫描**:快、确定性强,适合定位已知危险模式入口。
- **AI 语义审计**:能理解逻辑、解释成因、发现规则覆盖不到的问题,但可能漏报/幻觉。
- **人审**:最终确认数据流与可利用性。
- 三者结合 = 又快又准,这正是"AI 赋能安全作业"的落地姿势。

## 与岗位的对应

- P1 能力6「AI 在传统安全的自动化」→ 本工具。
- P0 能力3「代码审计」→ ai_audit 与 [agent-code-audit](../../03-agent-rag-security/agent-code-audit/) 配套。
- 能力7「前沿跟踪→落地」→ vuln_intel 可批量处理最新公告。

## 安全边界

- 仅在**授权/自有**环境使用;`verify_idea` 只给合规验证方向,不生成攻击 PoC。
- 密钥走 .env 不提交;AI 输出需人工复核(可能有幻觉)。
