export interface PaidRequestOptions {
  endpoint: string;
  payload: Record<string, unknown>;
  baseUrl: string;
  authorizationFactory?: () => Promise<string>;
}

export async function payAndRetry(options: PaidRequestOptions) {
  const firstAttempt = await fetch(`${options.baseUrl}${options.endpoint}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(options.payload)
  });

  if (firstAttempt.status !== 402) {
    return firstAttempt.json();
  }

  const authorization = options.authorizationFactory
    ? await options.authorizationFactory()
    : 'demo-payment-authorization';

  const paidAttempt = await fetch(`${options.baseUrl}${options.endpoint}`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-payment-authorization': authorization
    },
    body: JSON.stringify(options.payload)
  });

  return paidAttempt.json();
}
