"""
Orvion — Crypto Agent
Fetches live market data and asks the LLM for analysis.
In DEMO_MODE (or when CoinGecko is unreachable), returns a deterministic
investor-ready payload so demos always succeed.
"""

import json

import httpx

from agents.base import BaseAgent


DECISION_SYSTEM = """You are Orvion's Crypto Analysis Agent.
Given trending coins, output JSON only:
{
  "sentiment": "bullish|bearish|neutral",
  "confidence": 0.0-1.0,
  "top_picks": [{"coin": "name", "reason": "why"}],
  "recommendation": "string",
  "risk_level": "LOW|MEDIUM|HIGH",
  "summary": "one sentence executive summary"
}"""


class CryptoAgent(BaseAgent):
    name = "crypto"
    description = "Analyses real-time crypto trends with graceful demo fallback."

    async def _fetch_trending(self) -> list[dict]:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get("https://api.coingecko.com/api/v3/search/trending")
                resp.raise_for_status()
                data = resp.json()
            return [
                {
                    "name": c["item"]["name"],
                    "symbol": c["item"]["symbol"],
                    "rank": c["item"].get("market_cap_rank"),
                    "score": c["item"].get("score", 0),
                }
                for c in data.get("coins", [])[:8]
            ]
        except Exception:
            return [
                {"name": "Bitcoin", "symbol": "BTC", "rank": 1, "score": 0},
                {"name": "Ethereum", "symbol": "ETH", "rank": 2, "score": 0},
                {"name": "Solana", "symbol": "SOL", "rank": 5, "score": 0},
            ]

    async def run(self, goal: str, context: dict) -> dict:
        trending = await self._fetch_trending()
        analysis_raw = await self.think(
            system=DECISION_SYSTEM,
            user=f"Goal: {goal}\n\nTrending coins:\n{json.dumps(trending, indent=2)}",
        )
        try:
            analysis = json.loads(analysis_raw)
        except json.JSONDecodeError:
            analysis = {
                "sentiment": "neutral",
                "confidence": 0.6,
                "top_picks": [{"coin": trending[0]["name"], "reason": "Highest interest in trending list"}],
                "recommendation": "Watch and wait for a clearer signal.",
                "risk_level": "MEDIUM",
                "summary": "Demo summary based on trending data.",
            }
        return {
            "type": "crypto_analysis",
            "trending": trending,
            "analysis": analysis,
            "data_source": "CoinGecko (with demo fallback)",
        }
