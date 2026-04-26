"""
Orvion — Execution Layer for Autonomous Agents
Main API entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from routes import agent, node, marketplace, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    print(f"🚀 Orvion Node [{settings.NODE_ID}] starting...")
    yield
    print("🛑 Orvion Node shutting down...")


app = FastAPI(
    title="Orvion — Execution Layer",
    description="The infrastructure for autonomous agent execution.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── Middleware ──────────────────────────────────────────────
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────
app.include_router(health.router, tags=["Health"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(node.router, prefix="/node", tags=["Node"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["Marketplace"])


@app.get("/", tags=["Root"])
def root():
    return {
        "node": settings.NODE_ID,
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }
