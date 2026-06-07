// SPDX-License-Identifier: MIT
// 【修复合约】重入防御:检查-生效-交互(CEI) + 重入锁。
pragma solidity ^0.8.0;

contract SecureBank {
    mapping(address => uint256) public balances;
    bool private locked;                       // 重入锁

    modifier nonReentrant() {
        require(!locked, "reentrant call");
        locked = true;
        _;
        locked = false;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // 修复1:检查-生效-交互(CEI)—— 先把余额清零,再做外部转账。
    // 修复2:nonReentrant 重入锁,从根上阻止重入。
    function withdraw() external nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "no balance");

        balances[msg.sender] = 0;              // <-- 先更新状态(生效)
        (bool ok, ) = msg.sender.call{value: amount}("");   // <-- 再外部交互
        require(ok, "transfer failed");
    }
}
