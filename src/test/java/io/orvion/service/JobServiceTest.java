package io.orvion.service;

import io.orvion.model.Job;
import io.orvion.model.Job.JobStatus;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.math.BigDecimal;

public class JobServiceTest {
    private JobService jobService;

    @BeforeEach
    public void setUp() {
        jobService = new JobServiceImpl();
    }

    @Test
    public void testCreateJob() {
        String creator = "0x1234";
        String worker = "0x5678";
        BigDecimal amount = new BigDecimal("100.00");
        String jobHash = "hash123";

        Job job = jobService.createJob(creator, worker, amount, jobHash);

        assertNotNull(job);
        assertEquals(creator, job.getCreator());
        assertEquals(worker, job.getWorker());
        assertEquals(amount, job.getAmount());
        assertEquals(JobStatus.CREATED, job.getStatus());
    }

    @Test
    public void testCompleteJob() {
        Job job = jobService.createJob("0x1234", "0x5678", new BigDecimal("100"), "hash");
        Job completed = jobService.completeJob(1L);

        assertNotNull(completed);
        assertEquals(JobStatus.COMPLETED, completed.getStatus());
        assertNotNull(completed.getCompletedAt());
    }

    @Test
    public void testSettleJob() {
        Job job = jobService.createJob("0x1234", "0x5678", new BigDecimal("100"), "hash");
        Job settled = jobService.settleJob(1L);

        assertNotNull(settled);
        assertEquals(JobStatus.SETTLED, settled.getStatus());
        assertNotNull(settled.getSettledAt());
    }
}
