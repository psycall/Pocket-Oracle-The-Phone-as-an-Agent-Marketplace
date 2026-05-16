# Circle Agent Stack - Complete Integration Guide

**Financial Infrastructure for the Agentic Economy**

This guide covers the complete Circle Agent Stack integration in ORVION, including Agent Wallets, Marketplace, Nanopayments, and Circle Skills.

## Overview

The Circle Agent Stack enables agents to:
- **Hold Funds**: Controlled access to USDC through Agent Wallets
- **Discover Services**: Find and use services in the Agent Marketplace
- **Transact**: Machine-speed nanopayments powered by Circle Gateway
- **Extend Capabilities**: Leverage Circle Skills for specialized functions

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Circle Agent Stack Integration                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Agent Wallets│  │  Marketplace │  │ Nanopayments │ │
│  │              │  │              │  │              │ │
│  │ • USDC Hold  │  │ • Discovery  │  │ • Machine    │ │
│  │ • Balance    │  │ • Rating     │  │   Speed      │ │
│  │ • History    │  │ • Services   │  │ • Confirmed  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Circle Skills & Capabilities             │  │
│  │                                                  │  │
│  │ • Payment Processing    • Data Retrieval        │  │
│  │ • Computation          • Settlement             │  │
│  │ • Verification         • Analytics              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Agent Wallets

### Create Wallet

Create a new agent wallet for controlled USDC access.

**Endpoint**: `POST /api/v1/agent-stack/wallets/create`

**Request**:
```json
{
  "agent_id": "agent_123",
  "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f42bE",
  "initial_balance": 100.0
}
```

**Response**:
```json
{
  "agent_id": "agent_123",
  "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f42bE",
  "usdc_balance": 100.0,
  "created_at": "2024-01-15T10:30:00Z",
  "last_transaction": null,
  "transaction_count": 0,
  "total_volume": 0.0,
  "is_active": true
}
```

### Fund Wallet

Add USDC to an agent wallet.

**Endpoint**: `POST /api/v1/agent-stack/wallets/fund`

**Request**:
```json
{
  "agent_id": "agent_123",
  "amount": 50.0
}
```

**Response**:
```json
{
  "timestamp": "2024-01-15T10:35:00Z",
  "agent_id": "agent_123",
  "type": "funding",
  "amount": 50.0,
  "new_balance": 150.0
}
```

### Get Balance

Check current wallet balance.

**Endpoint**: `GET /api/v1/agent-stack/wallets/{agent_id}/balance`

**Response**:
```json
{
  "agent_id": "agent_123",
  "balance_usdc": 150.0
}
```

## Agent Marketplace

### Register Service

List a service in the marketplace.

**Endpoint**: `POST /api/v1/agent-stack/marketplace/services/register`

**Request**:
```json
{
  "provider_agent_id": "agent_123",
  "name": "Data Analysis Service",
  "description": "Advanced data analysis and insights",
  "category": "data_retrieval",
  "price_per_call": 0.50
}
```

**Response**:
```json
{
  "service_id": "svc_agent_123_0",
  "provider_agent_id": "agent_123",
  "name": "Data Analysis Service",
  "description": "Advanced data analysis and insights",
  "category": "data_retrieval",
  "price_per_call": 0.50,
  "currency": "USDC",
  "rating": 5.0,
  "call_count": 0,
  "uptime_percentage": 99.9,
  "created_at": "2024-01-15T10:40:00Z",
  "is_active": true
}
```

### Discover Services

Find services by category or rating.

**Endpoint**: `GET /api/v1/agent-stack/marketplace/services?category=data_retrieval&min_rating=4.0`

**Response**:
```json
[
  {
    "service_id": "svc_agent_123_0",
    "provider_agent_id": "agent_123",
    "name": "Data Analysis Service",
    "description": "Advanced data analysis and insights",
    "category": "data_retrieval",
    "price_per_call": 0.50,
    "currency": "USDC",
    "rating": 4.8,
    "call_count": 45,
    "uptime_percentage": 99.95,
    "created_at": "2024-01-15T10:40:00Z",
    "is_active": true
  }
]
```

### Rate Service

Rate a service (1-5 stars).

**Endpoint**: `POST /api/v1/agent-stack/marketplace/services/rate`

**Request**:
```json
{
  "service_id": "svc_agent_123_0",
  "rating": 4.5
}
```

**Response**:
```json
{
  "service_id": "svc_agent_123_0",
  "old_rating": 5.0,
  "new_rating": 4.75,
  "call_count": 46
}
```

## Nanopayments

### Create Nanopayment

Initiate a machine-speed payment for a service.

**Endpoint**: `POST /api/v1/agent-stack/nanopayments/create`

**Request**:
```json
{
  "from_agent_id": "agent_456",
  "to_agent_id": "agent_123",
  "service_id": "svc_agent_123_0",
  "amount": 0.50,
  "metadata": {
    "request_id": "req_789",
    "timestamp": "2024-01-15T10:45:00Z"
  }
}
```

