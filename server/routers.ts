import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, router } from "./_core/trpc";
import { z } from "zod";
import {
  getAgents,
  getAgentById,
  createAgent,
  getJobs,
  getJobById,
  createJob,
  getSettlements,
  getSettlementById,
  createSettlement,
  getLatestMetrics,
  updateMetrics,
} from "./db";
import { invokeLLM } from "./_core/llm";
import { notifyOwner } from "./_core/notification";
import { sendSettlement as arcPaySendSettlement, getWalletBalance, estimateGasCost } from "./_core/arcpay";

export const appRouter = router({
  system: systemRouter,
  auth: router({
    me: publicProcedure.query((opts) => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  // ============ AGENTS ROUTER ============
  agents: router({
    list: publicProcedure.query(async () => {
      const agents = await getAgents();
      return agents || [];
    }),

    getById: publicProcedure.input(z.object({ id: z.number() })).query(async ({ input }) => {
      return await getAgentById(input.id);
    }),

    create: protectedProcedure
      .input(
        z.object({
          name: z.string().min(1),
          description: z.string().optional(),
        })
      )
      .mutation(async ({ input, ctx }) => {
        await createAgent({
          userId: ctx.user.id,
          name: input.name,
          description: input.description,
          status: "active",
          reputationScore: 0,
          totalJobsCompleted: 0,
          totalVolumeSettled: "0",
        });
        return { success: true };
      }),
  }),

  // ============ JOBS ROUTER ============
  jobs: router({
    list: publicProcedure.query(async () => {
      const jobs = await getJobs();
      return jobs || [];
    }),

    getById: publicProcedure.input(z.object({ id: z.number() })).query(async ({ input }) => {
      return await getJobById(input.id);
    }),

    create: protectedProcedure
      .input(
        z.object({
          agentId: z.number(),
          title: z.string().min(1),
          description: z.string().optional(),
          inputData: z.string().optional(),
        })
      )
      .mutation(async ({ input }) => {
        await createJob({
          agentId: input.agentId,
          title: input.title,
          description: input.description,
          inputData: input.inputData,
          status: "pending",
        });
        return { success: true };
      }),

    updateStatus: protectedProcedure
      .input(
        z.object({
          jobId: z.number(),
          status: z.enum(["pending", "executing", "completed", "failed", "settled"]),
        })
      )
      .mutation(async ({ input }) => {
        // TODO: Implement status update logic
        return { success: true };
      }),
  }),

  // ============ SETTLEMENTS ROUTER ============
  settlements: router({
    list: publicProcedure.query(async () => {
      const settlements = await getSettlements();
      return settlements || [];
    }),

    getById: publicProcedure.input(z.object({ id: z.number() })).query(async ({ input }) => {
      return await getSettlementById(input.id);
    }),

    create: protectedProcedure
      .input(
        z.object({
          jobId: z.number(),
          agentId: z.number(),
          amount: z.string(),
          blockchainNetwork: z.string(),
          transactionHash: z.string().optional(),
        })
      )
      .mutation(async ({ input }) => {
        await createSettlement({
          jobId: input.jobId,
          agentId: input.agentId,
          amount: input.amount,
          currency: "USDC",
          blockchainNetwork: input.blockchainNetwork,
          transactionHash: input.transactionHash,
          status: "pending",
        });

        // Notify owner about new settlement
        await notifyOwner({
          title: `New Settlement Created`,
          content: `Settlement of ${input.amount} USDC on ${input.blockchainNetwork} for Job #${input.jobId}`,
        });

        return { success: true };
      }),

    filter: publicProcedure
      .input(
        z.object({
          network: z.string().optional(),
          status: z.string().optional(),
        })
      )
      .query(async ({ input }) => {
        const settlements = await getSettlements();
        return (settlements || []).filter((s) => {
          if (input.network && s.blockchainNetwork !== input.network) return false;
          if (input.status && s.status !== input.status) return false;
          return true;
        });
      }),

    // Real USDC settlement via ArcPay
    createReal: protectedProcedure
      .input(
        z.object({
          jobId: z.number(),
          agentId: z.number(),
          amount: z.string(),
          recipientAddress: z.string(),
          blockchainNetwork: z.string().default("arc"),
        })
      )
      .mutation(async ({ input }) => {
        try {
          // Send real USDC via ArcPay
          const result = await arcPaySendSettlement({
            recipientAddress: input.recipientAddress,
            amount: input.amount,
            jobId: input.jobId,
            agentId: input.agentId,
          });

          // Record settlement in database
          await createSettlement({
            jobId: input.jobId,
            agentId: input.agentId,
            amount: input.amount,
            currency: "USDC",
            blockchainNetwork: input.blockchainNetwork,
            transactionHash: result.transactionHash,
            status: result.status === 'confirmed' ? 'settled' : 'pending',
          });

          // Notify owner
          await notifyOwner({
            title: `Settlement Confirmed: ${input.amount} USDC`,
            content: `Real USDC settlement completed.\nTx: ${result.transactionHash}\nRecipient: ${input.recipientAddress}\nJob #${input.jobId} | Agent #${input.agentId}`,
          });

          return {
            success: true,
            transactionHash: result.transactionHash,
            status: result.status,
            blockNumber: result.blockNumber,
          };
        } catch (error) {
          // Notify owner about failure
          await notifyOwner({
            title: `Settlement Failed: ${input.amount} USDC`,
            content: `Settlement failed for Job #${input.jobId}.\nError: ${error instanceof Error ? error.message : 'Unknown error'}\nRecipient: ${input.recipientAddress}`,
          });

          throw error;
        }
      }),

    // Get wallet balance
    getWalletBalance: protectedProcedure.query(async () => {
      try {
        const balance = await getWalletBalance();
        return { balance, currency: 'USDC' };
      } catch {
        return { balance: '0', currency: 'USDC' };
      }
    }),

    // Estimate gas cost
    estimateGas: protectedProcedure
      .input(z.object({ amount: z.string() }))
      .query(async ({ input }) => {
        try {
          const gasCost = await estimateGasCost(input.amount);
          return { gasCost, currency: 'ETH' };
        } catch {
          return { gasCost: '0.001', currency: 'ETH' };
        }
      }),
  }),

  // ============ DASHBOARD ROUTER ============
  dashboard: router({
    getMetrics: publicProcedure.query(async () => {
      const metrics = await getLatestMetrics();
      if (metrics) {
        return metrics;
      }
      // Return default metrics if none exist
      return {
        id: 0,
        totalSettlements: 0,
        registeredAgents: 0,
        volumeTransacted: "0",
        networkStatus: "online" as const,
        averageSettlementTime: 0,
        successRate: "0",
        timestamp: new Date(),
      };
    }),
  }),

  // ============ LLM ANALYSIS ROUTER ============
  analysis: router({
    analyzeAgentPerformance: protectedProcedure
      .input(z.object({ agentId: z.number() }))
      .mutation(async ({ input }) => {
        const agent = await getAgentById(input.agentId);
        if (!agent) {
          throw new Error("Agent not found");
        }

        const jobs = (await getJobs()) || [];
        const agentJobs = jobs.filter((j) => j.agentId === input.agentId);

        const prompt = `
Analyze the performance of the AI agent "${agent.name}" based on the following metrics:
- Total Jobs Completed: ${agent.totalJobsCompleted}
- Reputation Score: ${agent.reputationScore}
- Total Volume Settled: ${agent.totalVolumeSettled} USDC
- Recent Jobs: ${agentJobs.length} jobs

Provide:
1. Performance Summary
2. Reputation Analysis
3. Optimization Recommendations
4. Risk Assessment

Format as a professional report.
        `;

        const response = await invokeLLM({
          messages: [
            {
              role: "system",
              content:
                "You are an expert AI agent performance analyst. Provide detailed, actionable insights.",
            },
            {
              role: "user",
              content: prompt,
            },
          ],
        });

        return {
          agentId: input.agentId,
          agentName: agent.name,
          analysis: response.choices[0]?.message.content || "Analysis unavailable",
          generatedAt: new Date(),
        };
      }),
  }),
});

export type AppRouter = typeof appRouter;
