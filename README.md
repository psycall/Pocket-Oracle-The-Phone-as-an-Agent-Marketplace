# 🧠 Pocket Oracle

> **Phone as an Agent Marketplace** — a decentralized network that turns smartphones into autonomous agents executing real-world tasks and earning USDC.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Node](https://img.shields.io/badge/node-%3E%3D18-brightgreen)
![Solidity](https://img.shields.io/badge/solidity-0.8.20-363636)
![Stack](https://img.shields.io/badge/stack-Express%20%7C%20Ethers%20v6%20%7C%20Circle-blueviolet)

---

## 🚀 Problem
Accessing real-world data and execution is expensive, centralized, and slow.

## 💡 Solution
A trustless marketplace where:
- Users create paid tasks
- Mobile devices act as agents
- Payments settle in USDC via **Circle**
- A **Solidity escrow** contract guarantees fairness

---

## ⚙️ Stack
- **Backend:** Node.js + Express
- **Blockchain:** Solidity 0.8.20, Hardhat, Ethers v6
- **Payments:** Circle USDC API (sandbox)
- **Networks:** Sepolia / Arbitrum Sepolia (Arc-ready)

---

## 🔄 Flow

```
 ┌──────────┐   USDC    ┌─────────┐   webhook   ┌─────────┐   tx     ┌──────────────┐
 │  User    │ ────────► │ Circle  │ ──────────► │ Backend │ ───────► │ PocketOracle │
 │          │           │  API    │             │ Express │          │  Contract    │
 └──────────┘           └─────────┘             └─────────┘          └──────────────┘
                                                                            │
                                                                       releasePayment
                                                                            ▼
                                                                       ┌─────────┐
                                                                       │ Agent   │
                                                                       │ (phone) │
                                                                       └─────────┘
```

1. User pays in USDC (Circle)
2. Circle webhook → backend creates an on-chain task
3. Mobile agent executes the task
4. Smart contract releases the escrowed payment

---

## 📦 Setup

```bash
git clone https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace.git
cd Pocket-Oracle-The-Phone-as-an-Agent-Marketplace
npm install
cp .env.example .env   # fill in your keys
npm run compile
npm run deploy:sepolia # deploy escrow
npm start              # start backend
```

---

## 🔌 API Endpoints

| Method | Path             | Description                    |
| ------ | ---------------- | ------------------------------ |
| GET    | `/`              | Health check                   |
| POST   | `/create-wallet` | Create a Circle wallet         |
| POST   | `/transfer`      | Transfer USDC between wallets  |
| POST   | `/webhook`       | Circle event receiver (HMAC)   |
| POST   | `/complete-task` | Release on-chain payment       |
| GET    | `/tasks`         | List all on-chain tasks        |

---

## 🔐 Security Notes
- **Never commit `.env`.** Use `.env.example` as the template.
- **Never share private keys or API tokens** in code, chat, screenshots, or commits.
- If a token is ever exposed, **revoke it immediately** at https://github.com/settings/tokens
- The webhook validates the `X-Circle-Signature` header (HMAC-SHA256) when `CIRCLE_WEBHOOK_SECRET` is set.

---

## 🗺️ Roadmap
- [ ] Mobile agent SDK (Android / iOS)
- [ ] Reputation & staking layer
- [ ] Arc Network deployment
- [ ] Multi-asset escrow (USDC, EURC, native)

---

## 📄 License
MIT © psycall
