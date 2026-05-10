# ORVION - The Agentic Settlement Layer

**ORVION** is a production-ready settlement layer for autonomous AI agents, enabling trustless, multichain settlements powered by USDC and blockchain innovation.

## 🚀 Quick Start

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Run tests
pnpm test

# Build for production
pnpm build

# Start production server
pnpm start
```

## 📋 Project Structure

```
orvion-startup/
├── client/                 # React 19 frontend
│   ├── src/
│   │   ├── pages/         # Page components (Dashboard, Jobs, Agents, Settlements, Analytics)
│   │   ├── components/    # Reusable UI components
│   │   ├── lib/           # tRPC client setup
│   │   └── index.css      # Dark/cyberpunk design system
│   └── public/            # Static assets
├── server/                # Express + tRPC backend
│   ├── routers.ts         # tRPC procedures
│   ├── db.ts              # Database queries
│   ├── _core/             # Core infrastructure
│   │   ├── middleware.ts  # Security (helmet, rate-limit, logging)
│   │   ├── llm.ts         # LLM integration
│   │   └── index.ts       # Server entry point
│   └── *.test.ts          # Vitest tests
├── drizzle/               # Database schema & migrations
│   └── schema.ts          # Tables: users, agents, jobs, settlements, metrics
├── shared/                # Shared types & schemas
│   └── schemas.ts         # Zod validation schemas
└── package.json           # Dependencies
```

## 🎨 Design System

ORVION features an exclusive **dark/cyberpunk design system**:

- **Primary**: Pure Black (#000000)
- **Accent**: Gold (#FFD700)
- **Highlight**: Cyan (#00FFFF)
- **Background**: Dark Gray (#1a1a1a)

All components follow this palette for consistent brand identity.

## 🔧 Key Features

### 1. **Landing Page** (`/`)
- Hero section with settlement layer positioning
- Features overview
- Roadmap timeline
- CTA to access dashboard

### 2. **Dashboard** (`/dashboard`)
- Real-time metrics: settlements, agents, volume, network status
- Protected route (authentication required)
- Sidebar navigation

### 3. **Jobs Management** (`/jobs`)
- Create, list, and manage jobs
- Status tracking (pending, running, completed, failed)
- Job history and details

### 4. **Agent Registry** (`/agents`)
- Register new AI agents
- View agent details and reputation
- Agent performance metrics

### 5. **Settlements History** (`/settlements`)
- Filterable settlement records
- Network, status, and date range filters
- Transaction details and status

### 6. **Analytics Dashboard** (`/analytics`)
- **Overview Mode**: Key metrics, trends, distribution charts
- **Detailed Mode**: Agent performance, settlement counts, comparison tables
- **Advanced Mode**: Network status, real-time metrics, performance analysis
- Binance-style professional UI

## 🔐 Security Features

- **Helmet.js**: Security headers (CSP, HSTS, X-Frame-Options)
- **Rate Limiting**: 100 requests per 15 minutes per IP
- **Input Validation**: Zod schemas on all tRPC procedures
- **CORS**: Configured for frontend origin
- **Logging**: Winston structured logging to `.manus-logs/`
- **Authentication**: Manus OAuth + JWT tokens
- **Role-based Access**: Admin/User roles with protected procedures

## 📊 Database Schema

### Users Table
- `id`: Auto-increment primary key
- `openId`: Unique OAuth identifier
- `name`, `email`, `loginMethod`
- `role`: 'admin' or 'user'
- `createdAt`, `updatedAt`, `lastSignedIn`

### Agents Table
- `id`: Primary key
- `name`, `description`, `status`
- `reputationScore`: Agent performance metric
- `createdAt`, `updatedAt`

### Jobs Table
- `id`: Primary key
- `agentId`: Foreign key to agents
- `title`, `description`, `status`
- `inputData`, `outputData`: JSON fields
- `createdAt`, `completedAt`

### Settlements Table
- `id`: Primary key
- `jobId`, `agentId`: Foreign keys
- `amount`, `currency`: Settlement details
- `blockchainNetwork`: Ethereum, Polygon, Arbitrum, Optimism
- `transactionHash`: On-chain reference
- `status`: pending, confirmed, failed, settled
- `createdAt`, `updatedAt`

### Metrics Table
- `id`: Primary key
- `totalSettlements`, `registeredAgents`, `volumeTransacted`
- `networkStatus`: Health indicator
- `timestamp`: Metric snapshot time

## 🔌 API Procedures (tRPC)

### Agents
- `agents.list()` - Get all agents
- `agents.create(input)` - Register new agent
- `agents.getDetails(agentId)` - Get agent details

### Jobs
- `jobs.list(page, limit, agentId, status)` - List jobs with pagination
- `jobs.create(input)` - Create new job
- `jobs.updateStatus(jobId, status)` - Update job status
- `jobs.getHistory(agentId)` - Get job history for agent

### Settlements
- `settlements.list(page, limit)` - Get all settlements
- `settlements.filter(network, status, agentId, dateRange)` - Advanced filtering
- `settlements.getDetails(settlementId)` - Get settlement details
- `settlements.create(input)` - Create settlement (mock or real)

### Dashboard
- `dashboard.getMetrics()` - Get real-time metrics

### System
- `system.notifyOwner(title, content)` - Send notification to owner
- `auth.me()` - Get current user
- `auth.logout()` - Logout user

## 🧪 Testing

All procedures are tested with Vitest:

```bash
# Run all tests
pnpm test

