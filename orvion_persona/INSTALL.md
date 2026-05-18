# 🜲 ORVION Persona — Installation Guide

> One-paste integration with your existing ORVION repo.
> Zero conflicts. Idempotent. Safe to re-run.

## Prerequisites

- You already cloned `github.com/psycall/ORVION-The-Agentic-Settlement-Layer`
- Python 3.11+, Node 20+, npm/pnpm
- (Optional) Hardhat configured for Arc Testnet

## Step 1 — Drop this pack into your repo

```bash
# from anywhere
unzip orvion_persona_pack.zip -d ~/Downloads/
cd ~/Downloads/orvion_persona

# 1. integrate the module (won't touch existing files)
python legal_body/scripts/integrate_with_orvion.py \
       --orvion-path /path/to/ORVION-The-Agentic-Settlement-Layer
```

The integrator:
1. **copies** `legal_body/` into your repo (skips any file that already exists)
2. **patches** `main.py` *only* if the router mount snippet isn't there
3. **appends** a README section *only* if the marker isn't there
4. never deletes, never overwrites

## Step 2 — Install dependencies

```bash
cd /path/to/ORVION-The-Agentic-Settlement-Layer

# Python
pip install pyyaml eth-utils web3   # already-present deps will be skipped

# Frontend (drop the two pages into your routes)
cp legal_body/frontend/src/pages/GiveAgentLegalBody.tsx frontend/src/pages/legal/
cp legal_body/frontend/src/pages/PersonaDashboard.tsx   frontend/src/pages/legal/
# register routes in your existing React Router config:
#   /legal/incorporate  -> GiveAgentLegalBody
#   /legal/dashboard    -> PersonaDashboard
```

## Step 3 — Smart contracts

```bash
# from repo root
npx hardhat compile
# deploy to Arc Testnet (uses your existing hardhat config)
npx hardhat run scripts/deploy_persona.js --network arc-testnet
```

(If you don't have a `scripts/deploy_persona.js`, create one that deploys
`JurisdictionRegistry` first, then `AgentPersona` passing the registry
address, then `OperatingAgreement`.)

## Step 4 — Run

```bash
python main.py
# → swagger: http://localhost:8000/docs   (look for "legal-body")
cd frontend && npm run dev
# → UI: http://localhost:5173/legal/incorporate
```

## Step 5 — Vitrine & Pitch deck

The `vitrine/` and `pitch_deck/` folders are **standalone** — they don't
need to live inside the repo. Host them separately (Vercel, Netlify) or
just open `vitrine/index.html` and `pitch_deck/index.html` locally.

```bash
# quick local serve
python -m http.server 4000 --directory vitrine
python -m http.server 4001 --directory pitch_deck
```

## Step 6 — Ship

```bash
cd /path/to/ORVION-The-Agentic-Settlement-Layer
bash legal_body/scripts/push_github.sh "feat(legal): ORVION Persona — Agent Incorporation Engine"
```

That opens a PR-ready branch named `feat/orvion-persona`. Merge when ready.

---

**Built for the moment Jeremy Allaire publicly asked for.**
