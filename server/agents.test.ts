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

describe("agents router", () => {
  it("should list agents", async () => {
    const ctx = createAuthContext();
    const caller = appRouter.createCaller(ctx);
    const agents = await caller.agents.list();
    expect(Array.isArray(agents)).toBe(true);
  });

  it("should create an agent", async () => {
    const ctx = createAuthContext();
    const caller = appRouter.createCaller(ctx);
    const result = await caller.agents.create({
      name: "Test Agent",
      description: "A test agent",
    });
    expect(result.success).toBe(true);
  });

  it("should get agent by id", async () => {
    const ctx = createAuthContext();
    const caller = appRouter.createCaller(ctx);
    const agent = await caller.agents.getById({ id: 1 });
    // Agent may or may not exist, but should not throw
    expect(agent === undefined || typeof agent === "object").toBe(true);
  });
});
