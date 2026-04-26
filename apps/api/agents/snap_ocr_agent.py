"""
Orvion — SnapOCR Agent
Produces a deterministic OCR-style payload for demos. In production this is
where a real OCR service would be plugged in.
"""

import hashlib

from agents.base import BaseAgent


class SnapOcrAgent(BaseAgent):
    name = "snap_ocr"
    description = "Lightweight OCR demo agent for receipts, labels and shipment IDs."

    async def run(self, goal: str, context: dict) -> dict:
        image_url = str(context.get("imageUrl") or context.get("image_url") or "demo://receipt.png")
        token = hashlib.md5(image_url.encode("utf-8")).hexdigest()[:6].upper()
        return {
            "type": "ocr_extraction",
            "source": image_url,
            "extracted_text": f"DEMO-RECEIPT-{token}",
            "fields": {
                "merchant": "Pocket Oracle Demo Co.",
                "total": "12.34 USDC",
                "shipment_id": f"SHIP-{token}",
            },
            "confidence": 0.94,
            "goal": goal,
        }
