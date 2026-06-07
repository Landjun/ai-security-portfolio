# 智能合约漏洞:可预测的随机数 (Bad Randomness)

## 1. 原理
链上一切都是确定且公开的。用 `block.timestamp`、`block.prevrandao`、`blockhash`、`msg.sender`
当随机源,**矿工/验证者可影响、攻击者可在同一交易内提前算出结果**——抽奖/发牌/NFT 抽稀有度
都会被"只在必赢时参与"地薅干。

## 2. 代码对照
- [`Vulnerable.sol`](Vulnerable.sol):`pickWinner` 用 `keccak256(block.timestamp, prevrandao, sender) % n`。
- [`Fixed.sol`](Fixed.sol):改用 **Chainlink VRF** 可验证随机数(异步回调);或 commit-reveal。

## 3. 审计要点(危险模式)
- `keccak256`/取模的输入里有 `block.timestamp`、`block.prevrandao`、`blockhash`、`block.number`。
- 随机结果在**同一笔交易内**即可被读取/复算。
- 抽奖/分配/稀有度依赖链上自造随机。

## 4. 修复建议
用 Chainlink VRF 等可验证随机函数(带密码学证明、异步回调);
或 commit-reveal(先提交哈希承诺、后揭示);避免任何链上可预测变量做随机源。

## 5. 审计检查清单
- [ ] 随机源是否包含链上可预测变量?
- [ ] 随机结果能否在交易内被提前算出?
- [ ] 是否用了 VRF 或 commit-reveal?

## 6. 面试表达
> "链上没有真随机:用 `block.timestamp` 或 `prevrandao` 做抽奖,矿工能影响、攻击者能在同一交易里先算出结果再决定参不参与。正确做法是 Chainlink VRF 这种带密码学证明的可验证随机数,或者 commit-reveal。审计时我会搜随机数的输入里有没有 block 系列变量。"

## 安全边界
Solidity 仅为审计教学示例,不编译部署、不执行、不针对任何真实合约。
