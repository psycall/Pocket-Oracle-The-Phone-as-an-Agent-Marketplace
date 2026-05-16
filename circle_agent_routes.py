"""
Circle Agent Stack API Routes
Endpoints for CCTP v2 bridging, cirBTC swaps, and error telemetry
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from orvion.circle_agent_stack import (
    get_circle_stack,
    Chain,
    Token,
    ErrorCategory,
)

router = APIRouter(prefix="/api/v1/circle", tags=["Circle Agent Stack"])

# Request/Response Models
class EstimateBridgeRequest(BaseModel):
    source_chain: str
    destination_chain: str
    token: str = "USDC"
    amount: float = Field(..., gt=0)

class BridgeRequest(BaseModel):
    source_chain: str
    destination_chain: str
    amount: float = Field(..., gt=0)
    recipient_address: str
    wallet_type: str = "evm"

class SwapRequest(BaseModel):
    from_token: str
    to_token: str
    amount: float = Field(..., gt=0)
    recipient_address: str

class BridgeResponse(BaseModel):
    success: bool
    tx_hash: str
    status: str
    source_chain: str
    destination_chain: str
    amount: float

class SwapResponse(BaseModel):
    success: bool
    tx_hash: str
    from_token: str
    to_token: str
    input_amount: float
    output_amount: float
    slippage: float

class RouteInfo(BaseModel):
    source_chain: str
    destination_chain: str
    token: str
    min_amount: float
    max_amount: float
    estimated_time_seconds: int

class ErrorTelemetry(BaseModel):
    total_errors: int
    errors_by_category: dict
    recent_errors: list

@router.get("/chains", response_model=List[str])
async def get_supported_chains():
    """Get all supported chains"""
    stack = get_circle_stack()
    return stack.get_supported_chains()

@router.get("/tokens", response_model=List[str])
async def get_supported_tokens():
    """Get all supported tokens"""
    stack = get_circle_stack()
    return stack.get_supported_tokens()

@router.get("/routes", response_model=List[RouteInfo])
async def get_available_routes():
    """Get all available CCTP v2 bridge routes"""
    stack = get_circle_stack()
    routes = stack.get_available_routes()
    return [
        RouteInfo(
            source_chain=route.source_chain.value,
            destination_chain=route.destination_chain.value,
            token=route.token.value,
            min_amount=route.min_amount,
            max_amount=route.max_amount,
            estimated_time_seconds=route.estimated_time_seconds,
        )
        for route in routes
    ]

@router.post("/estimate-bridge")
async def estimate_bridge(request: EstimateBridgeRequest):
    """
    Estimate bridge transfer with fees and time
    
    Supports:
    - Injective (NEW)
    - Pharos (NEW)
    - Sei
    - Arc, Ethereum, Polygon, Arbitrum, Optimism, Avalanche
    - Solana, Stellar, Flow, Near, Noble
    """
    try:
        stack = get_circle_stack()
        source = Chain(request.source_chain.lower())
        destination = Chain(request.destination_chain.lower())
        token = Token(request.token.upper())
        
        estimate = await stack.estimate_bridge(
            source, destination, token, request.amount
        )
        return estimate
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bridge", response_model=BridgeResponse)
async def bridge_usdc(request: BridgeRequest):
    """
    Execute USDC bridge transfer via CCTP v2
    
    New features:
    - Injective mainnet/testnet support
    - Pharos bridging (mainnet/testnet)
    - Fallback RPC for Circle Wallets
    - Machine-readable error categories
    """
    try:
        stack = get_circle_stack()
        source = Chain(request.source_chain.lower())
        destination = Chain(request.destination_chain.lower())
        
        result = await stack.bridge_usdc(
            source,
            destination,
            request.amount,
            request.recipient_address,
            request.wallet_type,
        )
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/swap-cirbtc", response_model=SwapResponse)
async def swap_cirbtc(request: SwapRequest):
    """
    Swap cirBTC on Arc Testnet (NEW)
    
    Supported pairs:
    - USDC ↔ cirBTC
    """
    try:
        stack = get_circle_stack()
        from_token = Token(request.from_token.upper())
        to_token = Token(request.to_token.upper())
        
        result = await stack.swap_cirbtc(
            from_token,
            to_token,
            request.amount,
            request.recipient_address,
        )
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bridge-history")
async def get_bridge_history(limit: int = 50):
    """Get bridge transaction history"""
    stack = get_circle_stack()
    return stack.get_bridge_history(limit)

@router.get("/error-telemetry", response_model=ErrorTelemetry)
async def get_error_telemetry():
    """
    Get error telemetry data
    
    Note: No sensitive data collected
    - Error messages, stack traces, wallet addresses, tx data stay on client
    - Only collects: error type, SDK version, chains, token symbol
    """
    stack = get_circle_stack()
    return stack.get_error_telemetry()

@router.get("/health")
async def health_check():
    """Health check for Circle Agent Stack"""
    stack = get_circle_stack()
    return {
        "status": "healthy",
        "service": "Circle Agent Stack",
        "supported_chains": len(stack.get_supported_chains()),
        "supported_tokens": len(stack.get_supported_tokens()),
        "available_routes": len(stack.get_available_routes()),
        "telemetry_enabled": stack.enable_telemetry,
    }
