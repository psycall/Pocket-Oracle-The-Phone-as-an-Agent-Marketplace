import express from "express";
import { createClient } from "redis";
import pkg from "pg";
const { Pool } = pkg;

const app = express();
app.use(express.json());

const redis = createClient({ url: process.env.REDIS_URL || "redis://localhost:6379" });
redis.on("error", (e) => console.error("Redis error:", e));
await redis.connect().catch(console.error);

const pg = new Pool({ connectionString: process.env.POSTGRES_URL });

// Plan quotas and pricing
const PLAN_QUOTAS = {
  free: {
    monthly: 1000,
    costPerCall: 0,
    description: "Free tier for testing",
  },
  pro: {
    monthly: 100000,
    costPerCall: 0.001,
    description: "Professional plan",
  },
  enterprise: {
    monthly: Infinity,
    costPerCall: 0.0005,
    description: "Enterprise plan",
  },
};

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    service: "billing",
  });
});

// Check billing status
app.post("/check", async (req, res) => {
  try {
    const { apiKey } = req.body;

    if (!apiKey) {
      return res.json({
        allowed: false,
        reason: "no_api_key",
      });
    }

    // Get user plan from database
    const { rows } = await pg.query(
      "SELECT plan FROM users WHERE api_key = $1",
      [apiKey]
    );

    const plan = rows[0]?.plan || "free";
    const quota = PLAN_QUOTAS[plan];

    // Get current month usage from Redis
    const monthKey = `usage:${apiKey}:${new Date().toISOString().slice(0, 7)}`;
    const used = parseInt((await redis.get(monthKey)) || "0", 10);

    // Check if quota exceeded
    if (used >= quota.monthly) {
      return res.json({
        allowed: false,
        reason: "quota_exceeded",
        plan,
        used,
        quota: quota.monthly,
        upgrade_url: "https://orvion.io/pricing",
      });
    }

    res.json({
      allowed: true,
      plan,
      used,
      remaining: quota.monthly - used,
      cost: quota.costPerCall,
      quota_total: quota.monthly,
      description: quota.description,
    });
  } catch (error) {
    console.error("Billing check error:", error.message);
    // Graceful degradation: allow request if billing service fails
    res.json({
      allowed: true,
      fallback: true,
      warning: "billing_service_unavailable",
    });
  }
});

// Get billing details for API key
app.get("/details/:apiKey", async (req, res) => {
  try {
    const { apiKey } = req.params;

    const { rows } = await pg.query(
      "SELECT plan, created_at FROM users WHERE api_key = $1",
      [apiKey]
    );

    if (rows.length === 0) {
      return res.status(404).json({
        error: "api_key_not_found",
      });
    }

    const user = rows[0];
    const plan = user.plan || "free";
    const quota = PLAN_QUOTAS[plan];

    // Get current month usage
    const monthKey = `usage:${apiKey}:${new Date().toISOString().slice(0, 7)}`;
    const used = parseInt((await redis.get(monthKey)) || "0", 10);

    res.json({
      status: "success",
      api_key: apiKey,
      plan,
      quota: {
        monthly: quota.monthly,
        used,
        remaining: quota.monthly - used,
        percentage_used: ((used / quota.monthly) * 100).toFixed(2),
      },
      pricing: {
        cost_per_call: quota.costPerCall,
        description: quota.description,
      },
      created_at: user.created_at,
    });
  } catch (error) {
    res.status(500).json({
      error: "billing_details_failed",
      detail: error.message,
    });
  }
});

// Upgrade plan
app.post("/upgrade", async (req, res) => {
  try {
    const { apiKey, newPlan } = req.body;

    if (!apiKey || !newPlan) {
      return res.status(400).json({
        error: "missing_fields",
        required: ["apiKey", "newPlan"],
      });
    }

    if (!PLAN_QUOTAS[newPlan]) {
      return res.status(400).json({
        error: "invalid_plan",
        available_plans: Object.keys(PLAN_QUOTAS),
      });
    }

    // Update plan in database
    await pg.query(
      "UPDATE users SET plan = $1, updated_at = NOW() WHERE api_key = $2",
      [newPlan, apiKey]
    );

    res.json({
      status: "success",
      message: `Plan upgraded to ${newPlan}`,
      new_plan: newPlan,
      quota: PLAN_QUOTAS[newPlan],
    });
  } catch (error) {
    res.status(500).json({
      error: "upgrade_failed",
      detail: error.message,
    });
  }
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
  console.log(`💳 ORVION Billing Service listening on port ${PORT}`);
  console.log("Available plans:", Object.keys(PLAN_QUOTAS));
});
