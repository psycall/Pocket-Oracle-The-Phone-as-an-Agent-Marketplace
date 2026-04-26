<p align="center">
  <img src="public/brand/orvion_logo_4k.png" width="220" alt="Orvion logo">
</p>

<h1 align="center">Orvion · Pocket Oracle</h1>

<p align="center">
  <strong>The phone as an agent marketplace.</strong><br/>
  An investor-ready monorepo: landing page, mobile operator PWA, admin
  dashboard, paid API gateway, FastAPI execution layer and TypeScript SDK.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-investor--ready-7af3cf" alt="status">
  <img src="https://img.shields.io/badge/stack-monorepo-56b7ff" alt="stack">
  <img src="https://img.shields.io/badge/payments-mock%20%E2%86%92%20x402-FF5733" alt="payments">
  <img src="https://img.shields.io/badge/license-MIT-9db4c8" alt="license">
</p>

---

## What is in this repo

| Surface | Path | Port (dev) | Purpose |
| --- | --- | --- | --- |
| Investor landing | `apps/web` | 3002 | Premium narrative, economics, roadmap |
| Mobile operator PWA | `apps/mobile-pwa` | 3000 | Phone-native job queue and escalation |
| Admin dashboard | `apps/admin-dashboard` | 3001 | Executive metrics and readiness checklist |
| Paid API gateway | `apps/api-gateway` | 8080 | 402-style paid endpoints with mock auth |
| Execution layer (FastAPI) | `apps/api` | 8000 | JWT-auth, agents, marketplace, history |
| Sensor orchestrator | `services/sensor-orchestrator` | 8100 | Deterministic GeoProof / OCR / HumanTap |
| TypeScript SDK | `packages/sdk` | – | Official client (`@orvion/sdk`) |

Everything is designed to keep working in **DEMO MODE** — Redis, Anthropic and
 the orchestrator are all optional thanks to graceful in-process fallbacks.

---

## Quick start (60 seconds)

```bash
# 1. Setup
cp .env.example .env
npm install

# 2. Build everything
npm run build

# 3. Start the surfaces (each in its own terminal)
npm run dev:api          # FastAPI on :8000
npm run dev:gateway      # Paid gateway on :8080
npm run dev:web          # Investor landing on :3002
npm run dev:mobile       # Mobile PWA on :3000
npm run dev:admin        # Admin dashboard on :3001
npm run dev:orchestrator # (optional) sensors on :8100

# 4. Tests
npm run test:py          # pytest for the FastAPI layer
npm run test:js          # vitest for the SDK
```

Optional infrastructure (Redis + Postgres + sensor orchestrator container):

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

---

## Why this is investable

| Market friction | Legacy workaround | Orvion answer |
| --- | --- | --- |
| Agents struggle to pay for tiny tasks | Cards / invoices / human billing loops | HTTP-native paid calls, sub-cent pricing |
| Automation fails at the messy edge of reality | Manual back-office interventions | Phone-native operators step in only when needed |
| Buyers need proof, not black-box promises | Loose logs, vendor trust | Execution records, routing trace, verification metadata |

---

## Paid Oracle services (demo pricing)

| Service | Price | Latency | Outcome |
| --- | --- | --- | --- |
| GeoProof | $0.0015 | < 2s | Signed-style location attestation with confidence |
| SnapOCR | $0.0040 | < 3s | Structured text extraction from receipts/labels |
| HumanTap Verify | $0.0060 | < 20s | Human approve/reject decision with operator trace |

---

## Architecture (simplified)

```
                     ┌──────────────┐
 Operator phone ───► │ Mobile PWA   │ ── job queue, escalation
                     └─────┬────────┘
                           │
                     ┌─────▼────────┐    402 challenge → retry with auth
 Investor / buyer ─► │ Web landing  │◄── shows economics & roadmap
                     └─────┬────────┘
                           │
                     ┌─────▼────────┐    pricing, catalog, stats
                     │ API Gateway  │────────────────────────────┐
                     │  (Express)   │                            │
                     └─────┬────────┘                            ▼
                           │                            ┌────────────────────┐
                           ▼                            │ Sensor Orchestrator│
                     ┌──────────────┐                   │     (FastAPI)      │
                     │  Exec API    │ JWT, agents,      └────────────────────┘
                     │ (FastAPI)    │ history, registry
                     └──────────────┘
```

---

## Roadmap

1. **Now** — polished demo stack (this repo).
2. **Next** — replace mock authorisation with real Circle / x402 settlement.
3. **Then** — open marketplace: external agent registration, partner distribution, usage-based billing across operator networks.

---

<p align="center">
  <strong>Orvion · Pocket Oracle © 2026</strong><br/>
  <em>The phone as an agent marketplace.</em>
</p>
