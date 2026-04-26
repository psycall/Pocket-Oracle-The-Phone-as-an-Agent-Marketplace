"""
Orvion — API Tests
Run with: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import sys
import os

# Add app root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test env vars before importing app
os.environ.setdefault("SECRET_KEY", "test-secret-key-minimum-32-chars!!")
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")

from main import app

client = TestClient(app)


# ── Health ────────────────────────────────────────────────────

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "node" in data
    assert "timestamp" in data


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "node" in data
    assert data["status"] == "running"


# ── Auth ──────────────────────────────────────────────────────

def test_get_token_invalid_key():
    res = client.post("/node/token", json={"api_key": "wrong-key"})
    assert res.status_code == 401


def test_get_token_valid_key():
    res = client.post(
        "/node/token",
        json={"api_key": os.environ["SECRET_KEY"]},
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def get_test_token() -> str:
    res = client.post("/node/token", json={"api_key": os.environ["SECRET_KEY"]})
    return res.json()["access_token"]


# ── Marketplace ───────────────────────────────────────────────

def test_list_agents():
    res = client.get("/marketplace/agents")
    assert res.status_code == 200
    data = res.json()
    assert "agents" in data
    assert len(data["agents"]) > 0


def test_get_agent_not_found():
    res = client.get("/marketplace/agents/nonexistent")
    assert res.status_code == 404


def test_get_agent_crypto():
    res = client.get("/marketplace/agents/crypto")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "crypto"


# ── Node ──────────────────────────────────────────────────────

def test_node_status_requires_auth():
    res = client.get("/node/status")
    assert res.status_code == 403


def test_node_status_with_token():
    token = get_test_token()
    res = client.get("/node/status", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert "node_id" in data
    assert data["status"] == "running"


# ── Agent Execution (mocked LLM) ──────────────────────────────

@pytest.mark.asyncio
async def test_execute_requires_auth():
    res = client.post("/agent/execute", json={"goal": "test goal"})
    assert res.status_code == 403


@patch("agents.decision_agent.DecisionAgent.think", new_callable=AsyncMock)
@patch("agents.crypto_agent.CryptoAgent._fetch_trending", new_callable=AsyncMock)
@patch("agents.crypto_agent.CryptoAgent.think", new_callable=AsyncMock)
@patch("core.memory.AgentMemory.store_task", new_callable=AsyncMock)
@patch("core.memory.AgentMemory.increment_metric", new_callable=AsyncMock)
def test_execute_crypto_goal(
    mock_metric, mock_store, mock_crypto_think, mock_fetch, mock_router
):
    mock_router.return_value = '{"agent": "crypto", "confidence": 0.9, "reasoning": "crypto keyword", "refined_goal": "Analyze crypto"}'
    mock_fetch.return_value = [{"name": "Bitcoin", "symbol": "BTC", "rank": 1, "price_btc": 1.0, "score": 100}]
    mock_crypto_think.return_value = '{"sentiment": "bullish", "confidence": 0.85, "top_picks": [], "recommendation": "test", "risk_level": "MEDIUM", "summary": "test summary"}'
    mock_store.return_value = "test-id"
    mock_metric.return_value = None

    token = get_test_token()
    res = client.post(
        "/agent/execute",
        json={"goal": "Analyze crypto trends"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert "result" in data
    assert data["agent_used"] == "crypto"
