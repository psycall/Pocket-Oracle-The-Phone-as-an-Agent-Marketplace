// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

/**
 * @title AgentRegistry
 * @notice Global registry for Orvion Agents on Arc Network.
 *         Stores capabilities, reputation, and earnings.
 */
contract AgentRegistry {
    address public owner;
    address public taskEscrow;

    struct Agent {
        address owner;
        address agentWallet;
        bytes32 capabilitiesHash;
        bytes32 ap2DidHash;
        uint256 reputation;         // 0-10,000 (100.00%)
        uint256 totalTasksCompleted;
        uint256 totalEarnedUSDC;
        uint64  registeredAt;
        bool    active;
    }

    mapping(address => Agent) public agents;
    mapping(address => bool)  public isRegistered;
    address[] public agentList;

    event AgentRegistered(address indexed wallet, address indexed owner, bytes32 capabilitiesHash, bytes32 ap2DidHash);
    event ReputationUpdated(address indexed wallet, uint256 newScore);
    event EarningsRecorded(address indexed wallet, uint256 amount, uint256 totalEarned);
    event AgentDeactivated(address indexed wallet);
    event TaskEscrowSet(address indexed escrow);

    error AlreadyRegistered();
    error NotOwner();
    error NotActive();
    error NotEscrow();
    error EscrowAlreadySet();

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    modifier onlyEscrow() {
        if (msg.sender != taskEscrow) revert NotEscrow();
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setTaskEscrow(address _escrow) external onlyOwner {
        if (taskEscrow != address(0)) revert EscrowAlreadySet();
        taskEscrow = _escrow;
        emit TaskEscrowSet(_escrow);
    }

    function register(
        address agentWallet,
        bytes32 capabilitiesHash,
        bytes32 ap2DidHash
    ) external {
        if (isRegistered[agentWallet]) revert AlreadyRegistered();

        agents[agentWallet] = Agent({
            owner: msg.sender,
            agentWallet: agentWallet,
            capabilitiesHash: capabilitiesHash,
            ap2DidHash: ap2DidHash,
            reputation: 5_000, // neutral start (50%)
            totalTasksCompleted: 0,
            totalEarnedUSDC: 0,
            registeredAt: uint64(block.timestamp),
            active: true
        });
        isRegistered[agentWallet] = true;
        agentList.push(agentWallet);

        emit AgentRegistered(agentWallet, msg.sender, capabilitiesHash, ap2DidHash);
    }

    function recordSuccess(address agentWallet, uint256 amountUSDC) external onlyEscrow {
        Agent storage a = agents[agentWallet];
        if (!a.active) revert NotActive();

        a.totalTasksCompleted += 1;
        a.totalEarnedUSDC += amountUSDC;

        // EMA: new = old * 0.95 + 10_000 * 0.05  (success bumps toward 100%)
        a.reputation = (a.reputation * 95 + 10_000 * 5) / 100;

        emit EarningsRecorded(agentWallet, amountUSDC, a.totalEarnedUSDC);
        emit ReputationUpdated(agentWallet, a.reputation);
    }

    function recordFailure(address agentWallet) external onlyEscrow {
        Agent storage a = agents[agentWallet];
        if (!a.active) revert NotActive();
        // EMA: new = old * 0.95  (failure decays score)
        a.reputation = (a.reputation * 95) / 100;
        emit ReputationUpdated(agentWallet, a.reputation);
    }

    function deactivate(address agentWallet) external {
        if (agents[agentWallet].owner != msg.sender) revert NotOwner();
        agents[agentWallet].active = false;
        emit AgentDeactivated(agentWallet);
    }

    function totalAgents() external view returns (uint256) {
        return agentList.length;
    }

    function getAgent(address wallet) external view returns (Agent memory) {
        return agents[wallet];
    }
}
