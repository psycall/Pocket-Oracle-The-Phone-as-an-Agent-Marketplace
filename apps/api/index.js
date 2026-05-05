import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'orvion-api',
    timestamp: new Date().toISOString(),
  });
});

// API endpoint
app.get('/api/status', (req, res) => {
  res.json({
    status: 'operational',
    network: 'arc-testnet',
    version: '2.0.0',
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 ORVION API listening on port ${PORT}`);
});

export default app;