**Response**:
```json
{
  "payment_id": "np_agent_456_agent_123_0",
  "from_agent_id": "agent_456",
  "to_agent_id": "agent_123",
  "service_id": "svc_agent_123_0",
  "amount": 0.50,
  "currency": "USDC",
  "status": "pending",
  "created_at": "2024-01-15T10:45:00Z",
  "confirmed_at": null,
  "tx_hash": null,
  "metadata": {
    "request_id": "req_789",
    "timestamp": "2024-01-15T10:45:00Z"
  }
}
```

### Confirm Nanopayment

Confirm payment on-chain.

**Endpoint**: `POST /api/v1/agent-stack/nanopayments/confirm`

**Request**:
```json
{
  "payment_id": "np_agent_456_agent_123_0",
  "tx_hash": "0x1234567890abcdef..."
}
```

**Response**:
```json
{
  "payment_id": "np_agent_456_agent_123_0",
  "from_agent_id": "agent_456",
  "to_agent_id": "agent_123",
  "service_id": "svc_agent_123_0",
  "amount": 0.50,
  "currency": "USDC",
  "status": "confirmed",
  "created_at": "2024-01-15T10:45:00Z",
  "confirmed_at": "2024-01-15T10:45:30Z",
  "tx_hash": "0x1234567890abcdef...",
  "metadata": {}
}
```

## Circle Skills

### Register Skill

Register a new Circle Skill capability.

**Endpoint**: `POST /api/v1/agent-stack/skills/register`

**Request**:
```json
{
  "name": "Advanced Analytics",
  "category": "analytics",
  "description": "Machine learning-based data analysis"
}
```

**Response**:
```json
{
  "skill_id": "skill_0",
  "name": "Advanced Analytics",
  "category": "analytics",
  "description": "Machine learning-based data analysis",
  "enabled_agents": [],
  "created_at": "2024-01-15T10:50:00Z"
}
```

### Enable Skill for Agent

Enable a skill for a specific agent.

**Endpoint**: `POST /api/v1/agent-stack/skills/enable`

**Request**:
```json
{
  "skill_id": "skill_0",
  "agent_id": "agent_123"
}
```

**Response**:
```json
{
  "skill_id": "skill_0",
  "agent_id": "agent_123",
  "enabled_agents": ["agent_123"]
}
```

### Get Agent Skills

Retrieve all skills enabled for an agent.

**Endpoint**: `GET /api/v1/agent-stack/skills/agent/{agent_id}`

**Response**:
```json
[
  {
    "skill_id": "skill_0",
    "name": "Advanced Analytics",
    "category": "analytics",
    "description": "Machine learning-based data analysis",
    "enabled_agents": ["agent_123"],
    "created_at": "2024-01-15T10:50:00Z"
  }
]
```

## Analytics & Reporting

### Agent Statistics

Get comprehensive statistics for an agent.

**Endpoint**: `GET /api/v1/agent-stack/stats/agent/{agent_id}`

**Response**:
```json
{
  "agent_id": "agent_123",
  "wallet": {
    "agent_id": "agent_123",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f42bE",
    "usdc_balance": 149.50,
    "created_at": "2024-01-15T10:30:00Z",
    "last_transaction": "2024-01-15T10:45:30Z",
    "transaction_count": 2,
    "total_volume": 0.50,
    "is_active": true
  },
  "services_provided": 1,
  "total_service_calls": 46,
  "avg_service_rating": 4.75,
  "payments_sent": 0,
  "payments_received": 1,
  "total_spent": 0.0,
  "total_earned": 0.50,
  "skills_enabled": 1,
  "transaction_count": 2
}
```

### Marketplace Statistics

Get overall marketplace statistics.

**Endpoint**: `GET /api/v1/agent-stack/stats/marketplace`

**Response**:
```json
{
  "total_services": 5,
  "active_services": 5,
  "total_agents": 3,
  "total_nanopayments": 15,
  "confirmed_payments": 12,
  "total_volume_usdc": 25.50,
  "avg_service_price": 0.45,
  "avg_service_rating": 4.8
}
```

### Transaction History

Get transaction history.

**Endpoint**: `GET /api/v1/agent-stack/transactions/history?limit=50`

**Response**:
```json
[
  {
    "timestamp": "2024-01-15T10:45:30Z",
    "type": "nanopayment",
    "payment_id": "np_agent_456_agent_123_0",
    "from": "agent_456",
    "to": "agent_123",
    "amount": 0.50,
    "tx_hash": "0x1234567890abcdef..."
  },
  {
    "timestamp": "2024-01-15T10:35:00Z",
    "type": "funding",
    "agent_id": "agent_123",
    "amount": 50.0,
    "new_balance": 150.0
  }
]
```

## Service Categories

Available service categories:

