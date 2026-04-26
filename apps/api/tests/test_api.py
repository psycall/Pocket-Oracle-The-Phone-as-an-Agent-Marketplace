"""
Orvion — API Tests
Run with: pytest tests/ -v
"""

import os
import sys

# Add app root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test env vars before importing app
os.environ.setdefault("SECRET_KEY", "test-secret-key-minimum-32-chars!!")
os.environ.setdefault("DEMO_MODE", "true")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

client = TestClient(app)


# ── Health ────────────────────────────────────────────────────


def test_health() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "node" in data and "timestamp" in data


def test_root() -> None:
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "node" in data
    assert data["status"] == "running"


# ── Auth ──────────────────────────────────────────────────────


def test_get_token_invalid_key() -> None:
    res = client.post("/node/token", json={"api_key": "wrong-key"})
    assert res.status_code == 401


def test_get_token_valid_key() -> None:
    res = client.post("/node/token", json={"api_key": os.environ["SECRET_KEY"]})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def get_test_token() -> str:
    res = client.post("/node/token", json={"api_key": os.environ["SECRET_KEY"]})
    return res.json()["access_token"]


# ── Marketplace ───────────────────────────────────────────────


def test_list_agents() -> None:
    res = client.get("/marketplace/agents")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 5


def test_get_agent_not_found() -> None:
    res = client.get("/marketplace/agents/nonexistent")
    assert res.status_code == 404


def test_get_agent_crypto() -> None:
    res = client.get("/marketplace/agents/crypto")
    assert res.status_code == 200
    assert res.json()["name"] == "crypto"


def test_pricing_catalog() -> None:
    res = client.get("/marketplace/pricing")
    assert res.status_code == 200
    data = res.json()
    assert data["currency"] == "USDC"
    assert len(data["services"]) >= 3


# ── Node ──────────────────────────────────────────────────────


def test_node_status_requires_auth() -> None:
    res = client.get("/node/status")
    assert res.status_code == 403


def test_node_status_with_token() -> None:
    token = get_test_token()
    res = client.get("/node/status", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert "node_id" in data
    assert data["status"] == "running"


# ── Agent Execution (demo mode, no external deps) ─────────────


def test_execute_requires_auth() -> None:
    res = client.post("/agent/execute", json={"goal": "test goal"})
    assert res.status_code == 403


def test_execute_geoproof_demo_mode() -> None:
    token = get_test_token()
    res = client.post(
        "/agent/execute",
        json={
            "goal": "Run a geoproof for delivery in Lisbon",
            "context": {"latitude": 38.7223, "longitude": -9.1393, "accuracy": 12.0},
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert "result" in data
    assert data["status"] == "complete"


def test_execute_snap_ocr_demo_mode() -> None:
    token = get_test_token()
    res = client.post(
        "/agent/execute",
        json={
            "goal": "Read this delivery receipt with snap ocr",
            "context": {"imageUrl": "https://example.com/receipt.png"},
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["agent_used"] in {"snap_ocr", "research", "general"}
