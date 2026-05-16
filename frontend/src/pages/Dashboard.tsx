/**
 * ORVION Dashboard
 * Real-time visualization of agents, jobs, and settlements
 */

import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import './Dashboard.css';

interface Agent {
  id: string;
  name: string;
  type: string;
  reputation: number;
  totalJobs: number;
  successRate: number;
}

interface Settlement {
  id: string;
  agentId: string;
  amount: number;
  status: 'pending' | 'confirmed' | 'failed';
  timestamp: string;
}

interface DashboardStats {
  totalAgents: number;
  totalSettlements: number;
  totalVolume: number;
  avgReputation: number;
  successRate: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalAgents: 0,
    totalSettlements: 0,
    totalVolume: 0,
    avgReputation: 0,
    successRate: 0,
  });

  const [agents, setAgents] = useState<Agent[]>([]);
  const [settlements, setSettlements] = useState<Settlement[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch stats
      const statsRes = await fetch('/api/v1/dashboard/stats');
      const statsData = await statsRes.json();
      setStats(statsData);

      // Fetch agents
      const agentsRes = await fetch('/api/v1/discovery/agents');
      const agentsData = await agentsRes.json();
      setAgents(agentsData.slice(0, 10));

      // Fetch settlements
      const settlementsRes = await fetch('/api/v1/settlement/settlements');
      const settlementsData = await settlementsRes.json();
      setSettlements(settlementsData.slice(0, 10));

      // Generate chart data
      generateChartData(settlementsData);

      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      setLoading(false);
    }
  };

  const generateChartData = (data: Settlement[]) => {
    const grouped = data.reduce((acc: any, settlement: Settlement) => {
      const date = new Date(settlement.timestamp).toLocaleDateString();
      const existing = acc.find((item: any) => item.date === date);

      if (existing) {
        existing.volume += settlement.amount;
        existing.count += 1;
      } else {
        acc.push({ date, volume: settlement.amount, count: 1 });
      }

      return acc;
    }, []);

    setChartData(grouped.slice(-7));
  };

  const COLORS = ['#10b981', '#f59e0b', '#ef4444'];

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>ORVION Dashboard</h1>
        <p>Real-time Settlement Layer Monitoring</p>
      </header>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Agents</div>
          <div className="stat-value">{stats.totalAgents}</div>
          <div className="stat-change">↑ 12% this week</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Total Settlements</div>
          <div className="stat-value">{stats.totalSettlements}</div>
          <div className="stat-change">↑ 8% this week</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Total Volume</div>
          <div className="stat-value">${stats.totalVolume.toFixed(2)}</div>
          <div className="stat-change">↑ 15% this week</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Avg Reputation</div>
          <div className="stat-value">{stats.avgReputation.toFixed(2)}/5</div>
          <div className="stat-change">Stable</div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        {/* Volume Chart */}
        <div className="chart-container">
          <h2>Settlement Volume (7 days)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="volume"
                stroke="#10b981"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Status Distribution */}
        <div className="chart-container">
          <h2>Settlement Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={[
                  {
                    name: 'Confirmed',
                    value: settlements.filter((s) => s.status === 'confirmed')
                      .length,
                  },
                  {
                    name: 'Pending',
                    value: settlements.filter((s) => s.status === 'pending')
                      .length,
                  },
                  {
                    name: 'Failed',
                    value: settlements.filter((s) => s.status === 'failed')
                      .length,
                  },
                ]}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {COLORS.map((color, index) => (
                  <Cell key={`cell-${index}`} fill={color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Agents Table */}
      <div className="table-container">
        <h2>Top Agents</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Reputation</th>
              <th>Jobs</th>
              <th>Success Rate</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((agent) => (
              <tr key={agent.id}>
                <td>{agent.name}</td>
                <td>{agent.type}</td>
                <td>{agent.reputation.toFixed(2)}</td>
                <td>{agent.totalJobs}</td>
                <td>{(agent.successRate * 100).toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Recent Settlements */}
      <div className="table-container">
        <h2>Recent Settlements</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Settlement ID</th>
              <th>Agent</th>
              <th>Amount (USDC)</th>
              <th>Status</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {settlements.map((settlement) => (
              <tr key={settlement.id}>
                <td className="mono">{settlement.id.slice(0, 10)}...</td>
                <td className="mono">{settlement.agentId.slice(0, 10)}...</td>
                <td>${settlement.amount.toFixed(2)}</td>
                <td>
                  <span className={`status status-${settlement.status}`}>
                    {settlement.status}
                  </span>
                </td>
                <td>{new Date(settlement.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
