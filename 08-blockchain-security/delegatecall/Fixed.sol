// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 修复示例:受控的 delegatecall
/// @notice 1) 实现地址固定/仅 owner 可改;2) 不把 delegatecall 目标交给任意调用者;
///         3) 代理与实现存储布局严格对齐(生产用 OpenZeppelin 的 ERC1967/UUPS 标准槽)。
contract FixedProxy {
    address public owner;          // slot 0(与实现严格对齐)
    address public impl;           // slot 1

    constructor(address _impl) {
        owner = msg.sender;
        impl = _impl;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    /// @dev 只有 owner 能升级实现;目标不再由任意调用者传入。
    function upgradeTo(address _impl) external onlyOwner {
        require(_impl.code.length > 0, "impl not a contract");
        impl = _impl;
    }

    /// @dev delegatecall 只指向受控的 impl,数据来自正常业务调用。
    function _delegate() internal {
        (bool ok, ) = impl.delegatecall(msg.data);
        require(ok, "delegatecall failed");
    }

    fallback() external payable { _delegate(); }
    receive() external payable {}
}
