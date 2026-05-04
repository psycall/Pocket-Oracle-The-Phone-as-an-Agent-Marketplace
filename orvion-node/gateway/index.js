import express from "express";
import axios from "axios";
import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import * as client from "prom-client";
import { v4 as uuidv4 } from "uuid";

const app = express();

const AUTH_URL = process.env.AUTH_URL || "http://localhost:3001";
const BILLING_URL = process.env.BILLING_URL || "http://localhost:3002";
const USAGE_URL = process.env.USAGE_URL || "http://localhost:3003";
const CIRCLE_URL = process.env.CIRCLE_URL || "http://localhost:3004";

// Security middlewares
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: "1mb" }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});
app.use(limiter);

// Prometheus metrics
client.collectDefaultMetrics();
const httpRequestDuration = new client.Histogram({
  name: "http_request_duration_seconds",
  help: "HTTP request duration in seconds",
  labelNames: ["method", "route", "status"],
  buckets: [0.05, 0.1, 0.3, 0.5, 1, 2, 5],
});

const requestCounter = new client.Counter({
  name: "orvion_requests_total",
  help: "Total ORVION API requests",
  labelNames: ["status", "endpoint"],
});

const paymentCounter = new client.Counter({
  name: "orvion_payments_total",
  help: "Total payments processed",
  labelNames: ["status"],
});

// Request ID + timing middleware
app.use((req, res, next) => {
  req.id = uuidv4();
  req.startTime = Date.now();
  res.setHeader("X-Request-Id", req.id);
  next();
});

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    service: "orvion-gateway",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});

// Metrics endpoint
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", client.register.contentType);
  res.end(await client.register.metrics());
});

// Payment endpoint (Circle/Arc)
app.post("/v1/pay", async (req, res) => {
  const end = httpRequestDuration.startTimer({ method: "POST", route: "/v1/pay" });
  try {
    const { apiKey, amount, recipient } = req.body;

    // Validation
    if (!apiKey || !amount || !recipient) {
      requestCounter.inc({ status: "400", endpoint: "/v1/pay" });
      paymentCounter.inc({ status: "failed" });
      end({ status: 400 });
      return res.status(400).json({
        error: "missing_fields",
        requestId: req.id,
        required: ["apiKey", "amount", "recipient"],
      });
    }

    // Validate amount is positive number
    const parsedAmount = parseFloat(amount);
    if (isNaN(parsedAmount) || parsedAmount <= 0) {
      requestCounter.inc({ status: "400", endpoint: "/v1/pay" });
      paymentCounter.inc({ status: "failed" });
      end({ status: 400 });
      return res.status(400).json({
        error: "invalid_amount",
        requestId: req.id,
        detail: "Amount must be a positive number",
      });
    }

    // Call Circle payments service
    const result = await axios.post(`${CIRCLE_URL}/transfer`, {
      apiKey,
      amount: parsedAmount,
      recipient,
    });

    requestCounter.inc({ status: "200", endpoint: "/v1/pay" });
    paymentCounter.inc({ status: "success" });
    end({ status: 200 });

    res.json({
      requestId: req.id,
      status: "success",
      payment: result.data,
      latency_ms: Date.now() - req.startTime,
    });
  } catch (error) {
    requestCounter.inc({ status: "500", endpoint: "/v1/pay" });
    paymentCounter.inc({ status: "failed" });
    end({ status: 500 });

    console.error(`[${req.id}] Payment error:`, error.message);
    res.status(500).json({
      error: "payment_failed",
      requestId: req.id,
      detail: error.response?.data || error.message,
    });
  }
});

// Main proxy: auth → billing → usage → response
app.all("/v1/*", async (req, res) => {
  const end = httpRequestDuration.startTimer({ method: req.method, route: "/v1/*" });
  try {
    const token = req.headers.authorization?.replace("Bearer ", "") || "";
    const apiKey = req.headers["x-api-key"] || "";

    // 1. Auth verification
    const auth = await axios.post(`${AUTH_URL}/verify`, { token });
    if (!auth.data.valid) {
      requestCounter.inc({ status: "401", endpoint: "/v1/*" });
      end({ status: 401 });
      return res.status(401).json({
        error: "invalid_token",
        requestId: req.id,
      });
    }

    // 2. Billing check
    const bill = await axios.post(`${BILLING_URL}/check`, { apiKey });
    if (!bill.data.allowed) {
      requestCounter.inc({ status: "402", endpoint: "/v1/*" });
      end({ status: 402 });
      return res.status(402).json({
        error: "payment_required",
        requestId: req.id,
        billing: bill.data,
      });
    }

    // 3. Usage tracking (fire-and-forget)
    axios.post(`${USAGE_URL}/track`, {
      apiKey,
      endpoint: req.path,
      cost: bill.data.cost || 0,
    }).catch((err) => console.error(`[${req.id}] Usage tracking error:`, err.message));

    // 4. Business response
    requestCounter.inc({ status: "200", endpoint: "/v1/*" });
    end({ status: 200 });

    res.json({
      requestId: req.id,
      status: "success",
      data: "ORVION Settlement Layer Active",
      user: auth.data.user,
      billing: {
        plan: bill.data.plan,
        remaining: bill.data.remaining,
        cost_per_call: bill.data.cost,
      },
      latency_ms: Date.now() - req.startTime,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    requestCounter.inc({ status: "500", endpoint: "/v1/*" });
    end({ status: 500 });

    console.error(`[${req.id}] Gateway error:`, error.message);
    res.status(500).json({
      error: "gateway_error",
      requestId: req.id,
      detail: error.message,
    });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: "not_found",
    path: req.path,
    method: req.method,
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 ORVION Gateway listening on port ${PORT}`);
  console.log(`📊 Metrics available at http://localhost:${PORT}/metrics`);
  console.log(`🏥 Health check at http://localhost:${PORT}/health`);
});
