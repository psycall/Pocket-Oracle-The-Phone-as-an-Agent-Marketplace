// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title  PocketOracle
/// @notice Escrow contract for the Pocket Oracle agent marketplace.
/// @dev    A client funds a task; the assigned agent completes it; the
///         payment is released on-chain. No admin, no upgrades.
contract PocketOracle {
    struct Task {
        address client;
        address agent;
        uint256 value;
        bool completed;
        bool paid;
    }

    mapping(uint256 => Task) public tasks;
    uint256 public taskCount;

    event TaskCreated(
        uint256 indexed id,
        address indexed client,
        address indexed agent,
        uint256 value
    );
    event TaskCompleted(uint256 indexed id);
    event PaymentReleased(
        uint256 indexed id,
        address indexed agent,
        uint256 value
    );

    /// @notice Client funds a new task addressed to a specific agent.
    function createTask(address _agent) external payable {
        require(msg.value > 0, "Value required");
        require(_agent != address(0), "Invalid agent");

        tasks[taskCount] = Task({
            client: msg.sender,
            agent: _agent,
            value: msg.value,
            completed: false,
            paid: false
        });

        emit TaskCreated(taskCount, msg.sender, _agent, msg.value);
        taskCount++;
    }

    /// @notice Agent marks the task as completed.
    function completeTask(uint256 _id) external {
        Task storage task = tasks[_id];
        require(msg.sender == task.agent, "Not the agent");
        require(!task.completed, "Already completed");

        task.completed = true;
        emit TaskCompleted(_id);
    }

    /// @notice Releases the escrowed payment to the agent.
    /// @dev    Anyone can trigger; funds always go to the registered agent.
    function releasePayment(uint256 _id) external {
        Task storage task = tasks[_id];
        require(task.completed, "Not completed");
        require(!task.paid, "Already paid");

        task.paid = true;
        (bool ok, ) = payable(task.agent).call{value: task.value}("");
        require(ok, "Transfer failed");

        emit PaymentReleased(_id, task.agent, task.value);
    }
}
