# ORVION Frontend-Backend Integration Guide

## Overview

This document describes the complete integration between the ORVION React frontend and FastAPI backend, including API contracts, data flows, and deployment strategies.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TypeScript)             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Dashboard │ AgentCard │ SettlementFlow │ VoteCounter │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ useAgents Hook │ useSettlements Hook │ API Client    │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (JSON)
┌────────────────────────▼────────────────────────────────────┐
│                    Backend (FastAPI + Python)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Agent Registry │ Settlement Engine │ Reputation Mgmt │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ SQLAlchemy ORM │ Pydantic Schemas │ Business Logic  │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL
┌────────────────────────▼────────────────────────────────────┐
│              Database (SQLite / PostgreSQL)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ agents │ settlements │ jobs │ execution_receipts    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## API Client Integration

### Setup

The frontend uses a centralized API client (`client/src/lib/api.ts`) that handles all backend communication:

```typescript
import { orvionAPI } from '@/lib/api';

// API client is a singleton instance
// Automatically configured with base URL from VITE_API_URL env var
```

### Configuration

**Environment Variables** (`.env` or `.env.local`):
```env
VITE_API_URL=http://localhost:8080
VITE_ANALYTICS_ENDPOINT=https://analytics.example.com
VITE_ANALYTICS_WEBSITE_ID=your_website_id
```

### Error Handling

The API client includes automatic error handling:

```typescript
// Errors are logged and thrown for component-level handling
try {
  const agents = await orvionAPI.getAgents();
} catch (error) {
  // Handle error in component
  console.error('Failed to fetch agents:', error);
}
```

## Custom Hooks

### useAgents Hook

Fetches and manages agent data with automatic polling:

```typescript
import { useAgents } from '@/hooks/useAgents';

export function MyComponent() {
  const { agents, loading, error } = useAgents({
    agentType: 'research',
    capabilities: 'data-analysis',
    limit: 50,
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {agents.map(agent => (
        <AgentCard key={agent.id} {...agent} />
      ))}
    </div>
  );
}
```

### useSettlements Hook

Fetches settlement data with optional polling:

```typescript
import { useSettlements } from '@/hooks/useSettlements';

export function SettlementMonitor() {
  const { settlements, loading, error } = useSettlements({
    agentId: 'agent-123',
    limit: 100,
    pollInterval: 5000,  // Poll every 5 seconds
  });

  return (
    <SettlementFlow settlements={settlements} />
  );
}
```

## Data Flow Examples

### Agent Registration Flow

```
1. User submits agent form in frontend
   ↓
2. Frontend calls: orvionAPI.registerAgent(agentData)
   ↓
3. POST /api/v1/discovery/agents
   ↓
4. Backend validates and creates agent in database
   ↓
5. Returns: { id, agent_name, agent_type, ... }
   ↓
6. Frontend updates UI with new agent
```

### Settlement Creation Flow

```
1. User initiates settlement from dashboard
   ↓
2. Frontend calls: orvionAPI.createSettlement(settlementData)
   ↓
3. POST /api/v1/settlement/settlements
   ↓
4. Backend creates settlement record (status: pending)
   ↓
5. Returns: { id, status, amount, ... }
   ↓
6. Frontend shows settlement in list (polling for updates)
   ↓
7. Backend processes batch and updates status to 'confirmed'
   ↓
8. Frontend automatically reflects status change
```

## Component Integration Examples

### Dashboard with Real Data

```typescript
import { useAgents } from '@/hooks/useAgents';

export function Dashboard() {
  const { agents, loading, error } = useAgents();

  // Fallback to mock data if API fails
  const displayAgents = error ? mockAgents : agents;

  return (
    <div>
      {loading && <LoadingSpinner />}
      {error && <ErrorBanner message={error} />}
      
      <div className="grid">
        {displayAgents.map(agent => (
          <AgentCard key={agent.id} {...agent} />
        ))}
      </div>
    </div>
  );
}
```

## Testing Integration

### API Test Suite

Run comprehensive API tests:

```bash
cd /home/ubuntu/ORVION-The-Agentic-Settlement-Layer
python test_api.py
```

