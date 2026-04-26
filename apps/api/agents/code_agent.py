"""
Orvion — Code Agent
Implementation-oriented structured output for product, API and engineering requests.
"""

from __future__ import annotations

import json

from agents.base import BaseAgent

CODE_SYSTEM = """You are Orvion's Code Agent.
Return JSON with a concise engineering plan, priority actions, risks and delivery summary.
"""


class CodeAgent(BaseAgent):
    name = "code"
    description = "Turns technical goals into an implementation-oriented plan."

    def _fallback_plan(self, goal: str, context: dict) -> dict:
        return {
            "goal": goal,
            "priority_actions": [
                "Harden the developer experience so the demo can always run.",
                "Improve the frontend narrative for non-technical stakeholders.",
                "Expose backend fallbacks and monitoring-friendly metadata."
            ],
            "technical_risks": [
                "Production integrations still require real provider credentials.",
                "Mock payment mode must be replaced before launch."
            ],
            "delivery_summary": "Code agent produced a deterministic plan suitable for demos and technical reviews.",
            "context": context,
        }

    async def run(self, goal: str, context: dict) -> dict:
        if self.llm_enabled:
            raw = await self.think(
                system=CODE_SYSTEM,
                user=json.dumps({"goal": goal, "context": context}, indent=2),
            )
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = self._fallback_plan(goal, context)
        else:
            payload = self._fallback_plan(goal, context)

        return {
            "type": "code_plan",
            "goal": goal,
            "plan": payload,
        }
