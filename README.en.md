<p align="center">
  <img src="public/brand/logo.png" width="200" alt="Pocket Oracle Logo">
</p>

<h1 align="center">Pocket Oracle</h1>

<p align="center">
  <strong>The Phone as an Agent Marketplace</strong><br>
  <em>Transforming smartphones into monetizable real-world oracles for AI agents.</em>
</p>

<p align="center">
  <a href="#-executive-vision">Executive Vision</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-current-features">Features</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-security">Security</a> •
  <a href="README.md">Portuguese Version</a>
</p>

<img src="public/brand/banner.png" width="100%" alt="Pocket Oracle Banner">

---

## 👁️ Executive Vision

**Pocket Oracle** solves the trust bottleneck between the digital and physical worlds. When an AI agent needs real-world confirmation, it shouldn't rely on slow manual processes. It should be able to **pay cents, receive a verifiable response, and continue its execution in real-time**.

Our thesis is to transform every smartphone into a node of a decentralized oracle network, where human verification and contextual signals are monetizable assets.

---

## 🏗️ Architecture

The project is structured as an industrial-grade monorepo, ensuring scalability and clear separation of concerns.

<img src="public/brand/architecture.png" width="100%" alt="Pocket Oracle Architecture">

| Layer | Strategic Role |
| :--- | :--- |
| **Paid Gateway** | Implements the commercial flow and `402 Payment Required` behavior. |
| **Mobile Operation** | PWA that turns the smartphone into the data collection hub. |
| **Sensor Orchestrator** | FastAPI intelligence for OCR, Geoproof, and human validation. |
| **Admin Dashboard** | Executive view of metrics, demo state, and governance. |
| **Infrastructure** | Dockerized environment for predictable and secure evolution. |

---

## 🚀 Current Features

The current version delivers the functional skeleton for a high-impact demonstration with a strong economic narrative.

| Service | Description | Suggested Price |
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

---

## 🛡️ Security and Governance

As a CEO-level project, security is not optional. We follow operational hygiene best practices:

- **Secret Hygiene:** We never commit `.env` files or credentials.
- **Branch Protection:** The `main` branch is protected and requires review.
- **Scanning:** Continuous monitoring of vulnerabilities in dependencies.

---

## 🛠️ Quick Start

```bash
# Clone and setup
git clone https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace.git
cd Pocket-Oracle-The-Phone-as-an-Agent-Marketplace

# Start infrastructure
docker compose -f infra/docker/docker-compose.yml up -d

# Start services
npm install
npm run dev:api
```

---

<p align="center">
  Developed with a focus on technical excellence and market vision.<br>
  <strong>Pocket Oracle © 2026</strong>
</p>
