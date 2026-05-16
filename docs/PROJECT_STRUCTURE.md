# ORVION Project Structure

Complete guide to the project organization and file structure.

## 📁 Directory Layout

```
ORVION/
├── 📂 backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── orvion/                 # Core backend modules
│   │   ├── models.py           # Database models (SQLAlchemy)
│   │   ├── schemas.py          # Pydantic request/response schemas
│   │   ├── database.py         # Database connection and session
│   │   ├── auth.py             # Authentication logic
│   │   ├── settlement_engine.py # Settlement processing
│   │   ├── agent_registry.py   # Agent management
│   │   ├── notifications.py    # WebSocket notifications
│   │   ├── circle_agent_stack.py # Circle integration (NEW)
│   │   ├── circle_service_real.py # Circle CCTP implementation
│   │   ├── arc_auth.py         # Arc wallet authentication
│   │   ├── rate_limiter.py     # Rate limiting middleware
│   │   ├── logging_config.py   # Structured logging
│   │   ├── webhook_manager.py  # Webhook event handling
│   │   ├── reputation_engine.py # Agent reputation scoring
│   │   └── dispute_engine.py   # Dispute resolution
│   ├── routes/                 # API route handlers
│   │   ├── auth_routes.py
│   │   ├── settlements_routes.py
│   │   ├── agents_routes.py
│   │   ├── circle_agent_routes.py # Circle endpoints (NEW)
│   │   ├── webhooks_routes.py
│   │   ├── reputation_routes.py
│   │   ├── disputes_routes.py
│   │   └── dashboard_routes.py
│   ├── orvion_sdk.py           # Python SDK v1
│   ├── orvion_sdk_enhanced.py  # Python SDK v2 (production)
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
│
├── 📂 frontend/
│   ├── src/
│   │   ├── components/         # Reusable React components
│   │   │   ├── GlassCard.tsx   # Glassmorphism card
│   │   │   ├── GlowButton.tsx  # Animated button
│   │   │   ├── GradientText.tsx # Gradient text effect
│   │   │   └── ...
│   │   ├── pages/              # Page components
│   │   │   ├── LandingPageShowcase.tsx # Hero/showcase page (NEW)
│   │   │   ├── LoginPage.tsx   # Arc wallet login
│   │   │   ├── DashboardPage.tsx # Main dashboard
│   │   │   └── ...
│   │   ├── hooks/              # Custom React hooks
│   │   │   ├── useAuth.ts      # Authentication state
│   │   │   ├── useApi.ts       # API calls
│   │   │   └── ...
│   │   ├── lib/
│   │   │   └── api.ts          # Axios HTTP client
│   │   ├── App.tsx             # Main app component
│   │   ├── main.tsx            # React entry point
│   │   └── index.css           # Global styles (SmartVault design)
│   ├── package.json            # Node dependencies
│   ├── tsconfig.json           # TypeScript config
│   ├── vite.config.ts          # Vite bundler config
│   └── .env.example            # Frontend env vars
│
├── 📂 contracts/
│   ├── Orvion.sol              # Main smart contract
│   ├── OrvionSettlement.sol    # Settlement logic
│   ├── OrvionAgent.sol         # Agent management
│   └── ...
│
├── 📂 scripts/
│   ├── deploy/
│   │   ├── deploy.js           # Contract deployment
│   │   └── deploy-secure.js    # Secure deployment with validation
│   ├── setup/
│   │   ├── setup.sh            # Automated setup script
│   │   └── init_db.py          # Database initialization
│   └── migrations/
│       └── alembic/            # Database migrations
│
├── 📂 examples/
│   ├── agents/
│   │   ├── agent-workflow.ts   # Example agent integration
│   │   └── agent-settlement.py # Python agent example
│   └── integrations/
│       ├── circle-integration.ts
│       ├── arc-integration.ts
│       └── webhook-integration.ts
│
├── 📂 docs/
│   ├── guides/
│   │   ├── QUICKSTART.md       # Quick start guide
│   │   ├── SETUP.md            # Detailed setup
│   │   └── DEPLOYMENT.md       # Production deployment
│   ├── architecture/
│   │   ├── ARCHITECTURE.md     # System architecture
│   │   ├── API_DESIGN.md       # API design patterns
│   │   └── DATABASE_SCHEMA.md  # Database design
│   ├── api/
│   │   ├── API_REFERENCE.md    # Complete API docs
│   │   ├── CIRCLE_AGENT_STACK.md # Circle integration (NEW)
│   │   └── WEBHOOKS.md         # Webhook documentation
│   ├── PROJECT_STRUCTURE.md    # This file
│   ├── SECURITY.md             # Security guidelines
│   ├── SECURITY_PRIVATE_KEY.md # Private key protection
│   └── CREDENTIALS_EXPLAINED.md # Credential setup
│
├── 📂 packages/
│   └── sdk/
│       ├── src/
│       │   ├── OrvionClient.ts # TypeScript SDK
│       │   └── index.ts        # SDK exports
│       ├── package.json        # SDK dependencies
│       ├── tsconfig.json
│       ├── README.md
│       └── tests/
│           └── OrvionClient.test.ts
│
├── 📂 tests/
│   ├── test_api.py             # API integration tests
│   ├── test_settlement_integration.py
│   ├── Orvion.test.js          # Solidity tests
│   └── test_integration.js     # E2E tests
│
├── 📂 .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
│
├── 📂 deployments/
│   ├── docker-compose.yml      # Local development
│   ├── Dockerfile              # Container image
│   └── kubernetes/             # K8s manifests
│
├── README.md                   # Project overview
├── package.json                # Root package config
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment template
└── LICENSE                     # MIT License
```

