// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

interface IPair {
    function getReserves() external view returns (uint112 r0, uint112 r1, uint32 ts);
}

/// @title 漏洞示例:价格预言机操纵(Oracle Manipulation)
/// @notice 直接用 DEX 现货储备算价格。攻击者用闪电贷瞬间拉偏储备 -> 价格被操纵,
///         再在本合约以错误价格借贷/清算套利。
contract VulnerableLending {
    IPair public pair;

    constructor(address _pair) {
        pair = IPair(_pair);
    }

    /// @dev 危险:用单一 DEX 的瞬时储备比当作价格,可被闪电贷操纵。
    function getPrice() public view returns (uint256) {
        (uint112 r0, uint112 r1, ) = pair.getReserves();
        return uint256(r1) * 1e18 / uint256(r0);   // <- 现货价,无 TWAP/多源
    }

    function borrowAgainst(uint256 collateral) external view returns (uint256) {
        return collateral * getPrice() / 1e18;     // 用被操纵的价格放贷
    }
}
