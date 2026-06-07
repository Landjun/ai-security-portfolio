# 智能合约漏洞:无保护的自毁 (Unprotected Self-Destruct, SWC-106)

## 1. 原理
`selfdestruct` 会销毁合约并把全部余额转给指定地址。若销毁/提全款类函数**缺少访问控制**,
任意人都能摧毁合约、卷走资金或冻结依赖它的系统。2017 年 Parity 多签库被无保护的 `kill`
误销毁、导致大量资金被永久冻结,即此类根因。

> 注:EIP-6780(坎昆升级)后 `selfdestruct` 语义已弱化(同交易创建才真正删除),
> 但"高危函数无访问控制"这一问题本质不变,且仍能转走余额。

## 2. 代码对照
- [`Vulnerable.sol`](Vulnerable.sol):`kill()` 无 `onlyOwner`,任意人可 `selfdestruct` 卷款。
- [`Fixed.sol`](Fixed.sol):`kill()` 加 `onlyOwner`;并建议改"可暂停 + 有序撤回"而非 selfdestruct。

## 3. 审计要点(危险模式)
- `selfdestruct(` / 提取全部余额的函数**无访问控制**。
- 销毁地址由调用者控制。
- 依赖 selfdestruct 的升级/清退逻辑(EIP-6780 后行为已变)。

## 4. 修复建议
高危函数一律加 `onlyOwner`/多签;尽量不用 selfdestruct,改用可暂停(circuit breaker)+ 资金有序撤回;
销毁地址固定为受信地址。

## 5. 审计检查清单
- [ ] 所有 `selfdestruct` / 提全款函数是否都有访问控制?
- [ ] 销毁/收款地址是否可被调用者操纵?
- [ ] 是否依赖 selfdestruct 的旧语义(EIP-6780 后已变)?

## 6. 面试表达
> "无保护的 selfdestruct 是 SWC-106:销毁合约、卷走全部余额的函数忘了加权限,任意人就能摧毁合约,Parity 多签库被误 kill 冻结资金就是这类。审计时我会搜 `selfdestruct`,确认它所在函数有没有 onlyOwner;现代实践其实更建议别用 selfdestruct,改成可暂停加有序撤回。"

## 安全边界
Solidity 仅为审计教学示例,不编译部署、不执行、不针对任何真实合约。
