import type { NextFunction, Request, Response } from 'express';

export function requirePayment(req: Request, res: Response, next: NextFunction) {
  const authorization = req.header('x-payment-authorization');

  if (!authorization) {
    return res.status(402).json({
      error: 'payment_required',
      message: 'This endpoint requires payment authorization before execution.',
      retry_hint: 'Retry the same request with x-payment-authorization.',
      settlement_mode: process.env.PAYMENT_MODE || 'mock'
    });
  }

  return next();
}
