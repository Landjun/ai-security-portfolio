// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 修复示例:访问控制
/// @notice 1) 关键函数加 onlyOwner;2) 用 msg.sender 鉴权(非 tx.origin);
///         3) 转移所有权用两步或事件留痕。生产建议用 OpenZeppelin Ownable。
contract FixedVault {
    address public owner;

    event OwnerChanged(address indexed from, address indexed to);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");   // msg.sender,不是 tx.origin
        _;
    }

    function setOwner(address newOwner) external onlyOwner {
        require(newOwner != address(0), "zero addr");
        emit OwnerChanged(owner, newOwner);
        owner = newOwner;
    }

    function withdraw(address payable to, uint256 amount) external onlyOwner {
        to.transfer(amount);
    }
}
