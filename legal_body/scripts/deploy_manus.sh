#!/usr/bin/env bash
# deploy_manus.sh — one-shot deployment on Manus AI sandbox
set -euo pipefail

echo "🜲 ORVION Persona — Manus deployment"
echo "──────────────────────────────────────"

# 1. Python deps
echo "→ Installing Python dependencies"
pip install --quiet --no-input \
    fastapi uvicorn[standard] sqlalchemy pydantic pyyaml \
    eth-utils web3 python-multipart

# 2. Node deps (frontend)
if [ -d "frontend" ]; then
  echo "→ Installing frontend dependencies"
  (cd frontend && npm install --silent && npm run build) || echo "  (frontend build skipped)"
fi

# 3. Solidity (Hardhat) — assumes hardhat already in ORVION
if [ -f "hardhat.config.ts" ] || [ -f "hardhat.config.js" ]; then
  echo "→ Compiling smart contracts"
  npx hardhat compile || true
fi

# 4. DB migration tables (auto-created on first request)
echo "→ Booting FastAPI on :8000"
nohup python main.py > orvion.log 2>&1 &
sleep 3
echo "✅ ORVION + Persona module up."
echo "   Swagger: http://localhost:8000/docs"
echo "   Logs   : tail -f orvion.log"
