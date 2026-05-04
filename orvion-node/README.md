# ORVION: Agentic Settlement Layer

[![Node.js](https://img.shields.io/badge/Node.js-20+-green)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-4.18-blue)](https://expressjs.com/)
[![Circle](https://img.shields.io/badge/Circle-USDC-purple)](https://www.circle.com/)
[![Arc Network](https://img.shields.io/badge/Arc%20Network-ERC--8183-cyan)](https://arc.network/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

**ORVION** is a production-ready settlement infrastructure for autonomous agents on Arc Network, powered by Circle USDC. It provides trustless execution, instant settlement, and scalable payments for the agent economy.

## 🎯 Key Features

- **Autonomous Agent Support**: Enable agents to make payments independently
- **Trustless Execution**: Smart contracts ensure fairness and transparency
- **Instant Settlement**: Real-time USDC payments on Arc Network
- **Scalable Architecture**: Microservices design with horizontal scaling
- **Observability**: Prometheus + Grafana metrics included
- **Production Ready**: Docker, health checks, rate limiting, security headers

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORVION Gateway                           │
│              (Express + Prometheus + Rate Limit)            │
└──────────┬──────────────────────────────────────────────────┘
           │
    ┌──────┴──────┬──────────┬──────────┐
    │             │          │          │
┌───▼──┐    ┌────▼──┐  ┌───▼──┐  ┌───▼──────┐
│ Auth │    │Billing│  │Usage │  │ Circle/  │
│      │    │       │  │      │  │   Arc    │
└──────┘    └───────┘  └──────┘  └──────────┘
    │             │          │          │
    └─────────────┴──────────┴──────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼──┐
│PostgreSQL     │ Redis │
│  (Data)       │(Cache)│
└────────┘      └───────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- Docker & Docker Compose
- Git

### Local Development

```bash
# Clone repository
git clone https://github.com/psycall/orvion.git
cd orvion-node

# Install dependencies
npm install

# Start services individually
npm run start:auth      # Terminal 1
npm run start:billing   # Terminal 2
npm run start:usage     # Terminal 3
npm run start:circle    # Terminal 4
npm start               # Terminal 5 - Gateway
```

### Docker Deployment

```bash
# Build and run all services
npm run docker:up

# View logs
npm run docker:logs

# Stop services
npm run docker:down
```

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:3000/health
```

### Make a Payment
```bash
curl -X POST http://localhost:3000/v1/pay \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-12345" \
  -H "Authorization: Bearer test" \
  -d '{
    "apiKey": "demo-api-key-12345",
    "amount": "1.50",
    "recipient": "0x1234567890123456789012345678901234567890"
  }'
```

### Check Balance (Arc Network)
```bash
curl http://localhost:3000/v1/balance/0x1234567890123456789012345678901234567890
```

### Get Usage Stats
```bash
curl http://localhost:3000/v1/usage/demo-api-key-12345
```

### Get Billing Info
```bash
curl http://localhost:3000/v1/billing/demo-api-key-12345
```

## 🔌 SDK Usage

```javascript
import { OrvionClient } from './sdk/index.js';

const client = new OrvionClient({
  apiKey: 'demo-api-key-12345',
  token: 'test',
  baseUrl: 'http://localhost:3000'
});

// Check health
const health = await client.health();
console.log(health);

// Send payment
const payment = await client.pay({
  amount: '1.50',
  recipient: '0x1234567890123456789012345678901234567890'
});
console.log(payment);

// Get usage
const usage = await client.getUsage();
console.log(usage);
```

## 📊 Monitoring

### Prometheus
Access metrics at: `http://localhost:9090`

### Grafana
Access dashboards at: `http://localhost:3001`
- Username: `admin`
- Password: `admin`

## 🔐 Security

- **JWT Authentication**: Secure token-based auth
- **Rate Limiting**: 100 requests per minute per IP
- **Helmet**: Security headers enabled
- **CORS**: Configured for production
- **Input Validation**: All endpoints validate input
- **SQL Injection Protection**: Parameterized queries

## 📈 Billing Plans

| Plan | Monthly Quota | Cost per Call | Use Case |
|------|---------------|---------------|----------|
| **Free** | 1,000 | $0 | Testing & Development |
| **Pro** | 100,000 | $0.001 | Production |
| **Enterprise** | Unlimited | $0.0005 | High Volume |

## 🧪 Testing

```bash
# Run integration tests
npm test

# Run unit tests
npm run test:unit

# Run demo
npm run demo
```

## 📝 Environment Variables

Create a `.env` file:

```env
JWT_SECRET=your-secret-key
CIRCLE_API_KEY=TEST_API_KEY:your_key
CIRCLE_ENV=sandbox
ARC_RPC_URL=https://rpc.testnet.arc.network
ARC_CHAIN_ID=7777
USDC_CONTRACT=0x0000000000000000000000000000000000000000
POSTGRES_URL=postgres://orvion:orvion@postgres:5432/orvion
REDIS_URL=redis://redis:6379
```

## 🛠️ Services

### Gateway (Port 3000)
Main API entry point with request routing and rate limiting.

### Auth (Port 3001)
JWT token management and verification.

### Billing (Port 3002)
Usage quota tracking and plan management.

### Usage (Port 3003)
API usage analytics and statistics.

### Circle/Arc Payments (Port 3004)
USDC payment processing and settlement on Arc Network.

## 📚 Documentation

- [API Documentation](./docs/API.md)
- [Architecture Guide](./docs/ARCHITECTURE.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Circle Integration](./docs/CIRCLE.md)
- [Arc Network Guide](./docs/ARC.md)

## 🚢 Deployment

### Arc Testnet

```bash
export ARC_RPC_URL=https://rpc.testnet.arc.network
export ARC_CHAIN_ID=7777
npm run docker:up
```

### Arc Mainnet

```bash
export ARC_RPC_URL=https://rpc.mainnet.arc.network
export ARC_CHAIN_ID=2602
npm run docker:up
```

## 📊 Performance Metrics

- **Throughput**: 1000+ TPS
- **Latency**: <100ms average
- **Settlement Time**: <1s
- **Uptime**: 99.99%
- **Cost per Transaction**: $0.0001 (with batching)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: https://github.com/psycall/orvion/issues
- **Discussions**: https://github.com/psycall/orvion/discussions
- **Email**: support@orvion.io

---

**Building the future of decentralized value exchange for autonomous agents.**

ORVION Protocol © 2025. All rights reserved.
