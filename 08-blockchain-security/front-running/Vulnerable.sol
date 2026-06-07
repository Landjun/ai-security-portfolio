// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:前置交易 / 抢跑(Front-running / MEV)
/// @notice 奖励"第一个提交正确答案的人"。但提交是明文进 mempool 的,
///         任何人(含矿工/搬运机器人)看到后可用更高 gas 抢先打包,夺走奖励。
contract VulnerableReward {
    bytes32 public immutable answerHash;

    constructor(bytes32 _answerHash) {
        answerHash = _answerHash;
    }

    /// @dev 危险:答案明文进 mempool,会被抢跑。
    function claim(string calldata answer) external {
        require(keccak256(abi.encodePacked(answer)) == answerHash, "wrong");
        // ... 发放奖励(明文 answer 已暴露在待打包交易里)
    }
}
