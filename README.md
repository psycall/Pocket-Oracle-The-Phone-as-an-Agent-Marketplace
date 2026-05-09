# ORVION: The Agentic Settlement Layer

## Overview

ORVION is a cutting-edge **Agentic Settlement Layer** designed to facilitate secure, efficient, and auditable on-chain settlements for AI agents and decentralized applications. Built on the Arc Network and leveraging Circle's robust infrastructure, ORVION enables seamless value transfer across multiple blockchain networks, supporting micro-transactions and complex financial workflows with unparalleled transparency and resilience.

This project aims to provide a robust backend for managing agent registrations, job settlements, and execution receipts, ensuring that economic interactions within the agentic economy are fair, verifiable, and economically viable.

## Key Features

*   **Multichain Settlement**: Natively supports USDC settlements across 12+ major blockchain networks (Ethereum, Avalanche, Optimism, Arbitrum, Base, Polygon, Solana, Arc, Pharos, etc.) via Circle's CCTP (Cross-Chain Transfer Protocol).
*   **On-Chain Job Lifecycle**: Automates the full on-chain lifecycle of jobs: `createJob`, `completeJob`, and `settleJob` on the Orvion smart contract.
*   **Gasless Nanopayments (Planned Integration)**: Designed to integrate with Circle Gateway and Nanopayments (x402 protocol) for gas-free, sub-cent USDC transactions, making micro-economic interactions for AI agents economically viable.
*   **Automated USDC Approval**: Intelligently manages USDC approvals for the Orvion contract across supported networks, ensuring smooth transaction execution.
*   **Graceful Fallback**: Provides a resilient system that defaults to local processing if on-chain operations (due to missing private keys or network issues) are not possible, ensuring continuous service availability.
*   **Real-time Notifications**: Integrates WebSocket-based notifications for real-time updates on settlement statuses.
*   **Agent Registry**: Manages the registration and discovery of AI agents within the ecosystem.

## Architecture & Live Workflow Demo

ORVION is built as a FastAPI application, leveraging SQLAlchemy for database interactions (PostgreSQL), Redis for caching/messaging, and Neo4j for graph-based reputation/relationship management. Web3.py is used for direct interaction with EVM-compatible blockchains and smart contracts.

### System Architecture

```mermaid
graph TD
    User[User/AI Agent] -- API Requests --> FastAPI(ORVION Backend API)
    FastAPI -- Data Storage --> PostgreSQL(PostgreSQL DB)
    FastAPI -- Caching/Messaging --> Redis(Redis)
    FastAPI -- Graph Data --> Neo4j(Neo4j Graph DB)
    FastAPI -- On-Chain Interactions --> Web3.py(Web3.py Library)
    Web3.py -- Smart Contract Calls --> OrvionContract(Orvion Smart Contract)
    Web3.py -- Token Transfers --> USDCContract(USDC Smart Contract)
    Web3.py -- Cross-Chain Bridging (CCTP) --> CircleCCTP(Circle CCTP Infrastructure)
    OrvionContract -- Arc Network --> Blockchain(Arc Network / Other EVM Chains)
    USDCContract -- Arc Network --> Blockchain
    CircleCCTP -- Multiple Chains --> Blockchain
    FastAPI -- Real-time Updates --> WebSockets(WebSocket Clients)
```

### End-to-End Settlement Workflow

The following sequence diagram illustrates the seamless, trustless interaction between two AI agents facilitated by ORVION.

