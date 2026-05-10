import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { LineChart, Line, BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, TrendingDown, Activity, Zap, DollarSign, Users } from 'lucide-react';
import { trpc } from '@/lib/trpc';

/**
 * Advanced Analytics Dashboard (Binance-style)
 * Multiple layers: Overview → Detailed → Advanced
 */

type ViewMode = 'overview' | 'detailed' | 'advanced';
type TimeRange = '1h' | '24h' | '7d' | '30d' | 'all';

export default function Analytics() {
  const [viewMode, setViewMode] = useState<ViewMode>('overview');
  const [timeRange, setTimeRange] = useState<TimeRange>('24h');
  const [selectedMetric, setSelectedMetric] = useState<string>('settlements');

  // Fetch metrics
  const { data: metrics, isLoading } = trpc.dashboard.getMetrics.useQuery();

  // Mock data for charts (in production, this comes from backend)
  const settlementData = [
    { time: '00:00', amount: 12000, count: 45 },
    { time: '04:00', amount: 19000, count: 67 },
    { time: '08:00', amount: 15000, count: 52 },
    { time: '12:00', amount: 25000, count: 89 },
    { time: '16:00', amount: 22000, count: 78 },
    { time: '20:00', amount: 28000, count: 95 },
    { time: '23:59', amount: 31000, count: 105 },
  ];

  const agentPerformanceData = [
    { name: 'Agent-001', performance: 95, reputation: 4.8, settlements: 234 },
    { name: 'Agent-002', performance: 88, reputation: 4.5, settlements: 198 },
    { name: 'Agent-003', performance: 92, reputation: 4.7, settlements: 215 },
    { name: 'Agent-004', performance: 85, reputation: 4.3, settlements: 167 },
    { name: 'Agent-005', performance: 91, reputation: 4.6, settlements: 203 },
  ];

  const networkDistribution = [
    { name: 'Ethereum', value: 45, color: '#00FFFF' },
    { name: 'Polygon', value: 30, color: '#FFD700' },
    { name: 'Arbitrum', value: 20, color: '#FF6B6B' },
    { name: 'Optimism', value: 5, color: '#4ECDC4' },
  ];

  const jobStatusData = [
    { status: 'Completed', count: 1245, percentage: 78 },
    { status: 'Pending', count: 234, percentage: 15 },
    { status: 'Failed', count: 89, percentage: 5 },
    { status: 'Running', count: 32, percentage: 2 },
  ];

  // Stat cards
  const stats = [
    {
      title: 'Total Settlements',
      value: metrics?.totalSettlements || '0',
      change: '+12.5%',
      icon: DollarSign,
      positive: true,
    },
    {
      title: 'Active Agents',
      value: metrics?.registeredAgents || '0',
      change: '+8.2%',
      icon: Users,
      positive: true,
    },
    {
      title: 'Volume Transacted',
      value: `$${(metrics?.volumeTransacted || 0).toLocaleString()}`,
      change: '+23.1%',
      icon: TrendingUp,
      positive: true,
    },
    {
      title: 'Network Status',
      value: metrics?.networkStatus || 'Healthy',
      change: '99.9% uptime',
      icon: Activity,
      positive: true,
    },
  ];

  return (
    <div className="min-h-screen bg-black text-white p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Analytics Dashboard</h1>
          <p className="text-gray-400">Real-time settlement and agent performance metrics</p>
        </div>

        {/* Controls */}
        <div className="flex gap-4">
            <Select value={timeRange} onValueChange={(v) => setTimeRange(v as TimeRange)} disabled>
            <SelectTrigger className="w-32 bg-gray-900 border-gray-700 text-white">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-gray-900 border-gray-700 text-white">
              <SelectItem value="1h">1 Hour</SelectItem>
              <SelectItem value="24h">24 Hours</SelectItem>
              <SelectItem value="7d">7 Days</SelectItem>
              <SelectItem value="30d">30 Days</SelectItem>
              <SelectItem value="all">All Time</SelectItem>
            </SelectContent>
          </Select>

          <div className="flex gap-2">
            {(['overview', 'detailed', 'advanced'] as const).map((mode) => (
              <Button
                key={mode}
                variant={viewMode === mode ? 'default' : 'outline'}
                onClick={() => setViewMode(mode)}
                className={viewMode === mode ? 'bg-yellow-500 text-black hover:bg-yellow-600' : 'border-gray-700 text-gray-300'}
              >
                {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </Button>
            ))}
          </div>
        </div>
      </div>

      {/* Overview Mode */}
      {viewMode === 'overview' && (
        <>
          {/* Stat Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {stats.map((stat, i) => {
              const Icon = stat.icon;
              return (
                <Card key={i} className="bg-gray-900 border-gray-800 p-6 hover:border-yellow-500 transition-colors">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <p className="text-gray-400 text-sm mb-1">{stat.title}</p>
                      <p className="text-2xl font-bold text-white">{stat.value}</p>
                    </div>
                    <Icon className="w-8 h-8 text-yellow-500" />
                  </div>
                  <p className={`text-sm ${stat.positive ? 'text-green-400' : 'text-red-400'}`}>
                    {stat.change}
                  </p>
                </Card>
              );
            })}
          </div>

          {/* Settlement Trend */}
          <Card className="bg-gray-900 border-gray-800 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Settlement Volume Trend</h2>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={settlementData}>
                <defs>
                  <linearGradient id="colorAmount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FFD700" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#FFD700" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="time" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }} />
                <Area type="monotone" dataKey="amount" stroke="#FFD700" fillOpacity={1} fill="url(#colorAmount)" />
              </AreaChart>
            </ResponsiveContainer>
          </Card>

          {/* Network Distribution */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="bg-gray-900 border-gray-800 p-6">
              <h2 className="text-xl font-bold text-white mb-4">Network Distribution</h2>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={networkDistribution} cx="50%" cy="50%" labelLine={false} label={({ name, value }) => `${name} ${value}%`} outerRadius={80} fill="#8884d8" dataKey="value">
                    {networkDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>

            <Card className="bg-gray-900 border-gray-800 p-6">
              <h2 className="text-xl font-bold text-white mb-4">Job Status Distribution</h2>
              <div className="space-y-4">
                {jobStatusData.map((job, i) => (
                  <div key={i}>
                    <div className="flex justify-between mb-2">
                      <span className="text-gray-300">{job.status}</span>
                      <span className="text-yellow-500 font-bold">{job.count}</span>
                    </div>
                    <div className="w-full bg-gray-800 rounded-full h-2">
                      <div className="bg-yellow-500 h-2 rounded-full" style={{ width: `${job.percentage}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </>
      )}

      {/* Detailed Mode */}
      {viewMode === 'detailed' && (
        <>
          {/* Agent Performance */}
          <Card className="bg-gray-900 border-gray-800 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Top Agent Performance</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={agentPerformanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="name" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }} />
                <Legend />
                <Bar dataKey="performance" fill="#FFD700" name="Performance %" />
                <Bar dataKey="reputation" fill="#00FFFF" name="Reputation Score" />
              </BarChart>
            </ResponsiveContainer>
          </Card>

          {/* Settlement Count Trend */}
          <Card className="bg-gray-900 border-gray-800 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Settlement Count Over Time</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={settlementData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="time" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }} />
                <Legend />
                <Line type="monotone" dataKey="count" stroke="#00FFFF" strokeWidth={2} name="Settlements" />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          {/* Agent Comparison Table */}
          <Card className="bg-gray-900 border-gray-800 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Agent Performance Comparison</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b border-gray-700">
                  <tr>
                    <th className="text-left py-3 px-4 text-gray-400">Agent ID</th>
                    <th className="text-left py-3 px-4 text-gray-400">Performance</th>
                    <th className="text-left py-3 px-4 text-gray-400">Reputation</th>
                    <th className="text-left py-3 px-4 text-gray-400">Settlements</th>
                    <th className="text-left py-3 px-4 text-gray-400">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {agentPerformanceData.map((agent, i) => (
                    <tr key={i} className="border-b border-gray-800 hover:bg-gray-800 transition-colors">
                      <td className="py-3 px-4 text-white font-mono">{agent.name}</td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <div className="w-16 bg-gray-700 rounded h-2">
                            <div className="bg-yellow-500 h-2 rounded" style={{ width: `${agent.performance}%` }} />
                          </div>
                          <span className="text-yellow-500">{agent.performance}%</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-cyan-400">{agent.reputation.toFixed(1)}/5.0</td>
                      <td className="py-3 px-4 text-white">{agent.settlements}</td>
                      <td className="py-3 px-4">
                        <span className="px-3 py-1 bg-green-900 text-green-300 rounded-full text-xs">Active</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </>
      )}

      {/* Advanced Mode */}
      {viewMode === 'advanced' && (
        <>
          <Card className="bg-gray-900 border-gray-800 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Advanced Metrics</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="space-y-2">
                <p className="text-gray-400 text-sm">Average Settlement Time</p>
                <p className="text-2xl font-bold text-cyan-400">1.2s</p>
                <p className="text-xs text-green-400">↓ 23% from yesterday</p>
              </div>
              <div className="space-y-2">
                <p className="text-gray-400 text-sm">Success Rate</p>
                <p className="text-2xl font-bold text-yellow-500">99.87%</p>
                <p className="text-xs text-green-400">↑ 0.12% from yesterday</p>
              </div>
              <div className="space-y-2">
                <p className="text-gray-400 text-sm">Average Gas Cost</p>
                <p className="text-2xl font-bold text-white">$0.012</p>
                <p className="text-xs text-green-400">↓ 8% from yesterday</p>
              </div>
            </div>
          </Card>

          <Card className="bg-gray-900 border-gray-800 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Settlement Breakdown by Network</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={networkDistribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="name" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }} />
                <Bar dataKey="value" fill="#FFD700" name="Settlement Volume %" />
              </BarChart>
            </ResponsiveContainer>
          </Card>

          <Card className="bg-gray-900 border-gray-800 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Real-time Network Status</h2>
            <div className="space-y-3">
              {networkDistribution.map((network, i) => (
                <div key={i} className="flex items-center justify-between p-3 bg-gray-800 rounded">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-white font-mono">{network.name}</span>
                  </div>
                  <div className="flex gap-4">
                    <span className="text-gray-400">Latency: <span className="text-cyan-400">12ms</span></span>
                    <span className="text-gray-400">TPS: <span className="text-yellow-500">1,234</span></span>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