## 📋 Key Files Explained

### Backend

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app setup, route registration |
| `orvion/models.py` | SQLAlchemy ORM models |
| `orvion/schemas.py` | Request/response validation |
| `orvion/settlement_engine.py` | Core settlement logic |
| `orvion/circle_agent_stack.py` | Circle integration (NEW) |
| `orvion_sdk_enhanced.py` | Production Python SDK |
| `requirements.txt` | All dependencies |

### Frontend

| File | Purpose |
|------|---------|
| `src/App.tsx` | Main app routing |
| `src/pages/LandingPageShowcase.tsx` | Hero/showcase page (NEW) |
| `src/pages/DashboardPage.tsx` | Main dashboard |
| `src/lib/api.ts` | Axios HTTP client |
| `src/index.css` | Global styles |
| `package.json` | Dependencies |

### Smart Contracts

| File | Purpose |
|------|---------|
| `contracts/Orvion.sol` | Main contract |
| `scripts/deploy-secure.js` | Deployment script |

### Documentation

| File | Purpose |
|------|---------|
| `docs/CIRCLE_AGENT_STACK.md` | Circle integration guide (NEW) |
| `docs/API_REFERENCE.md` | Complete API docs |
| `docs/ARCHITECTURE.md` | System design |
| `docs/SECURITY.md` | Security guidelines |

## 🔄 Data Flow

```
User → Frontend (React)
         ↓
    API Client (Axios)
         ↓
    FastAPI Backend
         ↓
    ├─ Settlement Engine
    ├─ Circle Agent Stack (NEW)
    ├─ Smart Contracts
    └─ Database
         ↓
    Response → Frontend
```

## 🚀 Getting Started

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Smart Contract Deployment**
   ```bash
   npm install
   npx hardhat run scripts/deploy-secure.js --network arc-testnet
   ```

## 📦 Dependencies

### Backend
- FastAPI - Web framework
- SQLAlchemy - ORM
- Pydantic - Validation
- Web3.py - Blockchain interaction
- Requests - HTTP client

### Frontend
- React 19 - UI framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Framer Motion - Animations
- Axios - HTTP client
- Recharts - Data visualization

### Smart Contracts
- Solidity 0.8.x
- Hardhat - Development framework
- ethers.js - Web3 library

## 🔐 Environment Variables

See `.env.example` for all required variables:

```bash
# Backend
DATABASE_URL=postgresql://...
JWT_SECRET=...
CIRCLE_API_KEY=...
PRIVATE_KEY=0x...

# Frontend
VITE_API_URL=http://localhost:8000
VITE_WALLET_CONNECT_ID=...
```

## 📚 Documentation Structure

```
docs/
├── guides/           # How-to guides
├── architecture/     # Design docs
├── api/              # API reference
└── [topic].md        # Topic-specific docs
```

## 🔗 Related Files

- **Configuration**: `.env.example`, `tsconfig.json`, `vite.config.ts`
- **Git**: `.gitignore`, `.github/workflows/ci.yml`
- **Package Management**: `package.json`, `requirements.txt`
- **Deployment**: `docker-compose.yml`, `Dockerfile`

## 📝 Naming Conventions

- **Python**: `snake_case` for functions/variables, `PascalCase` for classes
- **TypeScript**: `camelCase` for functions/variables, `PascalCase` for types/classes
- **Files**: `kebab-case` for components (e.g., `glass-card.tsx`)
- **Routes**: `/api/v1/[resource]/[action]`

## 🎯 Next Steps

1. Read [QUICKSTART.md](./guides/QUICKSTART.md) for setup
2. Check [API_REFERENCE.md](./api/API_REFERENCE.md) for endpoints
3. Review [CIRCLE_AGENT_STACK.md](./api/CIRCLE_AGENT_STACK.md) for new features
4. See [ARCHITECTURE.md](./architecture/ARCHITECTURE.md) for system design