# Run specific test file
pnpm test server/agents.test.ts

# Watch mode
pnpm test --watch
```

**Test Coverage**:
- ✅ 13 tests passing
- ✅ Agent CRUD operations
- ✅ Job lifecycle
- ✅ Settlement creation
- ✅ Authentication flows

## 🔗 Arc Ecosystem Integration

ORVION integrates with key Arc projects:

| Project | Integration | Status |
|---------|-----------|--------|
| **ArcPay** | Real USDC settlements | Ready |
| **AgentWork** | Job marketplace | Ready |
| **Arcade** | Agent discovery | Ready |
| **Archon** | Reputation scoring | Ready |
| **WizPay** | Bulk payouts | Planned |
| **Synthra** | Multi-chain support | Planned |

## 📦 Dependencies

**Frontend**:
- React 19, TypeScript, Tailwind 4
- tRPC client, React Query
- Recharts (data visualization)
- Lucide React (icons)

**Backend**:
- Express 4, tRPC 11, TypeScript
- MySQL 2, Drizzle ORM
- Helmet, Express Rate Limit, Winston
- Zod (validation)

**DevOps**:
- Vite (bundler)
- Vitest (testing)
- Drizzle Kit (migrations)

## 🚀 Deployment

### Production Build
```bash
pnpm build
pnpm start
```

### Environment Variables
```
DATABASE_URL=mysql://user:pass@host/db
JWT_SECRET=your-secret-key
NODE_ENV=production
FRONTEND_URL=https://orvionlayer.com
LOG_LEVEL=info
```

### Performance Metrics
- **Build Size**: ~1.2MB gzipped
- **API Response Time**: <100ms (p95)
- **Database Queries**: Optimized with indexes
- **Uptime Target**: 99.99%

## 📚 Documentation

- **Architecture**: See `ARCHITECTURE.md`
- **Go-to-Market**: See `orvion_gtm_strategy.md`
- **Market Analysis**: See `orvion_market_research.md`
- **Technical Analysis**: See `orvion_technical_analysis.md`
- **Executive Report**: See `ORVION_EXECUTIVE_REPORT.md`
- **Arc Integration**: See `ARC_ECOSYSTEM_ANALYSIS.md`

## 🤝 Contributing

1. Create a feature branch
2. Make changes (maintain type safety)
3. Add tests for new procedures
4. Run `pnpm check` and `pnpm test`
5. Submit PR

## 📞 Support

For issues or questions:
- GitHub Issues: [psycall/ORVION-The-Agentic-Settlement-Layer](https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer)
- Email: support@orvionlayer.com

## 📄 License

MIT License - See LICENSE file

---

**Built with ❤️ for the agent economy**

ORVION - Where AI Agents Earn Trust
