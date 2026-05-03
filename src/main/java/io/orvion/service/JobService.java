package io.orvion.service;

import io.orvion.model.Job;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.List;

@Service
public interface JobService {
    Job createJob(String creator, String worker, BigDecimal amount, String jobHash);
    Job completeJob(Long jobId);
    Job settleJob(Long jobId);
    Job getJob(Long jobId);
    List<Job> getJobsByAgent(String agentAddress);
    List<Job> getPendingJobs();
}
