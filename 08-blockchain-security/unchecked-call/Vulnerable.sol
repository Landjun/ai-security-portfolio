// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:未检查的外部调用返回值(Unchecked Call)
/// @notice 低级 `call`/`send` 失败时不会 revert,只返回 false。
///         不检查返回值,会把"转账失败"误当成功,造成记账与实际不一致。
contract VulnerablePayer {
    mapping(address => uint256) public credited;

    /// @dev 危险一:忽略 call 的返回值。
    function pay(address to, uint256 amount) external {
        to.call{value: amount}("");        // <- 返回值被丢弃,失败也"当成功"
        credited[to] += amount;            // 实际没转成功,却记了账
    }

    /// @dev 危险二:send 返回 false 未处理。
    function payViaSend(address payable to, uint256 amount) external {
        to.send(amount);                   // <- 未校验返回值
    }
}
