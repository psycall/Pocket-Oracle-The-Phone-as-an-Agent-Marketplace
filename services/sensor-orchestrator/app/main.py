from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import requests
import time
import uuid

app = FastAPI(title="Pocket Oracle GOD MODE 🚀")

# =========================
# CONFIG
# =========================

API_KEY = "oracle-secret-key"  # troque depois

# =========================
# SECURITY
# =========================

def verify_api_key(key: str):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# =========================
# MODELS
# =========================

class Task(BaseModel):
    type: str
    data: dict = {}

# =========================
# LOGGER
# =========================

def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

# =========================
# BASE AGENT
# =========================

class BaseAgent:
    def run(self, data: dict):
        raise NotImplementedError()

# =========================
# AGENTS
# =========================

class CryptoAgent(BaseAgent):
    def run(self, data):
        log("Fetching crypto trends...")
        url = "https://api.coingecko.com/api/v3/search/trending"
        res = requests.get(url).json()
        coins = [coin["item"]["name"] for coin in res["coins"][:5]]
        return {"trending": coins}


class SummarizerAgent(BaseAgent):
    def run(self, data):
        text = data.get("text", "")
        summary = text[:120] + "..." if len(text) > 120 else text
        return {"summary": summary}


class TelegramAgent(BaseAgent):
    def run(self, data):
        token = data.get("token")
        chat_id = data.get("chat_id")
        message = data.get("message")

        if not token or not chat_id:
            return {"error": "Missing Telegram credentials"}

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        try:
            requests.post(url, json={"chat_id": chat_id, "text": message})
            return {"status": "sent"}
        except:
            return {"error": "telegram_failed"}


# =========================
# AGENT REGISTRY
# =========================

AGENTS = {
    "crypto": CryptoAgent(),
    "summarize": SummarizerAgent(),
    "telegram": TelegramAgent()
}

# =========================
# ORCHESTRATOR
# =========================

class Orchestrator:

    def execute(self, task: Task):
        log(f"Executing task: {task.type}")

        if task.type == "crypto_pipeline":

            crypto = AGENTS["crypto"].run({})
            text = ", ".join(crypto["trending"])

            summary = AGENTS["summarize"].run({"text": text})

            telegram = AGENTS["telegram"].run({
                "token": task.data.get("token"),
                "chat_id": task.data.get("chat_id"),
                "message": summary["summary"]
            })

            return {
                "id": str(uuid.uuid4()),
                "flow": "crypto_pipeline",
                "steps": {
                    "crypto": crypto,
                    "summary": summary,
                    "telegram": telegram
                }
            }

        if task.type in AGENTS:
            result = AGENTS[task.type].run(task.data)
            return {
                "id": str(uuid.uuid4()),
                "result": result
            }

        raise HTTPException(status_code=400, detail="Unknown task")

orchestrator = Orchestrator()

# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {
        "name": "Pocket Oracle",
        "status": "running",
        "mode": "GOD"
    }

@app.get("/agents")
def list_agents():
    return {"agents": list(AGENTS.keys()) + ["crypto_pipeline"]}

@app.post("/execute")
def execute(task: Task, api_key: str):
    verify_api_key(api_key)
    return orchestrator.execute(task)
