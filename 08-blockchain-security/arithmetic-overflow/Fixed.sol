// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 修复示例:整数下溢/溢出
/// @notice 1) 显式 require 校验余额;2) 不在 unchecked 内做与资金相关的算术,
///         保留 0.8+ 的内建溢出/下溢检查(异常即 revert)。
contract FixedBank {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient balance"); // 显式校验
        balances[msg.sender] -= amount;   // 0.8+ 默认检查,下溢会 revert
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
    }
}
