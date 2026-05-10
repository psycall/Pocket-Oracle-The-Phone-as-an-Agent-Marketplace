# ORVION Production Setup Guide

## Quick Start (2-3 days to demo-ready)

### Phase 1: Environment Setup (1 hour)

```bash
# Clone repository
git clone https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer.git
cd ORVION

# Install dependencies
pip install -r requirements.txt
npm install

# Setup environment
cp .env.example .env
```

### Phase 2: Database Setup (30 minutes)

```bash
# Initialize database
python scripts/init_db.py

# Run migrations
alembic upgrade head

# Verify database
psql -U user -d orvion -c "SELECT COUNT(*) FROM users;"
```

### Phase 3: Smart Contract Deployment (2-4 hours)

```bash
# Compile contract
npx hardhat compile

# Deploy to Arc testnet
# Set PRIVATE_KEY in .env first
npx hardhat run scripts/deploy.js --network arc-testnet

# Verify deployment
cat deployments/arc-testnet.json
```

### Phase 4: Circle CCTP Integration (2 hours)

```bash
# Set Circle credentials in .env
export CIRCLE_API_KEY="your-api-key"
export CIRCLE_ENTITY_SECRET="your-secret"
export CIRCLE_WALLET_SET_ID="your-wallet-set-id"

# Test Circle connection
python -c "from orvion.circle_service_real import CircleCCTPService; print('✅ Circle SDK loaded')"
```

### Phase 5: Start Backend (15 minutes)

```bash
# Start FastAPI server
python main.py

# Verify API is running
curl http://localhost:8000/health
```

### Phase 6: Start Dashboard (15 minutes)

```bash
# Install frontend dependencies
cd frontend
npm install

# Start React development server
npm start

# Open http://localhost:3000
```

## Environment Variables

### Required for Production

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/orvion

# JWT
JWT_SECRET=your-super-secret-key-change-this

# Circle
CIRCLE_API_KEY=your-circle-api-key
CIRCLE_ENTITY_SECRET=your-circle-entity-secret
CIRCLE_WALLET_SET_ID=your-wallet-set-id

# Arc Network
ARC_RPC_URL=https://testnet-rpc.arc.io
ARC_CHAIN_ID=1234

# Private Key (for contract deployment)
PRIVATE_KEY=your-private-key-hex
```

### Optional

```bash
# Logging
LOG_LEVEL=INFO

# Server
API_PORT=8000
API_HOST=0.0.0.0

# Redis (for caching)
REDIS_URL=redis://localhost:6379
```

## API Endpoints

### Discovery
- `POST /api/v1/discovery/agents` - Register agent
- `GET /api/v1/discovery/agents` - List agents
- `GET /api/v1/discovery/agents/{id}` - Get agent

### Settlement
- `POST /api/v1/settlement/settlements` - Create settlement
- `GET /api/v1/settlement/settlements/{id}` - Get settlement
- `POST /api/v1/settlement/execution-receipts` - Submit proof

### Authentication
- `POST /api/v1/auth/wallet-login` - Login with wallet
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout

### Dashboard
- `GET /api/v1/dashboard/stats` - Get dashboard stats
- `GET /api/v1/dashboard/agents-overview` - Agents overview
- `GET /api/v1/dashboard/settlement-trends` - Settlement trends

### Webhooks
- `POST /api/v1/webhooks/subscribe` - Subscribe to events
- `DELETE /api/v1/webhooks/{id}` - Unsubscribe
- `GET /api/v1/webhooks/events` - Get events

## Testing

### Unit Tests
```bash
python -m pytest tests/ -v
```

### Integration Tests
```bash
python test_api.py
```

### SDK Tests
```bash
cd packages/sdk && npm test
```

### Contract Tests
```bash
npx hardhat test
```

## Deployment

### Docker
```bash
# Build image
docker build -t orvion:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e JWT_SECRET="..." \
  -e CIRCLE_API_KEY="..." \
  orvion:latest
```

### Kubernetes
```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods -l app=orvion
```

## Monitoring

### Logs
```bash
# View application logs
tail -f logs/app.log

# View error logs
tail -f logs/error.log

# Search logs
grep "ERROR" logs/app.log
```

### Metrics
```bash
# Prometheus metrics available at
curl http://localhost:8000/metrics
```

### Health Check
```bash
# Check API health
curl http://localhost:8000/health
```

## Troubleshooting

### Database Connection Failed
```bash
# Check PostgreSQL is running
psql -U user -d orvion -c "SELECT 1;"

# Check DATABASE_URL format
echo $DATABASE_URL
```

### Circle API Error
```bash
# Verify Circle credentials
python -c "import os; print('API Key:', os.getenv('CIRCLE_API_KEY')[:10] + '...')"

# Test Circle connection
curl -H "Authorization: Bearer $CIRCLE_API_KEY" https://api.circle.com/v1/configuration/networks
```

### Smart Contract Deploy Failed
```bash
# Check private key is set
echo $PRIVATE_KEY

# Check Arc RPC is accessible
curl -X POST $ARC_RPC_URL -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'
```

### Rate Limiting Issues
```bash
# Check rate limit headers
curl -i http://localhost:8000/api/v1/discovery/agents

# Look for:
# X-RateLimit-Limit: 100
# X-RateLimit-Remaining: 99
# X-RateLimit-Reset: 1234567890
```

## Security Checklist

- [ ] Change JWT_SECRET to strong random value
- [ ] Enable HTTPS in production
- [ ] Set DATABASE_URL to production database
- [ ] Rotate Circle API keys regularly
- [ ] Enable database backups
- [ ] Setup monitoring and alerting
- [ ] Run security audit
- [ ] Enable rate limiting
- [ ] Setup logging and log aggregation
- [ ] Configure CORS properly

## Performance Tuning

### Database
```sql
-- Add indexes
CREATE INDEX idx_agents_reputation ON agents(reputation_score DESC);
CREATE INDEX idx_settlements_status ON settlements(status);
CREATE INDEX idx_settlements_created ON settlements(created_at DESC);
```

### Caching
```python
# Redis cache for frequently accessed data
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

### Connection Pooling
```python
# SQLAlchemy pool configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

## Support

- 📖 [Documentation](./README.md)
- 🐛 [Report Issues](https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer/issues)
- 💬 [Discussions](https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer/discussions)

---

**Last Updated**: May 10, 2026  
**Version**: 2.0.0  
**Status**: Production Ready ✅
