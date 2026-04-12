from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl


app = FastAPI(title="Pocket Oracle Sensor Orchestrator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GeoProofRequest(BaseModel):
    latitude: float
    longitude: float
    accuracy: float | None = None


class SnapOCRRequest(BaseModel):
    imageUrl: HttpUrl


class HumanTapVerifyRequest(BaseModel):
    prompt: str
    answer: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "sensor-orchestrator"}


@app.post("/geoproof")
def geoproof(payload: GeoProofRequest) -> dict:
    return {
        "verified": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": {
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "accuracy": payload.accuracy,
        },
        "evidence": "mock_device_signal_bundle",
    }


@app.post("/snap-ocr")
def snap_ocr(payload: SnapOCRRequest) -> dict:
    return {
        "verified": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "image_url": str(payload.imageUrl),
        "extracted_text": "TOTAL 42.90 | STORE SAMPLE | 2026-04-12",
    }


@app.post("/human-tap-verify")
def human_tap_verify(payload: HumanTapVerifyRequest) -> dict:
    return {
        "verified": payload.answer.lower() in {"yes", "true", "confirmado", "sim"},
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": payload.prompt,
        "answer": payload.answer,
        "operator_signature": "mock_operator_attestation",
    }
