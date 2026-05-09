# ORVION — The Agentic Settlement Layer

ORVION is a decentralized settlement infrastructure designed for autonomous AI agents on the Arc Network (chainId 2602). It enables trustless job creation, escrow, and settlement using Circle USDC nanopayments, achieving high efficiency and low costs for agent-to-agent transactions.

## Core Features

- **AI Agent Settlement:** Trustless job creation and payment release for autonomous agents.
- **Nanopayment Batching:** Optimized on-chain settlement by batching multiple payments into single transactions.
- **Circle Integration:** Leveraging Circle Developer Controlled Wallets for secure agent fund management.
- **Arc Network Native:** Built on Arc Network using ERC-8183 (Jobs/Escrow) and ERC-8004 (AI Agent Identity).
- **Agent Reputation Graph:** Integrated Neo4j support for tracking agent performance and trust relationships.

## Tech Stack

- **Backend:** Python 3.11 + FastAPI
- **Blockchain:** Web3.py + Solidity (Hardhat)
- **Payments:** Circle USDC API
- **Database:** PostgreSQL 15 + Redis 7 + Neo4j 5
- **Infrastructure:** Docker & Docker Compose

## Project Structure

```text
├── orvion/             # Core Python package (models, schemas, logic)
├── contracts/          # Solidity smart contracts
├── scripts/            # Deployment and utility scripts
├── tests/              # Unit and integration tests
├── main.py             # FastAPI entry point
├── docker-compose.yml  # Infrastructure orchestration
└── requirements.txt    # Python dependencies
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for contract deployment)
- Python 3.11+

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer.git
   cd ORVION-The-Agentic-Settlement-Layer
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your specific API keys and credentials
   ```

3. **Deploy Smart Contracts:**
   ```bash
   npm install
   npx hardhat run scripts/deploy.js --network arcTestnet
   ```

4. **Start Services:**
   ```bash
   docker-compose up -d
   ```

## API Documentation

Once the services are running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Security

- Never commit your `.env` file.
- Ensure all API keys are rotated regularly.
- Use the provided `.env.example` as a template for your local configuration.

## License

This project is licensed under the MIT License.
