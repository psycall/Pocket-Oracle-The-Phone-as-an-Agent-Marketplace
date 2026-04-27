"use strict";
/**
 * Orvion SDK — TypeScript
 * The official client for the Orvion Execution Layer.
 *
 * Usage:
 *   import { OrvionClient } from '@orvion/sdk'
 *   const client = new OrvionClient({ apiKey: 'your-key', baseUrl: 'https://api.orvion.dev' })
 *   const result = await client.execute({ goal: 'Analyze crypto trends' })
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.OrvionError = exports.OrvionClient = void 0;
// ── Client ────────────────────────────────────────────────────
class OrvionClient {
    baseUrl;
    timeout;
    token = null;
    apiKey;
    constructor(config) {
        this.apiKey = config.apiKey;
        this.baseUrl = (config.baseUrl ?? 'http://localhost:8000').replace(/\/$/, '');
        this.timeout = config.timeout ?? 30_000;
    }
    // ── Auth ─────────────────────────────────────────────────
    async authenticate() {
        const res = await fetch(`${this.baseUrl}/node/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: this.apiKey }),
            signal: AbortSignal.timeout(this.timeout),
        });
        if (!res.ok)
            throw new OrvionError('Authentication failed', res.status);
        const data = await res.json();
        this.token = data.access_token;
    }
    async authHeaders() {
        if (!this.token)
            await this.authenticate();
        return {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.token}`,
        };
    }
    // ── Core execution ────────────────────────────────────────
    async execute(task) {
        const headers = await this.authHeaders();
        const res = await fetch(`${this.baseUrl}/agent/execute`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ goal: task.goal, context: task.context ?? {} }),
            signal: AbortSignal.timeout(this.timeout),
        });
        if (!res.ok)
            throw await this.handleError(res);
        const data = await res.json();
        return this.camelizeRecord(data);
    }
    async *executeStream(task) {
        const headers = await this.authHeaders();
        const res = await fetch(`${this.baseUrl}/agent/execute/stream`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ goal: task.goal, context: task.context ?? {} }),
        });
        if (!res.ok)
            throw await this.handleError(res);
        if (!res.body)
            throw new OrvionError('No response body for streaming', 500);
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        while (true) {
            const { done, value } = await reader.read();
            if (done)
                break;
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() ?? '';
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        yield JSON.parse(line.slice(6));
                    }
                    catch {
                        // skip malformed event
                    }
                }
            }
        }
    }
    // ── Node ─────────────────────────────────────────────────
    async getStatus() {
        const headers = await this.authHeaders();
        const res = await fetch(`${this.baseUrl}/node/status`, { headers });
        if (!res.ok)
            throw await this.handleError(res);
        const data = await res.json();
        return {
            nodeId: data.node_id,
            version: data.version,
            status: data.status,
            environment: data.environment,
            tasksExecuted: data.tasks_executed,
            uptimeSeconds: data.uptime_seconds,
        };
    }
    async getHistory(limit = 20, offset = 0) {
        const headers = await this.authHeaders();
        const res = await fetch(`${this.baseUrl}/node/history?limit=${limit}&offset=${offset}`, { headers });
        if (!res.ok)
            throw await this.handleError(res);
        const data = await res.json();
        return { tasks: data.tasks.map(this.camelizeRecord), total: data.total };
    }
    // ── Marketplace ──────────────────────────────────────────
    async listAgents() {
        const res = await fetch(`${this.baseUrl}/marketplace/agents`);
        if (!res.ok)
            throw await this.handleError(res);
        const data = await res.json();
        return data.agents;
    }
    // ── Internals ─────────────────────────────────────────────
    camelizeRecord(data) {
        return {
            id: data.id,
            node: data.node,
            goal: data.goal,
            agentUsed: data.agent_used,
            result: data.result,
            durationMs: data.duration_ms,
            timestamp: data.timestamp,
            status: data.status,
        };
    }
    async handleError(res) {
        try {
            const body = await res.json();
            return new OrvionError(body.detail ?? 'Unknown error', res.status);
        }
        catch {
            return new OrvionError(res.statusText, res.status);
        }
    }
}
exports.OrvionClient = OrvionClient;
// ── Error ─────────────────────────────────────────────────────
class OrvionError extends Error {
    statusCode;
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
        this.name = 'OrvionError';
    }
}
exports.OrvionError = OrvionError;
// ── Default export ─────────────────────────────────────────────
exports.default = OrvionClient;
//# sourceMappingURL=index.js.map