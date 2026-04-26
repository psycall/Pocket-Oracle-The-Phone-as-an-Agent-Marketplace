"""
Orvion — Decision Agent
Master router: classifies a natural language goal and selects which
specialised agent should handle it. Falls back to keyword routing in demo mode.
"""

import json

from agents.base import BaseAgent

ROUTER_SYSTEM = """You are Orvion's Decision Router.
Classify the user's goal and pick exactly one agent.

Available agents:
- crypto: cryptocurrency, market analysis, trading signals, DeFi
- research: research, information gathering, summaries, analysis
- geoproof: location proof, delivery, field operations
- snap_ocr: OCR, receipts, labels, shipment text extraction
- human_tap: human verification, escalation, last-mile confirmation
- general: anything that does not fit above

Respond ONLY with JSON (no markdown):
{
  "agent": "crypto|research|geoproof|snap_ocr|human_tap|general",
  "confidence": 0.0-1.0,
  "reasoning": "one sentence why",
  "refined_goal": "cleaned up version of the user's goal"
}"""


def keyword_route(goal: str) -> dict:
    g = goal.lower()
    # Order matters: more specific tokens first to avoid false positives.
    if any(k in g for k in ("ocr", "receipt", "label", "scan", "snap", "shipment id")):
        return {"agent": "snap_ocr", "confidence": 0.7, "reasoning": "keyword match", "refined_goal": goal}
    if any(k in g for k in ("human tap", "escalat", "approve", "reviewer")):
        return {"agent": "human_tap", "confidence": 0.7, "reasoning": "keyword match", "refined_goal": goal}
    if any(k in g for k in ("crypto", "bitcoin", "eth", " coin ", "market", "defi")):
        return {"agent": "crypto", "confidence": 0.7, "reasoning": "keyword match", "refined_goal": goal}
    if any(k in g for k in ("geoproof", "geo proof", "location", "latitude", "longitude", "proof of presence")):
        return {"agent": "geoproof", "confidence": 0.7, "reasoning": "keyword match", "refined_goal": goal}
    if any(k in g for k in ("delivery", "field")):
        return {"agent": "geoproof", "confidence": 0.6, "reasoning": "keyword match", "refined_goal": goal}
    if any(k in g for k in ("verify", "confirm")):
        return {"agent": "human_tap", "confidence": 0.6, "reasoning": "keyword match", "refined_goal": goal}
    if any(k in g for k in ("research", "analyze", "find", "what is", "summarize")):
        return {"agent": "research", "confidence": 0.7, "reasoning": "keyword match", "refined_goal": goal}
    return {"agent": "general", "confidence": 0.5, "reasoning": "fallback", "refined_goal": goal}


class DecisionAgent(BaseAgent):
    name = "decision"
    description = "Routes goals to the right specialised agent."

    async def route(self, goal: str) -> dict:
        # In demo mode (no LLM) we always use deterministic keyword routing.
        if self._llm is None:
            return keyword_route(goal)

        raw = await self.think(system=ROUTER_SYSTEM, user=f"User goal: {goal}")
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict) and "agent" in parsed:
                return parsed
        except json.JSONDecodeError:
            pass
        return keyword_route(goal)

    async def run(self, goal: str, context: dict) -> dict:
        routing = await self.route(goal)
        return {"type": "routing_decision", "routing": routing}
