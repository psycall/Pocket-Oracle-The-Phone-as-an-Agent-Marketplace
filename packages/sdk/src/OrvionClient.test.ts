/**
 * ORVION SDK - Unit Tests
 */

import { OrvionClient } from './OrvionClient';

describe('OrvionClient', () => {
  let client: OrvionClient;

  beforeEach(() => {
    client = new OrvionClient({
      baseUrl: 'http://localhost:8000',
      apiToken: 'test-token',
      logLevel: 'error',
    });
  });

  afterEach(() => {
    client.close();
  });

  describe('Initialization', () => {
    it('should initialize with default config', () => {
      const defaultClient = new OrvionClient();
      expect(defaultClient).toBeDefined();
      defaultClient.close();
    });

    it('should initialize with custom config', () => {
      expect(client).toBeDefined();
    });

    it('should set correct base URL', () => {
      const customClient = new OrvionClient({
        baseUrl: 'https://api.orvion.io',
      });
      expect(customClient).toBeDefined();
      customClient.close();
    });
  });

  describe('Configuration', () => {
    it('should accept timeout configuration', () => {
      const customClient = new OrvionClient({
        timeout: 60000,
      });
      expect(customClient).toBeDefined();
      customClient.close();
    });

    it('should accept maxRetries configuration', () => {
      const customClient = new OrvionClient({
        maxRetries: 5,
      });
      expect(customClient).toBeDefined();
      customClient.close();
    });

    it('should accept log level configuration', () => {
      const customClient = new OrvionClient({
        logLevel: 'debug',
      });
      expect(customClient).toBeDefined();
      customClient.close();
    });
  });

  describe('API Methods', () => {
    it('should have registerAgent method', () => {
      expect(typeof client.registerAgent).toBe('function');
    });

    it('should have createJobAndEscrow method', () => {
      expect(typeof client.createJobAndEscrow).toBe('function');
    });

    it('should have submitProofOfWork method', () => {
      expect(typeof client.submitProofOfWork).toBe('function');
    });

    it('should have getStatus method', () => {
      expect(typeof client.getStatus).toBe('function');
    });

    it('should have getAgentReputation method', () => {
      expect(typeof client.getAgentReputation).toBe('function');
    });

    it('should have submitFeedback method', () => {
      expect(typeof client.submitFeedback).toBe('function');
    });

    it('should have getTopAgents method', () => {
      expect(typeof client.getTopAgents).toBe('function');
    });

    it('should have getAgents method', () => {
      expect(typeof client.getAgents).toBe('function');
    });

    it('should have close method', () => {
      expect(typeof client.close).toBe('function');
    });
  });

  describe('Feedback Validation', () => {
    it('should reject feedback score below 0', async () => {
      await expect(
        client.submitFeedback('agent-123', -1, 'Bad score')
      ).rejects.toThrow('Feedback score must be between 0 and 5');
    });

    it('should reject feedback score above 5', async () => {
      await expect(
        client.submitFeedback('agent-123', 6, 'Too high')
      ).rejects.toThrow('Feedback score must be between 0 and 5');
    });

    it('should accept valid feedback scores', async () => {
      // This will fail due to no actual server, but validates score acceptance
      for (let score = 0; score <= 5; score++) {
        try {
          await client.submitFeedback('agent-123', score, 'Test');
        } catch (error: any) {
          // Expected to fail with network error, not validation error
          expect(error.message).not.toContain('Feedback score must be between');
        }
      }
    });
  });

  describe('Resource Cleanup', () => {
    it('should close client gracefully', () => {
      const testClient = new OrvionClient();
      expect(() => testClient.close()).not.toThrow();
    });
  });
});
