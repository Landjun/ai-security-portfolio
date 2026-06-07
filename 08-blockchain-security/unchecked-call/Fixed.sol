// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 修复示例:检查外部调用返回值
/// @notice 校验 `call` 的 bool 返回值并在失败时 revert;ERC20 转账用 SafeERC20。
///         状态更新遵循 CEI:先记账(或先扣),再外部调用并校验。
contract FixedPayer {
    mapping(address => uint256) public credited;

    function pay(address to, uint256 amount) external {
        credited[to] += amount;            // CEI:先记账(状态变更在外部调用之前)
        (bool ok, ) = to.call{value: amount}("");
        require(ok, "transfer failed");    // 校验返回值,失败即 revert
    }
}
