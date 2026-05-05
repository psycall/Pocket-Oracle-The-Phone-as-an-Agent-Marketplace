# ORVION - Vercel Deployment Guide

## Quick Deploy

### Option 1: Deploy Frontend to Vercel (Recommended)

```bash
# 1. Fork the repository
# 2. Connect to Vercel
# 3. Set root directory to: apps/web
# 4. Deploy
```

### Option 2: Deploy API to Vercel

```bash
# 1. Set root directory to: apps/api
# 2. Deploy
```

### Option 3: Deploy Full Monorepo

```bash
# 1. Use vercel.json configuration
# 2. Vercel will auto-detect and deploy
```

## Environment Variables

Add to Vercel project settings:

```
NEXT_PUBLIC_API_URL=https://orvion-api.vercel.app
CIRCLE_API_KEY=your_key
ARC_RPC_URL=https://rpc.testnet.arc.network
```

## Project Structure

```
orvion/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # Node.js API
├── orvion-node/      # Full Node.js backend
├── src/              # Java backend
├── contracts/        # Smart contracts
└── vercel.json       # Vercel configuration
```

## Troubleshooting

**Error: No build output found**
- Solution: Set root directory to `apps/web` in Vercel settings

**Error: Cannot find module**
- Solution: Run `npm install` in the correct directory

**Error: Port already in use**
- Solution: Vercel assigns ports automatically

---

**Deploy now:** https://vercel.com/new
