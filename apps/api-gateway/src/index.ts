import cors from 'cors';
import express from 'express';
import { z } from 'zod';
import { callOrchestrator } from './orchestrator.js';
import { requirePayment } from './payments.js';
import { pricingCatalog } from './pricing.js';

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
  res.json({ status: 'ok', service: 'api-gateway', payment_mode: process.env.PAYMENT_MODE || 'mock' });
});

app.get('/pricing', (_req, res) => {
  res.json({ currency: 'USDC', unit: 'per_request', services: pricingCatalog });
});

app.post('/oracle/geoproof', requirePayment, async (req, res) => {
  try {
    const payload = geoSchema.parse(req.body);
    const data = await callOrchestrator('/geoproof', payload);
    res.json({ paid: true, service: 'geoproof', price: 0.0015, data });
  } catch (error) {
    res.status(400).json({ error: 'invalid_geoproof_request', details: String(error) });
  }
});

app.post('/oracle/snap-ocr', requirePayment, async (req, res) => {
  try {
    const payload = ocrSchema.parse(req.body);
    const data = await callOrchestrator('/snap-ocr', payload);
    res.json({ paid: true, service: 'snap-ocr', price: 0.004, data });
  } catch (error) {
    res.status(400).json({ error: 'invalid_snap_ocr_request', details: String(error) });
  }
});

app.post('/oracle/human-tap-verify', requirePayment, async (req, res) => {
  try {
    const payload = tapSchema.parse(req.body);
    const data = await callOrchestrator('/human-tap-verify', payload);
    res.json({ paid: true, service: 'human-tap-verify', price: 0.006, data });
  } catch (error) {
    res.status(400).json({ error: 'invalid_human_tap_request', details: String(error) });
  }
});

app.listen(port, () => {
  console.log(`Pocket Oracle API Gateway running on port ${port}`);
});
