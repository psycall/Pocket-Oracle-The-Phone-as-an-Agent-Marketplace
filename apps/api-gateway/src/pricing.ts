export type OracleServiceKey = 'geoproof' | 'snap-ocr' | 'human-tap-verify';

export interface PricingItem {
  key: OracleServiceKey;
  label: string;
  price: number;
  currency: 'USDC';
  unit: 'per_request';
  latency: string;
  description: string;
  outcome: string;
}

export const pricingCatalog: PricingItem[] = [
  {
    key: 'geoproof',
    label: 'GeoProof',
    price: 0.0015,
    currency: 'USDC',
    unit: 'per_request',
    latency: '< 2s',
    description: 'Device-assisted location proof for delivery, field ops and compliance.',
    outcome: 'Signed-style geo-attestation with confidence score.'
  },
  {
    key: 'snap-ocr',
    label: 'SnapOCR',
    price: 0.004,
    currency: 'USDC',
    unit: 'per_request',
    latency: '< 3s',
    description: 'Lightweight OCR for receipts, labels and shipment identifiers.',
    outcome: 'Structured text extraction with confidence bands.'
  },
  {
    key: 'human-tap-verify',
    label: 'HumanTap Verify',
    price: 0.006,
    currency: 'USDC',
    unit: 'per_request',
    latency: '< 20s',
    description: 'Escalation endpoint when an agent needs a last-mile human confirmation.',
    outcome: 'Binary verification decision with operator trace.'
  }
];

export const featuredMetrics = {
  avgSettlementTime: '420ms',
  paymentMode: 'Mock / x402-ready',
  simulatedSuccessRate: '99.2%',
  activeServices: pricingCatalog.length
};

export function getPricingItem(serviceKey: OracleServiceKey) {
  return pricingCatalog.find((item) => item.key === serviceKey);
}
