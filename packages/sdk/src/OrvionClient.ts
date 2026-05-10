/**
 * ORVION Agent SDK - TypeScript/JavaScript
 * Production-grade SDK for interacting with ORVION Settlement Layer
 * 
 * @version 2.0.0
 * @license MIT
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

export interface OrvionClientConfig {
  baseUrl?: string;
  apiToken?: string;
  timeout?: number;
  maxRetries?: number;
  logLevel?: 'debug' | 'info' | 'warn' | 'error';
}

export interface AgentData {
  agent_address: string;
  agent_name: string;
  agent_type: string;
  capabilities: string[];
  pricing_per_call: number;
  endpoint_url?: string;
  settlement_address?: string;
}

export interface JobData {
  agent_id: string;
  job_id: string;
  amount: number;
  to_address: string;
}

export interface ProofData {
  job_id: string;
  proof: string;
}

export interface SettlementResponse {
  id: string;
  status: string;
  amount: number;
  transaction_hash?: string;
  created_at: string;
}

export interface AgentResponse {
  id: string;
  agent_name: string;
  agent_address: string;
  agent_type: string;
  reputation?: number;
  earnings?: number;
  is_active: boolean;
}

export interface ReputationResponse {
  agent_id: string;
  score: number;
  total_jobs: number;
  success_rate: number;
  average_rating: number;
}

export interface FeedbackResponse {
  id: string;
  agent_id: string;
  score: number;
  comment?: string;
  created_at: string;
}

/**
 * Logger utility for structured logging
 */
class Logger {
  private level: 'debug' | 'info' | 'warn' | 'error';
  private levels = { debug: 0, info: 1, warn: 2, error: 3 };

  constructor(level: 'debug' | 'info' | 'warn' | 'error' = 'info') {
    this.level = level;
  }

  private shouldLog(level: string): boolean {
    return this.levels[level as keyof typeof this.levels] >= this.levels[this.level];
  }

  debug(message: string, data?: any) {
    if (this.shouldLog('debug')) {
      console.log(`[DEBUG] ${message}`, data || '');
    }
  }

  info(message: string, data?: any) {
    if (this.shouldLog('info')) {
      console.log(`[INFO] ${message}`, data || '');
    }
  }

  warn(message: string, data?: any) {
    if (this.shouldLog('warn')) {
      console.warn(`[WARN] ${message}`, data || '');
    }
  }

  error(message: string, data?: any) {
    if (this.shouldLog('error')) {
      console.error(`[ERROR] ${message}`, data || '');
    }
  }
}

/**
 * Retry utility with exponential backoff
 */
class RetryHandler {
  private maxRetries: number;
  private baseDelay: number = 1000; // 1 second

  constructor(maxRetries: number = 3) {
    this.maxRetries = maxRetries;
  }

  async execute<T>(
    fn: () => Promise<T>,
    logger: Logger
  ): Promise<T> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error as Error;

        if (attempt < this.maxRetries - 1) {
          // Exponential backoff: 5s, 30s, 5m
          const delays = [5000, 30000, 300000];
          const delay = delays[attempt] || delays[delays.length - 1];

          logger.warn(
            `Attempt ${attempt + 1} failed, retrying in ${delay / 1000}s`,
            (error as AxiosError)?.message
          );

          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    throw lastError || new Error('Max retries exceeded');
  }
}

/**
 * ORVION Agent SDK - TypeScript/JavaScript Client
 * 
 * @example
 * ```typescript
 * const client = new OrvionClient({
 *   baseUrl: 'https://api.orvion.io',
 *   apiToken: 'your-token'
 * });
 * 
 * const agent = await client.registerAgent({
 *   agent_address: '0x...',
 *   agent_name: 'MyAgent',
 *   agent_type: 'processor',
 *   capabilities: ['processing', 'validation'],
 *   pricing_per_call: 0.5
 * });
 * ```
 */
export class OrvionClient {
  private baseUrl: string;
  private apiToken?: string;
  private timeout: number;
  private maxRetries: number;
  private logger: Logger;
  private retryHandler: RetryHandler;
  private client: AxiosInstance;

  constructor(config: OrvionClientConfig = {}) {
    this.baseUrl = config.baseUrl || 'http://localhost:8000';
    this.apiToken = config.apiToken;
    this.timeout = config.timeout || 30000; // 30 seconds
    this.maxRetries = config.maxRetries || 3;
    this.logger = new Logger(config.logLevel || 'info');
    this.retryHandler = new RetryHandler(this.maxRetries);

    // Setup axios instance
    this.client = axios.create({
      baseURL: `${this.baseUrl}/api/v1`,
      timeout: this.timeout,
      headers: this.getHeaders(),
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      response => response,
      error => {
        this.logger.error('API Error', {
          status: error.response?.status,
          message: error.message,
        });
        throw error;
      }
    );

    this.logger.info(`ORVION SDK initialized: ${this.baseUrl}`);
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'User-Agent': 'OrvionClient/2.0',
    };

    if (this.apiToken) {
      headers['Authorization'] = `Bearer ${this.apiToken}`;
    }

    return headers;
  }

