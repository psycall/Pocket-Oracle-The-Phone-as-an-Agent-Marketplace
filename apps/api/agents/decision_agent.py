"""
Orvion — Decision Agent
Master router: understands a natural language goal and
routes it to the right specialized agent. The brain of Orvion.
"""

import json
from agents.base import BaseAgent

ROUTER_SYSTEM = """You are Orvion's Decision Router.
Your job is to classify a user's goal and decide which specialized agent to use.

Available agents:
- crypto: for cryptocurrency, market analysis, trading signals, DeFi
- research: for research, information gathering, summaries, analysis
- code: for code generation, debugging, technical questions
- general: for anything that doesn't fit above

Respond ONLY with JSON (no markdown):
{
  "agent": "crypto|research|code|general",
  "confidence": 0.0-1.0,
  "reasoning": "one sentence why",
  "refined_goal": "cleaned up version of the user's goal"
}"""


class DecisionAgent(BaseAgent):
    name = "decision"
    description = "Routes goals to the right specialized agent."

    async def route(self, goal: str) -> dict:
        """Determine which agent should handle this goal."""
        raw = await self.think(
            system=ROUTER_SYSTEM,
            user=f"User goal: {goal}",
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback routing by keyword
            goal_lower = goal.lower()
            if any(k in goal_lower for k in ["crypto", "bitcoin", "eth", "coin", "market"]):
                return {"agent": "crypto", "confidence": 0.7, "reasoning": "keyword match", "refined_goal": goal}
            if any(k in goal_lower for k in ["research", "analyze", "find", "what is"]):
                return {"agent": "research", "confidence": 0.7, "reasoning": "keyword match", "refined_goal": goal}
            return {"agent": "general", "confidence": 0.5, "reasoning": "fallback", "refined_goal": goal}

    async def run(self, goal: str, context: dict) -> dict:
        routing = await self.route(goal)
        return {"type": "routing_decision", "routing": routing}
