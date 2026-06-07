// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:整数下溢/溢出(Arithmetic)
/// @notice Solidity 0.8+ 默认带溢出检查,但 `unchecked` 块会关闭检查。
///         本例在 unchecked 中做减法,余额不足时下溢成巨大数 -> 资金被抽走。
contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    /// @dev 危险:unchecked 关闭了下溢保护,amount 大于余额时
    ///      balances[msg.sender] 会下溢为接近 2^256 的天文数字。
    function withdraw(uint256 amount) external {
        unchecked {
            balances[msg.sender] -= amount;   // <- 缺少 require 校验 + 在 unchecked 内
        }
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
    }
}
