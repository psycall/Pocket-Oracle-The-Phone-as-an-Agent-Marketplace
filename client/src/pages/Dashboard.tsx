import { useAuth } from "@/_core/hooks/useAuth";
import { useLocation } from "wouter";
import { useEffect } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { trpc } from "@/lib/trpc";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Activity, Zap, TrendingUp, Gauge } from "lucide-react";

export default function Dashboard() {
  const { user, loading } = useAuth();
  const [, navigate] = useLocation();

  // Redirect to home if not authenticated
  useEffect(() => {
    if (!loading && !user) {
      navigate("/");
    }
  }, [user, loading, navigate]);

  const { data: metrics } = trpc.dashboard.getMetrics.useQuery();
  const { data: settlements } = trpc.settlements.list.useQuery();
  const { data: agents } = trpc.agents.list.useQuery();
  const { data: jobs } = trpc.jobs.list.useQuery();

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="spinner-orvion" />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const dashboardItems = [
    {
      label: "Total Settlements",
      value: metrics?.totalSettlements || 0,
      icon: Activity,
      color: "text-primary",
    },
    {
      label: "Registered Agents",
      value: metrics?.registeredAgents || 0,
      icon: Zap,
      color: "text-accent",
    },
    {
      label: "Volume Transacted",
      value: `$${metrics?.volumeTransacted || "0"} USDC`,
      icon: TrendingUp,
      color: "text-primary",
    },
    {
      label: "Network Status",
      value: metrics?.networkStatus || "online",
      icon: Gauge,
      color: "text-green-400",
    },
  ];

  // Mock data for charts
  const settlementData = [
    { name: "Mon", value: 400 },
    { name: "Tue", value: 300 },
    { name: "Wed", value: 200 },
    { name: "Thu", value: 278 },
    { name: "Fri", value: 190 },
    { name: "Sat", value: 229 },
    { name: "Sun", value: 200 },
  ];

  const agentPerformance = [
    { name: "Agent A", performance: 95 },
    { name: "Agent B", performance: 87 },
    { name: "Agent C", performance: 92 },
    { name: "Agent D", performance: 78 },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="section-title">Dashboard</h1>
          <p className="text-muted-foreground mt-2">Real-time settlement metrics and agent analytics</p>
        </div>

        {/* Metrics Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {dashboardItems.map((item, idx) => (
            <div key={idx} className="metric-card">
              <div className="flex items-start justify-between mb-4">
                <item.icon className={`w-6 h-6 ${item.color}`} />
              </div>
              <div className="metric-value mb-1">{item.value}</div>
              <div className="metric-label">{item.label}</div>
            </div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Settlement Trend */}
          <div className="card-orvion">
            <h3 className="font-bold text-lg mb-6">Settlement Trend (7 Days)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={settlementData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,215,0,0.1)" />
                <XAxis dataKey="name" stroke="rgba(255,215,0,0.5)" />
                <YAxis stroke="rgba(255,215,0,0.5)" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(5, 5, 5, 0.9)",
                    border: "1px solid rgba(255,215,0,0.5)",
                  }}
                />
                <Line type="monotone" dataKey="value" stroke="rgba(255,215,0,1)" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Agent Performance */}
          <div className="card-orvion">
            <h3 className="font-bold text-lg mb-6">Agent Performance</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={agentPerformance}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,215,0,0.1)" />
                <XAxis dataKey="name" stroke="rgba(255,215,0,0.5)" />
                <YAxis stroke="rgba(255,215,0,0.5)" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(5, 5, 5, 0.9)",
                    border: "1px solid rgba(255,215,0,0.5)",
                  }}
                />
                <Bar dataKey="performance" fill="rgba(255,215,0,0.8)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Settlements */}
        <div className="card-orvion">
          <h3 className="font-bold text-lg mb-6">Recent Settlements</h3>
          <div className="overflow-x-auto">
            <table className="table-orvion">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Agent</th>
                  <th>Amount</th>
                  <th>Network</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {(settlements || []).slice(0, 5).map((settlement, idx) => (
                  <tr key={idx}>
                    <td>#{settlement.id}</td>
                    <td>Agent {settlement.agentId}</td>
                    <td>{settlement.amount} {settlement.currency}</td>
                    <td className="font-mono text-sm">{settlement.blockchainNetwork}</td>
                    <td>
                      <span className={`status-${settlement.status}`}>{settlement.status}</span>
                    </td>
                    <td className="text-sm text-muted-foreground">
                      {new Date(settlement.createdAt).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="card-orvion text-center">
            <div className="metric-value mb-2">{jobs?.length || 0}</div>
            <div className="metric-label">Total Jobs</div>
          </div>
          <div className="card-orvion text-center">
            <div className="metric-value mb-2">{agents?.length || 0}</div>
            <div className="metric-label">Active Agents</div>
          </div>
          <div className="card-orvion text-center">
            <div className="metric-value mb-2">{metrics?.successRate || "0"}%</div>
            <div className="metric-label">Success Rate</div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
