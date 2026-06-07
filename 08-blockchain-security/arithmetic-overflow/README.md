# 智能合约漏洞:整数溢出 / 下溢 (Arithmetic Over/Underflow)

## 1. 原理
EVM 的整数是定长的(如 `uint256`)。超出范围会回绕:`0 - 1` 下溢成 `2^256-1`。
Solidity **0.8 之前**默认不检查,需手动用 SafeMath;**0.8 起**默认检查、溢出即 revert,
但 **`unchecked { }` 块会主动关闭检查**——很多新漏洞就出在被滥用的 `unchecked` 里。

## 2. 代码对照
- [`Vulnerable.sol`](Vulnerable.sol):`withdraw` 在 `unchecked` 中做 `balances -= amount` 且无余额校验,下溢可把余额刷成天文数字。
- [`Fixed.sol`](Fixed.sol):先 `require(balance >= amount)`,再在受检算术下扣减(0.8+ 下溢自动 revert)。

## 3. 审计要点(危险模式)
- 出现 `unchecked { }` 且块内是**与资金/余额相关的加减**。
- `-=` / `+=` 前**缺少 `require` 边界校验**。
- 老版本 `pragma`(< 0.8)且未引入 SafeMath。

## 4. 修复建议
0.8+ 默认检查不要随意 `unchecked`;关键算术配 `require` 显式边界;老项目用 OpenZeppelin SafeMath。

## 5. 审计检查清单
- [ ] 是否存在 `unchecked` 包裹的资金算术?
- [ ] 加减乘前是否有边界/余额校验?
- [ ] 编译器版本是否 ≥ 0.8 或已用 SafeMath?

## 6. 面试表达
> "0.8 以后整数默认带溢出检查,所以现在的溢出漏洞多半出在 `unchecked` 块被滥用——开发者为省 gas 关掉检查却忘了自己加边界校验。审计时我会重点搜 `unchecked` 里有没有资金相关的加减、前面有没有 `require` 兜底。"

## 安全边界
Solidity 仅为审计教学示例,不编译部署、不执行、不针对任何真实合约。
