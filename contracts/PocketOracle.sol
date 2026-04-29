// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title PocketOracle (Arc Network + Circle USDC Edition)
 * @notice Professional Agentic Economy Escrow supporting ERC-8183 and USDC settlement.
 * @dev Optimized for Arc Network Builders Fund compliance.
 */
contract PocketOracle {
    IERC20 public immutable usdc;
    
    struct Task {
        address client;
        address agent;
        uint256 amount;
        bool completed;
        bool paid;
        bytes32 metadataHash; // ERC-8183 compatible metadata
    }

    mapping(uint256 => Task) public tasks;
    uint256 public taskCount;

    event TaskCreated(uint256 indexed id, address indexed client, address indexed agent, uint256 amount, bytes32 metadataHash);
    event TaskCompleted(uint256 indexed id);
    event PaymentReleased(uint256 indexed id, address indexed agent, uint256 amount);

    constructor(address _usdcAddress) {
        require(_usdcAddress != address(0), "Invalid USDC address");
        usdc = IERC20(_usdcAddress);
    }

    /**
     * @notice Create a task with USDC funding.
     * @dev Aligned with Circle CCTP for cross-chain liquidity.
     */
    function createTask(address _agent, uint256 _amount, bytes32 _metadataHash) external {
        require(_amount > 0, "Amount must be > 0");
        require(_agent != address(0), "Invalid agent address");
        
        // Transfer USDC from client to this contract (Escrow)
        require(usdc.transferFrom(msg.sender, address(this), _amount), "USDC transfer failed");

        tasks[taskCount] = Task({
            client: msg.sender,
            agent: _agent,
            amount: _amount,
            completed: false,
            paid: false,
            metadataHash: _metadataHash
        });

        emit TaskCreated(taskCount, msg.sender, _agent, _amount, _metadataHash);
        taskCount++;
    }

    function completeTask(uint256 _id) external {
        Task storage task = tasks[_id];
        require(msg.sender == task.agent, "Only assigned agent can complete");
        require(!task.completed, "Task already completed");
        
        task.completed = true;
        emit TaskCompleted(_id);
    }

    function releasePayment(uint256 _id) external {
        Task storage task = tasks[_id];
        require(task.completed, "Task not yet completed");
        require(!task.paid, "Payment already released");

        task.paid = true;
        require(usdc.transfer(task.agent, task.amount), "USDC payment failed");
        
        emit PaymentReleased(_id, task.agent, task.amount);
    }
}
