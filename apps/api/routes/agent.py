"""
Orvion — Agent Routes
POST /agent/execute       → sync execution
POST /agent/execute/stream → SSE streaming execution
"""

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from core.engine import engine
from core.security import get_current_user
from models.schemas import TaskRequest, TaskRecord

router = APIRouter()


@router.post("/execute", response_model=TaskRecord, summary="Execute a task synchronously")
async def execute(
    task: TaskRequest,
    _user: dict = Depends(get_current_user),
):
    """
    Execute a natural language goal through Orvion's agent pipeline.

    The engine automatically:
    1. Routes your goal to the right specialized agent
    2. Executes with real AI (Claude) reasoning
    3. Persists the result
    4. Returns a complete execution record
    """
    return await engine.execute(task.goal, task.context)


@router.post("/execute/stream", summary="Execute with real-time SSE streaming")
async def execute_stream(
    task: TaskRequest,
    _user: dict = Depends(get_current_user),
):
    """
    Execute a goal with real-time streaming.
    Returns Server-Sent Events — connect with EventSource in the browser.

    Events emitted:
    - `started`   → execution began
    - `routing`   → analyzing goal
    - `routed`    → agent selected
    - `executing` → agent running
    - `result`    → execution result
    - `complete`  → done with duration
    """
    return StreamingResponse(
        engine.stream_execute(task.goal, task.context),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
