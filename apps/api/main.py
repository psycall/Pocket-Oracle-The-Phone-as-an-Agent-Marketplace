"""
Orvion — Execution Layer for Autonomous Agents
Main API entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from core.config import settings
from routes import agent, health, marketplace, node


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    print(f"🚀 Orvion Node [{settings.NODE_ID}] starting...")
    yield
    print("🛑 Orvion Node shutting down...")


app = FastAPI(
    title="Orvion — Execution Layer",
    description="The infrastructure for autonomous agent execution.",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(node.router, prefix="/node", tags=["Node"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["Marketplace"])


@app.get("/", tags=["Root"])
def root() -> dict:
    return {
        "node": settings.NODE_ID,
        "version": "2.1.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "demo_mode": settings.DEMO_MODE,
    }
