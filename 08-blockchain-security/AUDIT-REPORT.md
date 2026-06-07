# 智能合约安全审计报告(教学靶场)

> 对本模块 9 类漏洞靶场合约的静态审计示例报告,演示「自动化扫描定位 → 人工/AI 语义复核 → 评级 → 修复对照」的审计闭环。
> **纯静态审计,不编译、不部署、不执行、不针对任何真实合约。**

## 一、审计范围与方法

- **范围**:`08-blockchain-security/` 下 9 个漏洞主题,每个含 `Vulnerable.sol`(漏洞版)/ `Fixed.sol`(修复版)对照。
- **方法**:
  1. 自动化:`audit_scanner.py` 正则 + 函数级启发式扫描,快速定位危险模式;
  2. 人工/AI 复核:对扫描命中逐条确认数据流与语义(重入/预言机/抢跑等需语义判断);
  3. 评级与修复:给出严重度,并对照 `Fixed.sol` 给修复写法。
- **工具自评**:静态启发式有误报/漏报,用于缩小排查范围,不替代人工审计。

## 二、扫描概览

`python audit_scanner.py --selftest` → 8/8 漏洞签名命中;漏洞版总命中数 **12** 远高于修复版 **2**
(修复版残留 2 处为 `delegatecall/Fixed.sol` 的"始终需复核"提示,属合理保留)。

## 三、漏洞清单与评级

| # | 漏洞主题 | OWASP/SWC 对应 | 严重度 | 扫描器可定位 | 修复要点 |
|---|---------|---------------|:--:|:--:|---------|
| 1 | [重入 Reentrancy](reentrancy/) | SWC-107 | 高 | ✅(函数级 CEI 启发式) | CEI + `nonReentrant` |
| 2 | [整数溢出/下溢](arithmetic-overflow/) | SWC-101 | 中 | ✅(`unchecked` 块) | 0.8+ 受检算术 + `require` 边界 |
| 3 | [访问控制缺陷](access-control/) | SWC-115/105 | 高 | ✅(`tx.origin`) | `onlyOwner` + `msg.sender` |
| 4 | [未检查外部调用](unchecked-call/) | SWC-104 | 中 | ✅(`call`/`send` 返回值) | `require(ok)` / SafeERC20 |
| 5 | [预言机操纵](oracle-manipulation/) | — | 高 | ✅(`getReserves` 现货价) | TWAP / Chainlink + 新鲜度校验 |
| 6 | [拒绝服务 DoS](denial-of-service/) | SWC-113/128 | 中 | ✅(for 循环内转账) | 拉模式 pull payment |
| 7 | [弱随机数](bad-randomness/) | SWC-120 | 高 | ✅(block 变量 + 随机上下文) | Chainlink VRF / commit-reveal |
| 8 | [不安全 delegatecall](delegatecall/) | SWC-112 | 高 | ✅(`delegatecall`) | 受控目标 + 存储布局对齐 |
| 9 | [前置交易/抢跑 MEV](front-running/) | SWC-114 | 中 | ⚠️ 需语义复核 | commit-reveal + 滑点保护 |

## 四、逐条审计结论(摘录)

- **重入(高)**:`reentrancy/Vulnerable.sol:19` 在 `balances` 清零前 `call{value}` 外部转账,
  攻击者可在回调里重入抽干。修复见 `Fixed.sol`(先清零,加 `nonReentrant`)。扫描器函数级启发式命中。
- **访问控制(高)**:`access-control/Vulnerable.sol:22` 用 `tx.origin` 鉴权,且 `setOwner` 无校验。
  修复:`onlyOwner` + `msg.sender`。扫描器关键字命中。
- **预言机(高)**:`oracle-manipulation/Vulnerable.sol` 用 `getReserves()` 现货比定价,闪电贷可操纵。
  修复:Chainlink + 新鲜度/正负校验。**注意**:此类需结合"价格从哪来"的数据流语义复核。
- **抢跑(中)**:`front-running/Vulnerable.sol` 明文 `claim(answer)` 进 mempool 被抢跑。
  此类**扫描器难以纯语法定位**,依赖人工/AI 语义审计;修复用 commit-reveal。

## 五、与 AI 安全的交叉(本作品集差异化)

- 可用 LLM 做合约语义审计补充静态扫描(对照 [06 AI 辅助代码审计](../06-ai-development/ai-assisted-security/)),
  但需防范模型对漏洞的**幻觉误报/漏报**——这正是本作品集 AI 安全能力的用武之处。
- 智能合约 + AI Agent 自动交易场景下,Agent 的**过度授权**(对应 OWASP LLM06)与合约权限控制叠加,
  可复用 [03 工具调用权限审计](../03-agent-rag-security/tool-permission-audit/) 的最小权限思路。

## 六、面试表达

> "我把智能合约审计做成了一个小闭环:先用自研静态扫描器按危险模式快速定位(重入、tx.origin、delegatecall、弱随机、现货预言机、push 转账、unchecked 算术),
> 再人工/AI 复核需要语义判断的(重入的 CEI 顺序、预言机的价格来源、抢跑),最后逐条评级并对照修复版给写法。
> 我很清楚静态工具有误报漏报,所以它只用来缩小排查范围,关键漏洞靠数据流复核——这跟我做 AI 代码审计是同一套方法论。"

## 安全边界

所有 Solidity 仅为审计教学示例,不编译部署、不执行、不针对任何真实合约;
扫描器只读取文本做静态匹配,不连接任何链或节点。
