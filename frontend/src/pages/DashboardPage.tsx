import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { GlassCard } from "../components/GlassCard";
import { GlowButton } from "../components/GlowButton";
import { GradientText } from "../components/GradientText";
import { useAuth } from "../hooks/useAuth";
import { useApi, useApiMutation } from "../hooks/useApi";
import { apiClient, type Settlement, type Agent } from "../lib/api";
import {
  TrendingUp,
  Users,
  Zap,
  Shield,
  ArrowUpRight,
  ArrowDownRight,
  Loader2,
} from "lucide-react";

// Mock data for charts (will be replaced with real data)
const settlementData = [
  { name: "Mon", value: 2400, agents: 1200 },
  { name: "Tue", value: 1398, agents: 1221 },
  { name: "Wed", value: 9800, agents: 2290 },
  { name: "Thu", value: 3908, agents: 2000 },
  { name: "Fri", value: 4800, agents: 2181 },
  { name: "Sat", value: 3800, agents: 2500 },
  { name: "Sun", value: 4300, agents: 2100 },
];

export function DashboardPage() {
  const { user, isAuthenticated } = useAuth();
  const [settlements, setSettlements] = useState<Settlement[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);

  const atomicMutation = useApiMutation(
    (payload: { settlement_id: string; agent_wallet_id: string }) => 
      apiClient.processAtomicSettlement(payload.settlement_id, payload.agent_wallet_id)
  );

  const batchMutation = useApiMutation(
    (payload: { requests: { settlement_id: string; agent_wallet_id: string }[] }) => 
      apiClient.processBatchSettlement(payload.requests)
  );

  const createWalletMutation = useApiMutation(
    (agentId: string) => apiClient.createAgentWallet(agentId)
  );

  // Fetch dashboard stats
  const statsApi = useApi(
    () => apiClient.getDashboardStats(),
    [isAuthenticated]
  );

  // Fetch settlements
  const settlementsApi = useApi(
    () => apiClient.getSettlements(10, 0),
    [isAuthenticated]
  );

  // Fetch agents
  const agentsApi = useApi(
    () => apiClient.getAgents(10, 0),
    [isAuthenticated]
  );

  useEffect(() => {
    if (settlementsApi.data) {
      setSettlements(settlementsApi.data);
    }
  }, [settlementsApi.data]);

  useEffect(() => {
    if (agentsApi.data) {
      setAgents(agentsApi.data);
    }
  }, [agentsApi.data]);

  const stats = [
    {
      label: "Total Settlements",
      value: `$${(statsApi.data?.total_amount || 0).toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}`,
      change: "+12.5%",
      icon: Zap,
      color: "primary" as const,
    },
    {
      label: "Active Agents",
      value: statsApi.data?.active_agents || 0,
      change: "+8.2%",
      icon: Users,
      color: "secondary" as const,
    },
    {
      label: "Avg Reputation",
      value: `${(statsApi.data?.avg_reputation || 0).toFixed(1)}%`,
      change: "+2.1%",
      icon: TrendingUp,
      color: "primary" as const,
    },
    {
      label: "Success Rate",
      value: `${(statsApi.data?.success_rate || 0).toFixed(1)}%`,
      change: "+0.5%",
      icon: Shield,
      color: "secondary" as const,
    },
  ];

  const agentReputation = agents
    .slice(0, 4)
    .map((agent, idx) => ({
      name: agent.agent_name,
      value: agent.reputation_score,
      fill: ["#6366F1", "#10B981", "#F59E0B", "#EF4444"][idx],
    }));

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <GlassCard className="max-w-md">
          <h2 className="h3 mb-4">Authentication Required</h2>
          <p className="text-muted-foreground mb-6">
            Please log in with your Arc wallet to access the dashboard.
          </p>
          <GlowButton variant="primary" className="w-full">
            Connect Wallet
          </GlowButton>
        </GlassCard>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50"
      >
        <div className="container py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="h2 gradient-text">ORVION Dashboard</h1>
              <p className="text-muted-foreground mt-1">
                Welcome back, {user?.name || user?.wallet_address?.slice(0, 6)}
              </p>
            </div>
            <GlowButton variant="primary">New Settlement</GlowButton>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="container py-8">
        {/* Stats Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          {stats.map((stat, idx) => {
            const Icon = stat.icon;
            const isPositive = stat.change.startsWith("+");

            return (
              <motion.div key={idx} variants={itemVariants}>
                <GlassCard
                  highlighted={idx === 0}
                  glowColor={stat.color}
                  className="relative overflow-hidden"
                >
                  {statsApi.isLoading && (
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-pulse" />
                  )}
                  <div className="flex items-start justify-between mb-4">
                    <div className="p-3 rounded-lg bg-primary/10">
                      <Icon className="w-6 h-6 text-primary" />
                    </div>
                    <div
                      className={`flex items-center gap-1 text-sm font-medium ${
                        isPositive ? "text-secondary" : "text-danger"
                      }`}
                    >
                      {isPositive ? (
                        <ArrowUpRight className="w-4 h-4" />
                      ) : (
                        <ArrowDownRight className="w-4 h-4" />
                      )}
                      {stat.change}
                    </div>
                  </div>
                  <p className="text-muted-foreground text-sm mb-1">
                    {stat.label}
                  </p>
                  {statsApi.isLoading ? (
                    <div className="h-8 bg-white/5 rounded animate-pulse" />
                  ) : (
                    <p className="text-2xl font-bold">{stat.value}</p>
                  )}
                </GlassCard>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Charts Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8"
        >
          {/* Settlement Chart */}
          <motion.div variants={itemVariants} className="lg:col-span-2">
            <GlassCard>
              <h3 className="text-lg font-bold mb-6">Settlement Trend</h3>
              {settlementsApi.isLoading ? (
                <div className="h-80 flex items-center justify-center">
                  <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
              ) : (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={settlementData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis stroke="#B3B3B3" />
                    <YAxis stroke="#B3B3B3" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#1F1F1F",
                        border: "1px solid #333",
                        borderRadius: "8px",
                      }}
                    />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#6366F1"
                      strokeWidth={2}
                      dot={{ fill: "#6366F1", r: 4 }}
                      activeDot={{ r: 6 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="agents"
                      stroke="#10B981"
                      strokeWidth={2}
                      dot={{ fill: "#10B981", r: 4 }}
                      activeDot={{ r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </GlassCard>
          </motion.div>

          {/* Agent Reputation Pie */}
          <motion.div variants={itemVariants}>
            <GlassCard>
              <h3 className="text-lg font-bold mb-6">Agent Reputation</h3>
              {agentsApi.isLoading ? (
                <div className="h-80 flex items-center justify-center">
                  <Loader2 className="w-8 h-8 animate-spin text-secondary" />
                </div>
              ) : agentReputation.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={agentReputation}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {agentReputation.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-80 flex items-center justify-center text-muted-foreground">
                  No agent data available
                </div>
              )}
            </GlassCard>
          </motion.div>
        </motion.div>

        {/* Recent Settlements */}
        <motion.div variants={itemVariants}>
          <GlassCard>
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 className="text-lg font-bold">Recent Settlements</h3>
                <p className="text-xs text-muted-foreground">Atomic & Batch Settlement Control</p>
              </div>
              <div className="flex gap-2 w-full sm:w-auto">
                <GlowButton 
                  variant="secondary" 
                  size="sm" 
                  className="flex-1 sm:flex-none"
                  onClick={() => {
                    const pending = settlements.filter(s => s.status === "pending");
                    if (pending.length > 0) {
                      batchMutation.mutate({
                        requests: pending.map(s => ({ 
                          settlement_id: s.id, 
                          agent_wallet_id: "default-agent-wallet" 
                        }))
                      });
                    }
                  }}
                  isLoading={batchMutation.isLoading}
                >
                  Process All
                </GlowButton>
                <GlowButton variant="outline" size="sm" className="flex-1 sm:flex-none">
                  View All
                </GlowButton>
              </div>
            </div>

            {settlementsApi.isLoading ? (
              <div className="space-y-4">
                {[...Array(3)].map((_, idx) => (
                  <div
                    key={idx}
                    className="h-16 bg-white/5 rounded-lg animate-pulse"
                  />
                ))}
              </div>
            ) : settlements.length > 0 ? (
              <div className="space-y-4">
                {settlements.map((settlement, idx) => (
                  <motion.div
                    key={settlement.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 gap-4 rounded-lg bg-white/5 hover:bg-white/10 smooth-transition"
                  >
                    <div className="flex-1 min-w-0">
                      <p className="font-medium truncate">{settlement.agent_name}</p>
                      <p className="text-xs sm:text-sm text-muted-foreground truncate">
                        {settlement.id} • {new Date(settlement.created_at).toLocaleDateString()}
                      </p>
                    </div>

                    <div className="flex items-center justify-between sm:justify-end gap-4 w-full sm:w-auto">
                      <p className="font-bold text-lg">
                        ${settlement.amount.toFixed(2)}
                      </p>
                      <div className="flex items-center gap-2">
                        <div
                          className={`px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${
                            settlement.status === "completed"
                              ? "bg-secondary/20 text-secondary"
                              : settlement.status === "pending"
                              ? "bg-warning/20 text-warning"
                              : "bg-danger/20 text-danger"
                          }`}
                        >
                          {settlement.status.charAt(0).toUpperCase() +
                            settlement.status.slice(1)}
                        </div>
                        {settlement.status === "pending" && (
                          <GlowButton 
                            variant="primary" 
                            size="sm"
                            className="h-8 px-3"
                            isLoading={atomicMutation.isLoading}
                            onClick={() => atomicMutation.mutate({ 
                              settlement_id: settlement.id, 
                              agent_wallet_id: "default-agent-wallet" 
                            })}
                          >
                            Release
                          </GlowButton>
                        )}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                No settlements yet
              </div>
            )}
          </GlassCard>
        </motion.div>
      </div>
    </div>
  );
}

export default DashboardPage;
