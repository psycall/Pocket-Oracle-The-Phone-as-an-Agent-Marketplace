const orchestratorUrl = process.env.SENSOR_ORCHESTRATOR_URL || 'http://localhost:8100';

export async function callOrchestrator(path: string, payload: Record<string, unknown>) {
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
