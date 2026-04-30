// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title Orvion (Turbo Arc Edition)
 * @notice Full ERC-8183 Compliance with Unified USDC Settlement.
 * @dev Optimized for Nanopayments batching and Arc Builders Fund.
 */
contract Orvion {
    IERC20 public immutable usdc;
    
    enum JobStatus { Pending, Funded, Completed, Settled, Disputed }

    struct Job {
        address creator;
        address worker;
        uint256 amount;
        JobStatus status;
        bytes32 jobHash; // ERC-8183 Metadata
        uint256 createdAt;
    }

    mapping(uint256 => Job) public jobs;
    uint256 public jobCount;

    event JobCreated(uint256 indexed id, address indexed creator, address indexed worker, uint256 amount);
    event JobFunded(uint256 indexed id);
    event JobCompleted(uint256 indexed id);
    event JobSettled(uint256 indexed id, uint256 amount);

    constructor(address _usdcAddress) {
        usdc = IERC20(_usdcAddress);
    }

    /**
     * @notice Create and fund a job (ERC-8183 standard flow)
     */
    function createJob(address _worker, uint256 _amount, bytes32 _jobHash) external {
        require(usdc.transferFrom(msg.sender, address(this), _amount), "Escrow funding failed");

        jobs[jobCount] = Job({
            creator: msg.sender,
            worker: _worker,
            amount: _amount,
            status: JobStatus.Funded,
            jobHash: _jobHash,
            createdAt: block.timestamp
        });

        emit JobCreated(jobCount, msg.sender, _worker, _amount);
        emit JobFunded(jobCount);
        jobCount++;
    }

    function completeJob(uint256 _id) external {
        Job storage job = jobs[_id];
        require(msg.sender == job.worker, "Only worker can complete");
        job.status = JobStatus.Completed;
        emit JobCompleted(_id);
    }

    /**
     * @notice Final settlement on Arc
     */
    function settleJob(uint256 _id) external {
        Job storage job = jobs[_id];
        require(job.status == JobStatus.Completed, "Job not completed");
        
        job.status = JobStatus.Settled;
        require(usdc.transfer(job.worker, job.amount), "Payment failed");
        
        emit JobSettled(_id, job.amount);
    }
}
