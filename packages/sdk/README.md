# ORVION SDK - TypeScript/JavaScript

Production-grade SDK for interacting with ORVION Settlement Layer.

## Features

- ✅ **Type-safe**: Full TypeScript support with comprehensive type definitions
- ✅ **Automatic Retry**: Exponential backoff (5s, 30s, 5m) on network failures
- ✅ **Logging**: Structured logging with configurable levels
- ✅ **Session Pooling**: Reuses HTTP connections for better performance
- ✅ **Timeout Control**: Configurable request timeouts (default 30s)
- ✅ **Error Handling**: Comprehensive error handling and propagation
- ✅ **Zero Dependencies**: Only requires `axios` for HTTP requests

## Installation

### npm

```bash
npm install @orvion/sdk
```

### yarn

```bash
yarn add @orvion/sdk
```

### pnpm

```bash
pnpm add @orvion/sdk
```

## Quick Start

```typescript
import { OrvionClient } from '@orvion/sdk';

// Initialize client
const client = new OrvionClient({
  baseUrl: 'https://api.orvion.io',
  apiToken: 'your-api-token',
  timeout: 30000,
  maxRetries: 3,
  logLevel: 'info'
});

// Register an agent
const agent = await client.registerAgent({
  agent_address: '0x1234567890123456789012345678901234567890',
  agent_name: 'MyAgent',
  agent_type: 'processor',
  capabilities: ['data_processing', 'validation'],
  pricing_per_call: 0.5
});

console.log('Agent registered:', agent.id);

// Create a job
const settlement = await client.createJobAndEscrow({
  agent_id: agent.id,
  job_id: 'job-123',
  amount: 100.50,
  to_address: '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd'
});

console.log('Job created:', settlement.id);

// Submit proof of work
const receipt = await client.submitProofOfWork({
  job_id: 'job-123',
  proof: 'QmProof...'
});

console.log('Proof submitted:', receipt.id);

// Check status
const status = await client.getStatus(settlement.id);
console.log('Settlement status:', status.status);

// Get agent reputation
const reputation = await client.getAgentReputation(agent.id);
console.log('Agent reputation:', reputation.score);

// Submit feedback
const feedback = await client.submitFeedback(
  agent.id,
  5,
  'Excellent work!',
  settlement.id
);

console.log('Feedback submitted:', feedback.id);

// Get top agents
const topAgents = await client.getTopAgents('processor', 4.0, 10);
console.log('Top agents:', topAgents);

// Cleanup
client.close();
```

## Configuration

```typescript
interface OrvionClientConfig {
  baseUrl?: string;        // Default: 'http://localhost:8000'
  apiToken?: string;       // Optional API token for authentication
  timeout?: number;        // Default: 30000 (30 seconds)
  maxRetries?: number;     // Default: 3
  logLevel?: 'debug' | 'info' | 'warn' | 'error'; // Default: 'info'
}
```

## API Methods

### Core Methods

#### `registerAgent(agentData: AgentData): Promise<AgentResponse>`

Register an agent in the ORVION Discovery Registry.

```typescript
const agent = await client.registerAgent({
  agent_address: '0x...',
  agent_name: 'MyAgent',
  agent_type: 'processor',
  capabilities: ['processing'],
  pricing_per_call: 0.5
});
```

#### `createJobAndEscrow(jobData: JobData): Promise<SettlementResponse>`

Create a job and escrow funds in USDC.

```typescript
const settlement = await client.createJobAndEscrow({
  agent_id: 'agent-123',
  job_id: 'job-456',
  amount: 100.50,
  to_address: '0xabcd...'
});
```

#### `submitProofOfWork(proofData: ProofData): Promise<SettlementResponse>`

Submit execution receipt to trigger verification and payment release.

```typescript
const receipt = await client.submitProofOfWork({
  job_id: 'job-456',
  proof: 'QmProof...'
});
```

#### `getStatus(settlementId: string): Promise<SettlementResponse>`

Check the status of a settlement.

```typescript
const status = await client.getStatus('settlement-789');
```

### Reputation & Feedback

#### `getAgentReputation(agentId: string, days?: number): Promise<ReputationResponse>`

Get reputation score for an agent.

```typescript
const reputation = await client.getAgentReputation('agent-123', 30);
```

#### `submitFeedback(agentId: string, score: number, comment?: string, settlementId?: string): Promise<FeedbackResponse>`

Submit feedback about an agent (score: 0-5).

```typescript
const feedback = await client.submitFeedback(
  'agent-123',
  5,
  'Excellent work!',
  'settlement-789'
);
```

#### `getTopAgents(agentType?: string, minReputation?: number, limit?: number): Promise<AgentResponse[]>`

Get top-rated agents.

```typescript
const topAgents = await client.getTopAgents('processor', 4.0, 10);
```

#### `getAgents(limit?: number, offset?: number): Promise<AgentResponse[]>`

Get all agents with pagination.

```typescript
const agents = await client.getAgents(10, 0);
```

## Error Handling

The SDK automatically retries failed requests with exponential backoff:

```typescript
try {
  const agent = await client.registerAgent(agentData);
} catch (error) {
  console.error('Failed to register agent:', error.message);
  // Error already retried 3 times with backoff
}
```

## Logging

Configure logging level for debugging:

```typescript
const client = new OrvionClient({
  logLevel: 'debug'  // 'debug' | 'info' | 'warn' | 'error'
});

// Output:
// [DEBUG] Checking status for settlement: settlement-789
// [INFO] Registering agent: MyAgent
// [WARN] Attempt 1 failed, retrying in 5s
// [ERROR] Failed after 3 attempts
```

## TypeScript Support

Full TypeScript support with comprehensive type definitions:

```typescript
import {
  OrvionClient,
  AgentData,
  JobData,
  SettlementResponse,
  ReputationResponse,
  FeedbackResponse
} from '@orvion/sdk';

const client = new OrvionClient();
const settlement: SettlementResponse = await client.getStatus('id');
```

## Examples

See `examples/` directory for complete working examples:

- `agent-workflow.ts` - Complete agent lifecycle
- `client-workflow.ts` - Client job submission
- `reputation-system.ts` - Reputation and feedback

## Testing

```bash
npm test
npm run test:watch
```

## Building

```bash
npm run build
```

Outputs:
- `dist/index.js` - CommonJS build
- `dist/index.esm.js` - ES Module build
- `dist/index.d.ts` - TypeScript definitions

## Performance

- **Connection pooling**: Reuses HTTP connections
- **Automatic retry**: Exponential backoff prevents cascading failures
- **Configurable timeout**: Prevent hanging requests
- **Session reuse**: Better performance under load

## Security

- ✅ HTTPS support
- ✅ Bearer token authentication
- ✅ No credentials in logs
- ✅ Timeout protection against slowloris attacks

## Compatibility

- Node.js: >=14.0.0
- Browsers: Modern browsers with ES2020 support
- TypeScript: >=4.5.0

## License

MIT

## Support

- 📖 [Documentation](https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer)
- 🐛 [Report Issues](https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer/issues)
- 💬 [Discussions](https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer/discussions)

## Contributing

Contributions welcome! Please read our [Contributing Guide](../../CONTRIBUTING.md).

---

**Version**: 2.0.0  
**Last Updated**: May 10, 2026
