# 智能合约漏洞:不安全的委托调用 (Unsafe Delegatecall)

## 1. 原理
`delegatecall` 用**调用方(代理)的存储与上下文**执行被调合约的代码。若:
① 把 `delegatecall` 的**目标地址交给任意调用者**,或 ② 代理与实现的**存储布局错配**,
攻击者就能用被调代码改写代理的关键存储槽(如 `owner`),夺取整个合约。
2017 年 Parity 多签钱包冻结事件即与此相关。

## 2. 代码对照
- [`Vulnerable.sol`](Vulnerable.sol):`execute` 让任意人指定 `_impl` 与 calldata 做 `delegatecall`,可改写 slot0 的 owner。
- [`Fixed.sol`](Fixed.sol):实现地址仅 `onlyOwner` 可升级、`delegatecall` 只指向受控 `impl`、存储布局对齐。

## 3. 审计要点(危险模式)
- `delegatecall` 的**目标地址或 calldata 由外部输入控制**。
- 代理与实现的**存储变量顺序/类型不一致**(槽错配)。
- 可升级合约未用标准存储槽(ERC1967)或未做初始化保护。

## 4. 修复建议
delegatecall 目标固定且权限受控;用 OpenZeppelin UUPS/Transparent 代理与 ERC1967 标准槽;
严格对齐存储布局;实现合约加 `initializer` 防重复初始化。

## 5. 审计检查清单
- [ ] delegatecall 目标是否由外部可控?
- [ ] 代理/实现存储布局是否严格对齐?
- [ ] 升级权限是否受控、初始化是否防重入?

## 6. 面试表达
> "delegatecall 危险在于它用代理的存储执行别人的代码。两个坑:目标地址让调用者随便传,或者代理和实现的存储槽错配——攻击者就能改写 slot0 的 owner 夺权,Parity 钱包就是这类。修复是固定受控的实现地址、用 OpenZeppelin 的标准代理和 ERC1967 槽、严格对齐存储布局。"

## 安全边界
Solidity 仅为审计教学示例,不编译部署、不执行、不针对任何真实合约。
