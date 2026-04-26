"""
Orvion — Research Agent
Uses Claude to research and synthesize any topic.
"""

from agents.base import BaseAgent

RESEARCH_SYSTEM = """You are Orvion's Research Agent.
Given a research goal, you:
1. Identify the key questions to answer
2. Synthesize what you know about the topic
3. Identify gaps and what additional data would help
4. Provide a structured research report

Respond in JSON:
{
  "topic": "string",
  "key_findings": ["finding1", "finding2", ...],
  "confidence": 0.0-1.0,
  "data_gaps": ["gap1", "gap2"],
  "recommendations": ["action1", "action2"],
  "summary": "executive summary"
}"""


class ResearchAgent(BaseAgent):
    name = "research"
    description = "Researches and synthesizes information on any topic using Claude."

    async def run(self, goal: str, context: dict) -> dict:
        import json

        context_str = json.dumps(context) if context else "No additional context provided."

        result_raw = await self.think(
            system=RESEARCH_SYSTEM,
            user=f"Research Goal: {goal}\n\nContext: {context_str}",
        )

        try:
            result = json.loads(result_raw)
        except json.JSONDecodeError:
            result = {"raw_analysis": result_raw}

        return {
            "type": "research_report",
            "goal": goal,
            "report": result,
        }
