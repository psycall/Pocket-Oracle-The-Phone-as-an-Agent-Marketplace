# ORVION Deployment Guide

## Arc Testnet Setup

1. Add Arc Testnet to your wallet:
   - Network: Arc Testnet
   - RPC: https://testnet-rpc.arc.network
   - Chain ID: 2602

2. Get testnet USDC from faucet

## Deployment Steps

```bash
npm install
export PRIVATE_KEY=your_private_key
npx hardhat compile
npm run deploy:arc
```

## Contract Addresses

### Arc Testnet
- **ORVION:** [View on Explorer]
- **USDC:** 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
