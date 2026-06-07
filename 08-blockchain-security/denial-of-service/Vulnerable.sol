// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:拒绝服务(DoS via push payment / unbounded loop)
/// @notice push 模式:循环给一组地址逐个转账。只要有一个收款地址是
///         "拒收"的恶意合约(receive 里 revert),整个循环回滚,
///         所有人都拿不到钱 —— 合约被永久卡死。
contract VulnerableDistributor {
    address[] public recipients;

    function join() external {
        recipients.push(msg.sender);
    }

    /// @dev 危险:一个 recipient revert,整笔交易回滚,全员被阻塞。
    ///      recipients 过长还会 gas 耗尽。
    function distribute() external payable {
        uint256 share = msg.value / recipients.length;
        for (uint256 i = 0; i < recipients.length; i++) {
            payable(recipients[i]).transfer(share);   // <- push 模式,单点失败拖垮全局
        }
    }
}
