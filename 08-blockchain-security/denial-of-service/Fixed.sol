// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 修复示例:拉模式提款(Pull Payment)
/// @notice 不主动循环转账,而是记账后让每个用户**自己来领**。
///         单个用户的失败只影响他自己,不会拖垮全局;也避免无界循环 gas 耗尽。
contract FixedDistributor {
    mapping(address => uint256) public owed;

    /// @dev 只记账,O(1)。
    function allocate(address user, uint256 amount) external {
        owed[user] += amount;
    }

    /// @dev 用户主动领取,失败只影响自己;遵循 CEI 先清零再转账。
    function withdraw() external {
        uint256 amount = owed[msg.sender];
        require(amount > 0, "nothing to withdraw");
        owed[msg.sender] = 0;                          // 先清零(防重入 + 一致性)
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
    }
}
