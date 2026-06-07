// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 漏洞示例:访问控制缺陷(Access Control)
/// @notice 两个典型问题:1) 关键函数无访问控制;2) 用 tx.origin 鉴权(可被钓鱼中转)。
contract VulnerableVault {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    /// @dev 危险一:谁都能调用,直接夺取 owner。
    function setOwner(address newOwner) external {
        owner = newOwner;            // <- 缺少 onlyOwner 校验
    }

    /// @dev 危险二:用 tx.origin 鉴权。受害者被诱导调用恶意合约时,
    ///      tx.origin 仍是受害者,鉴权被绕过。
    function withdraw(address payable to, uint256 amount) external {
        require(tx.origin == owner, "not owner");   // <- 应为 msg.sender
        to.transfer(amount);
    }
}
