# 08 · 区块链安全 (Blockchain Security)

> 长期方向之一(传统安全 + AI 安全 + 区块链安全)。本模块沉淀智能合约**主流漏洞模式 + 审计方法论 + 静态扫描工具**。
> **只做静态审计示例与清单,不编译、不部署、不执行、不做攻击模拟、不针对任何真实合约。**

## 已建案例(11 类主流漏洞,每个含 `Vulnerable.sol` / `Fixed.sol` 对照 + README)

| # | 主题 | 漏洞类别(SWC) | 关键点 |
|---|------|---------------|--------|
| 1 | [重入 Reentrancy](reentrancy/) | SWC-107 | The DAO 经典漏洞;CEI + 重入锁 |
| 2 | [整数溢出/下溢](arithmetic-overflow/) | SWC-101 | `unchecked` 滥用;0.8+ 受检算术 + 边界校验 |
| 3 | [访问控制缺陷](access-control/) | SWC-115/105 | 缺 `onlyOwner`、`tx.origin` 鉴权 |
| 4 | [未检查外部调用](unchecked-call/) | SWC-104 | `call`/`send` 返回值未校验 |
| 5 | [价格预言机操纵](oracle-manipulation/) | — | 闪电贷操纵现货价;TWAP/Chainlink |
| 6 | [拒绝服务 DoS](denial-of-service/) | SWC-113/128 | push 模式单点失败、无界循环;拉模式 |
| 7 | [随机数可预测](bad-randomness/) | SWC-120 | `block.timestamp` 当随机源;VRF/commit-reveal |
| 8 | [委托调用风险](delegatecall/) | SWC-112 | 存储布局错配、目标可控的 `delegatecall` |
| 9 | [前置交易 MEV](front-running/) | SWC-114 | mempool 抢跑;commit-reveal + 滑点保护 |
| 10 | [签名重放](signature-replay/) | SWC-121 | `ecrecover` 无 nonce;EIP-712 + nonce |
| 11 | [无保护 selfdestruct](unprotected-selfdestruct/) | SWC-106 | 自毁/卷款函数缺访问控制 |

> 📍 **完整领域地图见 [LANDSCAPE.md](LANDSCAPE.md)**:穷尽合约漏洞、DeFi 经济攻击、跨链桥、钱包授权、
> 治理攻击、审计工具链(Slither/Mythril/Echidna)、链上取证、**AI × 区块链**交叉,及"走向真实成果"的进阶路径。

## 工具与报告

| 产物 | 说明 |
|------|------|
| [audit_scanner.py](audit_scanner.py) | 纯 Python 静态审计扫描器:正则 + 函数级启发式,定位 10 类危险模式;自测 10/10 签名命中 |
| [AUDIT-REPORT.md](AUDIT-REPORT.md) | 审计报告示例:扫描定位 → 人工/AI 复核 → 评级 → 修复对照(对标 03 代码审计闭环) |
| [LANDSCAPE.md](LANDSCAPE.md) | 区块链安全全景地图 + 审计方法论 + 进阶路径 |
| 已接入 CI | [tests/test_blockchain_audit.py](../tests/test_blockchain_audit.py),随 `unittest discover` 在 GitHub Actions 常绿 |

```bash
cd 08-blockchain-security
python audit_scanner.py            # 扫描全部 .sol,输出疑似风险
python audit_scanner.py --selftest # 自测:每个 Vulnerable 命中其签名类别
# 或随全仓单测一起跑:
python -m unittest discover -s tests
```

## 智能合约审计通用检查清单

**资金与状态**
- [ ] 是否遵循检查-生效-交互(CEI)?涉及资金的函数是否加重入锁?
- [ ] 外部调用(`call`/`send`/`transfer`)返回值是否校验?
- [ ] 算术是否用 0.8+ 内建溢出检查或 SafeMath?

**权限与初始化**
- [ ] 关键函数是否有正确的访问控制(避免 `tx.origin` 鉴权)?
- [ ] owner / 初始化是否防止被抢占或重复初始化?
- [ ] 可升级合约的 `delegatecall` 存储布局是否对齐?

**外部依赖**
- [ ] 预言机是否抗操纵(TWAP/多源)?是否防闪电贷?
- [ ] 是否存在前置交易/MEV 暴露面?
- [ ] 随机数来源是否安全(非链上可预测变量)?

**流程**
- [ ] 是否经过自动化工具扫描(Slither/Mythril 思路)?
- [ ] 是否有完善的事件日志与紧急暂停(circuit breaker)?

## 与 AI 安全的交叉(规划)

- 用 LLM 辅助合约审计(对照 `01` 的代码审计思路),并防范模型对合约漏洞的**幻觉误报/漏报**。
- 智能合约 + AI Agent 自动交易场景下的过度授权(对应 LLM06)。

## 面试表达

> "区块链安全是我长期布局的方向之一。我把智能合约的 9 类主流漏洞都做了**漏洞版/修复版对照**:
> 重入、整数溢出、访问控制、未检查调用、预言机操纵、DoS、弱随机、delegatecall、抢跑——
> 每个都讲清原理、危险模式、修复写法和审计清单。更关键的是我写了一个**纯 Python 静态审计扫描器**
> 自动定位这些危险模式(自测 8/8 命中),再人工/AI 复核需要语义判断的部分,最后出审计报告——
> 这跟我做 AI 代码审计是同一套'扫描定位→人工复核→评级→修复'的闭环,而且全程只做静态审计,不部署不攻击。"

## 安全边界

本模块所有 Solidity 仅为审计教学示例,**不编译部署、不上链、不执行、不进行任何攻击模拟**,
也不针对任何真实合约;只用于学习漏洞模式、修复写法与审计清单。
