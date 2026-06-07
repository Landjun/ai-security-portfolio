// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

interface IVRFConsumer {
    /// 真实场景由 Chainlink VRF 异步回调提供可验证随机数。
    function requestRandomWords() external returns (uint256 requestId);
}

/// @title 修复示例:可验证的随机源
/// @notice 不在链上自造随机数,而是用 Chainlink VRF 等**可验证随机函数**异步获取;
///         或用 commit-reveal(用户先提交哈希承诺,后揭示,杜绝事前预测)。
contract FixedLottery {
    IVRFConsumer public vrf;
    uint256 public latestRequestId;

    constructor(address _vrf) {
        vrf = IVRFConsumer(_vrf);
    }

    /// @dev 向 VRF 请求随机数(真实由预言机异步回调写回,带密码学证明)。
    function drawWinner() external {
        latestRequestId = vrf.requestRandomWords();
        // 随机结果在 VRF 回调里处理,链上变量不参与,无法被事前预测。
    }
}
