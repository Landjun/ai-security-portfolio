// SPDX-License-Identifier: MIT
// 【漏洞合约 · 审计靶场】重入(Reentrancy)漏洞 —— 经典 The DAO 漏洞
// 仅用于审计教学,请勿部署。
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // 漏洞:先外部转账(call 把控制权交给攻击者合约),再更新余额。
    // 攻击者在 receive/fallback 里再次调用 withdraw,反复重入抽干合约。
    function withdraw() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "no balance");

        (bool ok, ) = msg.sender.call{value: amount}("");   // <-- 外部调用,重入点
        require(ok, "transfer failed");

        balances[msg.sender] = 0;                            // <-- 太晚:重入期间余额仍是旧值
    }
}
