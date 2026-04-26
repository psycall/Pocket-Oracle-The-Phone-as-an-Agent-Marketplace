"""
Orvion — Execution Engine
Routes goals, executes agents, verifies output and persists records.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import AsyncGenerator
from uuid import uuid4

from agents import AGENT_REGISTRY
from agents.decision_agent import DecisionAgent
from core.arc_integration import arc_client
from core.config import settings
from core.memory import memory


class ExecutionEngine:
    async def execute(self, goal: str, context: dict) -> dict:
        task_id = str(uuid4())
        started_at = time.time()

        router = DecisionAgent()
        routing = await router.route(goal)
        agent_name = routing.get("agent", "research")
        refined_goal = routing.get("refined_goal", goal)

        agent_cls = AGENT_REGISTRY.get(agent_name) or AGENT_REGISTRY["research"]
        agent = agent_cls()
        result = await agent.run(refined_goal, context)

        result_hash = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
        arc_proof = await arc_client.verify_execution(task_id, result_hash)

        record = {
            "id": task_id,
            "node": settings.NODE_ID,
            "goal": goal,
            "routing": routing,
            "agent_used": agent_name,
            "result": result,
            "arc_verification": arc_proof,
            "duration_ms": round((time.time() - started_at) * 1000),
            "timestamp": started_at,
            "status": "complete",
        }

        await memory.store_task(record)
        await memory.increment_metric("total_executions")
        await memory.increment_metric(f"agent_{agent_name}_executions")
        return record

    async def stream_execute(self, goal: str, context: dict) -> AsyncGenerator[str, None]:
        task_id = str(uuid4())
        started_at = time.time()

        def event(data: dict) -> str:
            return f"data: {json.dumps(data)}\n\n"

        yield event({"type": "started", "task_id": task_id, "goal": goal})
        yield event({"type": "routing", "message": "Analyzing goal..."})

        router = DecisionAgent()
        routing = await router.route(goal)
        agent_name = routing.get("agent", "research")
        refined_goal = routing.get("refined_goal", goal)
        yield event({"type": "routed", "agent": agent_name, "routing": routing})

        yield event({"type": "executing", "agent": agent_name, "message": f"Running {agent_name} agent..."})
        agent_cls = AGENT_REGISTRY.get(agent_name) or AGENT_REGISTRY["research"]
        agent = agent_cls()
        result = await agent.run(refined_goal, context)
        yield event({"type": "result", "data": result})

        yield event({"type": "verifying", "message": "Submitting proof to Arc Network..."})
        result_hash = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
        arc_proof = await arc_client.verify_execution(task_id, result_hash)
        yield event({"type": "verified", "proof": arc_proof})

        record = {
            "id": task_id,
            "node": settings.NODE_ID,
            "goal": goal,
            "routing": routing,
            "agent_used": agent_name,
            "result": result,
            "arc_verification": arc_proof,
            "duration_ms": round((time.time() - started_at) * 1000),
            "timestamp": started_at,
            "status": "complete",
        }
        await memory.store_task(record)
        await memory.increment_metric("total_executions")
        await memory.increment_metric(f"agent_{agent_name}_executions")

        yield event({"type": "complete", "task_id": task_id, "duration_ms": record["duration_ms"]})


engine = ExecutionEngine()
