"""
Orvion — General Agent
Catch-all agent for goals that do not match a specialised one.
"""

from agents.base import BaseAgent


class GeneralAgent(BaseAgent):
    name = "general"
    description = "Fallback agent for goals that do not fit a specialised one."

    async def run(self, goal: str, context: dict) -> dict:
        return {
            "type": "general_response",
            "goal": goal,
            "context": context,
            "message": "Goal accepted — wire a specialised agent to deliver a richer answer.",
        }
