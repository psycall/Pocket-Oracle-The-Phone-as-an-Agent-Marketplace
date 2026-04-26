import type { NextFunction, Request, Response } from 'express';
import type { OracleServiceKey } from './pricing';
import { getPricingItem } from './pricing';

export function requirePayment(serviceKey: OracleServiceKey) {
  return function paymentMiddleware(req: Request, res: Response, next: NextFunction) {
    const authorization = req.header('x-payment-authorization');
    const service = getPricingItem(serviceKey);

    if (authorization) {
      return next();
    }

    return res.status(402).json({
      error: 'payment_required',
      service: service?.label ?? serviceKey,
      amount: service?.price ?? 0,
      currency: service?.currency ?? 'USDC',
      payment_mode: process.env.PAYMENT_MODE || 'mock',
      accepted_header: 'x-payment-authorization',
      demo_authorization_hint:
        'Use POST /checkout/authorize to mint a demo authorization token, then retry with the x-payment-authorization header.',
      retry_hint: 'Repeat the same request with x-payment-authorization.'
    });
  };
}
