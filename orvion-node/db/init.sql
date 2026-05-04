-- ORVION Database Schema

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  api_key VARCHAR(64) UNIQUE NOT NULL,
  wallet_address VARCHAR(66),
  plan VARCHAR(32) DEFAULT 'free',
  status VARCHAR(32) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- API Usage tracking
CREATE TABLE IF NOT EXISTS api_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  api_key VARCHAR(64) NOT NULL,
  endpoint VARCHAR(255),
  cost_usdc NUMERIC(18,6) DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  api_key VARCHAR(64) NOT NULL,
  tx_hash VARCHAR(128),
  amount_usdc NUMERIC(18,6),
  recipient VARCHAR(66),
  status VARCHAR(32) DEFAULT 'pending',
  chain VARCHAR(32) DEFAULT 'arc-testnet',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Billing records
CREATE TABLE IF NOT EXISTS billing_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  api_key VARCHAR(64) NOT NULL,
  period VARCHAR(7),
  total_calls INTEGER DEFAULT 0,
  total_cost_usdc NUMERIC(18,6) DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_api_key ON users(api_key);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_api_usage_api_key ON api_usage(api_key);
CREATE INDEX IF NOT EXISTS idx_api_usage_created_at ON api_usage(created_at);
CREATE INDEX IF NOT EXISTS idx_payments_api_key ON payments(api_key);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_payments_created_at ON payments(created_at);
CREATE INDEX IF NOT EXISTS idx_billing_records_api_key ON billing_records(api_key);
CREATE INDEX IF NOT EXISTS idx_billing_records_period ON billing_records(period);

-- Demo user
INSERT INTO users (email, api_key, plan, status)
VALUES ('demo@orvion.io', 'demo-api-key-12345', 'pro', 'active')
ON CONFLICT (email) DO NOTHING;

-- Demo user for testing
INSERT INTO users (email, api_key, plan, status)
VALUES ('test@orvion.io', 'test-api-key-67890', 'free', 'active')
ON CONFLICT (email) DO NOTHING;
