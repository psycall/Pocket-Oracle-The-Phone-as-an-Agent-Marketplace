"""
Orvion — Agent Registry
Add new agents here to make them available in the execution engine.
"""

from agents.crypto_agent import CryptoAgent
from agents.research_agent import ResearchAgent
from agents.decision_agent import DecisionAgent

# Registry: agent_name → class
AGENT_REGISTRY: dict = {
    "crypto": CryptoAgent,
    "research": ResearchAgent,
    "decision": DecisionAgent,
}

__all__ = ["AGENT_REGISTRY", "CryptoAgent", "ResearchAgent", "DecisionAgent"]
