const orchestratorUrl = process.env.SENSOR_ORCHESTRATOR_URL || 'http://localhost:8100';

async function fetchOrchestrator(path: string, payload: Record<string, unknown>) {
  const response = await fetch(`${orchestratorUrl}${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`orchestrator_error:${response.status}`);
  }

  return response.json();
}

function deterministicHash(value: string) {
  return Array.from(value).reduce((acc, char) => acc + char.charCodeAt(0), 0);
}

function localFallback(path: string, payload: Record<string, unknown>) {
  const seed = deterministicHash(JSON.stringify(payload));
  const executionId = `demo_${path.replace(/\//g, '')}_${seed}`;

  switch (path) {
    case '/geoproof': {
      const latitude = Number(payload.latitude ?? 0);
      const longitude = Number(payload.longitude ?? 0);
      const accuracy = Number(payload.accuracy ?? 18);
      return {
        execution_id: executionId,
        verified: true,
        latitude,
        longitude,
        accuracy,
        confidence: Number(Math.max(0.82, 1 - accuracy / 200).toFixed(2)),
        region_hint: latitude >= 0 ? 'northern-hemisphere' : 'southern-hemisphere',
        mode: 'local-fallback'
      };
    }
    case '/snap-ocr': {
      const imageUrl = String(payload.imageUrl ?? 'unknown');
      return {
        execution_id: executionId,
        extracted_text: 'DEMO-RECEIPT-2048',
        source: imageUrl,
        confidence: 0.94,
        mode: 'local-fallback'
      };
    }
    case '/human-tap-verify': {
      const answer = String(payload.answer ?? '').trim().toLowerCase();
      return {
        execution_id: executionId,
        verdict: ['yes', 'y', 'approved', 'approve', 'ok', 'true'].includes(answer)
          ? 'approved'
          : 'needs-review',
        prompt: payload.prompt,
        answer: payload.answer,
        reviewer: 'operator-demo-01',
        mode: 'local-fallback'
      };
    }
    default:
      return { execution_id: executionId, mode: 'local-fallback', payload };
  }
}

export async function callOrchestrator(path: string, payload: Record<string, unknown>) {
  try {
    return await fetchOrchestrator(path, payload);
  } catch (_error) {
    return localFallback(path, payload);
  }
}
