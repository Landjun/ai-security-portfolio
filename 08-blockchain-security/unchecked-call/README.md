# 智能合约漏洞:未检查的外部调用返回值 (Unchecked Low-level Call)

## 1. 原理
低级调用 `addr.call{value:}()` / `addr.send()` **失败时不会抛异常**,只返回 `false`。
若不检查返回值,合约会把"转账失败"误判为成功,导致**记账与实际资金不一致**。
(`transfer` 会自动 revert,但 2300 gas 限制又可能引发别的问题,需权衡。)

## 2. 代码对照
- [`Vulnerable.sol`](Vulnerable.sol):`pay` 丢弃 `call` 返回值后照常记账;`payViaSend` 不校验 `send`。
- [`Fixed.sol`](Fixed.sol):`(bool ok, ) = to.call{...}` + `require(ok)`,失败即 revert。

## 3. 审计要点(危险模式)
- `.call{value:...}("")` / `.send(...)` 的**返回值未赋值或未 `require`**。
- ERC20 的 `transfer`/`transferFrom` 返回值被忽略(有些代币不按标准返回)。
- 外部调用成功与否影响后续记账,却未做一致性处理。

## 4. 修复建议
低级调用一律 `(bool ok, ) = ...; require(ok)`;ERC20 用 OpenZeppelin `SafeERC20`;
遵循 CEI,失败时回滚整笔交易保持一致性。

## 5. 审计检查清单
- [ ] 所有 `call`/`send` 返回值是否都被校验?
- [ ] ERC20 转账是否用了 SafeERC20 或检查返回值?
- [ ] 外部调用失败时记账是否会回滚保持一致?

## 6. 面试表达
> "`call` 和 `send` 失败只返回 false 不 revert,忽略返回值就会把失败的转账当成功记账。我审计时会全局搜 `.call{value` 和 `.send(`,看返回值有没有被 `require`;ERC20 转账则看有没有用 SafeERC20,因为有些代币不按标准返回 bool。"

## 安全边界
Solidity 仅为审计教学示例,不编译部署、不执行、不针对任何真实合约。
