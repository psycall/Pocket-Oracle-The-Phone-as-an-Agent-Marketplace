# ORVION Project Structure

## Overview

ORVION is a comprehensive **Agentic Settlement Layer** combining financial infrastructure, legal frameworks, and developer tools for autonomous AI agents. This document outlines the complete project structure.

## Directory Hierarchy

```
ORVION-The-Agentic-Settlement-Layer/
├── contracts/                    # Smart Contracts (Solidity)
│   ├── Orvion.sol               # Core settlement contract
│   ├── OrvionEscrow.sol          # Escrow management
│   ├── OrvionEscrowFactory.sol   # Factory pattern for escrows
│   ├── OrvionSettlement.sol      # Job settlement logic
│   └── test/                     # Foundry test suites
│
├── orvion_persona/              # Agent Legal Body Module
│   ├── legal_body/              # Legal incorporation engine
│   │   ├── contracts/           # AgentPersona, OperatingAgreement contracts
│   │   ├── backend/             # FastAPI legal services
│   │   ├── frontend/            # React pages for legal UI
│   │   ├── templates/           # Operating agreement templates (WY, DE, NY)
│   │   ├── docs/WHITEPAPER.md   # Legal framework whitepaper
│   │   └── scripts/             # Integration and deployment scripts
│   ├── vitrine/                 # Landing page for Circle/Arc outreach
│   ├── pitch_deck/              # 10-slide HTML presentation
│   └── README.md                # Persona pack documentation
│
├── src/                         # Backend Python Application
│   ├── main/java/io/orvion/     # Java backend (Circle Agent Stack)
│   │   ├── api/                 # REST API controllers
│   │   ├── service/             # Business logic services
│   │   ├── model/               # Data models
│   │   ├── repository/          # Database repositories
│   │   └── config/              # Configuration classes
│   ├── orvion/                  # Python core modules
│   │   ├── settlement_engine.py # Settlement orchestration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── auth.py              # Authentication
│   │   └── config.py            # Configuration
│   ├── main.py                  # FastAPI application entry
│   ├── orvion_sdk.py            # Python SDK for agents
│   └── requirements.txt         # Python dependencies
│
├── orvion-frontend/             # Frontend Application
│   ├── client/src/              # React 19 source
│   │   ├── pages/               # Page components
│   │   │   ├── Home.tsx         # Landing page
│   │   │   ├── Dashboard.tsx    # Control center
│   │   │   ├── AgentRegistry.tsx # Agent discovery
│   │   │   └── DeveloperConsole.tsx # SDK testing
│   │   ├── components/          # Reusable UI components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── lib/                 # Utilities and API client
│   │   ├── contexts/            # React contexts
│   │   ├── App.tsx              # Main app component
│   │   └── index.css            # Global styles (Tailwind + custom)
│   ├── public/                  # Static assets
│   ├── package.json             # Frontend dependencies
│   └── vite.config.ts           # Vite configuration
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # System architecture
│   ├── API_INTEGRATION.md       # API setup guide
│   ├── DEPLOYMENT.md            # Deployment instructions
│   ├── SECURITY.md              # Security best practices
│   ├── SDK_GUIDE.md             # SDK usage guide
│   ├── CIRCLE_INTEGRATION_GUIDE.md # Circle integration
│   ├── guides/                  # Additional guides
│   └── images/                  # Diagrams and screenshots
│
├── tests/                       # Test Suites
│   ├── integration/             # Integration tests
│   ├── unit/                    # Unit tests
│   └── e2e/                     # End-to-end tests
│
├── infrastructure/              # Infrastructure & DevOps
│   ├── docker-compose.yml       # Local development
│   ├── docker-compose.production.yml # Production setup
│   ├── Dockerfile               # Container image
│   └── kubernetes/              # K8s manifests (optional)
│
├── scripts/                     # Utility Scripts
│   ├── deploy.sh                # Deployment script
│   ├── test.sh                  # Test runner
│   └── migrate.sh               # Database migrations
│
├── public/                      # Public Assets
│   └── assets/                  # Images, icons, etc.
│
├── .env.example                 # Environment template
├── .env                         # Environment variables (gitignored)
├── .gitignore                   # Git ignore rules
├── foundry.toml                 # Foundry configuration
├── hardhat.config.cjs           # Hardhat configuration
├── package.json                 # Root dependencies
├── README.md                    # Project README
└── LICENSE                      # MIT License

```

## Module Descriptions

### Smart Contracts (`contracts/`)

