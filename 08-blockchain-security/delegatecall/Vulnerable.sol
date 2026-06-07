// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:不安全的 delegatecall(Parity 钱包式)
/// @notice delegatecall 在**调用方的存储上下文**里执行被调代码。
///         若把目标地址交给用户、或存储布局错配,攻击者可改写本合约的关键槽(如 owner)。
contract VulnerableProxy {
    address public owner;          // slot 0
    address public impl;           // slot 1

    constructor() {
        owner = msg.sender;
    }

    /// @dev 危险:任意人可指定 _impl 并 delegatecall 任意数据,
    ///      被调代码若写 slot 0,就能改掉本合约 owner。
    function execute(address _impl, bytes calldata data) external {
        (bool ok, ) = _impl.delegatecall(data);    // <- 目标地址 + calldata 都由调用者控制
        require(ok, "delegatecall failed");
    }
}
