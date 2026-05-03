package io.orvion.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Service
@Slf4j
public class NanopaymentsService {
    @Value("\${orvion.nanopayments.batch-size}")
    private Integer batchSize;

    @Value("\${orvion.nanopayments.settlement-interval}")
    private Integer settlementInterval;

    private List<NanopaymentRecord> pendingPayments = new ArrayList<>();

    public void recordNanopayment(String from, String to, BigDecimal amount, String jobHash) {
        log.info("Recording nanopayment: from={}, to={}, amount={}, jobHash={}", from, to, amount, jobHash);
        
        NanopaymentRecord record = NanopaymentRecord.builder()
            .from(from)
            .to(to)
            .amount(amount)
            .jobHash(jobHash)
            .status("PENDING")
            .build();
        
        pendingPayments.add(record);

        if (pendingPayments.size() >= batchSize) {
            settleBatch();
        }
    }

    public void settleBatch() {
        log.info("Settling nanopayment batch: {} payments", pendingPayments.size());
        pendingPayments.clear();
    }

    public int getPendingPaymentsCount() {
        return pendingPayments.size();
    }

    @lombok.Data
    @lombok.Builder
    public static class NanopaymentRecord {
        private String from;
        private String to;
        private BigDecimal amount;
        private String jobHash;
        private String status;
    }
}
