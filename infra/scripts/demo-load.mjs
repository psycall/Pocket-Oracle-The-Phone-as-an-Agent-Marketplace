const baseUrl = process.env.BASE_URL || 'http://localhost:8080';
const authHeader = 'demo-payment-authorization';

const payloads = [
  { endpoint: '/oracle/geoproof', body: { latitude: -23.5505, longitude: -46.6333, accuracy: 12 } },
  { endpoint: '/oracle/snap-ocr', body: { imageUrl: 'https://example.com/sample-receipt.jpg' } },
  { endpoint: '/oracle/human-tap-verify', body: { prompt: 'A porta azul está visível?', answer: 'yes' } }
];

async function hit(endpoint, body) {
  await fetch(`${baseUrl}${endpoint}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body)
  });

  const paid = await fetch(`${baseUrl}${endpoint}`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-payment-authorization': authHeader
    },
    body: JSON.stringify(body)
  });

  return paid.json();
}

const results = [];
for (let i = 0; i < 15; i += 1) {
  for (const item of payloads) {
    results.push(await hit(item.endpoint, item.body));
  }
}

console.log(JSON.stringify({ total: results.length, sample: results.slice(0, 3) }, null, 2));
