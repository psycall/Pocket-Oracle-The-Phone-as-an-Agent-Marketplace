<p align="center">
  <img src="public/brand/logo.png" width="200" alt="Pocket Oracle Logo">
</p>

<h1 align="center">Pocket Oracle</h1>

<p align="center">
  <strong>The Phone as an Agent Marketplace</strong><br>
  <em>Transforming smartphones into monetizable real-world oracles for AI agents.</em>
</p>

<p align="center">
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/actions"><img src="https://img.shields.io/github/actions/workflow/status/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/ci.yml?branch=main&style=flat-square" alt="Build Status"></a>
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/blob/main/LICENSE"><img src="https://img.shields.io/github/license/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace?style=flat-square" alt="License"></a>
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/stargazers"><img src="https://img.shields.io/github/stars/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/network/members"><img src="https://img.shields.io/github/forks/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/issues"><img src="https://img.shields.io/github/issues/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace?style=flat-square" alt="Issues"></a>
</p>

<p align="center">
  <a href="README.md">Portuguese Version</a> •
  <a href="#-executive-vision">Executive Vision</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-current-features">Features</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-security">Security</a>
</p>

<img src="public/brand/banner.png" width="100%" alt="Pocket Oracle Banner">

---

## 👁️ Executive Vision

**Pocket Oracle** addresses the trust bottleneck between the digital and physical worlds. When an AI agent requires real-world confirmation, it should not be reliant on slow, manual processes. Instead, it should be able to **pay cents, receive a verifiable response, and continue its execution in real-time**.

Our thesis is to transform every smartphone into a node within a decentralized oracle network, where human verification and contextual signals become monetizable assets. We are not just another application; we are building an execution infrastructure for the agent-based economy.

---

## 🏗️ Architecture

The project is structured as an industrial-grade monorepo, ensuring scalability, security, and a clear separation of concerns.

<img src="public/brand/architecture.png" width="100%" alt="Pocket Oracle Architecture">

| Layer | Strategic Role |
| :--- | :--- |
| **Paid Gateway** | Implements the commercial flow and `402 Payment Required` behavior, acting as the primary monetization barrier. |
| **Mobile Operation** | Progressive Web App (PWA) that transforms the smartphone into the central hub for data collection and human interaction. |
| **Sensor Orchestrator** | FastAPI-based intelligence responsible for processing OCR, validating GeoProof, and managing human confirmation. |
| **Admin Dashboard** | Executive view of metrics, demonstration status, and system governance. |
| **Infrastructure** | Dockerized environment (PostgreSQL, Redis) for predictable, secure, and scalable evolution. |

---

## 🚀 Current Features

The current version delivers the functional skeleton for a high-impact demonstration with a strong economic narrative.

| Service | Description | Suggested Price (USDC) |
| :--- | :--- | :--- |
| **GeoProof** | Verifiable contextual location evidence. | `0.0015` |
| **SnapOCR** | Text extraction from physical environments via camera. | `0.0040` |
| **HumanTap** | Fast, auditable, and secure human confirmation. | `0.0060` |

---

## 🗺️ Strategic Roadmap

We are building more than a prototype; we are defining a new market for physical microservices for agents.

<img src="public/brand/roadmap_visual.png" width="100%" alt="Pocket Oracle Roadmap">

### Phase 1: Functional Demo (Current)
- [x] Operational Mobile PWA.
- [x] Gateway with `402 Payment Required` support.
- [x] Basic sensor orchestrator.

### Phase 2: Real Settlement
- [ ] Wallet and micropayment integration.
- [ ] On-chain auditable proofs.
- [ ] Initial reputation system.

### Phase 3: Submission Grade
- [ ] Large-scale deployment.
- [ ] Ultra-deep technical documentation.
- [ ] Pitch video and marketing materials.

### Phase 4: Real Product
- [ ] Multi-device marketplace.
- [ ] SLAs guaranteed by staking.
- [ ] Intelligent task routing.

For more details, consult our [Full Roadmap](ROADMAP.md).

---

## 🛡️ Security and Governance

As a CEO-level project, security is not optional. We adhere to best practices for operational hygiene:

- **Secret Hygiene:** We never commit `.env` files or credentials.
- **Branch Protection:** The `main` branch is protected and requires review (Pull Requests).
- **Scanning:** Continuous monitoring for vulnerabilities in dependencies.

To report vulnerabilities, please refer to our [Security Policy](SECURITY.md).

---

## 🛠️ Quick Start

To run Pocket Oracle locally, follow the steps below. For a detailed guide, please consult [SETUP.md](SETUP.md).

```bash
# 1. Clone the repository
git clone https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace.git
cd Pocket-Oracle-The-Phone-as-an-Agent-Marketplace

# 2. Configure environment variables
cp .env.example .env.local

# 3. Bring up infrastructure (PostgreSQL, Redis)
docker compose -f infra/docker/docker-compose.yml up -d

# 4. Install dependencies and start services
npm install
npm run dev:api
```

---

## 🤝 Contributing

We welcome contributions from the community! If you wish to help build the future of AI agent oracles, please read our [Contribution Guide](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md).

---

<p align="center">
  Developed with a focus on technical excellence and market vision.<br>
  <strong>Pocket Oracle © 2026</strong>
</p>
