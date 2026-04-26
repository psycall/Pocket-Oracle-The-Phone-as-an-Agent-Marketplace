# Contributing to Orvion

Welcome! Every new agent, bug fix, or improvement makes Orvion more powerful.

## Quick Start

```bash
git clone https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace.git
cd Pocket-Oracle-The-Phone-as-an-Agent-Marketplace

# Install
npm run setup        # creates .env from template
pip install -r apps/api/requirements.txt

# Run
npm run dev:api      # API at http://localhost:8000
npm run dev:web      # Dashboard at http://localhost:3000
```

## Adding a New Agent

This is the most impactful contribution. Here's the full recipe:

### 1. Create the agent file

```python
# apps/api/agents/my_agent.py
from agents.base import BaseAgent

MY_SYSTEM = """You are Orvion's [Name] Agent.
[Describe exactly what this agent does and what JSON format it should return]"""

class MyAgent(BaseAgent):
    name = "my_agent"
    description = "What this agent does in one sentence."

    async def run(self, goal: str, context: dict) -> dict:
        import json
        result_raw = await self.think(
            system=MY_SYSTEM,
            user=f"Goal: {goal}\nContext: {json.dumps(context)}",
        )
        try:
            result = json.loads(result_raw)
        except json.JSONDecodeError:
            result = {"raw": result_raw}
        return {"type": "my_agent_result", "data": result}
```

### 2. Register in the registry

```python
# apps/api/agents/__init__.py
from agents.my_agent import MyAgent

AGENT_REGISTRY = {
    "crypto": CryptoAgent,
    "research": ResearchAgent,
    "decision": DecisionAgent,
    "my_agent": MyAgent,     # ← add here
}
```

### 3. Update the router

```python
# apps/api/agents/decision_agent.py
# Add your agent name to the ROUTER_SYSTEM prompt so Claude knows to route to it.
```

### 4. Add tests

```python
# apps/api/tests/test_api.py
def test_my_agent():
    ...
```

### 5. Open a PR

Use the PR template. Make sure all tests pass.

## Code Standards

- No hardcoded secrets. Ever. Use `.env` and `settings.*`.
- Every agent must extend `BaseAgent`.
- Every route must have a docstring.
- All business logic in `agents/` or `core/`. Routes are thin.

## Roadmap

Check `ROADMAP.md` for what's most needed. PRs for roadmap items get priority review.
