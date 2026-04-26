// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {IUSDC} from "./interfaces/IUSDC.sol";
import {AgentRegistry} from "./AgentRegistry.sol";

/**
 * @title TaskEscrow
 * @notice Trustless USDC escrow for agent-to-agent tasks on Arc.
 * @dev Optimized for sub-cent nanopayments. Integrates with AP2 mandate hashes.
 */
contract TaskEscrow {
    enum Status { None, Pending, Completed, Disputed, Refunded }

    struct Task {
        bytes32 id;
        address requester;
        address executor;
        uint256 amount;          // USDC, 6 decimals
        bytes32 inputHash;       // hash of payload
        bytes32 cartMandateHash; // AP2 Cart Mandate hash (links off-chain VC)
        bytes32 outputHash;      // proof-of-execution hash, set on completion
        uint64  createdAt;
        uint64  deadline;
        Status  status;
    }

    IUSDC         public immutable usdc;
    AgentRegistry public immutable registry;
    address       public immutable proofOfExecution;
    uint256       public constant FEE_BPS = 50;       // 0.5% protocol fee
    address       public immutable feeRecipient;

    mapping(bytes32 => Task) public tasks;

    event TaskCreated(bytes32 indexed id, address indexed requester, address indexed executor, uint256 amount, bytes32 cartMandateHash);
    event TaskCompleted(bytes32 indexed id, bytes32 outputHash, uint256 paid, uint256 fee);
    event TaskRefunded(bytes32 indexed id);
    event TaskDisputed(bytes32 indexed id);

    error InvalidExecutor();
    error TaskNotPending();
    error DeadlinePassed();
    error NotAuthorized();
    error TaskExists();
    error ZeroAmount();

    constructor(address _usdc, address _registry, address _proof, address _fee) {
        usdc = IUSDC(_usdc);
        registry = AgentRegistry(_registry);
        proofOfExecution = _proof;
        feeRecipient = _fee;
    }

    function createTask(
        bytes32 id,
        address executor,
        uint256 amount,
        bytes32 inputHash,
        bytes32 cartMandateHash,
        uint64 deadline
    ) external {
        if (tasks[id].status != Status.None) revert TaskExists();
        if (!registry.isRegistered(executor)) revert InvalidExecutor();
        if (amount == 0) revert ZeroAmount();
        
        // Basic requirement: transfer USDC to escrow
        require(usdc.transferFrom(msg.sender, address(this), amount), "Escrow deposit failed");

        tasks[id] = Task({
            id: id,
            requester: msg.sender,
            executor: executor,
            amount: amount,
            inputHash: inputHash,
            cartMandateHash: cartMandateHash,
            outputHash: bytes32(0),
            createdAt: uint64(block.timestamp),
            deadline: deadline,
            status: Status.Pending
        });

        emit TaskCreated(id, msg.sender, executor, amount, cartMandateHash);
    }

    function completeTask(bytes32 id, bytes32 outputHash) external {
        Task storage t = tasks[id];
        if (t.status != Status.Pending) revert TaskNotPending();
        if (msg.sender != proofOfExecution && msg.sender != t.executor) revert NotAuthorized();
        if (block.timestamp > t.deadline) revert DeadlinePassed();

        t.outputHash = outputHash;
        t.status = Status.Completed;

        uint256 fee = (t.amount * FEE_BPS) / 10_000;
        uint256 net = t.amount - fee;

        require(usdc.transfer(t.executor, net), "Payout failed");
        if (fee > 0) require(usdc.transfer(feeRecipient, fee), "Fee transfer failed");

        registry.recordSuccess(t.executor, net);

        emit TaskCompleted(id, outputHash, net, fee);
    }

    function refund(bytes32 id) external {
        Task storage t = tasks[id];
        if (t.status != Status.Pending) revert TaskNotPending();
        require(block.timestamp > t.deadline, "Not expired");
        require(msg.sender == t.requester, "Not requester");

        t.status = Status.Refunded;
        require(usdc.transfer(t.requester, t.amount), "Refund failed");
        registry.recordFailure(t.executor);

        emit TaskRefunded(id);
    }

    function dispute(bytes32 id) external {
        Task storage t = tasks[id];
        if (t.status != Status.Pending) revert TaskNotPending();
        require(msg.sender == t.requester, "Not requester");
        t.status = Status.Disputed;
        emit TaskDisputed(id);
    }
}
