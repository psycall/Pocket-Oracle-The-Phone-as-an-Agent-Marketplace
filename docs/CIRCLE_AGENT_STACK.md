# Circle Agent Stack Integration

ORVION now integrates with Circle's latest Agent Stack kits, providing cutting-edge cross-chain settlement capabilities.

## 🆕 What's New (Latest Releases)

### New Chain Support
- **Injective** - Mainnet and testnet USDC transfers via CCTP v2
- **Pharos** - Mainnet and testnet bridging support
- **Sei** - Updated chain registry with correct block explorers

### New Features
- **cirBTC Swaps** - Live on Arc Testnet (USDC ↔ cirBTC)
- **Error Telemetry** - Machine-readable error categories for better UX
- **Fallback RPC** - Circle Wallets now fallback to local RPC when hosted RPC fails
- **Improved Error Handling** - Distinguish user rejections, wallet capability errors, and on/off-chain failures

## 📦 Supported Chains

### CCTP v2 Routes
```
Ethereum ↔ Arc
Polygon ↔ Injective
Arc ↔ Pharos
Arc ↔ Sei
Ethereum ↔ Polygon
Arbitrum ↔ Optimism
Avalanche ↔ Ethereum
Solana ↔ Ethereum
Stellar ↔ Ethereum
Flow ↔ Ethereum
Near ↔ Ethereum
Noble ↔ Ethereum
```

### Token Support
- **USDC** - Universal stablecoin
- **USDC.e** - Ethereum-bridged variant
- **cirBTC** - Bitcoin-backed stablecoin (Arc Testnet)

## 🔌 API Endpoints

### Get Supported Chains
```bash
GET /api/v1/circle/chains
```

Response:
```json
[
  "ethereum",
  "polygon",
  "arbitrum",
  "optimism",
  "avalanche",
  "solana",
  "stellar",
  "flow",
  "near",
  "noble",
  "arc",
  "pharos",
  "injective",
  "sei"
]
```

### Get Available Routes
```bash
GET /api/v1/circle/routes
```

Response:
```json
[
  {
    "source_chain": "ethereum",
    "destination_chain": "arc",
    "token": "USDC",
    "min_amount": 1,
    "max_amount": 1000000,
    "estimated_time_seconds": 300
  }
]
```

### Estimate Bridge Transfer
```bash
POST /api/v1/circle/estimate-bridge
Content-Type: application/json

{
  "source_chain": "ethereum",
  "destination_chain": "arc",
  "token": "USDC",
  "amount": 1000
}
```

Response:
```json
{
  "source_chain": "ethereum",
  "destination_chain": "arc",
  "token": "USDC",
  "amount": 1000,
  "estimated_fee": 1.5,
  "estimated_receive": 998.5,
  "estimated_time_seconds": 300,
  "route_available": true
}
```

### Execute Bridge Transfer
```bash
POST /api/v1/circle/bridge
Content-Type: application/json

{
  "source_chain": "ethereum",
  "destination_chain": "arc",
  "amount": 1000,
  "recipient_address": "0x...",
  "wallet_type": "evm"
}
```

Wallet types:
- `evm` - Ethereum, Polygon, Arbitrum, Optimism, Avalanche, Arc, Pharos, Sei
- `solana` - Solana blockchain
- `circle` - Circle Wallets (with fallback RPC)

Response:
```json
{
  "success": true,
  "tx_hash": "0x...",
  "status": "pending",
  "source_chain": "ethereum",
  "destination_chain": "arc",
  "amount": 1000
}
```

### Swap cirBTC (Arc Testnet)
```bash
POST /api/v1/circle/swap-cirbtc
Content-Type: application/json

{
  "from_token": "USDC",
  "to_token": "cirBTC",
  "amount": 100,
  "recipient_address": "0x..."
}
```

Response:
```json
{
  "success": true,
  "tx_hash": "0x...",
  "from_token": "USDC",
  "to_token": "cirBTC",
  "input_amount": 100,
  "output_amount": 99,
  "slippage": 0.01
}
```

### Get Bridge History
```bash
GET /api/v1/circle/bridge-history?limit=50
```

### Get Error Telemetry
```bash
GET /api/v1/circle/error-telemetry
```

