// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:签名重放(Signature Replay)
/// @notice 用链下签名授权链上动作(如代付提款),但签名内容**不含 nonce / 不标记已用**。
///         同一个签名可被**重复提交**,反复执行提款 -> 资金被多次支取。
contract VulnerableClaim {
    address public signer;

    constructor(address _signer) {
        signer = _signer;
    }

    /// @dev 危险:消息里只有 to+amount,没有 nonce,也不记录已用签名 -> 可重放。
    function claim(address to, uint256 amount, uint8 v, bytes32 r, bytes32 s) external {
        bytes32 hash = keccak256(abi.encodePacked(to, amount));
        require(ecrecover(hash, v, r, s) == signer, "bad sig");   // <- 无 nonce / 无防重放
        (bool ok, ) = to.call{value: amount}("");
        require(ok, "transfer failed");
    }
}
