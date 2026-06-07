# 智能合约漏洞:签名重放 (Signature Replay)

## 1. 原理
很多合约用**链下签名**授权链上动作(代付、permit、空投领取、跨链消息)。若被签名的消息
**不含 nonce、不绑定合约地址/chainid、不记录已用**,同一个签名就能被**重复提交**——
重放一次=多执行一次,提款类直接资金被多支。EIP-712 + nonce 是标准防御。

## 2. 代码对照
- [`Vulnerable.sol`](Vulnerable.sol):`claim` 的消息只有 `to+amount`,无 nonce、不标记已用 → 可重放。
- [`Fixed.sol`](Fixed.sol):消息加 `nonce + address(this) + block.chainid`,校验并消费 nonce,防重放与跨合约/跨链复用。

## 3. 审计要点(危险模式)
- 出现 `ecrecover(...)` 但合约里**没有 nonce / 已用标记**。
- 被签名的消息**不含合约地址、chainid**(可跨合约/跨链重放)。
- 自实现签名校验而非用 EIP-712 / OpenZeppelin ECDSA(易漏 malleability)。

## 4. 修复建议
消息含逐用户递增 nonce 并校验消费;绑定 `address(this)` 与 `block.chainid`;
用 EIP-712 结构化签名 + OpenZeppelin `ECDSA`(防 s 值 malleability);记录已用签名哈希。

## 5. 审计检查清单
- [ ] 用 `ecrecover` 的地方是否有 nonce / 防重放标记?
- [ ] 签名消息是否绑定合约地址与 chainid?
- [ ] 是否用 EIP-712 / OZ ECDSA 而非自造校验?

## 6. 面试表达
> "签名重放是链下签名授权的经典坑:消息里没 nonce 也不记录已用,同一个签名就能反复提交,提款类直接被多支。审计时我会搜 `ecrecover`,看有没有配 nonce、有没有绑定合约地址和 chainid 防跨链重放,以及是不是用了 EIP-712 和 OpenZeppelin 的 ECDSA。"

## 安全边界
Solidity 仅为审计教学示例,不编译部署、不执行、不针对任何真实合约。
