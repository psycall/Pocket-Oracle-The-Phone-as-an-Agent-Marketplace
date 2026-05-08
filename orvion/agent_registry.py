
from typing import List, Optional
from uuid import uuid4
from sqlalchemy.orm import Session
from . import models, schemas

def create_agent(db: Session, agent: schemas.AgentCreate):
    db_agent = models.Agent(
        id=str(uuid4()),
        agent_address=agent.agent_address,
        agent_name=agent.agent_name,
        agent_type=agent.agent_type,
        capabilities=",".join(agent.capabilities) if agent.capabilities else None,
        pricing_per_call=agent.pricing_per_call,
        endpoint_url=agent.endpoint_url,
        settlement_address=agent.settlement_address,
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def get_agent(db: Session, agent_id: str):
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

def get_agents(db: Session, skip: int = 0, limit: int = 100, agent_type: Optional[str] = None, capabilities: Optional[List[str]] = None):
    query = db.query(models.Agent)
    if agent_type:
        query = query.filter(models.Agent.agent_type == agent_type)
    if capabilities:
        for cap in capabilities:
            query = query.filter(models.Agent.capabilities.contains(cap))
    return query.offset(skip).limit(limit).all()

def update_agent(db: Session, agent_id: str, agent: schemas.AgentUpdate):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if db_agent:
        for key, value in agent.dict(exclude_unset=True).items():
            if key == "capabilities" and value is not None:
                setattr(db_agent, key, ",".join(value))
            elif value is not None:
                setattr(db_agent, key, value)
        db.commit()
        db.refresh(db_agent)
    return db_agent

def delete_agent(db: Session, agent_id: str):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if db_agent:
        db.delete(db_agent)
        db.commit()
    return db_agent
