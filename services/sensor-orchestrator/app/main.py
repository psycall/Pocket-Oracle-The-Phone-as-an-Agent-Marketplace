"""
Pocket Oracle — Sensor Orchestrator
Tiny FastAPI service called by the API Gateway to fulfil paid Oracle
requests. Deterministic responses keep demos predictable.
"""

import hashlib
import time
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Pocket Oracle — Sensor Orchestrator",
    version="1.0.0",
    description="Coordinates phone-side sensors for paid Oracle services.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GeoProofRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accuracy: float | None = Field(default=18.0, ge=0, le=10_000)


class SnapOcrRequest(BaseModel):
    imageUrl: str


class HumanTapRequest(BaseModel):
    prompt: str
    answer: str


def _exec_id(prefix: str, payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(repr(sorted(payload.items())).encode("utf-8")).hexdigest()
    return f"{prefix}_{digest[:12]}"


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "service": "sensor-orchestrator", "ts": time.time()}


@app.post("/geoproof")
def geoproof(req: GeoProofRequest) -> dict[str, Any]:
    payload = req.model_dump()
    accuracy = float(payload.get("accuracy") or 18.0)
    confidence = max(0.82, min(0.99, 1 - accuracy / 200))
    return {
        "execution_id": _exec_id("geoproof", payload),
        "verified": True,
        "latitude": req.latitude,
        "longitude": req.longitude,
        "accuracy": accuracy,
        "confidence": round(confidence, 2),
        "region_hint": "northern-hemisphere" if req.latitude >= 0 else "southern-hemisphere",
        "issued_at": time.time(),
    }


@app.post("/snap-ocr")
def snap_ocr(req: SnapOcrRequest) -> dict[str, Any]:
    token = hashlib.md5(req.imageUrl.encode("utf-8")).hexdigest()[:6].upper()
    return {
        "execution_id": _exec_id("snapocr", req.model_dump()),
        "extracted_text": f"DEMO-RECEIPT-{token}",
        "fields": {
            "merchant": "Pocket Oracle Demo Co.",
            "total": "12.34 USDC",
            "shipment_id": f"SHIP-{token}",
        },
        "confidence": 0.94,
        "source": req.imageUrl,
    }


@app.post("/human-tap-verify")
def human_tap_verify(req: HumanTapRequest) -> dict[str, Any]:
    answer = req.answer.strip().lower()
    approved = answer in {"yes", "y", "approved", "approve", "ok", "true"}
    return {
        "execution_id": _exec_id("humantap", req.model_dump()),
        "verdict": "approved" if approved else "needs-review",
        "prompt": req.prompt,
        "answer": req.answer,
        "reviewer": "operator-demo-01",
        "decided_at": time.time(),
    }
