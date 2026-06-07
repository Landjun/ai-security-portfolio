// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 修复示例:防签名重放
/// @notice 1) 消息里加 nonce(逐用户递增);2) 绑定本合约地址与 chainid(防跨合约/跨链重放);
///         3) 标记已用签名。生产建议用 EIP-712 结构化签名 + OpenZeppelin ECDSA。
contract FixedClaim {
    address public signer;
    mapping(address => uint256) public nonces;          // 每用户递增 nonce

    constructor(address _signer) {
        signer = _signer;
    }

    function claim(address to, uint256 amount, uint256 nonce, uint8 v, bytes32 r, bytes32 s) external {
        require(nonce == nonces[to], "bad nonce");      // 防重放:nonce 必须匹配
        // 绑定 nonce + 合约地址 + chainid,杜绝重放与跨合约/跨链复用
        bytes32 hash = keccak256(abi.encodePacked(to, amount, nonce, address(this), block.chainid));
        require(ecrecover(hash, v, r, s) == signer, "bad sig");
        nonces[to] += 1;                                // 生效:消费该 nonce
        (bool ok, ) = to.call{value: amount}("");
        require(ok, "transfer failed");
    }
}
