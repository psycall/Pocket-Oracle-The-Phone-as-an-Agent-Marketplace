<p align="center">
  <img src="public/brand/orvion_logo_4k.png" width="250" alt="Orvion 4K Logo">
</p>

<h1 align="center">🜂 Orvion — Investor-Ready Agent Commerce Layer</h1>

<p align="center">
  <strong>The complete monorepo for autonomous agent execution and commerce.</strong>
</p>

<p align="center">
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/actions"><img src="https://img.shields.io/github/actions/workflow/status/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/ci.yml?branch=main&style=flat-square" alt="Build Status"></a>
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/blob/main/LICENSE"><img src="https://img.shields.io/github/license/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/Version-2.1.0-blue.svg" alt="Version 2.1.0">
  <img src="https://img.shields.io/badge/Network-Arc_Network-blue.svg" alt="Arc Network">
</p>

---

## 🏗️ Monorepo Architecture

Orvion v2.1 is structured as a high-performance monorepo, providing all necessary surfaces for an agentic economy.

```
orvion/
├── apps/
│   ├── api/                ← FastAPI (Python, :8000) - Core Execution Engine
│   ├── api-gateway/        ← Express Gateway (TS, :8080) - Paid x402 Gateway
│   ├── web/                ← Investor Landing (Next.js, :3002)
│   ├── mobile-pwa/         ← Operator App (Next.js, :3000)
│   └── admin-dashboard/    ← Control Plane (Next.js, :3001)
├── packages/
│   └── sdk/                ← Official TypeScript SDK
├── contracts/
│   └── src/                ← Solidity (AgentRegistry + TaskEscrow)
├── services/
│   └── sensor-orchestrator/← Sensor Data Pipeline (:8100)
└── infra/
    └── docker/             ← Container Orchestration
```

---

## ⚡ Quick Start (60s)

```bash
# 1. Setup Environment
npm run setup

# 2. Install & Build
npm install
npm run build

# 3. Launch Services (Separate terminals recommended)
npm run dev:web          # Investor Landing (:3002)
npm run dev:mobile       # Operator PWA (:3000)
npm run dev:admin        # Admin Dashboard (:3001)
npm run dev:gateway      # x402 Gateway (:8080)
npm run dev:api          # Execution Engine (:8000)
npm run dev:orchestrator # Sensor Pipeline (:8100)
```

---

## 🧪 Testing

- **Python Core:** `npm run test:py` (13/13 passing in DEMO_MODE)
- **TypeScript/SDK:** `npm run test:js`

---

## 🗺️ Roadmap

<img src="public/brand/orvion_roadmap_4k.png" width="100%" alt="Orvion 4K Roadmap">

- [x] **v2.1 Investor-Ready:** Monorepo, 3 frontends, x402 gateway.
- [ ] **Multi-Agent Swarms:** Coordinated execution across nodes.
- [ ] **Mobile Native SDK:** Direct sensor integration for iOS/Android.
- [ ] **Global Liquidity:** Automated USDC settlement on Arc Mainnet.

---

<p align="center">
  <strong>Orvion © 2026</strong><br>
  <em>The execution layer for autonomous agents. Powered by Arc Network.</em>
</p>
