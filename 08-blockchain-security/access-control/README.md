# 智能合约漏洞:访问控制缺陷 (Access Control)

## 1. 原理
关键函数(改 owner、提款、铸币、升级)若**缺少权限校验**或**用错鉴权主体**,会被任意人调用。
两类最常见:① 忘加 `onlyOwner`;② 用 `tx.origin` 鉴权——它是整条交易的发起者,
用户被诱导调用恶意合约时 `tx.origin` 仍是用户,鉴权被钓鱼绕过(应始终用 `msg.sender`)。

## 2. 代码对照
- [`Vulnerable.sol`](Vulnerable.sol):`setOwner` 无任何校验(谁都能夺权);`withdraw` 用 `tx.origin == owner`。
- [`Fixed.sol`](Fixed.sol):`onlyOwner` 修饰符 + `msg.sender` 鉴权 + 转移所有权事件留痕。

## 3. 审计要点(危险模式)
- 改写 owner / 资金 / 权限的函数**没有访问控制修饰符**。
- 出现 `tx.origin ==`(几乎总是错误的鉴权方式)。
- 未初始化的 owner、可被重复 `initialize` 的可升级合约。

## 4. 修复建议
用 OpenZeppelin `Ownable` / `AccessControl`;鉴权一律 `msg.sender`;所有权转移用两步(propose + accept);
初始化函数加 `initializer` 防重入初始化。

## 5. 审计检查清单
- [ ] 每个状态变更/资金函数是否都有正确的权限校验?
- [ ] 是否存在 `tx.origin` 鉴权?
- [ ] owner / 初始化能否被抢占或重复调用?

## 6. 面试表达
> "访问控制是合约里最朴素也最致命的一类:关键函数忘了加 `onlyOwner`,或者用 `tx.origin` 鉴权被钓鱼绕过。我审计时会把所有改 owner、提款、铸币、升级的函数列出来,逐个确认权限修饰符,并全局搜 `tx.origin`——鉴权应该永远用 `msg.sender`。"

## 安全边界
Solidity 仅为审计教学示例,不编译部署、不执行、不针对任何真实合约。
