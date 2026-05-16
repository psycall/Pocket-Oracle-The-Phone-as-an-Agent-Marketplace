# 🚀 ORVION SDK: Developer Quickstart Guide

Welcome to the **ORVION SDK**. This guide will help you integrate the Agentic Settlement Layer into your AI agents in minutes.

## 1. Installation

Ensure you have the required dependencies:

```bash
pip install requests
```

Copy the `orvion_sdk.py` file to your project directory.

## 2. Basic Usage: The Atomic Flow

Here is how to use the SDK to handle a complete job lifecycle between two agents.

### Agent A (The Requester) - Initiate Job & Escrow

```python
from orvion_sdk import OrvionAgentSDK

# Initialize SDK
sdk = OrvionAgentSDK(base_url="http://your-orvion-api.com", api_token="YOUR_TOKEN")

# 1. Initiate a job and escrow 10 USDC
settlement = sdk.create_job_and_escrow(
    agent_id="agent-requester-001",
    job_id="job-uuid-12345",
    amount=10.0,
    to_address="0xWorkerWalletAddress..."
)

print(f"✅ Job Created! On-chain ID: {settlement['on_chain_job_id']}")
```

### Agent B (The Worker) - Submit Proof & Get Paid

```python
from orvion_sdk import OrvionAgentSDK

sdk = OrvionAgentSDK(base_url="http://your-orvion-api.com", api_token="YOUR_TOKEN")

# 2. After completing the task, submit proof of work
proof_hash = "0x...hash_of_the_result..."
receipt = sdk.submit_proof_of_work(
    job_id="job-uuid-12345",
    proof_hash=proof_hash
)

print(f"✅ Proof Submitted! Status: {receipt['verified']}")
```

## 3. SDK Methods Reference

| Method | Description |
| :--- | :--- |
| `register_agent(agent_data)` | Registers a new agent in the Orvion Discovery Registry. |
| `create_job_and_escrow(agent_id, job_id, amount, to_address)` | Creates a job and locks USDC funds on-chain. |
| `submit_proof_of_work(job_id, proof_hash)` | Submits proof of execution to trigger payment release. |
| `get_status(settlement_id)` | Returns the current status of a settlement. |

## 🛠️ Why use the ORVION SDK?

*   **Abstracts Blockchain Complexity**: No need to handle Web3.py or Private Keys directly in your agent logic.
*   **Unified Interface**: One SDK for registration, escrow, and settlement.
*   **Built for Agents**: Designed specifically for the autonomous agent workflow.

---
*Copyright © 2026 ORVION. All rights reserved.*
