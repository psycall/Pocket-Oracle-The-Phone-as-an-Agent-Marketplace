import { int, mysqlEnum, mysqlTable, text, timestamp, varchar } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * AI Agents Registry
 * Tracks all AI agents registered on the ORVION platform
 */
export const agents = mysqlTable("agents", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull().references(() => users.id),
  name: varchar("name", { length: 255 }).notNull(),
  description: text("description"),
  status: mysqlEnum("status", ["active", "inactive", "suspended"]).default("active").notNull(),
  reputationScore: int("reputationScore").default(0).notNull(),
  totalJobsCompleted: int("totalJobsCompleted").default(0).notNull(),
  totalVolumeSettled: varchar("totalVolumeSettled", { length: 255 }).default("0").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Agent = typeof agents.$inferSelect;
export type InsertAgent = typeof agents.$inferInsert;

/**
 * Jobs Management
 * Tracks all jobs created by agents, their execution status and results
 */
export const jobs = mysqlTable("jobs", {
  id: int("id").autoincrement().primaryKey(),
  agentId: int("agentId").notNull().references(() => agents.id),
  title: varchar("title", { length: 255 }).notNull(),
  description: text("description"),
  status: mysqlEnum("status", ["pending", "executing", "completed", "failed", "settled"]).default("pending").notNull(),
  inputData: text("inputData"),
  outputData: text("outputData"),
  executionTime: int("executionTime"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  completedAt: timestamp("completedAt"),
  settledAt: timestamp("settledAt"),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Job = typeof jobs.$inferSelect;
export type InsertJob = typeof jobs.$inferInsert;

/**
 * Settlements History
 * Records all on-chain settlements and USDC transfers
 */
export const settlements = mysqlTable("settlements", {
  id: int("id").autoincrement().primaryKey(),
  jobId: int("jobId").notNull().references(() => jobs.id),
  agentId: int("agentId").notNull().references(() => agents.id),
  amount: varchar("amount", { length: 255 }).notNull(),
  currency: varchar("currency", { length: 10 }).default("USDC").notNull(),
  blockchainNetwork: varchar("blockchainNetwork", { length: 100 }).notNull(),
  transactionHash: varchar("transactionHash", { length: 255 }),
  status: mysqlEnum("status", ["pending", "confirmed", "failed", "settled"]).default("pending").notNull(),
  gasUsed: varchar("gasUsed", { length: 255 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  confirmedAt: timestamp("confirmedAt"),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Settlement = typeof settlements.$inferSelect;
export type InsertSettlement = typeof settlements.$inferInsert;

/**
 * Dashboard Metrics
 * Real-time snapshots of platform statistics
 */
export const metrics = mysqlTable("metrics", {
  id: int("id").autoincrement().primaryKey(),
  totalSettlements: int("totalSettlements").default(0).notNull(),
  registeredAgents: int("registeredAgents").default(0).notNull(),
  volumeTransacted: varchar("volumeTransacted", { length: 255 }).default("0").notNull(),
  networkStatus: mysqlEnum("networkStatus", ["online", "degraded", "offline"]).default("online").notNull(),
  averageSettlementTime: int("averageSettlementTime").default(0).notNull(),
  successRate: varchar("successRate", { length: 10 }).default("0").notNull(),
  timestamp: timestamp("timestamp").defaultNow().notNull(),
});

export type Metric = typeof metrics.$inferSelect;
export type InsertMetric = typeof metrics.$inferInsert;