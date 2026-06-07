// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:无保护的 selfdestruct(Unprotected Self-Destruct, SWC-106)
/// @notice 销毁合约 / 提走全部余额的高危函数没有访问控制 -> 任意人可摧毁合约、卷走资金。
///         2017 Parity 多签库被无保护的 kill 函数销毁、冻结大量资金即类似根因。
contract VulnerableWallet {
    address public owner;

    constructor() payable {
        owner = msg.sender;
    }

    /// @dev 危险:谁都能调用,把合约自毁并把全部余额发给调用者。
    function kill() external {
        selfdestruct(payable(msg.sender));   // <- 无 onlyOwner,任意人可摧毁/卷款
    }
}
