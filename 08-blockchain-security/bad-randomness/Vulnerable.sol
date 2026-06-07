// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:可预测的随机数(Bad Randomness)
/// @notice 用链上变量(block.timestamp / prevrandao / blockhash)做随机源。
///         这些值矿工/验证者可影响或预测,攻击者能在同一区块算出结果只在必赢时参与。
contract VulnerableLottery {
    /// @dev 危险:链上可预测变量当随机源。
    function pickWinner(uint256 players) public view returns (uint256) {
        return uint256(
            keccak256(abi.encodePacked(block.timestamp, block.prevrandao, msg.sender))
        ) % players;                       // <- 结果在交易内即可被算出/操纵
    }
}
