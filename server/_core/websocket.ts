import { Server as HTTPServer } from 'http';
import { Server as SocketIOServer, Socket } from 'socket.io';
import { logger } from './middleware';

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

class WebSocketServer {
  private io: SocketIOServer;
  private connectedClients: Map<string, Socket> = new Map();
  private subscriptions: Map<string, Set<string>> = new Map();

  constructor(httpServer: HTTPServer) {
    this.io = new SocketIOServer(httpServer, {
      cors: {
        origin: process.env.FRONTEND_URL || 'http://localhost:5173',
        methods: ['GET', 'POST'],
        credentials: true,
      },
      transports: ['websocket', 'polling'],
    });

    this.setupEventHandlers();
    logger.info('WebSocket server initialized');
  }

  private setupEventHandlers() {
    this.io.on('connection', (socket: Socket) => {
      const clientId = socket.id;
      this.connectedClients.set(clientId, socket);

      logger.info('Client connected', { clientId, totalClients: this.connectedClients.size });

      socket.on('subscribe:settlements', () => {
        if (!this.subscriptions.has('settlements')) {
          this.subscriptions.set('settlements', new Set());
        }
        this.subscriptions.get('settlements')!.add(clientId);
        socket.emit('subscribed', { channel: 'settlements' });
        logger.debug('Client subscribed to settlements', { clientId });
      });

      socket.on('subscribe:jobs', () => {
        if (!this.subscriptions.has('jobs')) {
          this.subscriptions.set('jobs', new Set());
        }
        this.subscriptions.get('jobs')!.add(clientId);
        socket.emit('subscribed', { channel: 'jobs' });
        logger.debug('Client subscribed to jobs', { clientId });
      });

      socket.on('subscribe:metrics', () => {
        if (!this.subscriptions.has('metrics')) {
          this.subscriptions.set('metrics', new Set());
        }
        this.subscriptions.get('metrics')!.add(clientId);
        socket.emit('subscribed', { channel: 'metrics' });
        logger.debug('Client subscribed to metrics', { clientId });
      });

      socket.on('unsubscribe', (channel: string) => {
        const subscribers = this.subscriptions.get(channel);
        if (subscribers) {
          subscribers.delete(clientId);
        }
        logger.debug('Client unsubscribed', { clientId, channel });
      });

      socket.on('ping', () => {
        socket.emit('pong');
      });

      socket.on('disconnect', () => {
        this.connectedClients.delete(clientId);

        this.subscriptions.forEach((subscribers) => {
          subscribers.delete(clientId);
        });

        logger.info('Client disconnected', { clientId, totalClients: this.connectedClients.size });
      });

      socket.on('error', (error: any) => {
        logger.error('WebSocket error', { clientId, error });
      });
    });
  }

  broadcastSettlementUpdate(update: SettlementUpdate) {
    const subscribers = this.subscriptions.get('settlements');
    if (!subscribers || subscribers.size === 0) {
      return;
    }

    subscribers.forEach((clientId) => {
      const socket = this.connectedClients.get(clientId);
      if (socket) {
        socket.emit('settlement:update', update);
      }
    });

    logger.debug('Settlement update broadcast', {
      update,
      recipientCount: subscribers.size,
    });
  }

  broadcastJobUpdate(update: JobUpdate) {
    const subscribers = this.subscriptions.get('jobs');
    if (!subscribers || subscribers.size === 0) {
      return;
    }

    subscribers.forEach((clientId) => {
      const socket = this.connectedClients.get(clientId);
      if (socket) {
        socket.emit('job:update', update);
      }
    });

    logger.debug('Job update broadcast', {
      update,
      recipientCount: subscribers.size,
    });
  }

  broadcastMetricsUpdate(update: MetricsUpdate) {
    const subscribers = this.subscriptions.get('metrics');
    if (!subscribers || subscribers.size === 0) {
      return;
    }

    subscribers.forEach((clientId) => {
      const socket = this.connectedClients.get(clientId);
      if (socket) {
        socket.emit('metrics:update', update);
      }
    });

    logger.debug('Metrics update broadcast', {
      update,
      recipientCount: subscribers.size,
    });
  }

  getIO(): SocketIOServer {
    return this.io;
  }

  getConnectedClientsCount(): number {
    return this.connectedClients.size;
  }

  getSubscriptionCount(channel: string): number {
    return this.subscriptions.get(channel)?.size || 0;
  }

  async shutdown(): Promise<void> {
    return new Promise((resolve) => {
      this.io.close(() => {
        logger.info('WebSocket server shut down');
        resolve();
      });
    });
  }
}

let wsServer: WebSocketServer | null = null;

export function initializeWebSocket(httpServer: HTTPServer): WebSocketServer {
  if (!wsServer) {
    wsServer = new WebSocketServer(httpServer);
  }
  return wsServer;
}

export function getWebSocketServer(): WebSocketServer {
  if (!wsServer) {
    throw new Error('WebSocket server not initialized. Call initializeWebSocket first.');
  }
  return wsServer;
}

export function broadcastSettlementUpdate(update: SettlementUpdate) {
  const server = getWebSocketServer();
  server.broadcastSettlementUpdate(update);
}

export function broadcastJobUpdate(update: JobUpdate) {
  const server = getWebSocketServer();
  server.broadcastJobUpdate(update);
}

export function broadcastMetricsUpdate(update: MetricsUpdate) {
  const server = getWebSocketServer();
  server.broadcastMetricsUpdate(update);
}

export type { SettlementUpdate, JobUpdate, MetricsUpdate };
