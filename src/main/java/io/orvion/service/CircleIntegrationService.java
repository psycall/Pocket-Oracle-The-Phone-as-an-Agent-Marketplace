package io.orvion.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;

@Service
@Slf4j
public class CircleIntegrationService {
    @Value("\${orvion.circle.api-key}")
    private String circleApiKey;

    @Value("\${orvion.circle.api-url}")
    private String circleApiUrl;

    public void createModularWallet(String agentAddress) {
        log.info("Creating modular wallet for agent: {}", agentAddress);
    }

    public void initiateNanopayment(String from, String to, BigDecimal amount) {
        log.info("Initiating nanopayment: from={}, to={}, amount={}", from, to, amount);
    }

    public void settleNanopaymentBatch(String batchId) {
        log.info("Settling nanopayment batch: {}", batchId);
    }
}
