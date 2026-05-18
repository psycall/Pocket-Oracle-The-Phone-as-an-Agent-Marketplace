# 🧬 ORVION Persona — Agent Incorporation Engine

> *"Give your agent a legal body."*
> A plug-in module for [ORVION — The Agentic Settlement Layer](https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer).

Spawns a zero-member-eligible LLC (Wyoming · Delaware · NY · Marshall Islands)
for any ORVION agent wallet, cryptographically bound to the agent's keys.
Built to plug directly into **Circle Agent Stack + Arc Network**.

---

## Why

In May 2026, Aaron Wright argued that AI agents need *legal bodies* to fully
participate in the economy ([thread](https://x.com/awrigh01/status/2055291605083463758)).
Jeremy Allaire (Circle) responded the next day: *"Calling @Arc Architects —
I would love to back a team building this."*

ORVION already provides the Settlement Layer. This module provides the
**Legal Body Layer** that sits on top.

## What's inside

```
legal_body/
├── contracts/                # Solidity (Arc / EVM)
│   ├── AgentPersona.sol
│   ├── OperatingAgreement.sol
│   └── JurisdictionRegistry.sol
├── backend/                  # FastAPI module
│   ├── api/v1/legal.py
│   ├── services/{incorporation,onchain}.py
│   ├── models/persona.py
│   └── schemas/persona.py
├── frontend/                 # React 19 + Tailwind v4 + Framer Motion
│   └── src/pages/{GiveAgentLegalBody,PersonaDashboard}.tsx
├── templates/                # Operating Agreement YAMLs
│   ├── wyoming/
│   ├── delaware/
│   └── new_york/
├── scripts/
│   ├── integrate_with_orvion.py   # ← idempotent plug-in installer
│   └── push_github.sh
└── docs/WHITEPAPER.md
```

## Install into ORVION (zero-conflict)

```bash
# from the root of ORVION-The-Agentic-Settlement-Layer
python legal_body/scripts/integrate_with_orvion.py --orvion-path .
python main.py
```

The script:
* never overwrites existing files (skip-on-conflict);
* only appends the FastAPI router mount when not already present;
* leaves your existing `main.py`, `frontend/`, and contracts untouched.

## API

| Method | Path | Description |
|--------|------|-------------|
| POST   | `/api/v1/legal/incorporate`         | Spawn a persona for an agent wallet |
| GET    | `/api/v1/legal/persona/{id}`        | Fetch a persona |
| GET    | `/api/v1/legal/persona/by-wallet/{addr}` | Lookup by wallet |
| GET    | `/api/v1/legal/personas`            | List with paging + filter |
| POST   | `/api/v1/legal/sign`                | Record / amend Operating Agreement |
| POST   | `/api/v1/legal/dissociate`          | Transition to zero-member (Bayern model) |

## Compatible with

* Circle Agent Stack
* Arc Network
* USDC / CCTP
* ERC-8183 (Agentic Commerce)

## License

MIT © Will S.S.
