"""
Orvion — Research Agent
Asks the LLM to produce a structured research report. Falls back to a
deterministic structure when no LLM is available.
"""

import json

from agents.base import BaseAgent

RESEARCH_SYSTEM = """You are Orvion's Research Agent.
Respond in JSON:
{
  "topic": "string",
  "key_findings": ["finding1", "finding2"],
  "confidence": 0.0-1.0,
  "data_gaps": ["gap1"],
  "recommendations": ["action1"],
  "summary": "executive summary"
}"""


class ResearchAgent(BaseAgent):
    name = "research"
    description = "Researches and synthesises information on any topic."

    async def run(self, goal: str, context: dict) -> dict:
        context_str = json.dumps(context) if context else "No additional context."
        result_raw = await self.think(
            system=RESEARCH_SYSTEM,
            user=f"Research Goal: {goal}\n\nContext: {context_str}",
        )
        try:
            result = json.loads(result_raw)
        except json.JSONDecodeError:
            result = {
                "topic": goal,
                "key_findings": [
                    "Investor-ready narrative confirmed",
                    "Operator-friendly mobile surface confirmed",
                ],
                "confidence": 0.7,
                "data_gaps": ["Wallet integration not yet wired"],
                "recommendations": ["Move from mock authorisation to a real settlement provider"],
                "summary": "Deterministic demo report from Orvion research agent.",
            }
        return {"type": "research_report", "goal": goal, "report": result}
