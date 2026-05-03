package io.orvion.api;

import io.orvion.model.Job;
import io.orvion.service.JobService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.math.BigDecimal;
import java.util.List;

@RestController
@RequestMapping("/jobs")
@RequiredArgsConstructor
@Slf4j
public class JobController {
    private final JobService jobService;

    @PostMapping
    public ResponseEntity<Job> createJob(
            @RequestParam String creator,
            @RequestParam String worker,
            @RequestParam BigDecimal amount,
            @RequestParam String jobHash) {
        Job job = jobService.createJob(creator, worker, amount, jobHash);
        return ResponseEntity.status(HttpStatus.CREATED).body(job);
    }

    @PutMapping("/{jobId}/complete")
    public ResponseEntity<Job> completeJob(@PathVariable Long jobId) {
        Job job = jobService.completeJob(jobId);
        return ResponseEntity.ok(job);
    }

    @PutMapping("/{jobId}/settle")
    public ResponseEntity<Job> settleJob(@PathVariable Long jobId) {
        Job job = jobService.settleJob(jobId);
        return ResponseEntity.ok(job);
    }

    @GetMapping("/{jobId}")
    public ResponseEntity<Job> getJob(@PathVariable Long jobId) {
        Job job = jobService.getJob(jobId);
        return ResponseEntity.ok(job);
    }

    @GetMapping("/agent/{agentAddress}")
    public ResponseEntity<List<Job>> getJobsByAgent(@PathVariable String agentAddress) {
        List<Job> jobs = jobService.getJobsByAgent(agentAddress);
        return ResponseEntity.ok(jobs);
    }

    @GetMapping("/pending")
    public ResponseEntity<List<Job>> getPendingJobs() {
        List<Job> jobs = jobService.getPendingJobs();
        return ResponseEntity.ok(jobs);
    }
}
