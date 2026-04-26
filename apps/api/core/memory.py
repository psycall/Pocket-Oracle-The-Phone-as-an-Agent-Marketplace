"""
Orvion — Agent Memory Layer
Persistent storage via Redis with automatic in-process fallback so the API
keeps working in demo / investor scenarios when Redis is offline.
"""

import json
import time
from typing import Optional, List
from uuid import uuid4

from core.config import settings


class _InMemoryStore:
    """Lightweight Redis stand-in good enough for demos and tests."""

    def __init__(self) -> None:
        self.kv: dict[str, str] = {}
        self.zset: list[tuple[float, str]] = []
        self.metrics: dict[str, int] = {}

    async def setex(self, key: str, _ttl: int, value: str) -> None:
        self.kv[key] = value

    async def set(self, key: str, value: str) -> None:
        self.kv[key] = value

    async def get(self, key: str) -> Optional[str]:
        return self.kv.get(key)

    async def zadd(self, _index: str, mapping: dict[str, float]) -> None:
        for task_id, score in mapping.items():
            self.zset = [(s, t) for s, t in self.zset if t != task_id]
            self.zset.append((score, task_id))

    async def zrevrange(self, _index: str, start: int, end: int) -> list[str]:
        ordered = sorted(self.zset, key=lambda item: item[0], reverse=True)
        return [task_id for _score, task_id in ordered[start : end + 1]]

    async def zcard(self, _index: str) -> int:
        return len(self.zset)

    async def incrby(self, key: str, amount: int) -> None:
        self.metrics[key] = self.metrics.get(key, 0) + amount

    async def get_metric(self, key: str) -> int:
        return self.metrics.get(key, 0)


class AgentMemory:
    """Redis-backed memory with graceful fallback to in-process store."""

    def __init__(self) -> None:
        self._client = None
        self._fallback: Optional[_InMemoryStore] = None

    async def client(self):
        if self._client is not None:
            return self._client
        if self._fallback is not None:
            return self._fallback

        try:
            import redis.asyncio as aioredis  # type: ignore

            client = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
            await client.ping()
            self._client = client
            return client
        except Exception:
            self._fallback = _InMemoryStore()
            return self._fallback

    async def store_task(self, record: dict) -> str:
        task_id = record.get("id") or str(uuid4())
        record["id"] = task_id
        record["timestamp"] = record.get("timestamp") or time.time()

        client = await self.client()
        await client.setex(f"task:{task_id}", 60 * 60 * 24 * 30, json.dumps(record))
        await client.zadd("task:index", {task_id: record["timestamp"]})
        return task_id

    async def get_task(self, task_id: str) -> Optional[dict]:
        client = await self.client()
        raw = await client.get(f"task:{task_id}")
        return json.loads(raw) if raw else None

    async def get_history(self, limit: int = 50, offset: int = 0) -> List[dict]:
        client = await self.client()
        ids = await client.zrevrange("task:index", offset, offset + limit - 1)
        tasks: List[dict] = []
        for task_id in ids:
            raw = await client.get(f"task:{task_id}")
            if raw:
                tasks.append(json.loads(raw))
        return tasks

    async def count(self) -> int:
        client = await self.client()
        return await client.zcard("task:index")

    async def increment_metric(self, key: str, amount: int = 1) -> None:
        client = await self.client()
        if hasattr(client, "incrby"):
            await client.incrby(f"metric:{key}", amount)

    async def get_metric(self, key: str) -> int:
        client = await self.client()
        if hasattr(client, "get_metric"):
            return await client.get_metric(f"metric:{key}")
        raw = await client.get(f"metric:{key}")
        return int(raw) if raw else 0


memory = AgentMemory()
