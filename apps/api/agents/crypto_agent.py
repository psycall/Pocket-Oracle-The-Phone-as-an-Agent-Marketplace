"""
Orvion — Crypto Agent
Fetches live market data + uses Claude for real analysis.
No more if/else decisions.
"""

import httpx
from agents.base import BaseAgent


DECISION_SYSTEM = """You are Orvion's Crypto Analysis Agent.
You receive a list of trending cryptocurrencies and must provide:

1. A market sentiment assessment (bullish / bearish / neutral)
2. The top 2 coins worth watching and why
3. One actionable recommendation
4. Risk level: LOW / MEDIUM / HIGH

Respond in this exact JSON format (no markdown, no preamble):
{
  "sentiment": "bullish|bearish|neutral",
  "confidence": 0.0-1.0,
  "top_picks": [
    {"coin": "name", "reason": "why"},
    {"coin": "name", "reason": "why"}
  ],
  "recommendation": "string",
  "risk_level": "LOW|MEDIUM|HIGH",
  "summary": "one sentence executive summary"
}"""


class CryptoAgent(BaseAgent):
    name = "crypto"
    description = "Analyzes real-time crypto trends using Claude AI for decisions."

    async def _fetch_trending(self) -> list[dict]:
        """Fetch live trending coins from CoinGecko."""
        url = "https://api.coingecko.com/api/v3/search/trending"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

        return [
            {
                "name": c["item"]["name"],
                "symbol": c["item"]["symbol"],
                "rank": c["item"]["market_cap_rank"],
                "price_btc": c["item"].get("price_btc"),
                "score": c["item"].get("score", 0),
            }
            for c in data.get("coins", [])[:8]
        ]

    async def run(self, goal: str, context: dict) -> dict:
        # 1. Fetch live data
        trending = await self._fetch_trending()

        # 2. Claude makes the real decision (no more if/else)
        import json
        analysis_raw = await self.think(
            system=DECISION_SYSTEM,
            user=f"Goal: {goal}\n\nTrending coins data:\n{json.dumps(trending, indent=2)}",
        )

        try:
            analysis = json.loads(analysis_raw)
        except json.JSONDecodeError:
            analysis = {"raw": analysis_raw}

        return {
            "type": "crypto_analysis",
            "trending": trending,
            "analysis": analysis,
            "data_source": "CoinGecko",
        }
