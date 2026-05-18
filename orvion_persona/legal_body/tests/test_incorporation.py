"""Smoke tests for the incorporation pipeline (no chain required)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from legal_body.backend.schemas.persona import IncorporateRequest
from legal_body.backend.models.persona import JurisdictionEnum
from legal_body.backend.services.incorporation import (
    render_operating_agreement, canonical_hash,
)


def _sample(j: JurisdictionEnum) -> IncorporateRequest:
    return IncorporateRequest(
        agent_wallet="0x" + "ab" * 20,
        legal_name="Orion Trading Agent LLC",
        jurisdiction=j,
        human_sponsor="0x" + "cd" * 20,
        registered_agent_uri="ipfs://test/registered-agent",
        purpose="Autonomous USDC trading & agent-to-agent commerce.",
        initial_capital_usdc=0.0,
    )


def test_render_wyoming():
    r = _sample(JurisdictionEnum.WYOMING_DAO_LLC)
    doc = render_operating_agreement(r)
    assert doc["entity"]["legal_name"] == "Orion Trading Agent LLC"
    assert doc["jurisdiction"]["code"] == "US-WY"
    assert doc["jurisdiction"]["supports_zero_member"] is True


def test_render_delaware():
    r = _sample(JurisdictionEnum.DELAWARE_SERIES_LLC)
    doc = render_operating_agreement(r)
    assert doc["jurisdiction"]["code"] == "US-DE"


def test_canonical_hash_deterministic():
    r = _sample(JurisdictionEnum.WYOMING_DAO_LLC)
    doc = render_operating_agreement(r)
    h1 = canonical_hash(doc)
    h2 = canonical_hash(doc)
    assert h1 == h2
    assert h1.startswith("0x") and len(h1) == 66


if __name__ == "__main__":
    test_render_wyoming()
    test_render_delaware()
    test_canonical_hash_deterministic()
    print("✅ All smoke tests passed")