- **PAYMENT_PROCESSING**: Payment and settlement services
- **DATA_RETRIEVAL**: Data fetching and aggregation
- **COMPUTATION**: Computational services
- **SETTLEMENT**: Settlement and reconciliation
- **VERIFICATION**: Verification and validation
- **ANALYTICS**: Analytics and reporting

## Nanopayment Status

Nanopayment lifecycle:

- **PENDING**: Created, awaiting confirmation
- **PROCESSING**: Being processed on-chain
- **CONFIRMED**: Successfully confirmed on-chain
- **FAILED**: Failed to confirm
- **DISPUTED**: Under dispute

## Error Handling

### Common Errors

| Status | Error | Solution |
|--------|-------|----------|
| 400 | Insufficient balance | Fund wallet with more USDC |
| 400 | Service not found | Use valid service_id |
| 400 | Invalid rating | Rating must be 1-5 |
| 404 | Wallet not found | Create wallet first |
| 404 | Agent not found | Register agent in system |
| 500 | Internal error | Check logs and retry |

### Error Response Format

```json
{
  "detail": "Insufficient balance. Have 10.0, need 50.0"
}
```

## Best Practices

### Wallet Management

1. **Always fund before transacting**: Ensure sufficient USDC balance
2. **Monitor balance**: Check balance before creating payments
3. **Track transactions**: Use transaction history for reconciliation
4. **Enable security**: Use wallet address verification

### Service Management

1. **Competitive pricing**: Research market rates
2. **Maintain uptime**: Keep service availability high
3. **Respond to ratings**: Address low ratings promptly
4. **Update descriptions**: Keep service info current

### Nanopayments

1. **Verify before paying**: Check service details and rating
2. **Include metadata**: Add request_id for tracking
3. **Confirm on-chain**: Always confirm payments
4. **Monitor status**: Check payment status regularly

## CLI Commands

### Create Wallet

```bash
curl -X POST http://localhost:8000/api/v1/agent-stack/wallets/create \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_123",
    "wallet_address": "0x...",
    "initial_balance": 100.0
  }'
```

### Discover Services

```bash
curl -X GET "http://localhost:8000/api/v1/agent-stack/marketplace/services?category=data_retrieval&min_rating=4.0"
```

### Create Nanopayment

```bash
curl -X POST http://localhost:8000/api/v1/agent-stack/nanopayments/create \
  -H "Content-Type: application/json" \
  -d '{
    "from_agent_id": "agent_456",
    "to_agent_id": "agent_123",
    "service_id": "svc_agent_123_0",
    "amount": 0.50
  }'
```

## Integration Examples

### Python SDK

```python
from orvion.agent_stack_full import get_agent_stack
from decimal import Decimal

async def example():
    stack = get_agent_stack()
    
    # Create wallet
    wallet = await stack.create_agent_wallet(
        "agent_123",
        "0x742d35Cc6634C0532925a3b844Bc9e7595f42bE",
        Decimal("100.0")
    )
    
    # Register service
    service = await stack.register_service(
        "agent_123",
        "Data Analysis",
        "Advanced analytics",
        SkillCategory.DATA_RETRIEVAL,
        Decimal("0.50")
    )
    
    # Create nanopayment
    payment = await stack.create_nanopayment(
        "agent_456",
        "agent_123",
        service.service_id,
        Decimal("0.50")
    )
```

### TypeScript SDK

```typescript
import { OrvionClient } from '@orvion/sdk';

const client = new OrvionClient({
  baseURL: 'http://localhost:8000',
});

// Create wallet
const wallet = await client.createWallet({
  agentId: 'agent_123',
  walletAddress: '0x...',
  initialBalance: 100.0,
});

// Discover services
const services = await client.discoverServices({
  category: 'data_retrieval',
  minRating: 4.0,
});

// Create nanopayment
const payment = await client.createNanopayment({
  fromAgentId: 'agent_456',
  toAgentId: 'agent_123',
  serviceId: services[0].serviceId,
  amount: 0.50,
});
```

## Health Check

**Endpoint**: `GET /api/v1/agent-stack/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Circle Agent Stack",
  "marketplace": {
    "total_services": 5,
    "active_services": 5,
    "total_agents": 3,
    "total_nanopayments": 15,
    "confirmed_payments": 12,
    "total_volume_usdc": 25.50,
    "avg_service_price": 0.45,
    "avg_service_rating": 4.8
  }
}
```

## Support

For issues or questions:

1. Check the error message and status code
2. Review this documentation
3. Check logs: `tail -f logs/server.log`
4. Create an issue on GitHub

## Related Documentation

- [CIRCLE_AGENT_STACK.md](./CIRCLE_AGENT_STACK.md) - Circle Agent Stack v1.10.0
- [API_REFERENCE.md](./api/API_REFERENCE.md) - Complete API reference
- [ARCHITECTURE.md](./architecture/ARCHITECTURE.md) - System architecture
