# Pocket Oracle

![Pocket Oracle Social Preview](public/brand/pocket-oracle-social-preview.png)

[**Versão em Português**](README.md) | **EN**

**Pocket Oracle** turns any smartphone into a **monetizable real-world oracle for AI agents**, combining human verification, contextual sensing, and usage-based billing in a repository designed to look credible to developers, partners, judges, and investors.

> The core thesis is simple: when an agent needs confirmation from the physical world, it should not wait for slow integrations, expensive manual operations, or fragile one-off workflows. It should pay cents, receive a verifiable answer, and keep executing.

## Executive overview

This repository was structured to look and operate like a **serious startup foundation**, not a loose prototype. The current base presents a product-oriented monorepo with a clear separation between monetization, mobile experience, field services, shared contracts, strategic documentation, visual branding, and governance controls.

| Layer | Directory | Strategic role |
| --- | --- | --- |
| Paid gateway | `apps/api-gateway` | Implements the commercial flow and `402 Payment Required` behavior |
| Mobile operations | `apps/mobile-pwa` | Carries the product into the smartphone, the center of the thesis |
| Operational intelligence | `apps/admin-dashboard` | Organizes demo metrics, state visibility, and executive monitoring |
| Field services | `services/sensor-orchestrator` | Delivers OCR, geoproof, and human verification with FastAPI |
| Contracts and SDK | `packages/*` | Reduces coupling and accelerates buyer-side integrations |
| Local infra | `infra/docker` | Supports queue, database, and repeatable environment evolution |
| Brand | `public/brand` | Centralizes visual identity for README, pitch, and product layers |
| Governance | `.github`, `SECURITY.md`, `CODEOWNERS` | Reinforces engineering discipline and public trust |

## What the product already offers

The current version already covers the functional skeleton required for a compelling demo with strong commercial logic and obvious product potential.

| Service | Endpoint | Suggested price | Expected outcome |
| --- | --- | ---: | --- |
| GeoProof | `POST /oracle/geoproof` | `0.0015` | Contextual location evidence |
| SnapOCR | `POST /oracle/snap-ocr` | `0.0040` | Short-form text extraction from the real world |
| HumanTap Verify | `POST /oracle/human-tap-verify` | `0.0060` | Fast, auditable human confirmation |

The gateway already demonstrates the central business mechanic: an unpaid first call returns **HTTP 402**, the buyer signs or sends the payment authorization, retries the request, and immediately receives the service result. That pattern makes the demo much stronger for usage-based billing, agentic commerce, and physical microservice marketplace narratives.

## Why this repository can impress serious audiences

The goal is not only to “run.” The goal is to make companies, judges, partners, and developers **understand the value quickly**, trust the execution, and see a credible path to scale.

| Dimension | What already exists | Why it matters |
| --- | --- | --- |
| Narrative | Executive README, roadmap, architecture, and checklist | Explains the product clearly to technical and business audiences |
| Security | Security policy, hardening guide, scanning, and secret hygiene | Reduces amateur signals and strengthens public credibility |
| Product | Monorepo with apps, services, SDK, and contracts | Shows long-term architectural thinking |
| Visual identity | Logo, icon, tokens, and premium-generated artwork | Improves first impression and memorability |
| Operations | Docker, scripts, and validated build base | Makes onboarding and iteration easier |
| Governance | Templates, review structure, and ownership | Moves the project closer to professional engineering standards |

## Monorepo structure

```text
.
├── apps/
│   ├── admin-dashboard/
│   ├── api-gateway/
│   └── mobile-pwa/
├── docs/
├── infra/
│   ├── docker/
│   └── scripts/
├── packages/
│   ├── agent-sdk/
│   └── shared-types/
├── public/
│   └── brand/
└── services/
    └── sensor-orchestrator/
```

## Quick start

The base was organized to support fast local iteration while keeping operational clarity.

```bash
cp .env.example .env.local
npm install
docker compose -f infra/docker/docker-compose.yml up -d
npm run dev:api
```

