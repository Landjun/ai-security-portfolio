// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 修复示例:受控的合约销毁
/// @notice 1) 自毁/提全款类函数必须 onlyOwner;2) 现代实践更倾向**不用 selfdestruct**
///         (其语义在 EIP-6780 后已弱化),改用"暂停 + 资金有序撤回"。
contract FixedWallet {
    address public owner;

    constructor() payable {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    /// @dev 仅 owner 可销毁;更稳妥的做法是用可暂停 + 提款,避免 selfdestruct。
    function kill() external onlyOwner {
        selfdestruct(payable(owner));
    }
}
