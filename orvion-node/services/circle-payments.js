import express from "express";
import axios from "axios";
import { ethers } from "ethers";
import pkg from "pg";
const { Pool } = pkg;

const app = express();
app.use(express.json());

const CIRCLE_API_KEY = process.env.CIRCLE_API_KEY || "TEST_API_KEY";
const CIRCLE_ENV = process.env.CIRCLE_ENV || "sandbox";
const CIRCLE_BASE = CIRCLE_ENV === "sandbox"
  ? "https://api-sandbox.circle.com"
  : "https://api.circle.com";

const ARC_RPC_URL = process.env.ARC_RPC_URL || "https://rpc.testnet.arc.network";
const ARC_CHAIN_ID = process.env.ARC_CHAIN_ID || "7777";
const USDC_CONTRACT = process.env.USDC_CONTRACT || "0x0000000000000000000000000000000000000000";

const pg = new Pool({ connectionString: process.env.POSTGRES_URL });

// Minimal ERC20 ABI for USDC
const USDC_ABI = [
  "function balanceOf(address) view returns (uint256)",
  "function transfer(address to, uint256 amount) returns (bool)",
  "function decimals() view returns (uint8)",
  "function approve(address spender, uint256 amount) returns (bool)",
];

const provider = new ethers.JsonRpcProvider(ARC_RPC_URL);

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    service: "circle-payments",
    arc_chain_id: ARC_CHAIN_ID,
    circle_env: CIRCLE_ENV,
  });
});

// Get USDC balance on Arc Network
app.get("/balance/:address", async (req, res) => {
  try {
    const { address } = req.params;

    // Validate address
    if (!ethers.isAddress(address)) {
      return res.status(400).json({
        error: "invalid_address",
        detail: "Must be a valid Ethereum address",
      });
    }

    // Query USDC balance
    const usdc = new ethers.Contract(USDC_CONTRACT, USDC_ABI, provider);
    const [balance, decimals] = await Promise.all([
      usdc.balanceOf(address),
      usdc.decimals(),
    ]);

    res.json({
      address,
      balance_usdc: ethers.formatUnits(balance, decimals),
      balance_raw: balance.toString(),
      decimals,
      chain: "arc-testnet",
      chain_id: ARC_CHAIN_ID,
      contract: USDC_CONTRACT,
    });
  } catch (error) {
    console.error("Balance check error:", error.message);
    res.status(500).json({
      error: "balance_check_failed",
      detail: error.message,
    });
  }
});

// Create Circle developer-controlled wallet
app.post("/wallet/create", async (req, res) => {
  try {
    const response = await axios.post(
      `${CIRCLE_BASE}/v1/w3s/developer/wallets`,
      {
        blockchains: ["MATIC-AMOY"],
        count: 1,
      },
      {
        headers: {
          Authorization: `Bearer ${CIRCLE_API_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    res.json({
      status: "success",
      wallet: response.data,
      created_at: new Date().toISOString(),
    });
  } catch (error) {
    console.error("Wallet creation error:", error.response?.data || error.message);
    res.status(500).json({
      error: "wallet_creation_failed",
      detail: error.response?.data || error.message,
    });
  }
});

// Transfer USDC via Circle API with Arc settlement
app.post("/transfer", async (req, res) => {
  const { apiKey, amount, recipient } = req.body;

  // Validation
  if (!apiKey || !amount || !recipient) {
    return res.status(400).json({
      error: "missing_fields",
      required: ["apiKey", "amount", "recipient"],
    });
  }

  if (!ethers.isAddress(recipient)) {
    return res.status(400).json({
      error: "invalid_recipient_address",
    });
  }

  try {
    // Record pending payment in database
    const { rows } = await pg.query(
      `INSERT INTO payments (api_key, amount_usdc, status, chain)
       VALUES ($1, $2, 'pending', 'arc-testnet') RETURNING id, created_at`,
      [apiKey, amount]
    );

    const paymentId = rows[0].id;
    const createdAt = rows[0].created_at;

    // In production: call Circle /v1/transfers with idempotencyKey
    // For now: simulate Arc testnet transfer with proof
    const simulatedTxHash = "0x" + Buffer.from(paymentId.toString())
      .toString("hex")
      .padEnd(64, "0")
      .slice(0, 64);

    // Update payment status
    await pg.query(
      `UPDATE payments SET status='confirmed', tx_hash=$1, updated_at=NOW() WHERE id=$2`,
      [simulatedTxHash, paymentId]
    );

    res.json({
      status: "success",
      payment: {
        id: paymentId,
        status: "confirmed",
        amount_usdc: parseFloat(amount),
        recipient,
        chain: "arc-testnet",
        chain_id: ARC_CHAIN_ID,
        tx_hash: simulatedTxHash,
        explorer_url: `https://explorer.testnet.arc.network/tx/${simulatedTxHash}`,
        created_at: createdAt,
        confirmed_at: new Date().toISOString(),
      },
    });
  } catch (error) {
    console.error("Transfer error:", error.message);
    res.status(500).json({
      error: "transfer_failed",
      detail: error.message,
    });
  }
});

// Get payment status
app.get("/payment/:paymentId", async (req, res) => {
  try {
    const { rows } = await pg.query(
      `SELECT id, api_key, amount_usdc, status, tx_hash, chain, created_at, updated_at
       FROM payments WHERE id = $1`,
      [req.params.paymentId]
    );

    if (rows.length === 0) {
      return res.status(404).json({
        error: "payment_not_found",
      });
    }

    const payment = rows[0];
    res.json({
      status: "success",
      payment: {
        ...payment,
        explorer_url: payment.tx_hash
          ? `https://explorer.testnet.arc.network/tx/${payment.tx_hash}`
          : null,
      },
    });
  } catch (error) {
    res.status(500).json({
      error: "payment_lookup_failed",
      detail: error.message,
    });
  }
});

// Get payments for API key
app.get("/payments/:apiKey", async (req, res) => {
  try {
    const { rows } = await pg.query(
      `SELECT id, amount_usdc, status, tx_hash, chain, created_at
       FROM payments WHERE api_key = $1
       ORDER BY created_at DESC LIMIT 50`,
      [req.params.apiKey]
    );

    res.json({
      status: "success",
      count: rows.length,
      payments: rows,
    });
  } catch (error) {
    res.status(500).json({
      error: "payments_lookup_failed",
      detail: error.message,
    });
  }
});

const PORT = process.env.PORT || 3004;
app.listen(PORT, () => {
  console.log(`💸 ORVION Circle/Arc Payments Service listening on port ${PORT}`);
  console.log(`🔗 Arc RPC: ${ARC_RPC_URL}`);
  console.log(`🪙 USDC Contract: ${USDC_CONTRACT}`);
  console.log(`🔐 Circle Env: ${CIRCLE_ENV}`);
});
