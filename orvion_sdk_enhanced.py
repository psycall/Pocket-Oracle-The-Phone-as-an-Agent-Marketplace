# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Enhanced ORVION Agent SDK with retry logic, logging, and type hints.
Production-grade Python SDK for interacting with ORVION Settlement Layer.
"""

import logging
import time
from typing import Dict, Any, Optional, List
from functools import wraps

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries: int = 3, backoff_factor: float = 0.5):
    """
    Decorator for automatic retry with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Backoff multiplier (5s, 30s, 5m)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed after {max_retries} attempts: {str(e)}")
                        raise
                    
                    # Exponential backoff: 5s, 30s, 5m
                    delays = [5, 30, 300]
                    delay = delays[attempt] if attempt < len(delays) else delays[-1]
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}")
                    time.sleep(delay)
        return wrapper
    return decorator


class OrvionAgentSDK:
    """
    Production-grade SDK for AI Agents to interact with the ORVION Settlement Layer.
    
    Features:
    - Automatic retry with exponential backoff
    - Built-in logging and error handling
    - Type hints for IDE support
    - Configurable timeouts
    - Session pooling for performance
    
    Example:
        sdk = OrvionAgentSDK(
            base_url="https://api.orvion.io",
            api_token="your-token",
            timeout=30
        )
        agent = sdk.register_agent({
            "agent_address": "0x...",
            "agent_name": "MyAgent",
            "agent_type": "processor"
        })
    """
    
    DEFAULT_TIMEOUT = 30  # seconds
    DEFAULT_MAX_RETRIES = 3
    
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_token: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        log_level: str = "INFO"
    ):
        """
        Initialize ORVION Agent SDK.
        
        Args:
            base_url: Base URL of ORVION API
            api_token: Optional API token for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.base_url = base_url
        self.api_token = api_token
        self.timeout = timeout
        self.max_retries = max_retries
        self.api_v1 = f"{base_url}/api/v1"
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup session with retry strategy
        self.session = self._create_session()
        
        self.logger.info(f"ORVION SDK initialized: {base_url}")
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry strategy."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "OrvionAgentSDK/2.0"
        }
        
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        
        return headers
    
    @retry_on_failure(max_retries=3)
    def register_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register the agent in the ORVION Discovery Registry.
        
        Args:
            agent_data: Agent information (address, name, type, capabilities, etc.)
            
        Returns:
            Registered agent details with ID
            
        Raises:
            requests.RequestException: If registration fails after retries
            
        Example:
            agent = sdk.register_agent({
                "agent_address": "0x1234...",
                "agent_name": "DataProcessor",
                "agent_type": "processor",
                "capabilities": ["data_processing", "validation"],
                "pricing_per_call": 0.5
            })
        """
        url = f"{self.api_v1}/discovery/agents"
        
        self.logger.info(f"Registering agent: {agent_data.get('agent_name', 'Unknown')}")
        
        response = self.session.post(
            url,
            json=agent_data,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        self.logger.info(f"Agent registered successfully: {result.get('id')}")
        
        return result
    
    @retry_on_failure(max_retries=3)
    def create_job_and_escrow(
        self,
        agent_id: str,
        job_id: str,
        amount: float,
        to_address: str
    ) -> Dict[str, Any]:
        """
        Initiate a job and escrow funds in USDC.
        
        Args:
            agent_id: ID of the agent to execute the job
            job_id: Unique job identifier
            amount: Amount in USDC to escrow
            to_address: Ethereum address to receive payment
            
        Returns:
            Settlement details with ID and status
            
        Raises:
            requests.RequestException: If creation fails after retries
            
        Example:
            settlement = sdk.create_job_and_escrow(
                agent_id="agent-123",
                job_id="job-456",
                amount=100.50,
                to_address="0xabcd..."
            )
        """
        url = f"{self.api_v1}/settlement/settlements"
        
        data = {
            "agent_id": agent_id,
            "job_id": job_id,
            "amount": amount,
            "to_address": to_address
        }
        
        self.logger.info(f"Creating job: {job_id} for agent {agent_id} (amount: {amount} USDC)")
        
        response = self.session.post(
            url,
            json=data,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        self.logger.info(f"Job created: {result.get('id')} (status: {result.get('status')})")
        
        return result
    
    @retry_on_failure(max_retries=3)
    def submit_proof_of_work(
        self,
        job_id: str,
        proof_hash: str
    ) -> Dict[str, Any]:
        """
        Submit execution receipt to trigger verification and payment release.
        
        Args:
            job_id: Job ID to submit proof for
            proof_hash: IPFS hash or proof of execution
            
        Returns:
            Receipt details with verification status
            
        Raises:
            requests.RequestException: If submission fails after retries
            
        Example:
            receipt = sdk.submit_proof_of_work(
                job_id="job-456",
                proof_hash="QmProof..."
            )
        """
        url = f"{self.api_v1}/settlement/execution-receipts"
        
        data = {
            "job_id": job_id,
            "proof": proof_hash
        }
        
        self.logger.info(f"Submitting proof for job: {job_id}")
        
        response = self.session.post(
            url,
            json=data,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        self.logger.info(f"Proof submitted: {result.get('id')} (verified: {result.get('verified')})")
        
        return result
    
    @retry_on_failure(max_retries=3)
    def get_status(self, settlement_id: str) -> Dict[str, Any]:
        """
        Check the status of a settlement.
        
        Args:
            settlement_id: Settlement ID to check
            
        Returns:
            Settlement details including status and transaction hash
            
        Raises:
            requests.RequestException: If request fails after retries
            
        Example:
            status = sdk.get_status("settlement-789")
        """
        url = f"{self.api_v1}/settlement/settlements/{settlement_id}"
        
        self.logger.debug(f"Checking status for settlement: {settlement_id}")
        
        response = self.session.get(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        self.logger.debug(f"Settlement status: {result.get('status')}")
        
        return result
    
    def get_agent_reputation(self, agent_id: str, days: Optional[int] = None) -> Dict[str, Any]:
        """
        Get reputation score for an agent.
        
        Args:
            agent_id: Agent ID
            days: Optional time window (None = all time)
            
        Returns:
            Reputation score and breakdown
        """
        url = f"{self.api_v1}/agents/{agent_id}/reputation-score"
        params = {}
        if days:
            params["days"] = days
        
        self.logger.info(f"Fetching reputation for agent: {agent_id}")
        
        response = self.session.get(
            url,
            params=params,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        
        return response.json()
    
    def submit_feedback(
        self,
        agent_id: str,
        score: float,
        comment: Optional[str] = None,
        settlement_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit feedback about an agent.
        
        Args:
            agent_id: Agent ID
            score: Feedback score (0-5)
            comment: Optional comment
            settlement_id: Optional settlement ID
            
        Returns:
            Feedback record
        """
        if not (0 <= score <= 5):
            raise ValueError("Feedback score must be between 0 and 5")
        
        url = f"{self.api_v1}/agents/{agent_id}/feedback"
        
        data = {
            "score": score,
            "comment": comment,
            "settlement_id": settlement_id
        }
        
        self.logger.info(f"Submitting feedback for agent {agent_id}: {score}/5")
        
        response = self.session.post(
            url,
            json=data,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        
        return response.json()
    
    def get_top_agents(
        self,
        agent_type: Optional[str] = None,
        min_reputation: float = 0.0,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get top-rated agents.
        
        Args:
            agent_type: Optional filter by agent type
            min_reputation: Minimum reputation score
            limit: Max agents to return
            
        Returns:
            List of top-rated agents
        """
        url = f"{self.api_v1}/agents/top-rated"
        
        params = {
            "limit": limit,
            "min_reputation": min_reputation
        }
        if agent_type:
            params["agent_type"] = agent_type
        
        self.logger.info(f"Fetching top {limit} agents")
        
        response = self.session.get(
            url,
            params=params,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        
        return response.json()
    
    def close(self) -> None:
        """Close the session and cleanup resources."""
        self.session.close()
        self.logger.info("SDK session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
