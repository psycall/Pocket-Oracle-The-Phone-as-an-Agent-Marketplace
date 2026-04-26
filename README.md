<p align="center">
  <img src="public/brand/orvion_logo.png" width="200" alt="Orvion Logo">
</p>

<h1 align="center">🧠 Orvion — Execution Layer for Autonomous Agents</h1>

<p align="center">
  <strong>Give a goal. Orvion executes. Real AI. Real results.</strong>
</p>

<p align="center">
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/actions"><img src="https://img.shields.io/github/actions/workflow/status/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/ci.yml?branch=main&style=flat-square" alt="Build Status"></a>
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/blob/main/LICENSE"><img src="https://img.shields.io/github/license/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12">
  <img src="https://img.shields.io/badge/TypeScript-5.5-blue.svg" alt="TypeScript 5.5">
</p>

<p align="center">
  <a href="#-what-is-orvion">What is Orvion?</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="README.pt-br.md">Versão em Português</a>
</p>

<img src="public/brand/orvion_banner.png" width="100%" alt="Orvion Banner">

---

## 👁️ What is Orvion?

**Orvion** is the infrastructure layer for autonomous agents. While other AI tools focus on conversation, Orvion focuses on **execution**. You send a natural language goal. Orvion routes it to the right specialized agent, executes it using real AI reasoning, and returns a structured result — all in one API call.

```json
POST /agent/execute
{ "goal": "Analyze crypto trends and find the best opportunity" }

→ Routes to CryptoAgent
→ Fetches live market data
→ AI analyzes and decides
→ Returns structured JSON decision
```

**No if/else. No hardcoded rules. Real AI execution.**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Orvion Node                        │
│                                                     │
│  Goal → DecisionAgent (AI) → Route                  │
│                ↓                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Crypto  │  │ Research │  │   Code   │  + more  │
│  │  Agent   │  │  Agent   │  │  Agent   │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│                ↓                                    │
│  Redis (Persistent Memory) → Response               │
└─────────────────────────────────────────────────────┘
```

- **Execution Engine** — routes goals to specialized agents.
- **Agent Marketplace** — discover and register new agents.
- **Real-time Streaming** — SSE for live execution updates.
- **Persistent Memory** — Redis-backed task history.
- **JWT Security** — professional-grade authentication.

---

## 🗺️ Roadmap

<img src="public/brand/orvion_roadmap.png" width="100%" alt="Orvion Roadmap">

- [x] **Real-Time Execution:** Instant, intelligent, and reliable.
- [ ] **Autonomous Orchestration:** Intelligent agent planning and routing.
- [ ] **Enterprise Integration:** Built to scale and fit your systems.
- [ ] **Global Execution Network:** Leverage a distributed network of agents.

---

## 🛠️ Getting Started

### 1-Minute Setup

```bash
# Clone
git clone https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace.git
cd Orvion

# Configure
npm run setup
# Edit .env and add your API_KEY and SECRET_KEY

# Run (Docker — full stack)
npm run dev
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive API.
Open [http://localhost:3000](http://localhost:3000) for the execution dashboard.

---

<p align="center">
  <strong>Orvion © 2026</strong><br>
  <em>The execution layer for autonomous agents.</em>
</p>
