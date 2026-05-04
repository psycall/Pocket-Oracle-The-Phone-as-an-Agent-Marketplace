import express from "express";
import { createClient } from "redis";
import pkg from "pg";
const { Pool } = pkg;

const app = express();
app.use(express.json());

const redis = createClient({ url: process.env.REDIS_URL || "redis://localhost:6379" });
await redis.connect().catch(console.error);

const pg = new Pool({ connectionString: process.env.POSTGRES_URL });

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    service: "usage",
  });
});

// Track API usage
app.post("/track", async (req, res) => {
  try {
    const { apiKey, endpoint, cost = 0 } = req.body;

    if (!apiKey) {
      return res.status(400).json({
        error: "api_key_required",
      });
    }

    // Increment monthly usage counter
    const monthKey = `usage:${apiKey}:${new Date().toISOString().slice(0, 7)}`;
    await redis.incr(monthKey);
    await redis.expire(monthKey, 60 * 60 * 24 * 40); // Expire after 40 days

    // Record usage in database
    pg.query(
      `INSERT INTO api_usage (api_key, endpoint, cost_usdc)
       VALUES ($1, $2, $3)`,
      [apiKey, endpoint || "unknown", cost]
    ).catch((err) => console.error("Usage insert error:", err.message));

    res.json({
      status: "success",
      tracked: true,
    });
  } catch (error) {
    console.error("Usage tracking error:", error.message);
    res.status(500).json({
      error: "usage_tracking_failed",
      detail: error.message,
    });
  }
});

// Get usage statistics
app.get("/stats/:apiKey", async (req, res) => {
  try {
    const { apiKey } = req.params;
    const { days = 30 } = req.query;

    const { rows } = await pg.query(
      `SELECT
        COUNT(*) as total_calls,
        COALESCE(SUM(cost_usdc), 0) as total_cost,
        MIN(created_at) as first_call,
        MAX(created_at) as last_call,
        COUNT(DISTINCT DATE(created_at)) as active_days
       FROM api_usage
       WHERE api_key = $1
       AND created_at >= NOW() - INTERVAL '1 day' * $2`,
      [apiKey, parseInt(days)]
    );

    const stats = rows[0];

    res.json({
      status: "success",
      api_key: apiKey,
      period_days: parseInt(days),
      statistics: {
        total_calls: parseInt(stats.total_calls),
        total_cost_usdc: parseFloat(stats.total_cost),
        average_cost_per_call: stats.total_calls > 0
          ? (parseFloat(stats.total_cost) / parseInt(stats.total_calls)).toFixed(6)
          : "0",
        first_call: stats.first_call,
        last_call: stats.last_call,
        active_days: parseInt(stats.active_days),
      },
    });
  } catch (error) {
    res.status(500).json({
      error: "stats_retrieval_failed",
      detail: error.message,
    });
  }
});

// Get endpoint breakdown
app.get("/breakdown/:apiKey", async (req, res) => {
  try {
    const { apiKey } = req.params;
    const { days = 30 } = req.query;

    const { rows } = await pg.query(
      `SELECT
        endpoint,
        COUNT(*) as calls,
        COALESCE(SUM(cost_usdc), 0) as total_cost
       FROM api_usage
       WHERE api_key = $1
       AND created_at >= NOW() - INTERVAL '1 day' * $2
       GROUP BY endpoint
       ORDER BY calls DESC`,
      [apiKey, parseInt(days)]
    );

    res.json({
      status: "success",
      api_key: apiKey,
      period_days: parseInt(days),
      breakdown: rows.map((row) => ({
        endpoint: row.endpoint,
        calls: parseInt(row.calls),
        total_cost_usdc: parseFloat(row.total_cost),
        average_cost: (parseFloat(row.total_cost) / parseInt(row.calls)).toFixed(6),
      })),
    });
  } catch (error) {
    res.status(500).json({
      error: "breakdown_retrieval_failed",
      detail: error.message,
    });
  }
});

// Get current month usage
app.get("/current/:apiKey", async (req, res) => {
  try {
    const { apiKey } = req.params;

    const monthKey = `usage:${apiKey}:${new Date().toISOString().slice(0, 7)}`;
    const used = parseInt((await redis.get(monthKey)) || "0", 10);

    res.json({
      status: "success",
      api_key: apiKey,
      current_month: new Date().toISOString().slice(0, 7),
      usage: used,
    });
  } catch (error) {
    res.status(500).json({
      error: "current_usage_retrieval_failed",
      detail: error.message,
    });
  }
});

const PORT = process.env.PORT || 3003;
app.listen(PORT, () => {
  console.log(`📊 ORVION Usage Service listening on port ${PORT}`);
});