**Test Coverage:**
- ✅ Health Check
- ✅ Agent Registration
- ✅ Agent Discovery
- ✅ Settlement Creation
- ✅ Settlement Retrieval
- ✅ Batch Processing
- ✅ Execution Receipts

### Frontend Testing

```bash
cd client

# Run unit tests
pnpm test

# Run with coverage
pnpm test:coverage

# E2E tests (if configured)
pnpm test:e2e
```

## Deployment Strategies

### Development

**Backend:**
```bash
cd /home/ubuntu/ORVION-The-Agentic-Settlement-Layer
python -m uvicorn main:app --host 0.0.0.0 --port 8080
```

**Frontend:**
```bash
cd client
pnpm dev  # Runs on http://localhost:5173
```

**Environment:**
```env
VITE_API_URL=http://localhost:8080
```

### Production (Railway)

**Backend Deployment:**
```bash
# railway.json configures automatic deployment
# Procfile: web: python -m uvicorn main:app --host 0.0.0.0 --port $PORT

railway up
```

**Frontend Deployment:**
```bash
# Build static files
pnpm build

# Deploy to production or external CDN
# VITE_API_URL points to production backend
```

### Docker Compose

```bash
docker-compose up -d

# Services:
# - orvion-api: http://localhost:8080
# - orvion-frontend: http://localhost:3000
# - postgres: localhost:5432
# - redis: localhost:6379
```

## Error Handling & Fallbacks

### API Failure Handling

The frontend implements graceful degradation:

```typescript
export function Dashboard() {
  const { agents, error } = useAgents();

  if (error) {
    // Show warning badge
    return (
      <div>
        <AlertBanner>Using demo data - API unavailable</AlertBanner>
        <AgentGrid agents={mockAgents} />
      </div>
    );
  }

  return <AgentGrid agents={agents} />;
}
```

### Network Resilience

- Automatic retry on transient failures
- Exponential backoff for rate limiting
- Fallback to mock data for UX continuity
- Error logging for debugging

## Performance Optimization

### Frontend Optimization

- **Lazy Loading**: Components load on demand
- **Code Splitting**: Route-based code splitting
- **Memoization**: useCallback/useMemo for expensive computations
- **Caching**: HTTP caching headers on API responses

### Backend Optimization

- **Query Optimization**: Indexed database queries
- **Pagination**: Limit/offset for large datasets
- **Batch Processing**: Efficient settlement batching
- **Connection Pooling**: SQLAlchemy session management

## Security Considerations

### Frontend Security

- Input validation on all forms
- XSS protection via React's automatic escaping
- CSRF tokens for state-changing operations
- Secure storage of sensitive data

### Backend Security

- Pydantic validation on all inputs
- SQL injection prevention via ORM
- Rate limiting on API endpoints
- CORS configuration for frontend domain

## Monitoring & Logging

### Frontend Logging

```typescript
// Browser console logs
console.log('API Request:', method, url);
console.error('API Error:', error);
```

### Backend Logging

```python
# Server logs
logger.info(f"Agent registered: {agent_id}")
logger.error(f"Settlement failed: {error}")
```

### Health Checks

**Frontend:**
```typescript
const health = await orvionAPI.healthCheck();
// { status: 'healthy', service: 'ORVION', version: '2.0.0' }
```

**Backend:**
```bash
curl http://localhost:8080/health
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| CORS Error | Backend not allowing frontend domain | Add frontend URL to CORS config |
| API Timeout | Backend slow/unresponsive | Check backend logs, increase timeout |
| 404 Not Found | Wrong API endpoint | Verify endpoint path in API client |
| 500 Server Error | Backend exception | Check backend logs for stack trace |
| Empty Data | API returns empty list | Verify test data exists in database |

### Debug Mode

Enable detailed logging:

```typescript
// Frontend
localStorage.setItem('DEBUG', 'orvion:*');

// Backend
export DEBUG=orvion:* python -m uvicorn main:app
```

## Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] GraphQL API alternative
- [ ] Advanced caching strategies
- [ ] Offline mode support
- [ ] Mobile app integration
- [ ] Multi-chain support

---

**ORVION Integration Guide © 2026**
