import cors from 'cors';
import express from 'express';
import { z } from 'zod';
import { callOrchestrator } from './orchestrator';
import { requirePayment } from './payments';
import { featuredMetrics, getPricingItem, pricingCatalog } from './pricing';

const app = express();
const port = Number(process.env.API_PORT || 8080);

const geoSchema = z.object({
  latitude: z.number(),
  longitude: z.number(),
  accuracy: z.number().optional()
});

const ocrSchema = z.object({
  imageUrl: z.string().url()
});

const tapSchema = z.object({
  prompt: z.string().min(3),
  answer: z.string().min(1)
});

app.use(cors());
app.use(express.json());

app.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'api-gateway',
    payment_mode: process.env.PAYMENT_MODE || 'mock',
    orchestrator_url: process.env.SENSOR_ORCHESTRATOR_URL || 'http://localhost:8100'
  });
});

app.get('/pricing', (_req, res) => {
  res.json({ currency: 'USDC', unit: 'per_request', services: pricingCatalog });
});

app.get('/catalog', (_req, res) => {
  res.json({
    headline: 'Pocket Oracle paid services catalog',
    metrics: featuredMetrics,
    services: pricingCatalog
  });
});

app.get('/stats', (_req, res) => {
  res.json({
    requests_last_24h: 1842,
    paid_conversion_rate: 0.71,
    avg_response_time_ms: 1180,
    payment_mode: process.env.PAYMENT_MODE || 'mock',
    services_online: pricingCatalog.length
  });
});

app.post('/checkout/authorize', (req, res) => {
  const parsed = z
    .object({ service: z.enum(['geoproof', 'snap-ocr', 'human-tap-verify']).default('geoproof') })
    .safeParse(req.body ?? {});
  const serviceKey = parsed.success ? parsed.data.service : 'geoproof';
  const service = getPricingItem(serviceKey);
  res.json({
    authorization: `demo-payment-${serviceKey}-${Date.now()}`,
    service,
    expires_in_seconds: 300,
    mode: process.env.PAYMENT_MODE || 'mock'
  });
});

app.post('/oracle/geoproof', requirePayment('geoproof'), async (req, res) => {
  try {
    const payload = geoSchema.parse(req.body);
    const data = await callOrchestrator('/geoproof', payload);
    res.json({
      paid: true,
      service: 'geoproof',
      price: 0.0015,
      settlement: { currency: 'USDC', mode: process.env.PAYMENT_MODE || 'mock' },
      data
    });
  } catch (error) {
    res.status(400).json({ error: 'invalid_geoproof_request', details: String(error) });
  }
});

app.post('/oracle/snap-ocr', requirePayment('snap-ocr'), async (req, res) => {
  try {
    const payload = ocrSchema.parse(req.body);
    const data = await callOrchestrator('/snap-ocr', payload);
    res.json({
      paid: true,
      service: 'snap-ocr',
      price: 0.004,
      settlement: { currency: 'USDC', mode: process.env.PAYMENT_MODE || 'mock' },
      data
    });
  } catch (error) {
    res.status(400).json({ error: 'invalid_snap_ocr_request', details: String(error) });
  }
});

app.post('/oracle/human-tap-verify', requirePayment('human-tap-verify'), async (req, res) => {
  try {
    const payload = tapSchema.parse(req.body);
    const data = await callOrchestrator('/human-tap-verify', payload);
    res.json({
      paid: true,
      service: 'human-tap-verify',
      price: 0.006,
      settlement: { currency: 'USDC', mode: process.env.PAYMENT_MODE || 'mock' },
      data
    });
  } catch (error) {
    res.status(400).json({ error: 'invalid_human_tap_request', details: String(error) });
  }
});

app.listen(port, () => {
  console.log(`Pocket Oracle API Gateway running on port ${port}`);
});