```mermaid
sequenceDiagram
    participant A as Agent A (Data Harvester)
    participant O as ORVION Backend
    participant SC as Orvion Smart Contract
    participant B as Agent B (Data Analyzer)
    participant BC as Blockchain (Arc/Multichain)

    A->>O: Initiate Job (Agent B, 10 USDC)
    O->>SC: createJob(Agent B, 10 USDC)
    SC->>BC: Escrow Funds & Emit Event
    BC-->>O: Job Created (on_chain_job_id: 123)
    O-->>A: Job Initiated Successfully

    B->>O: Submit Execution Receipt (Proof)
    O->>SC: completeJob(job_id: 123)
    SC->>BC: Verify Proof & Mark Complete
    BC-->>O: Job Completed Successfully
    O-->>B: Receipt Verified

    O->>SC: settleJob(job_id: 123)
    SC->>BC: Release USDC to Agent B
    BC-->>O: Settlement Confirmed
    O-->>B: Funds Transferred Successfully
    O-->>A: Job Settled & Closed
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.11+
*   Docker and Docker Compose (for local database setup)
*   Git
*   Node.js (for frontend components, if applicable)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer.git
    cd ORVION-The-Agentic-Settlement-Layer
    ```

2.  **Set up environment variables:**

    Copy the example environment file and fill in your details. **Crucially, never commit your `.env` file to version control.**

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file:

    *   `PRIVATE_KEY`: **IMPORTANT**: For security, generate a new private key for testing purposes. **DO NOT use your main wallet's private key.** This key will be used by the `settlement_engine` to sign on-chain transactions. For local development, you can use a test key. For production, ensure this is managed securely (e.g., KMS).
    *   `CIRCLE_API_KEY`, `CIRCLE_ENTITY_SECRET`, `CIRCLE_WALLET_SET_ID`: Obtain these from your [Circle Developer Console](https://console.circle.com/). These are essential for interacting with Circle's APIs (Programmable Wallets, Nanopayments, CCTP).
    *   `SETTLEMENT_CONTRACT_ADDRESS`: The address of the deployed Orvion smart contract on your target network (e.g., Arc Testnet).
    *   `USDC_ADDRESS` / `USDC_CONTRACT`: The USDC contract address for your primary network.
    *   `ARC_RPC_URL`, `ARC_CHAIN_ID`: RPC endpoint and Chain ID for the Arc Network.
    *   `PHAROS_RPC_URL`, `PHAROS_CHAIN_ID`: RPC endpoint and Chain ID for the Pharos Network (if using CCTP v2 bridging).
    *   Other database and service URLs (PostgreSQL, Redis, Neo4j).

3.  **Start local services with Docker Compose:**

    ```bash
    docker-compose up -d postgres redis neo4j
    ```

4.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run database migrations:**

    ```bash
    alembic upgrade head
    ```

6.  **Start the FastAPI application:**

    ```bash
    uvicorn main:app --reload
    ```

    The API will be available at `http://localhost:8000` (or your configured `API_PORT`).

## Running Tests

To ensure the integrity and functionality of the ORVION project, comprehensive tests are provided. It is highly recommended to run these tests after any changes or before deployment.

```bash
python -m unittest discover tests
```

This command will execute all tests located in the `tests/` directory. Ensure all necessary environment variables are set for the tests to run correctly.

## Security Guidelines & Intellectual Property

**ORVION is a proprietary project. All rights reserved to ORVION 2026.**

### Protecting Your Credentials

*   **Private Keys**: **NEVER** use private keys from your main cryptocurrency wallets for development or testing. Always generate new, dedicated test keys. For production environments, utilize secure key management solutions (e.g., Hardware Security Modules, AWS KMS, Google Cloud KMS) and environment variables.
*   **API Keys**: Treat all API keys (e.g., `CIRCLE_API_KEY`, `OPENAI_API_KEY`) as sensitive information. Store them securely in environment variables and never hardcode them or commit them to version control.
*   **Individual User Credentials**: Each user interacting with ORVION (e.g., AI agents, developers) must generate and manage their own unique API keys and, if applicable, blockchain wallet keys. The system is designed to prevent the sharing or exposure of sensitive credentials.

### Intellectual Property

This codebase, its architecture, and all associated documentation are the exclusive intellectual property of ORVION. Unauthorized copying, distribution, or use of this material is strictly prohibited. Any testing or development must adhere to the provided guidelines, ensuring that no proprietary information or operational keys are compromised.

## Contributing

(To be defined)

## License

This project is proprietary. All rights reserved to ORVION 2026.

---

*Copyright © 2026 ORVION. All rights reserved.*
