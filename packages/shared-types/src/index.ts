export type OracleService = 'geoproof' | 'snap-ocr' | 'human-tap-verify';

export interface PricingItem {
  key: OracleService;
  label: string;
  price: number;
  currency: 'USDC';
  unit: 'per_request';
}

export const pricingCatalog: PricingItem[] = [
  { key: 'geoproof', label: 'GeoProof', price: 0.0015, currency: 'USDC', unit: 'per_request' },
  { key: 'snap-ocr', label: 'SnapOCR', price: 0.0040, currency: 'USDC', unit: 'per_request' },
  { key: 'human-tap-verify', label: 'HumanTap Verify', price: 0.0060, currency: 'USDC', unit: 'per_request' }
];
