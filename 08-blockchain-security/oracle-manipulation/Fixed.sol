// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

interface IChainlinkFeed {
    function latestRoundData() external view returns (
        uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound
    );
}

/// @title 修复示例:抗操纵的价格来源
/// @notice 用 Chainlink 等去中心化预言机,并校验数据新鲜度与正负;
///         (另一路线是用 DEX 的 TWAP 时间加权均价,抬高瞬时操纵成本。)
contract FixedLending {
    IChainlinkFeed public feed;
    uint256 public constant MAX_DELAY = 1 hours;

    constructor(address _feed) {
        feed = IChainlinkFeed(_feed);
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , uint256 updatedAt, ) = feed.latestRoundData();
        require(answer > 0, "bad price");                 // 防 0/负价
        require(block.timestamp - updatedAt <= MAX_DELAY, "stale price"); // 防过期
        return uint256(answer);
    }

    function borrowAgainst(uint256 collateral) external view returns (uint256) {
        return collateral * getPrice() / 1e18;
    }
}
