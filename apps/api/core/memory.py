"""
Orvion — Agent Memory Layer
Persistent storage via Redis. Task history survives restarts.
"""

import json
import time
from typing import Optional, List
from uuid import uuid4

import redis.asyncio as aioredis

from core.config import settings


class AgentMemory:
    """
    Redis-backed memory for agent execution history.
    Replaces in-memory list that died on every restart.
    """

    def __init__(self):
        self._client: Optional[aioredis.Redis] = None

    async def client(self) -> aioredis.Redis:
        if self._client is None:
            self._client = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
        return self._client

    # ── Write ────────────────────────────────────────────────

    async def store_task(self, record: dict) -> str:
        task_id = record.get("id") or str(uuid4())
        record["id"] = task_id
        record["timestamp"] = record.get("timestamp") or time.time()

        client = await self.client()
        # Store individual task — expire after 30 days
        await client.setex(f"task:{task_id}", 60 * 60 * 24 * 30, json.dumps(record))
        # Push to sorted set for ordered history
        await client.zadd("task:index", {task_id: record["timestamp"]})
        return task_id

    # ── Read ─────────────────────────────────────────────────

    async def get_task(self, task_id: str) -> Optional[dict]:
        client = await self.client()
        raw = await client.get(f"task:{task_id}")
        return json.loads(raw) if raw else None

    async def get_history(self, limit: int = 50, offset: int = 0) -> List[dict]:
        client = await self.client()
        # Get IDs ordered by timestamp desc
        ids = await client.zrevrange("task:index", offset, offset + limit - 1)
        tasks = []
        for task_id in ids:
            raw = await client.get(f"task:{task_id}")
            if raw:
                tasks.append(json.loads(raw))
        return tasks

    async def count(self) -> int:
        client = await self.client()
        return await client.zcard("task:index")

    # ── Metrics ──────────────────────────────────────────────

    async def increment_metric(self, key: str, amount: int = 1):
        client = await self.client()
        await client.incrby(f"metric:{key}", amount)

    async def get_metric(self, key: str) -> int:
        client = await self.client()
        val = await client.get(f"metric:{key}")
        return int(val) if val else 0


memory = AgentMemory()
