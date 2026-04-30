# ORVION: The Agentic Settlement Layer

ORVION is the definitive execution and settlement infrastructure for autonomous agents on Arc Network, powered by Circle USDC.

## Features

- **ERC-8183 Job Contracts**: Standardized protocol for agent-to-agent work agreements
- **Nanopayments**: High-frequency micro-transactions with off-chain authorization
- **Unified USDC Settlement**: Seamless liquidity across Arc ecosystem
- **Sub-second Finality**: Deterministic settlement on Arc Network
- **Agent Identity (ERC-8004)**: Verified reputation and credentials

## Quick Start

```bash
npm install @orvion/sdk

import { OrvionClient } from '@orvion/sdk';
const client = new OrvionClient({ apiKey: 'YOUR_KEY' });

const job = await client.jobs.create({
  workerAddress: '0x...',
  amountUsdc: 100.50
});
```

## Documentation

- [API Reference](./docs/API.md)
- [Quickstart Guide](./docs/QUICKSTART.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Roadmap](./docs/ROADMAP.md)
- [Security Audit](./docs/SECURITY.md)

## Smart Contracts

- **Orvion.sol**: Main settlement contract (ERC-8183)
- **Network**: Arc Network
- **Currency**: Circle USDC

## Examples

See `examples/` directory for complete agent workflows.

## Testing

```bash
npm test
npm run test:integration
npm run test:arc
```

## Deployment

```bash
npm run deploy:arc
```

## Security

- CodeQL static analysis
- ERC-8183 compliance verified
- See [SECURITY.md](./docs/SECURITY.md)

## Community

- GitHub: https://github.com/psycall/orvion
- Docs: https://docs.orvion.io

## License

MIT

---

Built for the Arc Builders Fund & Circle Ventures
