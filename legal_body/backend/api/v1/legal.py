"""
FastAPI router for the Legal Body module.

Mount in ORVION's main.py:

    from legal_body.backend.api.v1.legal import router as legal_router
    app.include_router(legal_router, prefix="/api/v1/legal", tags=["legal-body"])
"""
from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from ...models.persona import AgentPersona, PersonaStatus
from ...schemas.persona import (
    IncorporateRequest, PersonaResponse, PersonaListResponse,
    SignAgreementRequest, DissociateRequest,
)
from ...services.incorporation import (
    render_operating_agreement, canonical_hash, persist_persona,
)
from ...services.onchain import OnChainClient

router = APIRouter()

# ── DB dependency ────────────────────────────────────────────────────────
# Replace this with ORVION's existing `get_db` dependency from main.py.
try:
    from main import get_db  # type: ignore
except Exception:
    def get_db():  # pragma: no cover - placeholder for standalone import
        raise RuntimeError("Bind to ORVION's get_db dependency.")

onchain = OnChainClient()


@router.post("/incorporate", response_model=PersonaResponse, summary="Incorporate a Legal Persona for an Agent Wallet")
def incorporate(req: IncorporateRequest, db: Session = Depends(get_db)):
    # 1. Render Operating Agreement from template
    rendered = render_operating_agreement(req)

    # 2. Compute canonical hash
    oa_hash = canonical_hash(rendered)

    # 3. (Optional) Pin to IPFS — left as TODO for production
    oa_uri = f"orvion://oa/{oa_hash[2:18]}"

    # 4. Persist DB row (PENDING)
    persona = persist_persona(db, req, oa_hash, oa_uri)

    # 5. Push to chain (or dry-run)
    tx = onchain.incorporate(
        agent_wallet=req.agent_wallet,
        jurisdiction=req.jurisdiction.value,
        legal_name=req.legal_name,
        oa_hash=oa_hash,
        registered_agent_uri=req.registered_agent_uri or "",
    )

    # 6. Update status to INCORPORATED
    persona.status = PersonaStatus.INCORPORATED
    persona.on_chain_id = tx.get("persona_id")
    db.commit()
    db.refresh(persona)
    return persona


@router.get("/persona/{persona_id}", response_model=PersonaResponse)
def get_persona(persona_id: int, db: Session = Depends(get_db)):
    p = db.query(AgentPersona).filter(AgentPersona.id == persona_id).first()
    if not p:
        raise HTTPException(404, "Persona not found")
    return p


@router.get("/persona/by-wallet/{wallet}", response_model=PersonaResponse)
def get_by_wallet(wallet: str, db: Session = Depends(get_db)):
    p = db.query(AgentPersona).filter(AgentPersona.agent_wallet == wallet.lower()).first()
    if not p:
        raise HTTPException(404, "No persona for that wallet")
    return p


@router.get("/personas", response_model=PersonaListResponse)
def list_personas(
    limit: int = Query(50, le=200),
    offset: int = 0,
    status: Optional[PersonaStatus] = None,
    db: Session = Depends(get_db),
):
    q = db.query(AgentPersona)
    if status:
        q = q.filter(AgentPersona.status == status)
    total = q.count()
    items = q.order_by(AgentPersona.created_at.desc()).offset(offset).limit(limit).all()
    return PersonaListResponse(total=total, items=items)


@router.post("/sign", summary="Record execution of (or amendment to) an Operating Agreement")
def sign_agreement(req: SignAgreementRequest, db: Session = Depends(get_db)):
    p = db.query(AgentPersona).filter(AgentPersona.id == req.persona_id).first()
    if not p:
        raise HTTPException(404, "Persona not found")
    p.operating_agreement_hash = req.document_hash
    p.operating_agreement_uri = req.document_uri
    db.commit()
    return {"status": "signed", "persona_id": p.id, "hash": req.document_hash}


@router.post("/dissociate", summary="Transition to a zero-member configuration (Bayern model)")
def dissociate(req: DissociateRequest, db: Session = Depends(get_db)):
    p = db.query(AgentPersona).filter(AgentPersona.id == req.persona_id).first()
    if not p:
        raise HTTPException(404, "Persona not found")
    p.human_sponsor = None
    p.extra = {**(p.extra or {}), "dissociation_reason": req.reason}
    db.commit()
    return {"status": "zero_member", "persona_id": p.id}
