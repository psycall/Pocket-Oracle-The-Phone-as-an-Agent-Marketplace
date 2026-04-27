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
    apiKey: string;
    baseUrl?: string;
    timeout?: number;
}
export interface TaskRequest {
    goal: string;
    context?: Record<string, unknown>;
}
export interface TaskRecord {
    id: string;
    node: string;
    goal: string;
    agentUsed: string;
    result: Record<string, unknown>;
    durationMs: number;
    timestamp: number;
    status: string;
}
export interface StreamEvent {
    type: 'started' | 'routing' | 'routed' | 'executing' | 'result' | 'complete';
    taskId?: string;
    data?: unknown;
    message?: string;
    agent?: string;
    durationMs?: number;
}
export interface NodeStatus {
    nodeId: string;
    version: string;
    status: string;
    environment: string;
    tasksExecuted: number;
    uptimeSeconds: number;
}
export interface MarketplaceAgent {
    name: string;
    description: string;
    type: string;
    version: string;
}
export declare class OrvionClient {
    private baseUrl;
    private timeout;
    private token;
    private apiKey;
    constructor(config: OrvionConfig);
    private authenticate;
    private authHeaders;
    execute(task: TaskRequest): Promise<TaskRecord>;
    executeStream(task: TaskRequest): AsyncGenerator<StreamEvent>;
    getStatus(): Promise<NodeStatus>;
    getHistory(limit?: number, offset?: number): Promise<{
        tasks: TaskRecord[];
        total: number;
    }>;
    listAgents(): Promise<MarketplaceAgent[]>;
    private camelizeRecord;
    private handleError;
}
export declare class OrvionError extends Error {
    statusCode: number;
    constructor(message: string, statusCode: number);
}
export default OrvionClient;
//# sourceMappingURL=index.d.ts.map