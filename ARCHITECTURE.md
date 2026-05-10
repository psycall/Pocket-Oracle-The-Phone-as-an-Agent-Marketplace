# ORVION Architecture & Implementation Guide

## Overview

**ORVION** is a production-ready Agentic Settlement Layer built with a modern tech stack combining React 19, tRPC 11, Express 4, and MySQL. The platform enables trustless, multichain settlements for AI agents with real-time metrics and comprehensive management dashboards.

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 19 + Tailwind 4 | User interface with dark/cyberpunk design |
| Backend | Express 4 + tRPC 11 | Type-safe API with end-to-end type safety |
| Database | MySQL + Drizzle ORM | Persistent data storage with migrations |
| Authentication | Manus OAuth | Secure user authentication and session management |
| Real-time | WebSocket (planned) | Live settlement notifications |

## Project Structure

```
orvion-startup/
├── client/                    # React frontend
│   ├── src/
│   │   ├── pages/            # Page components (Home, Dashboard, Jobs, Agents, Settlements)
│   │   ├── components/       # Reusable UI components
│   │   ├── lib/              # tRPC client setup
│   │   ├── contexts/         # React contexts (Theme, etc.)
│   │   ├── App.tsx           # Main router
│   │   └── index.css         # ORVION design system (dark/cyberpunk)
│   └── public/               # Static assets
├── server/                    # Express backend
│   ├── routers.ts            # tRPC procedure definitions
│   ├── db.ts                 # Database query helpers
│   ├── *.test.ts             # Vitest unit tests
│   └── _core/                # Framework infrastructure
├── drizzle/                   # Database schema & migrations
│   ├── schema.ts             # Table definitions
│   └── *.sql                 # Migration files
├── shared/                    # Shared types & constants
└── storage/                   # S3 file storage helpers
```

## Database Schema

### Core Tables

**users** - Manus OAuth user accounts
- id (PK), openId (unique), name, email, role, timestamps

**agents** - AI agents registered on ORVION
- id (PK), userId (FK), name, description, status, reputationScore, totalJobsCompleted, totalVolumeSettled, timestamps

**jobs** - Job execution records
- id (PK), agentId (FK), title, description, status, inputData, outputData, executionTime, timestamps

**settlements** - On-chain USDC settlements
- id (PK), jobId (FK), agentId (FK), amount, currency, blockchainNetwork, transactionHash, status, gasUsed, timestamps

**metrics** - Real-time platform statistics
- id (PK), totalSettlements, registeredAgents, volumeTransacted, networkStatus, averageSettlementTime, successRate, timestamp

## API Design (tRPC)

### Public Procedures

- `agents.list()` - List all registered agents
- `jobs.list()` - List all jobs
- `settlements.list()` - List all settlements
- `settlements.filter({network?, status?})` - Filter settlements
- `dashboard.getMetrics()` - Get real-time metrics

### Protected Procedures (Requires Authentication)

- `agents.create({name, description})` - Register new agent
- `agents.getById({id})` - Get agent details
- `jobs.create({agentId, title, description, inputData})` - Create job
- `jobs.getById({id})` - Get job details
- `jobs.updateStatus({jobId, status})` - Update job status
- `settlements.create({jobId, agentId, amount, blockchainNetwork, transactionHash})` - Create settlement (triggers owner notification)
- `settlements.getById({id})` - Get settlement details
- `analysis.analyzeAgentPerformance({agentId})` - LLM-powered performance analysis

### System Procedures

- `auth.me()` - Get current user
- `auth.logout()` - Clear session
- `system.notifyOwner({title, content})` - Send notification to project owner

## Frontend Architecture

### Pages

| Page | Route | Protection | Purpose |
|------|-------|-----------|---------|
| Home | `/` | Public | Landing page with features, roadmap, CTA |
| Dashboard | `/dashboard` | Protected | Real-time metrics, charts, quick stats |
| Jobs | `/jobs` | Protected | Create, list, manage job execution |
| Agents | `/agents` | Protected | Register, list, view agent details |
| Settlements | `/settlements` | Protected | Track on-chain settlements, filter by network/status |

### Design System

**ORVION Dark/Cyberpunk Theme** - Exclusive brand identity

