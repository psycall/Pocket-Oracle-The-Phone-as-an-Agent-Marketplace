from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def get_agent(db: Session, agent_id: str):
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

def get_agents(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    agent_type: Optional[str] = None,
    capabilities: Optional[List[str]] = None
):
    """
    Busca escalável de agentes com filtros avançados.
    """
    query = db.query(models.Agent)
    
    if agent_type:
        query = query.filter(models.Agent.agent_type == agent_type)
    
    if capabilities:
        for cap in capabilities:
            query = query.filter(models.Agent.capabilities.contains(cap))
            
    return query.order_by(models.Agent.reputation_score.desc()).offset(skip).limit(limit).all()

def create_agent(db: Session, agent: schemas.AgentCreate):
    db_agent = models.Agent(
        id=agent.id,
        agent_name=agent.agent_name,
        agent_type=agent.agent_type,
        capabilities=agent.capabilities,
        reputation_score=100.0, # Inicial padrão
        total_settlements=0
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def update_agent_reputation(db: Session, agent_id: str, score_delta: float):
    agent = get_agent(db, agent_id)
    if agent:
        agent.reputation_score = max(0, min(100, agent.reputation_score + score_delta))
        agent.total_settlements += 1
        db.commit()
    return agent
