// Pocket Oracle — Backend
// Decentralized agent marketplace powered by mobile devices.
// Stack: Node.js + Express + Ethers v6 + Circle USDC API

import express from "express";
import fetch from "node-fetch";
import dotenv from "dotenv";
import { ethers } from "ethers";
import crypto from "crypto";

dotenv.config();

/* =========================================================
   ENV VALIDATION
   ========================================================= */
const REQUIRED_ENV = [
  "CIRCLE_API_KEY",
  "RPC_URL",
  "PRIVATE_KEY",
  "CONTRACT_ADDRESS",
  "SOURCE_WALLET_ID",
  "AGENT_ADDRESS",
];

for (const key of REQUIRED_ENV) {
  if (!process.env[key]) {
    console.error(`[BOOT] Missing environment variable: ${key}`);
    process.exit(1);
  }
}

/* =========================================================
   APP INIT
   ========================================================= */
const app = express();

// Capture raw body for HMAC verification on /webhook
app.use(
  express.json({
    verify: (req, _res, buf) => {
      req.rawBody = buf;
    },
  })
);

const PORT = process.env.PORT || 3000;
const CIRCLE_BASE = process.env.CIRCLE_BASE || "https://api-sandbox.circle.com";
const CIRCLE_API_KEY = process.env.CIRCLE_API_KEY;
const CIRCLE_WEBHOOK_SECRET = process.env.CIRCLE_WEBHOOK_SECRET || "";
const TASK_VALUE_ETH = process.env.TASK_VALUE_ETH || "0.01";

const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

const ABI = [
  "function createTask(address _agent) external payable",
  "function completeTask(uint _id) external",
  "function releasePayment(uint _id) external",
  "function tasks(uint) view returns (address client, address agent, uint256 value, bool completed, bool paid)",
  "function taskCount() view returns (uint)",
  "event TaskCreated(uint indexed id, address indexed client, address indexed agent, uint value)",
  "event TaskCompleted(uint indexed id)",
  "event PaymentReleased(uint indexed id, address indexed agent, uint value)",
];

const contract = new ethers.Contract(
  process.env.CONTRACT_ADDRESS,
  ABI,
  wallet
);

/* =========================================================
   HELPERS
   ========================================================= */
const log = (...args) => console.log(`[${new Date().toISOString()}]`, ...args);

const circleFetch = async (path, options = {}) => {
  const res = await fetch(`${CIRCLE_BASE}${path}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${CIRCLE_API_KEY}`,
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(
      `Circle API ${res.status}: ${data?.message || JSON.stringify(data)}`
    );
  }
  return data;
};

const verifyCircleSignature = (req) => {
  if (!CIRCLE_WEBHOOK_SECRET) return true; // skip in dev
  const signature = req.header("X-Circle-Signature") || "";
  const expected = crypto
    .createHmac("sha256", CIRCLE_WEBHOOK_SECRET)
    .update(req.rawBody || Buffer.from(""))
    .digest("hex");
  try {
    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(expected)
    );
  } catch {
    return false;
  }
};

/* =========================================================
   ROUTES
   ========================================================= */

// Health check
app.get("/", (_req, res) => {
  res.json({
    status: "ok",
    service: "Pocket Oracle",
    network: process.env.RPC_URL ? "connected" : "missing",
    contract: process.env.CONTRACT_ADDRESS,
  });
});

// Create Circle wallet
app.post("/create-wallet", async (_req, res) => {
  try {
    const data = await circleFetch("/v1/wallets", {
      method: "POST",
      body: JSON.stringify({
        idempotencyKey: crypto.randomUUID(),
        description: "Pocket Oracle Wallet",
      }),
    });
    res.json(data);
  } catch (err) {
    log("create-wallet error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

// Transfer USDC
app.post("/transfer", async (req, res) => {
  const { amount, destinationWalletId } = req.body || {};
  if (!amount || !destinationWalletId) {
    return res
      .status(400)
      .json({ error: "amount and destinationWalletId are required" });
  }
  try {
    const data = await circleFetch("/v1/transfers", {
      method: "POST",
      body: JSON.stringify({
        idempotencyKey: crypto.randomUUID(),
        source: { type: "wallet", id: process.env.SOURCE_WALLET_ID },
        destination: { type: "wallet", id: destinationWalletId },
        amount: { amount: String(amount), currency: "USD" },
      }),
    });
    res.json(data);
  } catch (err) {
    log("transfer error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

// Webhook: Circle → Smart Contract
app.post("/webhook", async (req, res) => {
  if (!verifyCircleSignature(req)) {
    log("webhook: invalid signature");
    return res.sendStatus(401);
  }

  const event = req.body || {};
  log("Circle event:", event.type);

  try {
    if (event.type === "payment.confirmed") {
      const tx = await contract.createTask(process.env.AGENT_ADDRESS, {
        value: ethers.parseEther(TASK_VALUE_ETH),
      });
      const receipt = await tx.wait();
      log("Task created on-chain:", tx.hash, "block:", receipt.blockNumber);
    }
    res.sendStatus(200);
  } catch (err) {
    log("webhook error:", err.message);
    res.sendStatus(500);
  }
});

// Complete + release payment
app.post("/complete-task", async (req, res) => {
  const { taskId } = req.body || {};
  if (taskId === undefined || taskId === null) {
    return res.status(400).json({ error: "taskId required" });
  }
  try {
    const tx = await contract.releasePayment(taskId);
    const receipt = await tx.wait();
    res.json({ success: true, txHash: tx.hash, block: receipt.blockNumber });
  } catch (err) {
    log("complete-task error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

// List tasks
app.get("/tasks", async (_req, res) => {
  try {
    const count = Number(await contract.taskCount());
    const tasks = [];
    for (let i = 0; i < count; i++) {
      const t = await contract.tasks(i);
      tasks.push({
        id: i,
        client: t.client,
        agent: t.agent,
        value: t.value.toString(),
        completed: t.completed,
        paid: t.paid,
      });
    }
    res.json({ count, tasks });
  } catch (err) {
    log("tasks error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

/* =========================================================
   START
   ========================================================= */
app.listen(PORT, () => {
  log(`Pocket Oracle running on http://localhost:${PORT}`);
});