In another terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/sensor-orchestrator/requirements.txt
uvicorn app.main:app --app-dir services/sensor-orchestrator --host 0.0.0.0 --port 8100 --reload
```

To run the interfaces:

```bash
npm run dev:mobile
npm run dev:admin
```

## Core documentation

The documentation was designed both as operational material and as a credibility asset.

| Document | Purpose |
| --- | --- |
| [`SETUP.md`](SETUP.md) | Bilingual guide for installation, local execution, governance, and demo preparation |
| [`ROADMAP.md`](ROADMAP.md) | Executive roadmap covering present and future product phases |
| [`docs/architecture.md`](docs/architecture.md) | Explains the technical design of the product |
| [`docs/roadmap.md`](docs/roadmap.md) | Organizes evolution across business and engineering phases |
| [`docs/submission-checklist.md`](docs/submission-checklist.md) | Structures demo and submission readiness |
| [`docs/github-hardening.md`](docs/github-hardening.md) | Details GitHub security and governance controls |
| [`docs/release-readiness.md`](docs/release-readiness.md) | Summarizes the validated current state |
| [`docs/ultra-hardening-and-profile-plan.md`](docs/ultra-hardening-and-profile-plan.md) | Defines the next premium positioning layer |
| [`docs/founder-launch-playbook.md`](docs/founder-launch-playbook.md) | Provides the executive step-by-step guide for turning the project into a premium startup showcase |
| [`docs/brand-system.md`](docs/brand-system.md) | Documents the premium brand identity and official visual usage rules |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Defines professional collaboration and behavior standards |

## Security and operational hygiene

Any exposed secret must be treated as **immediately compromised**. The correct flow is revoke, regenerate, limit scope, and shorten expiration. GitHub recommends controls such as branch protection, required reviews, secret scanning, and secure build practices to strengthen public repositories and software supply chains [1] [2].

| Rule | Recommended standard |
| --- | --- |
| Exposed credentials | Revoke immediately |
| Main branch | Protected `main` |
| Sensitive changes | Mandatory review |
| Workflows | Least privilege permissions |
| Dependencies | Ongoing auditing and updates |

## Executive roadmap

The project already communicates present-day market potential, but it was also structured for credible staged expansion. A more visible executive version is available in [`ROADMAP.md`](ROADMAP.md).

| Phase | Objective | Outcome |
| --- | --- | --- |
| Phase 1 | Lock a functional demo | PWA, gateway, orchestrator, and dashboard working together |
| Phase 2 | Connect real settlement | Wallet integration, settlement, and auditable proof |
| Phase 3 | Become submission-grade | Deployment, public narrative, video, slides, and metrics |
| Phase 4 | Evolve into a real product | Multi-device marketplace, reputation, SLA, and routing |

## Product expansion opportunities

The same conceptual infrastructure can evolve into multiple markets where agents need trusted and fast physical-world signals.

| Vertical | Potential use |
| --- | --- |
| Retail compliance | Price, stock, execution, and audit checks |
| Delivery verification | Proof of delivery and contextual confirmation |
| Field operations | Inspection, presence, and operational validation |
| Agentic commerce | Physical microtasks for autonomous agents |
| Proof-of-presence | Fast evidence for hybrid workflows |

## Recommended Git rules

Git governance was organized to signal seriousness from the first repository impression.

| Topic | Standard |
| --- | --- |
| Main branch | `main` |
| Features | `feat/...` |
| Fixes | `fix/...` |
| Ops and docs | `chore/...`, `docs/...` |
| Commit style | `feat:`, `fix:`, `docs:`, `chore:` |
| Critical policy | Never commit `.env`, secrets, or credentials |

## References

[1]: https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository "GitHub Docs — Quickstart for securing your repository"
[2]: https://docs.github.com/en/code-security/tutorials/implement-supply-chain-best-practices/securing-builds "GitHub Docs — Securing builds"