| Element | Color | OKLCH Value |
|---------|-------|------------|
| Background | Pure Black | `oklch(0.05 0 0)` |
| Foreground | Near White | `oklch(0.95 0.01 65)` |
| Primary (Gold) | Gold | `oklch(0.75 0.2 45)` |
| Accent (Cyan) | Cyan | `oklch(1 0.3 180)` |
| Card | Very Dark Gray | `oklch(0.1 0.01 0)` |
| Border | Dark Border | `oklch(0.2 0.02 0)` |

**Custom Components**

- `.btn-primary` - Gold gradient button with glow effect
- `.btn-secondary` - Cyan button with glow effect
- `.card-orvion` - Dark card with gold border
- `.metric-card` - Metric display with gold accent
- `.status-{active|pending|completed|failed|settled}` - Status badges
- `.table-orvion` - Styled table with gold headers
- `.input-orvion` - Dark input with gold focus ring

## Authentication Flow

1. User clicks "Access Dashboard" on landing page
2. Redirected to Manus OAuth login portal
3. After authentication, callback to `/api/oauth/callback`
4. Session cookie set with JWT token
5. User redirected to `/dashboard`
6. Protected pages check `useAuth()` and redirect to home if not authenticated

## Deployment Checklist

- [ ] Build frontend: `pnpm build`
- [ ] Run tests: `pnpm test`
- [ ] Check TypeScript: `pnpm check`
- [ ] Verify environment variables are set
- [ ] Database migrations applied
- [ ] OAuth credentials configured
- [ ] S3 storage configured (if using file uploads)
- [ ] Create production checkpoint
- [ ] Click "Publish" in Manus UI

## Development Workflow

### Adding a New Feature

1. **Update Schema** (if needed)
   ```bash
   # Edit drizzle/schema.ts
   pnpm drizzle-kit generate
   # Review generated SQL
   # Apply via webdev_execute_sql
   ```

2. **Add Database Helpers** (server/db.ts)
   ```ts
   export async function getFeature(id: number) {
     const db = await getDb();
     return db.select().from(features).where(eq(features.id, id));
   }
   ```

3. **Add tRPC Procedures** (server/routers.ts)
   ```ts
   feature: router({
     list: publicProcedure.query(async () => getFeatures()),
     create: protectedProcedure.input(z.object({...})).mutation(...)
   })
   ```

4. **Create Frontend Page** (client/src/pages/Feature.tsx)
   ```tsx
   const { data } = trpc.feature.list.useQuery();
   ```

5. **Add Route** (client/src/App.tsx)
   ```tsx
   <Route path={"/feature"} component={Feature} />
   ```

6. **Write Tests** (server/feature.test.ts)
   ```ts
   it("should list features", async () => {
     const result = await caller.feature.list();
     expect(Array.isArray(result)).toBe(true);
   });
   ```

7. **Run Tests**
   ```bash
   pnpm test
   ```

## Performance Optimization

- **Frontend**: React 19 with automatic memoization, Tailwind 4 with CSS-in-JS optimization
- **Backend**: tRPC with automatic batching, Drizzle ORM with query optimization
- **Database**: Indexed foreign keys, optimized query patterns
- **Caching**: Redis integration available for metrics snapshots

## Security Considerations

- **Authentication**: Manus OAuth with secure session cookies
- **Authorization**: Protected procedures with `protectedProcedure`
- **CORS**: Configured for frontend domain only
- **SQL Injection**: Parameterized queries via Drizzle ORM
- **Environment Variables**: Sensitive data in `.env` (never committed)
- **Private Keys**: For blockchain operations, use secure key management (KMS/HSM)

## Monitoring & Logging

- **Dev Server Logs**: `.manus-logs/devserver.log`
- **Browser Console**: `.manus-logs/browserConsole.log`
- **Network Requests**: `.manus-logs/networkRequests.log`
- **Session Replay**: `.manus-logs/sessionReplay.log`

## Support & Resources

- **Manus Documentation**: https://help.manus.im
- **tRPC Documentation**: https://trpc.io
- **Drizzle ORM**: https://orm.drizzle.team
- **Tailwind CSS**: https://tailwindcss.com
- **React Documentation**: https://react.dev

---

**ORVION © 2026. All rights reserved.**
