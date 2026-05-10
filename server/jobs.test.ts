import { describe, expect, it } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

function createAuthContext(): TrpcContext {
  const user = {
    id: 1,
    openId: "test-user",
    email: "test@example.com",
    name: "Test User",
    loginMethod: "manus",
    role: "user" as const,
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  return {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: () => {},
    } as TrpcContext["res"],
  };
}

describe("jobs router", () => {
  it("should list jobs", async () => {
    const ctx = createAuthContext();
    const caller = appRouter.createCaller(ctx);
    const jobs = await caller.jobs.list();
    expect(Array.isArray(jobs)).toBe(true);
  });

  it("should create a job", async () => {
    const ctx = createAuthContext();
    const caller = appRouter.createCaller(ctx);
    const result = await caller.jobs.create({
      agentId: 1,
      title: "Test Job",
      description: "A test job",
    });
    expect(result.success).toBe(true);
  });

  it("should get job by id", async () => {
    const ctx = createAuthContext();
    const caller = appRouter.createCaller(ctx);
    const job = await caller.jobs.getById({ id: 1 });
    // Job may or may not exist, but should not throw
    expect(job === undefined || typeof job === "object").toBe(true);
  });

  it("should update job status", async () => {
    const ctx = createAuthContext();
    const caller = appRouter.createCaller(ctx);
    const result = await caller.jobs.updateStatus({
      jobId: 1,
      status: "completed",
    });
    expect(result.success).toBe(true);
  });
});
