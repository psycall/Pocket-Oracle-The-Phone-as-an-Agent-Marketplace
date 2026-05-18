// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title OrvionSettlement
 * @dev Gerencia ciclo completo de liquidação de jobs entre agentes
 */
contract OrvionSettlement is Ownable, ReentrancyGuard {
    IERC20 public immutable usdcToken;

    enum JobStatus {
        PENDING,
        ESCROW_LOCKED,
        EXECUTION_SUBMITTED,
        COMPLETED,
        DISPUTED,
        RESOLVED
    }

    struct Job {
        bytes32 jobId;
        address employer;
        address executor;
        uint256 amount;
        JobStatus status;
        string taskDescription;
        bytes32 executionProof;
        uint256 createdAt;
        uint256 completedAt;
    }

    mapping(bytes32 => Job) public jobs;
    mapping(address => uint256) public agentEarnings;
    mapping(address => uint256) public agentCompletedJobs;
    mapping(address => uint256) public agentDisputedJobs;

    uint256 public totalSettled;
    uint256 public jobCounter;

    event JobCreated(bytes32 indexed jobId, address employer, address executor, uint256 amount, string taskDescription);
    event EscrowLocked(bytes32 indexed jobId, uint256 amount);
    event ExecutionSubmitted(bytes32 indexed jobId, address executor, bytes32 executionProof);
    event JobCompleted(bytes32 indexed jobId, address executor, uint256 amount);
    event JobDisputed(bytes32 indexed jobId, address initiator);
    event DisputeResolved(bytes32 indexed jobId, address recipient, uint256 amount);

    constructor(address _usdcToken) Ownable(msg.sender) {
        usdcToken = IERC20(_usdcToken);
    }

    /**
     * @dev Cria um novo job com escrow automático
     */
    function createJob(
        address _executor,
        uint256 _amount,
        string memory _taskDescription
    ) external nonReentrant returns (bytes32) {
        require(_amount > 0, "Amount must be greater than zero");
        require(_executor != address(0), "Invalid executor address");
        require(
            usdcToken.transferFrom(msg.sender, address(this), _amount),
            "USDC transfer failed"
        );

        bytes32 jobId = keccak256(abi.encodePacked(msg.sender, _executor, block.timestamp, jobCounter));
        jobCounter++;

        jobs[jobId] = Job({
            jobId: jobId,
            employer: msg.sender,
            executor: _executor,
            amount: _amount,
            status: JobStatus.ESCROW_LOCKED,
            taskDescription: _taskDescription,
            executionProof: bytes32(0),
            createdAt: block.timestamp,
            completedAt: 0
        });

        emit JobCreated(jobId, msg.sender, _executor, _amount, _taskDescription);
        emit EscrowLocked(jobId, _amount);

        return jobId;
    }

    /**
     * @dev Executor submete prova de execução (hash do resultado)
     */
    function submitExecutionProof(bytes32 _jobId, bytes32 _executionProof) external nonReentrant {
        Job storage job = jobs[_jobId];
        require(msg.sender == job.executor, "Only executor can submit proof");
        require(job.status == JobStatus.ESCROW_LOCKED, "Invalid job status");
        require(_executionProof != bytes32(0), "Invalid proof");

        job.executionProof = _executionProof;
        job.status = JobStatus.EXECUTION_SUBMITTED;

        emit ExecutionSubmitted(_jobId, msg.sender, _executionProof);
    }

    /**
     * @dev Employer aprova execução e libera pagamento
     */
    function approveExecution(bytes32 _jobId) external nonReentrant {
        Job storage job = jobs[_jobId];
        require(msg.sender == job.employer, "Only employer can approve");
        require(job.status == JobStatus.EXECUTION_SUBMITTED, "Invalid job status");

        job.status = JobStatus.COMPLETED;
        job.completedAt = block.timestamp;

        // Transferir para executor
        require(usdcToken.transfer(job.executor, job.amount), "Payment transfer failed");

        // Atualizar estatísticas
        agentEarnings[job.executor] += job.amount;
        agentCompletedJobs[job.executor]++;
        totalSettled += job.amount;

        emit JobCompleted(_jobId, job.executor, job.amount);
    }

    /**
     * @dev Abre disputa sobre o job
     */
    function disputeJob(bytes32 _jobId) external {
        Job storage job = jobs[_jobId];
        require(
            msg.sender == job.employer || msg.sender == job.executor,
            "Only employer or executor can dispute"
        );
        require(job.status != JobStatus.COMPLETED && job.status != JobStatus.RESOLVED, "Cannot dispute completed job");

        job.status = JobStatus.DISPUTED;
        agentDisputedJobs[job.executor]++;

        emit JobDisputed(_jobId, msg.sender);
    }

    /**
     * @dev Owner resolve disputa
     */
    function resolveDispute(bytes32 _jobId, bool _payExecutor) external onlyOwner nonReentrant {
        Job storage job = jobs[_jobId];
        require(job.status == JobStatus.DISPUTED, "Job not in dispute");

        job.status = JobStatus.RESOLVED;

        address recipient = _payExecutor ? job.executor : job.employer;

        require(usdcToken.transfer(recipient, job.amount), "Resolution transfer failed");

        if (_payExecutor) {
            agentEarnings[job.executor] += job.amount;
            agentCompletedJobs[job.executor]++;
        }

        emit DisputeResolved(_jobId, recipient, job.amount);
    }

    /**
     * @dev Retorna informações do job
     */
    function getJob(bytes32 _jobId) external view returns (Job memory) {
        return jobs[_jobId];
    }

    /**
     * @dev Retorna estatísticas do agente
     */
    function getAgentStats(address _agent) external view returns (
        uint256 earnings,
        uint256 completedJobs,
        uint256 disputedJobs
    ) {
        return (
            agentEarnings[_agent],
            agentCompletedJobs[_agent],
            agentDisputedJobs[_agent]
        );
    }

    /**
     * @dev Retorna total liquidado
     */
    function getTotalSettled() external view returns (uint256) {
        return totalSettled;
    }
}
