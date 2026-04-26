"""
Orvion — Base Agent
All agents inherit from this. Ensures consistent interface.
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator
from anthropic import AsyncAnthropic

from core.config import settings


class BaseAgent(ABC):
    """
    Every Orvion agent extends this class.
    Provides LLM access, streaming, and standard interface.
    """

    name: str = "base"
    description: str = "Base agent"

    def __init__(self):
        self._llm = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    @abstractmethod
    async def run(self, goal: str, context: dict) -> dict:
        """Execute the agent's primary task. Must be implemented."""
        ...

    async def think(self, system: str, user: str) -> str:
        """Call Claude for a single decision. Returns text."""
        response = await self._llm.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=settings.ANTHROPIC_MAX_TOKENS,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text

    async def stream_think(
        self, system: str, user: str
    ) -> AsyncGenerator[str, None]:
        """Stream Claude's thinking token by token."""
        async with self._llm.messages.stream(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=settings.ANTHROPIC_MAX_TOKENS,
            system=system,
            messages=[{"role": "user", "content": user}],
        ) as stream:
            async for text in stream.text_stream:
                yield text

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
        }
