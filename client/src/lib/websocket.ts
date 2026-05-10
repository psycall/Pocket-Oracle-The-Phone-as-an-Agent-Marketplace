import { io, Socket } from 'socket.io-client';

interface SettlementUpdate {
  settlementId: number;
  jobId: number;
  agentId: number;
  transactionHash: string;
  status: 'pending' | 'confirmed' | 'failed' | 'settled';
  amount: string;
  timestamp: number;
}

interface JobUpdate {
  jobId: number;
  agentId: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  timestamp: number;
}

interface MetricsUpdate {
  totalSettlements: number;
  registeredAgents: number;
  volumeTransacted: number;
  networkStatus: 'healthy' | 'degraded' | 'offline';
  timestamp: number;
}

type EventCallback<T> = (data: T) => void;

class WebSocketClient {
  private socket: Socket | null = null;
  private url: string;
  private listeners: Map<string, Set<EventCallback<any>>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(url: string = window.location.origin) {
    this.url = url;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.socket = io(this.url, {
          reconnection: true,
          reconnectionDelay: this.reconnectDelay,
          reconnectionDelayMax: 5000,
          reconnectionAttempts: this.maxReconnectAttempts,
          transports: ['websocket', 'polling'],
        });

        this.socket.on('connect', () => {
          console.log('[WebSocket] Connected to server');
          this.reconnectAttempts = 0;
          this.emit('connected', {});
          resolve();
        });

        this.socket.on('disconnect', () => {
          console.log('[WebSocket] Disconnected from server');
          this.emit('disconnected', {});
        });

        this.socket.on('error', (error: any) => {
          console.error('[WebSocket] Error:', error);
          this.emit('error', { error });
          reject(error);
        });

        this.setupEventListeners();
      } catch (error) {
        reject(error);
      }
    });
  }

  private setupEventListeners() {
    if (!this.socket) return;

    this.socket.on('settlement:update', (data: SettlementUpdate) => {
      console.log('[WebSocket] Settlement update:', data);
      this.emit('settlement:update', data);
    });

    this.socket.on('job:update', (data: JobUpdate) => {
      console.log('[WebSocket] Job update:', data);
      this.emit('job:update', data);
    });

    this.socket.on('metrics:update', (data: MetricsUpdate) => {
      console.log('[WebSocket] Metrics update:', data);
      this.emit('metrics:update', data);
    });

    this.socket.on('subscribed', (data: { channel: string }) => {
      console.log('[WebSocket] Subscribed to channel:', data.channel);
      this.emit('subscribed', data);
    });

    this.socket.on('pong', () => {
      console.log('[WebSocket] Pong received');
    });
  }

  subscribeToSettlements(callback: EventCallback<SettlementUpdate>) {
    if (!this.socket) {
      throw new Error('WebSocket not connected');
    }

    this.on('settlement:update', callback);
    this.socket.emit('subscribe:settlements');
  }

  subscribeToJobs(callback: EventCallback<JobUpdate>) {
    if (!this.socket) {
      throw new Error('WebSocket not connected');
    }

    this.on('job:update', callback);
    this.socket.emit('subscribe:jobs');
  }

  subscribeToMetrics(callback: EventCallback<MetricsUpdate>) {
    if (!this.socket) {
      throw new Error('WebSocket not connected');
    }

    this.on('metrics:update', callback);
    this.socket.emit('subscribe:metrics');
  }

  unsubscribe(channel: string) {
    if (!this.socket) return;

    this.socket.emit('unsubscribe', channel);
    this.listeners.delete(channel);
  }

  ping() {
    if (!this.socket) return;
    this.socket.emit('ping');
  }

  on<T>(event: string, callback: EventCallback<T>) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off<T>(event: string, callback: EventCallback<T>) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.delete(callback);
    }
  }

  private emit<T>(event: string, data: T) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach((callback) => {
        try {
          callback(data);
        } catch (error) {
          console.error(`[WebSocket] Error in listener for ${event}:`, error);
        }
      });
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  reconnect() {
    if (this.socket) {
      this.socket.connect();
    }
  }
}

let wsClient: WebSocketClient | null = null;

export function getWebSocketClient(): WebSocketClient {
  if (!wsClient) {
    wsClient = new WebSocketClient();
  }
  return wsClient;
}

export async function initializeWebSocket(): Promise<WebSocketClient> {
  const client = getWebSocketClient();
  await client.connect();
  return client;
}

export type { SettlementUpdate, JobUpdate, MetricsUpdate };
