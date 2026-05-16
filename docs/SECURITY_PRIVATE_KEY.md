# 🔐 Private Key Security Guide

## ⚠️ CRITICAL: Never Commit Private Keys

Your private key is the master key to your smart contract deployment account. **NEVER** commit it to version control.

## Safe Storage

### ✅ DO

- ✅ Store in `.env` file (which is in `.gitignore`)
- ✅ Use environment variables in deployment scripts
- ✅ Rotate keys regularly
- ✅ Use hardware wallets for production
- ✅ Keep backups in secure location (encrypted)
- ✅ Use different keys for different networks

### ❌ DON'T

- ❌ Commit `.env` to Git
- ❌ Share private key in chat/email/Slack
- ❌ Hardcode in source files
- ❌ Store in plain text files
- ❌ Use same key for multiple networks
- ❌ Leave in browser console
- ❌ Screenshot or photograph

## Setup Instructions

### 1. Create `.env` from template

```bash
cp .env.example .env
```

### 2. Add your private key to `.env`

```bash
# .env (NEVER commit this file)
PRIVATE_KEY=0x41975126c6465e2d42bd75154867d75604fd67a2da40a91d2ab3489cac9186c8
```

### 3. Verify `.env` is in `.gitignore`

```bash
grep "^\.env$" .gitignore
# Should output: .env
```

### 4. Deploy safely

```bash
# Private key is loaded from .env automatically
npm run deploy:arc
```

## Deployment Script Security

The `scripts/deploy-secure.js` script:

1. ✅ Loads private key from `.env` only
2. ✅ Never logs the full private key
3. ✅ Validates network before deployment
4. ✅ Checks account balance
5. ✅ Saves deployment info securely
6. ✅ Verifies contract after deployment

```bash
# Safe deployment with validation
npm run deploy:arc
```

## If Private Key is Compromised

### Immediate Actions

1. **Stop all transactions** - Don't use the compromised key
2. **Revoke permissions** - If deployed to mainnet
3. **Create new key** - Generate new private key
4. **Redeploy** - Use new key for future deployments
5. **Notify team** - Alert all team members

### Recovery Steps

```bash
# 1. Generate new private key (using ethers.js)
node -e "console.log(require('ethers').Wallet.createRandom().privateKey)"

# 2. Update .env with new key
echo "PRIVATE_KEY=0xNEW_KEY_HERE" > .env

# 3. Deploy with new key
npm run deploy:arc

# 4. Verify new deployment
cat deployments/arc-testnet.json
```

## Production Security Checklist

- [ ] Private key stored in `.env` (not committed)
- [ ] `.env` is in `.gitignore`
- [ ] Different keys for testnet/mainnet
- [ ] Account has sufficient balance
- [ ] Deployment script validates environment
- [ ] Backup of private key in secure location
- [ ] Team knows security procedures
- [ ] Monitoring for unauthorized transactions

## Environment Variables Reference

```bash
# Required for deployment
PRIVATE_KEY=0x...          # Your deployer private key
ARC_RPC_URL=https://...    # Arc network RPC endpoint
ARC_CHAIN_ID=5042002       # Arc testnet chain ID

# Optional but recommended
ENVIRONMENT=production     # development|staging|production
LOG_LEVEL=INFO            # DEBUG|INFO|WARNING|ERROR
```

## Hardhat Configuration

The `hardhat.config.js` loads private key from environment:

```javascript
// hardhat.config.js
require("dotenv").config();

module.exports = {
  networks: {
    "arc-testnet": {
      url: process.env.ARC_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
      chainId: parseInt(process.env.ARC_CHAIN_ID),
    },
  },
};
```

## Emergency Contacts

If you suspect a security breach:

1. 📧 Email: security@orvion.io
2. 🚨 Discord: #security-incidents
3. 📞 Emergency: +1-XXX-XXX-XXXX

## Additional Resources

- [Hardhat Security Best Practices](https://hardhat.org/docs/guides/deploying)
- [Ethers.js Security](https://docs.ethers.org/v6/getting-started/)
- [OWASP Smart Contract Security](https://owasp.org/www-community/attacks/Smart_Contract_Weakness)

---

**Last Updated**: May 10, 2026  
**Status**: Production Ready ✅  
**Version**: 2.0.0
