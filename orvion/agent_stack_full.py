"""
Circle Agent Stack - Complete Integration
Agent Wallets, Marketplace, CLI, Nanopayments, and Skills
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal

logger = logging.getLogger(__name__)

class AgentRole(str, Enum):
    """Agent roles in the ecosystem"""
    SERVICE_PROVIDER = "service_provider"
    DATA_PROVIDER = "data_provider"
    COMPUTE_PROVIDER = "compute_provider"
    API_PROVIDER = "api_provider"
    CONSUMER = "consumer"

class SkillCategory(str, Enum):
    """Circle Skills categories"""
    PAYMENT_PROCESSING = "payment_processing"
    DATA_RETRIEVAL = "data_retrieval"
    COMPUTATION = "computation"
    SETTLEMENT = "settlement"
    VERIFICATION = "verification"
    ANALYTICS = "analytics"

class NanopaymentStatus(str, Enum):
    """Nanopayment lifecycle"""
    PENDING = "pending"
    PROCESSING = "processing"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    DISPUTED = "disputed"

@dataclass
class AgentWallet:
    """Agent Wallet for controlled USDC access"""
    agent_id: str
    wallet_address: str
    usdc_balance: Decimal = Decimal("0")
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_transaction: Optional[datetime] = None
    transaction_count: int = 0
    total_volume: Decimal = Decimal("0")
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "wallet_address": self.wallet_address,
            "usdc_balance": float(self.usdc_balance),
            "created_at": self.created_at.isoformat(),
            "last_transaction": self.last_transaction.isoformat() if self.last_transaction else None,
            "transaction_count": self.transaction_count,
            "total_volume": float(self.total_volume),
            "is_active": self.is_active,
        }

@dataclass
class AgentService:
    """Service offered in Agent Marketplace"""
    service_id: str
    provider_agent_id: str
    name: str
    description: str
    category: SkillCategory
    price_per_call: Decimal
    currency: str = "USDC"
    rating: float = 5.0
    call_count: int = 0
    uptime_percentage: float = 99.9
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "provider_agent_id": self.provider_agent_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "price_per_call": float(self.price_per_call),
            "currency": self.currency,
            "rating": self.rating,
            "call_count": self.call_count,
            "uptime_percentage": self.uptime_percentage,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
        }

@dataclass
class Nanopayment:
    """Nanopayment transaction"""
    payment_id: str
    from_agent_id: str
    to_agent_id: str
    service_id: str
    amount: Decimal
    currency: str = "USDC"
    status: NanopaymentStatus = NanopaymentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None
    tx_hash: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "payment_id": self.payment_id,
            "from_agent_id": self.from_agent_id,
            "to_agent_id": self.to_agent_id,
            "service_id": self.service_id,
            "amount": float(self.amount),
            "currency": self.currency,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "tx_hash": self.tx_hash,
            "metadata": self.metadata,
        }

@dataclass
class CircleSkill:
    """Circle Skill for agent capabilities"""
    skill_id: str
    name: str
    category: SkillCategory
    description: str
    enabled_agents: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "enabled_agents": self.enabled_agents,
            "created_at": self.created_at.isoformat(),
        }

class AgentStackFull:
    """
    Complete Circle Agent Stack Integration
    
    Features:
    - Agent Wallets for controlled USDC access
    - Agent Marketplace for service discovery
    - Nanopayments for machine-speed transactions
    - Circle Skills for agent capabilities
    - CLI-ready operations
    """
    
    def __init__(self):
        self.wallets: Dict[str, AgentWallet] = {}
        self.services: Dict[str, AgentService] = {}
        self.nanopayments: Dict[str, Nanopayment] = {}
        self.skills: Dict[str, CircleSkill] = {}
        self.transaction_history: List[Dict[str, Any]] = []
    
    # ============ Agent Wallets ============
    
    async def create_agent_wallet(
        self,
        agent_id: str,
        wallet_address: str,
        initial_balance: Decimal = Decimal("0"),
    ) -> AgentWallet:
        """Create a new agent wallet"""
        if agent_id in self.wallets:
            raise ValueError(f"Wallet for agent {agent_id} already exists")
        
        wallet = AgentWallet(
            agent_id=agent_id,
            wallet_address=wallet_address,
            usdc_balance=initial_balance,
        )
        self.wallets[agent_id] = wallet
        logger.info(f"Created wallet for agent {agent_id}: {wallet_address}")
        return wallet
    
    async def get_agent_wallet(self, agent_id: str) -> Optional[AgentWallet]:
        """Get agent wallet by ID"""
        return self.wallets.get(agent_id)
    
    async def fund_agent_wallet(
        self,
        agent_id: str,
        amount: Decimal,
    ) -> Dict[str, Any]:
        """Fund an agent wallet with USDC"""
        wallet = self.wallets.get(agent_id)
        if not wallet:
            raise ValueError(f"Wallet not found for agent {agent_id}")
        
        wallet.usdc_balance += amount
        wallet.last_transaction = datetime.utcnow()
        wallet.transaction_count += 1
        
        tx_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "type": "funding",
            "amount": float(amount),
            "new_balance": float(wallet.usdc_balance),
        }
        self.transaction_history.append(tx_record)
        
        logger.info(f"Funded wallet {agent_id} with {amount} USDC")
        return tx_record
    
    async def get_wallet_balance(self, agent_id: str) -> Decimal:
        """Get agent wallet balance"""
        wallet = self.wallets.get(agent_id)
        if not wallet:
            raise ValueError(f"Wallet not found for agent {agent_id}")
        return wallet.usdc_balance
    
    # ============ Agent Marketplace ============
    
    async def register_service(
        self,
        provider_agent_id: str,
        name: str,
        description: str,
        category: SkillCategory,
        price_per_call: Decimal,
    ) -> AgentService:
        """Register a service in the marketplace"""
        service_id = f"svc_{provider_agent_id}_{len(self.services)}"
        
        service = AgentService(
            service_id=service_id,
            provider_agent_id=provider_agent_id,
            name=name,
            description=description,
            category=category,
            price_per_call=price_per_call,
        )
        self.services[service_id] = service
        logger.info(f"Registered service {service_id} by {provider_agent_id}")
        return service
    
    async def discover_services(
        self,
        category: Optional[SkillCategory] = None,
        min_rating: float = 0.0,
    ) -> List[AgentService]:
        """Discover services in marketplace"""
        services = list(self.services.values())
        
        if category:
            services = [s for s in services if s.category == category]
        
        services = [s for s in services if s.rating >= min_rating and s.is_active]
        services.sort(key=lambda s: s.rating, reverse=True)
        
        return services
    
    async def get_service(self, service_id: str) -> Optional[AgentService]:
        """Get service details"""
        return self.services.get(service_id)
    
    async def rate_service(
        self,
        service_id: str,
        rating: float,
    ) -> Dict[str, Any]:
        """Rate a service (1-5 stars)"""
        service = self.services.get(service_id)
        if not service:
            raise ValueError(f"Service not found: {service_id}")
        
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        # Update rating (simple average)
        old_rating = service.rating
        service.rating = (service.rating * service.call_count + rating) / (service.call_count + 1)
        
        return {
            "service_id": service_id,
            "old_rating": old_rating,
            "new_rating": service.rating,
            "call_count": service.call_count,
        }
    
    # ============ Nanopayments ============
    
    async def create_nanopayment(
        self,
        from_agent_id: str,
        to_agent_id: str,
        service_id: str,
        amount: Decimal,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Nanopayment:
        """Create a nanopayment transaction"""
        # Validate sender has sufficient balance
        sender_wallet = self.wallets.get(from_agent_id)
        if not sender_wallet:
            raise ValueError(f"Sender wallet not found: {from_agent_id}")
        
        if sender_wallet.usdc_balance < amount:
            raise ValueError(f"Insufficient balance. Have {sender_wallet.usdc_balance}, need {amount}")
        
        # Validate service exists
        service = self.services.get(service_id)
        if not service:
            raise ValueError(f"Service not found: {service_id}")
        
        payment_id = f"np_{from_agent_id}_{to_agent_id}_{len(self.nanopayments)}"
        
        payment = Nanopayment(
            payment_id=payment_id,
            from_agent_id=from_agent_id,
            to_agent_id=to_agent_id,
            service_id=service_id,
            amount=amount,
            metadata=metadata or {},
        )
        self.nanopayments[payment_id] = payment
        
        logger.info(f"Created nanopayment {payment_id}: {amount} USDC")
        return payment
    
    async def confirm_nanopayment(
        self,
        payment_id: str,
        tx_hash: str,
    ) -> Dict[str, Any]:
        """Confirm a nanopayment on-chain"""
        payment = self.nanopayments.get(payment_id)
        if not payment:
            raise ValueError(f"Payment not found: {payment_id}")
        
        # Deduct from sender
        sender_wallet = self.wallets[payment.from_agent_id]
        sender_wallet.usdc_balance -= payment.amount
        sender_wallet.total_volume += payment.amount
        
        # Add to receiver
        receiver_wallet = self.wallets.get(payment.to_agent_id)
        if receiver_wallet:
            receiver_wallet.usdc_balance += payment.amount
            receiver_wallet.total_volume += payment.amount
        
        # Update payment
        payment.status = NanopaymentStatus.CONFIRMED
        payment.confirmed_at = datetime.utcnow()
        payment.tx_hash = tx_hash
        
        # Update service
        service = self.services[payment.service_id]
        service.call_count += 1
        
        tx_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "nanopayment",
            "payment_id": payment_id,
            "from": payment.from_agent_id,
            "to": payment.to_agent_id,
            "amount": float(payment.amount),
            "tx_hash": tx_hash,
        }
        self.transaction_history.append(tx_record)
        
        logger.info(f"Confirmed nanopayment {payment_id}")
        return payment.to_dict()
    
    async def get_nanopayment(self, payment_id: str) -> Optional[Nanopayment]:
        """Get nanopayment details"""
        return self.nanopayments.get(payment_id)
    
    # ============ Circle Skills ============
    
    async def register_skill(
        self,
        name: str,
        category: SkillCategory,
        description: str,
    ) -> CircleSkill:
        """Register a Circle Skill"""
        skill_id = f"skill_{len(self.skills)}"
        
        skill = CircleSkill(
            skill_id=skill_id,
            name=name,
            category=category,
            description=description,
        )
        self.skills[skill_id] = skill
        logger.info(f"Registered skill {skill_id}: {name}")
        return skill
    
    async def enable_skill_for_agent(
        self,
        skill_id: str,
        agent_id: str,
    ) -> Dict[str, Any]:
        """Enable a skill for an agent"""
        skill = self.skills.get(skill_id)
        if not skill:
            raise ValueError(f"Skill not found: {skill_id}")
        
        if agent_id not in skill.enabled_agents:
            skill.enabled_agents.append(agent_id)
        
        logger.info(f"Enabled skill {skill_id} for agent {agent_id}")
        return {
            "skill_id": skill_id,
            "agent_id": agent_id,
            "enabled_agents": skill.enabled_agents,
        }
    
    async def get_agent_skills(self, agent_id: str) -> List[CircleSkill]:
        """Get all skills enabled for an agent"""
        return [s for s in self.skills.values() if agent_id in s.enabled_agents]
    
    # ============ Analytics & Reporting ============
    
    async def get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive agent statistics"""
        wallet = self.wallets.get(agent_id)
        if not wallet:
            raise ValueError(f"Agent not found: {agent_id}")
        
        # Services provided
        provided_services = [s for s in self.services.values() if s.provider_agent_id == agent_id]
        
        # Nanopayments sent/received
        payments_sent = [p for p in self.nanopayments.values() if p.from_agent_id == agent_id]
        payments_received = [p for p in self.nanopayments.values() if p.to_agent_id == agent_id]
        
        # Skills enabled
        skills = await self.get_agent_skills(agent_id)
        
        return {
            "agent_id": agent_id,
            "wallet": wallet.to_dict(),
            "services_provided": len(provided_services),
            "total_service_calls": sum(s.call_count for s in provided_services),
            "avg_service_rating": sum(s.rating for s in provided_services) / len(provided_services) if provided_services else 0,
            "payments_sent": len(payments_sent),
            "payments_received": len(payments_received),
            "total_spent": float(sum(p.amount for p in payments_sent if p.status == NanopaymentStatus.CONFIRMED)),
            "total_earned": float(sum(p.amount for p in payments_received if p.status == NanopaymentStatus.CONFIRMED)),
            "skills_enabled": len(skills),
            "transaction_count": wallet.transaction_count,
        }
    
    async def get_marketplace_stats(self) -> Dict[str, Any]:
        """Get marketplace statistics"""
        active_services = [s for s in self.services.values() if s.is_active]
        confirmed_payments = [p for p in self.nanopayments.values() if p.status == NanopaymentStatus.CONFIRMED]
        
        total_volume = sum(p.amount for p in confirmed_payments)
        
        return {
            "total_services": len(self.services),
            "active_services": len(active_services),
            "total_agents": len(self.wallets),
            "total_nanopayments": len(self.nanopayments),
            "confirmed_payments": len(confirmed_payments),
            "total_volume_usdc": float(total_volume),
            "avg_service_price": float(sum(s.price_per_call for s in active_services) / len(active_services)) if active_services else 0,
            "avg_service_rating": sum(s.rating for s in active_services) / len(active_services) if active_services else 0,
        }
    
    async def get_transaction_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get transaction history"""
        return self.transaction_history[-limit:]

# Singleton instance
_agent_stack: Optional[AgentStackFull] = None

def get_agent_stack() -> AgentStackFull:
    """Get or create Agent Stack instance"""
    global _agent_stack
    if _agent_stack is None:
        _agent_stack = AgentStackFull()
    return _agent_stack