  /**
   * Register an agent in the ORVION Discovery Registry
   */
  async registerAgent(agentData: AgentData): Promise<AgentResponse> {
    return this.retryHandler.execute(async () => {
      this.logger.info(`Registering agent: ${agentData.agent_name}`);

      const response = await this.client.post<AgentResponse>(
        '/discovery/agents',
        agentData
      );

      this.logger.info(`Agent registered: ${response.data.id}`);
      return response.data;
    }, this.logger);
  }

  /**
   * Create a job and escrow funds in USDC
   */
  async createJobAndEscrow(jobData: JobData): Promise<SettlementResponse> {
    return this.retryHandler.execute(async () => {
      this.logger.info(
        `Creating job: ${jobData.job_id} for agent ${jobData.agent_id}`
      );

      const response = await this.client.post<SettlementResponse>(
        '/settlement/settlements',
        jobData
      );

      this.logger.info(`Job created: ${response.data.id}`);
      return response.data;
    }, this.logger);
  }

  /**
   * Submit proof of work to trigger verification and payment release
   */
  async submitProofOfWork(proofData: ProofData): Promise<SettlementResponse> {
    return this.retryHandler.execute(async () => {
      this.logger.info(`Submitting proof for job: ${proofData.job_id}`);

      const response = await this.client.post<SettlementResponse>(
        '/settlement/execution-receipts',
        proofData
      );

      this.logger.info(`Proof submitted: ${response.data.id}`);
      return response.data;
    }, this.logger);
  }

  /**
   * Check the status of a settlement
   */
  async getStatus(settlementId: string): Promise<SettlementResponse> {
    return this.retryHandler.execute(async () => {
      this.logger.debug(`Checking status for settlement: ${settlementId}`);

      const response = await this.client.get<SettlementResponse>(
        `/settlement/settlements/${settlementId}`
      );

      this.logger.debug(`Settlement status: ${response.data.status}`);
      return response.data;
    }, this.logger);
  }

  /**
   * Get reputation score for an agent
   */
  async getAgentReputation(
    agentId: string,
    days?: number
  ): Promise<ReputationResponse> {
    return this.retryHandler.execute(async () => {
      this.logger.info(`Fetching reputation for agent: ${agentId}`);

      const params: Record<string, any> = {};
      if (days) {
        params.days = days;
      }

      const response = await this.client.get<ReputationResponse>(
        `/agents/${agentId}/reputation-score`,
        { params }
      );

      return response.data;
    }, this.logger);
  }

  /**
   * Submit feedback about an agent
   */
  async submitFeedback(
    agentId: string,
    score: number,
    comment?: string,
    settlementId?: string
  ): Promise<FeedbackResponse> {
    if (score < 0 || score > 5) {
      throw new Error('Feedback score must be between 0 and 5');
    }

    return this.retryHandler.execute(async () => {
      this.logger.info(`Submitting feedback for agent ${agentId}: ${score}/5`);

      const response = await this.client.post<FeedbackResponse>(
        `/agents/${agentId}/feedback`,
        {
          score,
          comment,
          settlement_id: settlementId,
        }
      );

      return response.data;
    }, this.logger);
  }

  /**
   * Get top-rated agents
   */
  async getTopAgents(
    agentType?: string,
    minReputation: number = 0,
    limit: number = 10
  ): Promise<AgentResponse[]> {
    return this.retryHandler.execute(async () => {
      this.logger.info(`Fetching top ${limit} agents`);

      const params: Record<string, any> = {
        limit,
        min_reputation: minReputation,
      };

      if (agentType) {
        params.agent_type = agentType;
      }

      const response = await this.client.get<AgentResponse[]>(
        '/agents/top-rated',
        { params }
      );

      return response.data;
    }, this.logger);
  }

  /**
   * Get all agents with pagination
   */
  async getAgents(limit: number = 10, offset: number = 0): Promise<AgentResponse[]> {
    return this.retryHandler.execute(async () => {
      this.logger.info(`Fetching agents (limit: ${limit}, offset: ${offset})`);

      const response = await this.client.get<AgentResponse[]>(
        '/discovery/agents',
        {
          params: { limit, offset },
        }
      );

      return response.data;
    }, this.logger);
  }

  /**
   * Close the client and cleanup resources
   */
  close(): void {
    this.logger.info('ORVION SDK client closed');
  }
}

export default OrvionClient;
