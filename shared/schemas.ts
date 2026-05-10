import { z } from 'zod';

/**
 * Shared validation schemas for tRPC procedures
 * Ensures type safety and input validation across the API
 */

// Agent schemas
export const createAgentSchema = z.object({
  name: z.string().min(3).max(100),
  description: z.string().min(10).max(1000).optional(),
  status: z.enum(['active' as const, 'inactive' as const, 'suspended' as const]).default('active'),
});

export const updateAgentStatusSchema = z.object({
  agentId: z.number().positive(),
  status: z.enum(['active' as const, 'inactive' as const, 'suspended' as const]),
});

export const getAgentSchema = z.object({
  agentId: z.number().positive(),
});

// Job schemas
export const createJobSchema = z.object({
  agentId: z.number().positive(),
  title: z.string().min(3).max(200),
  description: z.string().min(10).max(2000).optional(),
  inputData: z.record(z.string(), z.any()).optional(),
});

export const updateJobStatusSchema = z.object({
  jobId: z.number().positive(),
  status: z.enum(['pending' as const, 'running' as const, 'completed' as const, 'failed' as const]),
  outputData: z.record(z.string(), z.any()).optional(),
});

export const getJobSchema = z.object({
  jobId: z.number().positive(),
});

export const listJobsSchema = z.object({
  page: z.number().int().positive().default(1),
  limit: z.number().int().positive().max(100).default(20),
  agentId: z.number().positive().optional(),
  status: z.enum(['pending' as const, 'running' as const, 'completed' as const, 'failed' as const]).optional(),
});

// Settlement schemas
export const createSettlementSchema = z.object({
  jobId: z.number().positive(),
  agentId: z.number().positive(),
  amount: z.string().regex(/^\d+(\.\d{1,6})?$/, 'Invalid amount format'),
  currency: z.enum(['USDC' as const, 'USDT' as const, 'ETH' as const]).default('USDC'),
  blockchainNetwork: z.enum(['Ethereum' as const, 'Polygon' as const, 'Arbitrum' as const, 'Optimism' as const]),
  transactionHash: z.string().regex(/^0x[a-fA-F0-9]{64}$/).optional(),
});

export const updateSettlementStatusSchema = z.object({
  settlementId: z.number().positive(),
  status: z.enum(['pending' as const, 'confirmed' as const, 'failed' as const, 'settled' as const]),
  transactionHash: z.string().regex(/^0x[a-fA-F0-9]{64}$/).optional(),
});

export const getSettlementSchema = z.object({
  settlementId: z.number().positive(),
});

export const filterSettlementsSchema = z.object({
  page: z.number().int().positive().default(1),
  limit: z.number().int().positive().max(100).default(20),
  network: z.enum(['Ethereum' as const, 'Polygon' as const, 'Arbitrum' as const, 'Optimism' as const]).optional(),
  status: z.enum(['pending' as const, 'confirmed' as const, 'failed' as const, 'settled' as const]).optional(),
  agentId: z.number().positive().optional(),
  startDate: z.string().optional(),
  endDate: z.string().optional(),
});

// Metrics schemas
export const getMetricsSchema = z.object({
  period: z.enum(['1h' as const, '24h' as const, '7d' as const, '30d' as const, 'all' as const]).default('24h'),
});

// Analysis schemas
export const analyzeAgentPerformanceSchema = z.object({
  agentId: z.number().positive(),
  period: z.enum(['7d' as const, '30d' as const, '90d' as const, 'all' as const]).default('30d'),
});

// Notification schemas
export const notifyOwnerSchema = z.object({
  title: z.string().min(5).max(200),
  content: z.string().min(10).max(2000),
  type: z.enum(['settlement' as const, 'job' as const, 'alert' as const, 'info' as const]).default('info'),
  metadata: z.record(z.string(), z.any()).optional(),
});

// Type exports for frontend
export type CreateAgentInput = z.infer<typeof createAgentSchema>;
export type UpdateAgentStatusInput = z.infer<typeof updateAgentStatusSchema>;
export type CreateJobInput = z.infer<typeof createJobSchema>;
export type UpdateJobStatusInput = z.infer<typeof updateJobStatusSchema>;
export type CreateSettlementInput = z.infer<typeof createSettlementSchema>;
export type UpdateSettlementStatusInput = z.infer<typeof updateSettlementStatusSchema>;
export type FilterSettlementsInput = z.infer<typeof filterSettlementsSchema>;
export type GetMetricsInput = z.infer<typeof getMetricsSchema>;
export type AnalyzeAgentPerformanceInput = z.infer<typeof analyzeAgentPerformanceSchema>;
export type NotifyOwnerInput = z.infer<typeof notifyOwnerSchema>;
