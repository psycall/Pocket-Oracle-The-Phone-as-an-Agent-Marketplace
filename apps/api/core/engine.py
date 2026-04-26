"""
Orvion — Execution Engine
The orchestrator. Takes a goal, routes it, executes, stores result, and verifies via Arc Network.
"""

import time
import json
import hashlib
from uuid import uuid4
from typing import AsyncGenerator

from agents import AGENT_REGISTRY
from agents.decision_agent import DecisionAgent
from core.memory import memory
from core.config import settings
from core.arc_integration import arc_client


class ExecutionEngine:
    """
    Core engine. Workflow:
      1. DecisionAgent routes the goal to right agent
      2. Specialized agent executes
      3. Arc Network verifies execution proof
      4. Result is persisted in Redis
      5. Full record returned
    """

    async def execute(self, goal: str, context: dict) -> dict:
        task_id = str(uuid4())
        started_at = time.time()

        # Step 1 — Route
        router = DecisionAgent()
        routing = await router.route(goal)
        agent_name = routing.get("agent", "research")
        refined_goal = routing.get("refined_goal", goal)

        # Step 2 — Execute specialized agent
        agent_cls = AGENT_REGISTRY.get(agent_name) or AGENT_REGISTRY["research"]
        agent = agent_cls()
        result = await agent.run(refined_goal, context)

        # Step 3 — Arc Network Verification (The Proof Layer)
        result_hash = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
        arc_proof = await arc_client.verify_execution(task_id, result_hash)

        # Step 4 — Build record
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

        # Step 5 — Persist
        await memory.store_task(record)
        await memory.increment_metric("total_executions")
        await memory.increment_metric(f"agent_{agent_name}_executions")

        return record

    async def stream_execute(
        self, goal: str, context: dict
    ) -> AsyncGenerator[str, None]:
        """
        Streaming execution — sends SSE events as each step completes.
        Frontend sees execution in real time with Arc Network proofing.
        """
        task_id = str(uuid4())
        started_at = time.time()

        def event(data: dict) -> str:
            return f"data: {json.dumps(data)}\n\n"

        yield event({"type": "started", "task_id": task_id, "goal": goal})

        # Route
        yield event({"type": "routing", "message": "Analyzing goal..."})
        router = DecisionAgent()
        routing = await router.route(goal)
        agent_name = routing.get("agent", "research")
        refined_goal = routing.get("refined_goal", goal)
        yield event({"type": "routed", "agent": agent_name, "routing": routing})

        # Execute
        yield event({"type": "executing", "agent": agent_name, "message": f"Running {agent_name} agent..."})
        agent_cls = AGENT_REGISTRY.get(agent_name) or AGENT_REGISTRY["research"]
        agent = agent_cls()
        result = await agent.run(refined_goal, context)
        yield event({"type": "result", "data": result})

        # Arc Network Verification
        yield event({"type": "verifying", "message": "Submitting proof to Arc Network..."})
        result_hash = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
        arc_proof = await arc_client.verify_execution(task_id, result_hash)
        yield event({"type": "verified", "proof": arc_proof})

        # Persist
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

        yield event({
            "type": "complete",
            "task_id": task_id,
            "duration_ms": record["duration_ms"],
        })


engine = ExecutionEngine()
