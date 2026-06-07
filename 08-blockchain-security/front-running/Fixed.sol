// SPDX-License-Identifier: MIT
// 仅用于静态审计教学,不部署、不执行、不针对任何真实合约。
pragma solidity ^0.8.20;

/// @title 修复示例:commit-reveal 抗抢跑
/// @notice 两阶段:① commit 只提交"答案+地址+盐"的哈希承诺(不暴露明文);
///         ② 一段时间后 reveal 揭示明文,合约校验承诺。抢跑者看不到明文,
///         即便抄走承诺哈希,reveal 时绑定了原提交者地址也无法冒领。
contract FixedReward {
    bytes32 public immutable answerHash;
    mapping(address => bytes32) public commitOf;
    mapping(address => uint256) public commitBlock;
    uint256 public constant REVEAL_DELAY = 5;   // 至少隔几个区块再揭示

    constructor(bytes32 _answerHash) {
        answerHash = _answerHash;
    }

    /// @dev 阶段一:提交承诺 = keccak256(answer, msg.sender, salt)。
    function commit(bytes32 commitment) external {
        commitOf[msg.sender] = commitment;
        commitBlock[msg.sender] = block.number;
    }

    /// @dev 阶段二:揭示明文,校验承诺与答案。承诺绑定了 msg.sender,无法被冒领。
    function reveal(string calldata answer, bytes32 salt) external {
        require(block.number >= commitBlock[msg.sender] + REVEAL_DELAY, "too early");
        bytes32 c = keccak256(abi.encodePacked(answer, msg.sender, salt));
        require(c == commitOf[msg.sender], "commit mismatch");
        require(keccak256(abi.encodePacked(answer)) == answerHash, "wrong answer");
        // ... 发放奖励
    }
}
