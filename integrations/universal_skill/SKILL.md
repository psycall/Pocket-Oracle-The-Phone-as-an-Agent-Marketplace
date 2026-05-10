# `integrations/universal_skill/` - ORVION Universal Skill Manifest

This directory contains the **Universal Skill Manifest** for ORVION, designed to enable seamless integration with any AI platform or agent ecosystem that supports external skill definitions. This manifest allows ORVION to be recognized and invoked as a core capability for on-chain, data-driven settlements.

## Concept: ORVION as a Core Agentic Capability

By defining ORVION as a universal skill, we empower other AI agents and platforms to programmatically access its functionalities for creating, completing, and settling jobs on-chain. This positions ORVION as the go-to settlement layer for any autonomous economic interaction.

## Skill Definition: ORVION Settlement Layer

### Name:
`orvion-settlement-layer`

### Description:
Facilitates trustless, multichain, and data-driven on-chain settlements for AI agents. Supports USDC transfers across various EVM and non-EVM networks, automated job lifecycle management, and integration with external intelligence for performance-based payouts.

### Capabilities:

*   **`create_agent_job(agent_id: str, amount: float, to_address: str, job_description: str, network: str)`**
    *   **Description**: Initiates a new on-chain job for an AI agent, escrowing the specified USDC amount on the designated network.
    *   **Parameters**:
        *   `agent_id`: Unique identifier of the agent receiving the payment.
        *   `amount`: Amount of USDC to be settled.
        *   `to_address`: Blockchain address of the agent to receive funds.
        *   `job_description`: A brief description of the task being performed.
        *   `network`: Target blockchain network (e.g., "arc-testnet", "ethereum", "polygon").
    *   **Returns**: `on_chain_job_id` (integer) and `transaction_hash` (string).

*   **`complete_agent_job(on_chain_job_id: int, proof: str, network: str)`**
    *   **Description**: Marks an existing on-chain job as completed, typically after an agent submits proof of work.
    *   **Parameters**:
        *   `on_chain_job_id`: The ID of the job on the Orvion smart contract.
        *   `proof`: Cryptographic proof or verifiable receipt of job completion.
        *   `network`: Target blockchain network.
    *   **Returns**: `transaction_hash` (string).

*   **`settle_agent_job(on_chain_job_id: int, network: str)`**
    *   **Description**: Finalizes an on-chain job, releasing the escrowed USDC to the designated agent.
    *   **Parameters**:
        *   `on_chain_job_id`: The ID of the job on the Orvion smart contract.
        *   `network`: Target blockchain network.
    *   **Returns**: `transaction_hash` (string).

*   **`get_agent_balance(agent_address: str, network: str)`**
    *   **Description**: Retrieves the USDC balance for a given agent address on a specific network.
    *   **Parameters**:
        *   `agent_address`: Blockchain address of the agent.
        *   `network`: Target blockchain network.
    *   **Returns**: `balance` (float).

*   **`verify_traffic_performance(agent_id: str, website_url: str, min_traffic: int, period: str)`**
    *   **Description**: Verifies web traffic performance for an agent's associated website, using external data (e.g., SimilarWeb integration).
    *   **Parameters**:
        *   `agent_id`: Unique identifier of the agent.
        *   `website_url`: URL of the website to verify.
        *   `min_traffic`: Minimum unique visitors required.
        *   `period`: Time period for verification (e.g., "last_month").
    *   **Returns**: `is_verified` (boolean).

*   **`evaluate_stock_performance(agent_id: str, ticker: str, min_roi: float, period: str)`**
    *   **Description**: Evaluates an agent's performance based on stock market data, using external data (e.g., Stock Analysis API integration).
    *   **Parameters**:
        *   `agent_id`: Unique identifier of the agent.
        *   `ticker`: Stock ticker symbol.
        *   `min_roi`: Minimum Return on Investment required.
        *   `period`: Time period for evaluation.
    *   **Returns**: `is_performing` (boolean).

## Integration Guidelines

To integrate ORVION as a skill, platforms should:

1.  **Configure API Access**: Ensure secure API access to the ORVION backend, typically via API keys or OAuth tokens.
2.  **Map Skill Functions**: Translate the platform's internal commands or agent requests to the corresponding ORVION skill functions.
3.  **Handle Responses**: Process the `transaction_hash`, `on_chain_job_id`, and other return values from ORVION to update internal states or notify users.

---

*Copyright © 2026 ORVION. All rights reserved. Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.*
