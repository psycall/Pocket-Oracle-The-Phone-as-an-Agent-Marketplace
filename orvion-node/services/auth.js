import express from "express";
import jwt from "jsonwebtoken";
import pkg from "pg";
const { Pool } = pkg;

const app = express();
app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET || "orvion-dev-secret-change-me";
const pg = new Pool({ connectionString: process.env.POSTGRES_URL });

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    service: "auth",
  });
});

// Login endpoint - issue JWT token
app.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email) {
      return res.status(400).json({
        error: "email_required",
      });
    }

    // In production: hash and verify password
    // For demo: accept any email
    const token = jwt.sign(
      {
        email,
        role: "user",
        iat: Math.floor(Date.now() / 1000),
      },
      JWT_SECRET,
      { expiresIn: "24h" }
    );

    res.json({
      status: "success",
      token,
      expires_in: "24h",
      user: { email },
    });
  } catch (error) {
    res.status(500).json({
      error: "login_failed",
      detail: error.message,
    });
  }
});

// Verify token endpoint
app.post("/verify", (req, res) => {
  try {
    const { token } = req.body;

    if (!token) {
      return res.json({
        valid: false,
        error: "token_missing",
      });
    }

    // Dev fallback for testing
    if (token === "test") {
      return res.json({
        valid: true,
        user: {
          email: "demo@orvion.io",
          role: "user",
        },
      });
    }

    try {
      const decoded = jwt.verify(token, JWT_SECRET);
      res.json({
        valid: true,
        user: decoded,
      });
    } catch (jwtError) {
      res.json({
        valid: false,
        error: "invalid_token",
        detail: jwtError.message,
      });
    }
  } catch (error) {
    res.status(500).json({
      error: "verification_failed",
      detail: error.message,
    });
  }
});

// Refresh token endpoint
app.post("/refresh", (req, res) => {
  try {
    const { token } = req.body;

    if (!token) {
      return res.status(400).json({
        error: "token_required",
      });
    }

    try {
      const decoded = jwt.verify(token, JWT_SECRET, { ignoreExpiration: true });
      const newToken = jwt.sign(
        {
          email: decoded.email,
          role: decoded.role,
        },
        JWT_SECRET,
        { expiresIn: "24h" }
      );

      res.json({
        status: "success",
        token: newToken,
        expires_in: "24h",
      });
    } catch (jwtError) {
      res.status(401).json({
        error: "invalid_token",
        detail: jwtError.message,
      });
    }
  } catch (error) {
    res.status(500).json({
      error: "refresh_failed",
      detail: error.message,
    });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🔐 ORVION Auth Service listening on port ${PORT}`);
});
