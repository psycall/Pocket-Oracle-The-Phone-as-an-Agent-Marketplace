#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env.local || true
npm install
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/sensor-orchestrator/requirements.txt
docker compose -f infra/docker/docker-compose.yml up -d

echo "Bootstrap concluído."