Response:
```json
{
  "total_errors": 5,
  "errors_by_category": {
    "USER_REJECTION": 2,
    "WALLET_CAPABILITY": 1,
    "OFFCHAIN_FAILURE": 1,
    "ONCHAIN_FAILURE": 1,
    "UNKNOWN": 0
  },
  "recent_errors": [
    {
      "category": "USER_REJECTION",
      "message": "User rejected transaction",
      "timestamp": "2026-05-11T20:30:00"
    }
  ]
}
```

## 🛡️ Error Handling

The Circle Agent Stack provides machine-readable error categories:

```python
from orvion.circle_agent_stack import ErrorCategory

# USER_REJECTION - User rejected the transaction
# WALLET_CAPABILITY - Wallet doesn't support the operation
# OFFCHAIN_FAILURE - Off-chain service error (API, RPC)
# ONCHAIN_FAILURE - On-chain transaction failure
# UNKNOWN - Unknown error
```

Example error handling:

```python
try:
    await bridge_usdc(...)
except BridgeError as e:
    if e.error_category == ErrorCategory.USER_REJECTION:
        # Show user-friendly message
        print("Transaction cancelled by user")
    elif e.error_category == ErrorCategory.WALLET_CAPABILITY:
        # Suggest alternative wallet
        print("Your wallet doesn't support this chain")
    elif e.error_category == ErrorCategory.OFFCHAIN_FAILURE:
        # Retry with backoff
        print("Service temporarily unavailable, retrying...")
    elif e.error_category == ErrorCategory.ONCHAIN_FAILURE:
        # Show transaction error
        print(f"Transaction failed: {e.message}")
```

## 📊 Telemetry

Error telemetry is enabled by default but collects **no sensitive data**:

✅ Collected:
- Error type/category
- SDK name and version
- Source/destination chains
- Token symbol

❌ Not collected:
- Error messages or stack traces
- Wallet addresses
- Transaction data
- User information

Opt out by setting `enable_telemetry=False`:

```python
from orvion.circle_agent_stack import CircleAgentStack

stack = CircleAgentStack(enable_telemetry=False)
```

## 🚀 Python SDK Usage

```python
from orvion.circle_agent_stack import get_circle_stack, Chain, Token

stack = get_circle_stack()

# Get available routes
routes = stack.get_available_routes()
print(f"Available routes: {len(routes)}")

# Estimate bridge
estimate = await stack.estimate_bridge(
    Chain.ETHEREUM,
    Chain.ARC,
    Token.USDC,
    1000
)
print(f"Fee: {estimate['estimated_fee']} USDC")

# Execute bridge
result = await stack.bridge_usdc(
    Chain.ETHEREUM,
    Chain.ARC,
    1000,
    "0x...",
    wallet_type="evm"
)
print(f"TX: {result['tx_hash']}")

# Swap cirBTC
swap = await stack.swap_cirbtc(
    Token.USDC,
    Token.CIRC_BTC,
    100,
    "0x..."
)
print(f"Received: {swap['output_amount']} cirBTC")

# Get telemetry
telemetry = stack.get_error_telemetry()
print(f"Total errors: {telemetry['total_errors']}")
```

## 🔗 Integration with ORVION Settlements

The Circle Agent Stack is integrated into ORVION's settlement engine:

```python
from orvion.settlement_engine import SettlementEngine
from orvion.circle_agent_stack import Chain

engine = SettlementEngine()

# Settlements automatically use Circle Agent Stack for transfers
settlement = await engine.settle_job(
    job_id="job-123",
    source_chain=Chain.ETHEREUM,
    destination_chain=Chain.ARC,
    amount=1000,
    recipient="0x..."
)
```

## 📚 References

- [Circle Agent Stack Quickstart](https://community.arc.network/home/videos/introducing-circle-agent-stack-quickstart)
- [Circle Bridge Kit Docs](https://developers.circle.com/stablecoins/docs/bridge-kit)
- [Circle App Kit Docs](https://developers.circle.com/stablecoins/docs/app-kit)
- [CCTP v2 Documentation](https://developers.circle.com/stablecoins/docs/cctp-v2)

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.10.0+ | 2026-05-11 | Injective, Pharos, cirBTC support |
| 1.9.0 | 2026-05-10 | Pharos bridging, error categories |
| 1.8.0 | 2026-05-09 | Fallback RPC for Circle Wallets |
| 1.7.0+ | 2026-05-08 | Error telemetry, Sei support |
