"""
Incorporation service — orchestrates:
  1. Template selection from `templates/{jurisdiction}/operating_agreement.yaml`
  2. Variable interpolation (legal_name, agent_wallet, sponsor, purpose…)
  3. Canonical hash (keccak256) of the rendered Operating Agreement
  4. (Optional) IPFS upload via web3.storage / Pinata
  5. On-chain incorporation via AgentPersona.sol
  6. Persistence in ORVION DB
"""
from __future__ import annotations
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml
except ImportError:  # graceful fallback for envs without pyyaml at import time
    yaml = None

from ..models.persona import (
    AgentPersona, PersonaStatus, JurisdictionEnum, PersonaSigner,
)
from ..schemas.persona import IncorporateRequest

TEMPLATE_ROOT = Path(__file__).resolve().parents[2] / "templates"

JURISDICTION_FOLDER = {
    JurisdictionEnum.WYOMING_DAO_LLC: "wyoming",
    JurisdictionEnum.DELAWARE_SERIES_LLC: "delaware",
    JurisdictionEnum.NEW_YORK_LLC: "new_york",
    JurisdictionEnum.MARSHALL_ISLANDS_DAO: "wyoming",  # fallback template
}


def _load_template(jurisdiction: JurisdictionEnum) -> Dict[str, Any]:
    folder = JURISDICTION_FOLDER[jurisdiction]
    path = TEMPLATE_ROOT / folder / "operating_agreement.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    if yaml is None:
        raise RuntimeError("pyyaml not installed — run `pip install pyyaml`")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_operating_agreement(req: IncorporateRequest) -> Dict[str, Any]:
    """Render the Operating Agreement with the request's parameters."""
    template = _load_template(req.jurisdiction)
    rendered = json.loads(json.dumps(template))  # deep copy

    rendered["entity"]["legal_name"] = req.legal_name
    rendered["entity"]["agent_wallet"] = req.agent_wallet
    rendered["entity"]["human_sponsor"] = req.human_sponsor or "0x0000000000000000000000000000000000000000"
    rendered["entity"]["purpose"] = req.purpose
    rendered["entity"]["initial_capital_usdc"] = req.initial_capital_usdc
    if req.registered_agent_uri:
        rendered["entity"]["registered_agent_uri"] = req.registered_agent_uri
    return rendered


def canonical_hash(rendered: Dict[str, Any]) -> str:
    """
    Canonical hash = keccak256 of the JSON-serialized agreement with
    sorted keys + no whitespace. Returns 0x-prefixed hex string.
    Falls back to sha3_256 (Keccak-like) when pysha3/eth-utils unavailable.
    """
    canonical = json.dumps(rendered, sort_keys=True, separators=(",", ":")).encode("utf-8")
    try:
        from eth_utils import keccak  # type: ignore
        return "0x" + keccak(canonical).hex()
    except ImportError:
        # SHA3-256 (FIPS 202) — close enough for off-chain commit; on-chain
        # path should always use eth_utils.keccak.
        return "0x" + hashlib.sha3_256(canonical).hexdigest()


def persist_persona(db, req: IncorporateRequest, oa_hash: str, oa_uri: Optional[str]) -> AgentPersona:
    persona = AgentPersona(
        agent_wallet=req.agent_wallet.lower(),
        human_sponsor=(req.human_sponsor or "").lower() or None,
        jurisdiction=req.jurisdiction,
        status=PersonaStatus.PENDING,
        legal_name=req.legal_name,
        operating_agreement_hash=oa_hash,
        operating_agreement_uri=oa_uri,
        registered_agent_uri=req.registered_agent_uri,
        extra={"purpose": req.purpose, "initial_capital_usdc": req.initial_capital_usdc},
    )
    db.add(persona)
    db.flush()
    if req.human_sponsor:
        db.add(PersonaSigner(persona_id=persona.id, signer_address=req.human_sponsor.lower(), role="sponsor"))
    db.add(PersonaSigner(persona_id=persona.id, signer_address=req.agent_wallet.lower(), role="agent"))
    db.commit()
    db.refresh(persona)
    return persona
