"""
Orvion — Base Agent
All agents inherit from this. Ensures consistent interface and graceful
degradation when the LLM provider is unavailable (DEMO_MODE).
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from core.config import settings


class BaseAgent(ABC):
    """Every Orvion agent extends this class."""

    name: str = "base"
    description: str = "Base agent"

    def __init__(self) -> None:
        self._llm = None
        if settings.ANTHROPIC_API_KEY and not settings.DEMO_MODE:
            try:
                from anthropic import AsyncAnthropic  # type: ignore

                self._llm = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            except Exception:
                self._llm = None

    @abstractmethod
    async def run(self, goal: str, context: dict) -> dict:
        ...

    async def think(self, system: str, user: str) -> str:
        if self._llm is None:
            return self._mock_response(system, user)
        try:
            response = await self._llm.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=settings.ANTHROPIC_MAX_TOKENS,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return response.content[0].text
        except Exception:
            return self._mock_response(system, user)

    async def stream_think(self, system: str, user: str) -> AsyncGenerator[str, None]:
        if self._llm is None:
            yield self._mock_response(system, user)
            return
        try:
            async with self._llm.messages.stream(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=settings.ANTHROPIC_MAX_TOKENS,
                system=system,
                messages=[{"role": "user", "content": user}],
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception:
            yield self._mock_response(system, user)

    def _mock_response(self, system: str, user: str) -> str:  # noqa: ARG002
        """
        Deterministic, demo-safe response used when no LLM is configured.
        Each subclass can override to produce richer mock JSON.
        """
        return (
            '{"summary": "Demo-mode response from Orvion.",'
            ' "agent": "' + self.name + '",'
            ' "ok": true}'
        )

    def to_dict(self) -> dict:
        return {"name": self.name, "description": self.description}
