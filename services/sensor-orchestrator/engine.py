from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import requests, uuid, time
from typing import List, Optional

app = FastAPI(title="Pocket Oracle OS - Engine")

# =========================
# AUTH SYSTEM
# =========================
# In production, this would be integrated with a DB/Vault
USERS = {
    "demo-key": {"name": "demo-user"}
}

def auth(api_key: str):
    if api_key not in USERS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return USERS[api_key]

# =========================
# MODELS
# =========================
class Task(BaseModel):
    goal: str
    context: Optional[dict] = {}

# =========================
# AGENTS (Core Execution Units)
# =========================
class CryptoAgent:
    """Monitors crypto trends and opportunities"""
    def run(self):
        try:
            url = "https://api.coingecko.com/api/v3/search/trending"
            res = requests.get(url, timeout=10).json()
            return [c["item"]["name"] for c in res["coins"][:5]]
        except Exception as e:
            return [f"Error fetching crypto data: {str(e)}"]

class DecisionAgent:
    """Analyzes data and makes logical decisions"""
    def run(self, data: List[str]):
        if any(coin in ["Bitcoin", "Ethereum", "Solana"] for coin in data):
            return "Market is heating up in major assets. Potential opportunity detected."
        return "No strong signals from major assets at the moment."

class NotificationAgent:
    """Manages delivery of alerts and results"""
    def run(self, message: str):
        return {"notify": message, "channel": "push/api", "status": "sent"}

# =========================
# ORCHESTRATOR (The Brain)
# =========================
class Engine:
    """Orchestrates agent execution based on intent (goal)"""
    def execute(self, goal: str, context: dict):
        goal_lower = goal.lower()
        
        # Pipeline: Crypto Intelligence
        if "crypto" in goal_lower or "coin" in goal_lower:
            data = CryptoAgent().run()
            decision = DecisionAgent().run(data)
            notification = NotificationAgent().run(decision)
            
            return {
                "pipeline": "Crypto Intelligence",
                "goal": goal,
                "execution_steps": [
                    {"agent": "CryptoAgent", "status": "completed", "output": data},
                    {"agent": "DecisionAgent", "status": "completed", "output": decision},
                    {"agent": "NotificationAgent", "status": "completed", "output": notification}
                ],
                "final_result": decision
            }
            
        return {
            "pipeline": "Unknown",
            "message": "No specific execution path found for this intent. Routing to general LLM agent (Coming soon)."
        }

engine = Engine()

# =========================
# API ENDPOINTS
# =========================
@app.post("/execute")
def execute_task(task: Task, user=Depends(auth)):
    """Main entry point for task execution"""
    result = engine.execute(task.goal, task.context)
    return {
        "execution_id": str(uuid.uuid4()),
        "user": user["name"],
        "result": result,
        "timestamp": time.time()
    }

@app.get("/status")
def status():
    """System status"""
    return {
        "product": "Pocket Oracle OS",
        "version": "1.0.0-alpha",
        "mode": "execution-layer",
        "status": "active"
    }

@app.get("/")
def root():
    return {"message": "Pocket Oracle OS Engine is running. Access /docs for API documentation."}
