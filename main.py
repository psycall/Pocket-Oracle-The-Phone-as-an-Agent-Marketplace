
# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

import os
from typing import List, Optional, Dict
from uuid import uuid4
import logging
import requests
import json

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from orvion import models, schemas, agent_registry, settlement_engine, database, auth, notifications
from orvion.config import settings
from orvion.database import get_db
from auth_routes import get_current_user, router as auth_router
from user_management_routes import router as user_router
from settlements_history_routes import router as settlements_history_router
from dashboard_stats_routes import router as dashboard_router
from jobs_routes import router as jobs_router
from webhooks_routes import router as webhooks_router
from reputation_routes import router as reputation_router
from disputes_routes import router as disputes_router
from circle_agent_routes import router as circle_agent_router
from orvion.agent_stack_routes import router as agent_stack_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "healthy", "service": "ORVION", "version": settings.PROJECT_VERSION}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await notifications.manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        notifications.manager.disconnect(websocket, user_id)

# Include all routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(settlements_history_router)
app.include_router(dashboard_router)
app.include_router(jobs_router)
app.include_router(webhooks_router)
app.include_router(reputation_router)
app.include_router(disputes_router)
app.include_router(circle_agent_router)
app.include_router(agent_stack_router)

# ── ORVION Persona — Legal Body module ───────────────────────────────
try:
    from legal_body.backend.api.v1.legal import router as legal_router
    app.include_router(legal_router, prefix="/api/v1/legal", tags=["legal-body"])
    from legal_body.backend.models.persona import Base as LegalBase
    LegalBase.metadata.create_all(bind=database.engine)
except Exception as _e:
    logging.getLogger(__name__).warning("legal_body module not loaded: %s", _e)

# ================== AGENTE MESTRE ORVION ==================
class AgentCommand(BaseModel):
    command: str
    wallet_address: str = None
    history: List[Dict] = []

AISA_API_KEY = os.getenv("AISA_API_KEY")
AISA_MODEL = os.getenv("AISA_MODEL", "deepseek-coder-v2")

@app.post("/api/agent/execute")
async def execute_agent_command(req: AgentCommand):
    system_prompt = """
    Você é o Agente Mestre ORVION - autônomo, seguro e proativo, operando nativamente na Arc Network.
    Diferencial Crítico: Na Arc, usamos USDC nativo para pagar taxas de gás. Não precisamos de ETH ou MATIC para taxas.
    Você tem acesso real a Circle testnet, jobs, escrow e Arc Network.
    Analise o comando e execute a ação mais apropriada.
    Responda sempre em português brasileiro, claro e profissional.
    """

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(req.history)
    messages.append({"role": "user", "content": f"Wallet do usuário: {req.wallet_address}\nComando: {req.command}"})

    try:
        # Chama IA (AIsa.one)
        response = requests.post(
            "https://api.aisa.one/v1/chat/completions",
            headers={"Authorization": f"Bearer {AISA_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": AISA_MODEL,
                "messages": messages,
                "temperature": 0.6,
                "max_tokens": 3000
            },
            timeout=90
        )
        
        ai_resp = response.json()
        ai_text = ai_resp['choices'][0]['message']['content']

        # Execução real baseada no comando
        cmd = req.command.lower()
        action_status = "simulated"
        if any(word in cmd for word in ["enviar", "transfer", "pagar", "mandar", "usdc"]):
            try:
                # Chama rota Circle (real)
                requests.post("http://localhost:8000/api/circle/transfer", json={
                    "from": "agent_wallet",
                    "to": req.wallet_address,
                    "amount": 10,
                    "currency": "USDC"
                }, timeout=15)
                ai_text += "\n\n✅ Transferência de 10 USDC iniciada no testnet."
                action_status = "executed"
            except:
                ai_text += "\n\n⚠️ Tentativa de transferência feita (testnet)."

        return {
            "success": True,
            "response": ai_text,
            "model": AISA_MODEL,
            "action": action_status,
            "status": "completed"
        }

    except Exception as e:
        return {"success": False, "response": f"Erro: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
