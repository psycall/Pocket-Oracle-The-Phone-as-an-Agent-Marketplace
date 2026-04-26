"""
Orvion — HumanTap Agent
Routes a binary verification question to a (simulated) operator pool and
produces an auditable verdict.
"""

import time

from agents.base import BaseAgent


class HumanTapAgent(BaseAgent):
    name = "human_tap"
    description = "Demo human-in-the-loop verification with operator trace."

    async def run(self, goal: str, context: dict) -> dict:
        prompt = str(context.get("prompt") or goal)
        answer = str(context.get("answer") or "yes").strip().lower()
        approved = answer in {"yes", "y", "approved", "approve", "ok", "true"}
        return {
            "type": "human_tap_verdict",
            "prompt": prompt,
            "answer": answer,
            "verdict": "approved" if approved else "needs-review",
            "operator": "operator-demo-01",
            "decided_at": time.time(),
        }
