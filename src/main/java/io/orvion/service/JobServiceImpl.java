package io.orvion.service;

import io.orvion.model.Job;
import io.orvion.model.Job.JobStatus;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Service
@Slf4j
public class JobServiceImpl implements JobService {

    @Override
    @Transactional
    public Job createJob(String creator, String worker, BigDecimal amount, String jobHash) {
        log.info("Creating job: creator={}, worker={}, amount={}", creator, worker, amount);
        
        Job job = Job.builder()
            .creator(creator)
            .worker(worker)
            .amount(amount)
            .jobHash(jobHash)
            .status(JobStatus.CREATED)
            .createdAt(LocalDateTime.now())
            .build();
        
        return job;
    }

    @Override
    @Transactional
    public Job completeJob(Long jobId) {
        log.info("Completing job: jobId={}", jobId);
        Job job = getJob(jobId);
        job.setStatus(JobStatus.COMPLETED);
        job.setCompletedAt(LocalDateTime.now());
        return job;
    }

    @Override
    @Transactional
    public Job settleJob(Long jobId) {
        log.info("Settling job: jobId={}", jobId);
        Job job = getJob(jobId);
        job.setStatus(JobStatus.SETTLED);
        job.setSettledAt(LocalDateTime.now());
        return job;
    }

    @Override
    public Job getJob(Long jobId) {
        return new Job();
    }

    @Override
    public List<Job> getJobsByAgent(String agentAddress) {
        return List.of();
    }

    @Override
    public List<Job> getPendingJobs() {
        return List.of();
    }
}
