"""
Orvion — Agent Registry
"""

from agents.crypto_agent import CryptoAgent
from agents.decision_agent import DecisionAgent
from agents.general_agent import GeneralAgent
from agents.geoproof_agent import GeoProofAgent
from agents.human_tap_agent import HumanTapAgent
from agents.research_agent import ResearchAgent
from agents.snap_ocr_agent import SnapOcrAgent

AGENT_REGISTRY: dict = {
    "crypto": CryptoAgent,
    "research": ResearchAgent,
    "decision": DecisionAgent,
    "geoproof": GeoProofAgent,
    "snap_ocr": SnapOcrAgent,
    "human_tap": HumanTapAgent,
    "general": GeneralAgent,
}

__all__ = [
    "AGENT_REGISTRY",
    "CryptoAgent",
    "ResearchAgent",
    "DecisionAgent",
    "GeoProofAgent",
    "SnapOcrAgent",
    "HumanTapAgent",
    "GeneralAgent",
]
