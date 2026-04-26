/**
 * Orvion SDK — TypeScript
 * The official client for the Orvion Execution Layer.
 *
 * Usage:
 *   import { OrvionClient } from '@orvion/sdk'
 *   const client = new OrvionClient({ apiKey: 'your-key', baseUrl: 'https://api.orvion.dev' })
 *   const result = await client.execute({ goal: 'Analyze crypto trends' })
 */

export interface OrvionConfig {
  apiKey: string
  baseUrl?: string
  timeout?: number
}

export interface TaskRequest {
  goal: string
  context?: Record<string, unknown>
}

export interface TaskRecord {
  id: string
  node: string
  goal: string
  agentUsed: string
  result: Record<string, unknown>
  durationMs: number
  timestamp: number
  status: string
}

export interface StreamEvent {
  type: 'started' | 'routing' | 'routed' | 'executing' | 'result' | 'complete'
  taskId?: string
  data?: unknown
  message?: string
  agent?: string
  durationMs?: number
}

export interface NodeStatus {
  nodeId: string
  version: string
  status: string
  environment: string
  tasksExecuted: number
  uptimeSeconds: number
}

export interface MarketplaceAgent {
  name: string
  description: string
  type: string
  version: string
}

// ── Client ────────────────────────────────────────────────────

export class OrvionClient {
  private baseUrl: string
  private timeout: number
  private token: string | null = null
  private apiKey: string

  constructor(config: OrvionConfig) {
    this.apiKey = config.apiKey
    this.baseUrl = (config.baseUrl ?? 'http://localhost:8000').replace(/\/$/, '')
    this.timeout = config.timeout ?? 30_000
  }

  // ── Auth ─────────────────────────────────────────────────

  private async authenticate(): Promise<void> {
    const res = await fetch(`${this.baseUrl}/node/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: this.apiKey }),
      signal: AbortSignal.timeout(this.timeout),
    })
    if (!res.ok) throw new OrvionError('Authentication failed', res.status)
    const data = await res.json()
    this.token = data.access_token
  }

  private async authHeaders(): Promise<Record<string, string>> {
    if (!this.token) await this.authenticate()
    return {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${this.token}`,
    }
  }

  // ── Core execution ────────────────────────────────────────

  async execute(task: TaskRequest): Promise<TaskRecord> {
    const headers = await this.authHeaders()
    const res = await fetch(`${this.baseUrl}/agent/execute`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ goal: task.goal, context: task.context ?? {} }),
      signal: AbortSignal.timeout(this.timeout),
    })
    if (!res.ok) throw await this.handleError(res)
    const data = await res.json()
    return this.camelizeRecord(data)
  }

  async *executeStream(task: TaskRequest): AsyncGenerator<StreamEvent> {
    const headers = await this.authHeaders()
    const res = await fetch(`${this.baseUrl}/agent/execute/stream`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ goal: task.goal, context: task.context ?? {} }),
    })
    if (!res.ok) throw await this.handleError(res)
    if (!res.body) throw new OrvionError('No response body for streaming', 500)

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() ?? ''
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            yield JSON.parse(line.slice(6)) as StreamEvent
          } catch {
            // skip malformed event
          }
        }
      }
    }
  }

  // ── Node ─────────────────────────────────────────────────

  async getStatus(): Promise<NodeStatus> {
    const headers = await this.authHeaders()
    const res = await fetch(`${this.baseUrl}/node/status`, { headers })
    if (!res.ok) throw await this.handleError(res)
    const data = await res.json()
    return {
      nodeId: data.node_id,
      version: data.version,
      status: data.status,
      environment: data.environment,
      tasksExecuted: data.tasks_executed,
      uptimeSeconds: data.uptime_seconds,
    }
  }

  async getHistory(limit = 20, offset = 0): Promise<{ tasks: TaskRecord[]; total: number }> {
    const headers = await this.authHeaders()
    const res = await fetch(
      `${this.baseUrl}/node/history?limit=${limit}&offset=${offset}`,
      { headers }
    )
    if (!res.ok) throw await this.handleError(res)
    const data = await res.json()
    return { tasks: data.tasks.map(this.camelizeRecord), total: data.total }
  }

  // ── Marketplace ──────────────────────────────────────────

  async listAgents(): Promise<MarketplaceAgent[]> {
    const res = await fetch(`${this.baseUrl}/marketplace/agents`)
    if (!res.ok) throw await this.handleError(res)
    const data = await res.json()
    return data.agents
  }

  // ── Internals ─────────────────────────────────────────────

  private camelizeRecord(data: Record<string, unknown>): TaskRecord {
    return {
      id: data.id as string,
      node: data.node as string,
      goal: data.goal as string,
      agentUsed: data.agent_used as string,
      result: data.result as Record<string, unknown>,
      durationMs: data.duration_ms as number,
      timestamp: data.timestamp as number,
      status: data.status as string,
    }
  }

  private async handleError(res: Response): Promise<OrvionError> {
    try {
      const body = await res.json()
      return new OrvionError(body.detail ?? 'Unknown error', res.status)
    } catch {
      return new OrvionError(res.statusText, res.status)
    }
  }
}

// ── Error ─────────────────────────────────────────────────────

export class OrvionError extends Error {
  constructor(message: string, public statusCode: number) {
    super(message)
    this.name = 'OrvionError'
  }
}

// ── Default export ─────────────────────────────────────────────
export default OrvionClient
