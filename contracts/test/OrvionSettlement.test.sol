// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../OrvionSettlement.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title MockUSDC
 * @dev Mock USDC token for testing
 */
contract MockUSDC is ERC20 {
    constructor() ERC20("USD Coin", "USDC") {
        _mint(msg.sender, 1000000 * 10 ** 6);
    }

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/**
 * @title OrvionSettlementTest
 * @dev Comprehensive test suite for OrvionSettlement contract
 */
contract OrvionSettlementTest is Test {
    OrvionSettlement public settlement;
    MockUSDC public usdc;

    address public employer = address(0x1);
    address public executor = address(0x2);
    address public owner = address(0x3);

    uint256 constant JOB_AMOUNT = 100 * 10 ** 6; // 100 USDC

    function setUp() public {
        usdc = new MockUSDC();

        vm.prank(owner);
        settlement = new OrvionSettlement(address(usdc));

        usdc.mint(employer, 10000 * 10 ** 6);

        vm.prank(employer);
        usdc.approve(address(settlement), type(uint256).max);
    }

    /**
     * @dev Test: Create job
     */
    function test_CreateJob() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Data analysis task");

        OrvionSettlement.Job memory job = settlement.getJob(jobId);

        assertEq(job.employer, employer);
        assertEq(job.executor, executor);
        assertEq(job.amount, JOB_AMOUNT);
        assertEq(uint(job.status), uint(OrvionSettlement.JobStatus.ESCROW_LOCKED));
    }

    /**
     * @dev Test: Submit execution proof
     */
    function test_SubmitExecutionProof() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Data analysis task");

        bytes32 proof = keccak256(abi.encodePacked("execution_result_hash"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId, proof);

        OrvionSettlement.Job memory job = settlement.getJob(jobId);
        assertEq(job.executionProof, proof);
        assertEq(uint(job.status), uint(OrvionSettlement.JobStatus.EXECUTION_SUBMITTED));
    }

    /**
     * @dev Test: Approve execution and complete job
     */
    function test_ApproveExecutionAndComplete() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Data analysis task");

        bytes32 proof = keccak256(abi.encodePacked("execution_result_hash"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId, proof);

        uint256 executorBalanceBefore = usdc.balanceOf(executor);

        vm.prank(employer);
        settlement.approveExecution(jobId);

        uint256 executorBalanceAfter = usdc.balanceOf(executor);
        assertEq(executorBalanceAfter - executorBalanceBefore, JOB_AMOUNT);

        OrvionSettlement.Job memory job = settlement.getJob(jobId);
        assertEq(uint(job.status), uint(OrvionSettlement.JobStatus.COMPLETED));
    }

    /**
     * @dev Test: Agent earnings tracking
     */
    function test_AgentEarningsTracking() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof = keccak256(abi.encodePacked("proof1"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId, proof);

        vm.prank(employer);
        settlement.approveExecution(jobId);

        (uint256 earnings, uint256 completed, uint256 disputed) = settlement.getAgentStats(executor);

        assertEq(earnings, JOB_AMOUNT);
        assertEq(completed, 1);
        assertEq(disputed, 0);
    }

    /**
     * @dev Test: Dispute job
     */
    function test_DisputeJob() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof = keccak256(abi.encodePacked("proof1"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId, proof);

        vm.prank(employer);
        settlement.disputeJob(jobId);

        OrvionSettlement.Job memory job = settlement.getJob(jobId);
        assertEq(uint(job.status), uint(OrvionSettlement.JobStatus.DISPUTED));
    }

    /**
     * @dev Test: Resolve dispute - pay executor
     */
    function test_ResolveDisputePayExecutor() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof = keccak256(abi.encodePacked("proof1"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId, proof);

        vm.prank(employer);
        settlement.disputeJob(jobId);

        uint256 executorBalanceBefore = usdc.balanceOf(executor);

        vm.prank(owner);
        settlement.resolveDispute(jobId, true);

        uint256 executorBalanceAfter = usdc.balanceOf(executor);
        assertEq(executorBalanceAfter - executorBalanceBefore, JOB_AMOUNT);
    }

    /**
     * @dev Test: Resolve dispute - refund employer
     */
    function test_ResolveDisputeRefundEmployer() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof = keccak256(abi.encodePacked("proof1"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId, proof);

        vm.prank(employer);
        settlement.disputeJob(jobId);

        uint256 employerBalanceBefore = usdc.balanceOf(employer);

        vm.prank(owner);
        settlement.resolveDispute(jobId, false);

        uint256 employerBalanceAfter = usdc.balanceOf(employer);
        assertEq(employerBalanceAfter - employerBalanceBefore, JOB_AMOUNT);
    }

    /**
     * @dev Test: Total settled tracking
     */
    function test_TotalSettledTracking() public {
        vm.prank(employer);
        bytes32 jobId1 = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof1 = keccak256(abi.encodePacked("proof1"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId1, proof1);

        vm.prank(employer);
        settlement.approveExecution(jobId1);

        uint256 totalSettled = settlement.getTotalSettled();
        assertEq(totalSettled, JOB_AMOUNT);
    }

    /**
     * @dev Test: Cannot submit proof with invalid status
     */
    function test_CannotSubmitProofInvalidStatus() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof = keccak256(abi.encodePacked("proof1"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId, proof);

        vm.prank(executor);
        vm.expectRevert("Invalid job status");
        settlement.submitExecutionProof(jobId, proof);
    }

    /**
     * @dev Test: Only executor can submit proof
     */
    function test_OnlyExecutorCanSubmitProof() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof = keccak256(abi.encodePacked("proof1"));

        address unauthorized = address(0x5);
        vm.prank(unauthorized);
        vm.expectRevert("Only executor can submit proof");
        settlement.submitExecutionProof(jobId, proof);
    }

    /**
     * @dev Test: Only employer can approve
     */
    function test_OnlyEmployerCanApprove() public {
        vm.prank(employer);
        bytes32 jobId = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof = keccak256(abi.encodePacked("proof1"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId, proof);

        address unauthorized = address(0x5);
        vm.prank(unauthorized);
        vm.expectRevert("Only employer can approve");
        settlement.approveExecution(jobId);
    }

    /**
     * @dev Test: Multiple jobs tracking
     */
    function test_MultipleJobsTracking() public {
        // Job 1
        vm.prank(employer);
        bytes32 jobId1 = settlement.createJob(executor, JOB_AMOUNT, "Task 1");

        bytes32 proof1 = keccak256(abi.encodePacked("proof1"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId1, proof1);

        vm.prank(employer);
        settlement.approveExecution(jobId1);

        // Job 2
        vm.prank(employer);
        bytes32 jobId2 = settlement.createJob(executor, JOB_AMOUNT, "Task 2");

        bytes32 proof2 = keccak256(abi.encodePacked("proof2"));

        vm.prank(executor);
        settlement.submitExecutionProof(jobId2, proof2);

        vm.prank(employer);
        settlement.approveExecution(jobId2);

        (uint256 earnings, uint256 completed, ) = settlement.getAgentStats(executor);

        assertEq(earnings, JOB_AMOUNT * 2);
        assertEq(completed, 2);
    }
}
