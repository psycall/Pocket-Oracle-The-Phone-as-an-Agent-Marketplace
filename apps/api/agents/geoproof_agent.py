"""
Orvion — GeoProof Agent
Produces a deterministic geo-attestation suitable for demos.
"""

import hashlib
import time

from agents.base import BaseAgent


class GeoProofAgent(BaseAgent):
    name = "geoproof"
    description = "Produces a signed-style location attestation for delivery and field ops."

    async def run(self, goal: str, context: dict) -> dict:
        latitude = float(context.get("latitude", -23.5505))
        longitude = float(context.get("longitude", -46.6333))
        accuracy = float(context.get("accuracy", 18.0))
        signature = hashlib.sha256(
            f"{goal}|{latitude}|{longitude}|{accuracy}".encode("utf-8")
        ).hexdigest()
        confidence = max(0.82, min(0.99, 1 - accuracy / 200))
        return {
            "type": "geoproof_attestation",
            "verified": True,
            "latitude": latitude,
            "longitude": longitude,
            "accuracy_meters": accuracy,
            "confidence": round(confidence, 2),
            "issued_at": time.time(),
            "signature": signature[:32],
        }