The Solidity smart contracts form the on-chain backbone of ORVION:

- **Orvion.sol**: Core settlement contract managing the overall job lifecycle
- **OrvionEscrow.sol**: Handles escrow deposits and releases with dispute resolution
- **OrvionEscrowFactory.sol**: Factory pattern for creating isolated escrow instances
- **OrvionSettlement.sol**: Manages job creation, execution proof, and settlement completion

All contracts are tested with Foundry and deployable to Arc Network Testnet/Mainnet.

### Agent Legal Body (`orvion_persona/`)

The persona pack integrates legal incorporation for autonomous agents:

- **Smart Contracts**: `AgentPersona.sol`, `OperatingAgreement.sol`, `JurisdictionRegistry.sol`
- **Backend Services**: FastAPI routes for legal entity management, incorporation workflows
- **Frontend Pages**: React components for agent legal body registration and dashboard
- **Templates**: Operating agreement templates for Wyoming, Delaware, and New York jurisdictions
- **Whitepaper**: Comprehensive legal framework documentation

### Backend Application (`src/`)

The backend provides the settlement engine and API:

- **FastAPI Server** (`main.py`): REST API with routes for settlements, agents, disputes
- **Settlement Engine** (`orvion/settlement_engine.py`): Orchestrates job lifecycle and USDC transfers
- **Java Backend**: Circle Agent Stack integration for advanced agent capabilities
- **SDK** (`orvion_sdk.py`): Python library for agent integration
- **Models**: SQLAlchemy ORM models for agents, jobs, settlements, and transactions

### Frontend Application (`orvion-frontend/`)

The React 19 frontend provides the user interface:

- **Landing Page** (`Home.tsx`): Vitrine for Circle/Arc outreach
- **Dashboard** (`Dashboard.tsx`): Real-time settlement metrics and controls
- **Agent Registry** (`AgentRegistry.tsx`): Discover and hire agents
- **Developer Console** (`DeveloperConsole.tsx`): SDK testing and API key management
- **Design**: Dark mode "Agentic Noir" aesthetic with Tailwind CSS v4

### Documentation (`docs/`)

Comprehensive guides and references:

- Architecture diagrams and system design
- API integration instructions
- Deployment and DevOps guides
- Security best practices
- SDK usage examples
- Circle and Arc integration guides

### Tests (`tests/`)

Multiple testing layers:

- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-module interaction testing
- **End-to-End Tests**: Full workflow validation
- **Smart Contract Tests**: Foundry test suites for Solidity contracts

## Environment Setup

### Prerequisites

- Node.js 22+
- Python 3.11+
- Solidity 0.8.20+
- Docker & Docker Compose (optional)
- Foundry (for contract testing)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer.git
cd ORVION-The-Agentic-Settlement-Layer
```

2. Install dependencies:
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd orvion-frontend
npm install
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Circle API credentials and Arc RPC URL
```

4. Start services:
```bash
# Backend
python main.py

# Frontend (in another terminal)
cd orvion-frontend
npm run dev
```

## Key Features

| Feature | Location | Status |
|---------|----------|--------|
| Settlement Engine | `orvion/settlement_engine.py` | ✅ Complete |
| USDC Integration | `contracts/OrvionEscrow.sol` | ✅ Complete |
| Agent Registry | `orvion-frontend/pages/AgentRegistry.tsx` | ✅ Complete |
| Legal Body Framework | `orvion_persona/legal_body/` | ✅ Complete |
| Circle Agent Stack | `src/main/java/io/orvion/` | ✅ Complete |
| WebSocket Real-time Updates | `orvion-frontend/hooks/` | 🔄 In Progress |
| Wallet Integration | `orvion-frontend/` | 🔄 In Progress |

## Deployment

### Local Development

```bash
docker-compose up
```

### Production

```bash
docker-compose -f docker-compose.production.yml up -d
```

### Arc Network Testnet

Contracts are pre-configured for Arc Testnet. Deploy using:

```bash
npm run deploy:testnet
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add your feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## Security

- All credentials are stored in `.env` (gitignored)
- Private keys are never committed to version control
- Smart contracts are audited and use OpenZeppelin standards
- API endpoints require authentication via Bearer tokens

## Support

- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Discord**: [ORVION Community](https://discord.gg/orvion)
- **Twitter**: [@OrvionLabs](https://twitter.com/OrvionLabs)

## License

MIT License - see LICENSE file for details

---

**Built for the Agentic Economy.** 🜲
