import { useAuth } from "@/_core/hooks/useAuth";
import { useLocation } from "wouter";
import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { trpc } from "@/lib/trpc";

export default function Settlements() {
  const { user, loading } = useAuth();
  const [, navigate] = useLocation();
  const [filterNetwork, setFilterNetwork] = useState<string>("");
  const [filterStatus, setFilterStatus] = useState<string>("");

  useEffect(() => {
    if (!loading && !user) {
      navigate("/");
    }
  }, [user, loading, navigate]);

  const { data: settlements } = trpc.settlements.list.useQuery();

  const filteredSettlements = (settlements || []).filter((s) => {
    if (filterNetwork && s.blockchainNetwork !== filterNetwork) return false;
    if (filterStatus && s.status !== filterStatus) return false;
    return true;
  });

  const networks = Array.from(new Set((settlements || []).map((s) => s.blockchainNetwork)));
  const statuses = Array.from(new Set((settlements || []).map((s) => s.status)));

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

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="section-title">Settlements History</h1>
          <p className="text-muted-foreground mt-2">Track all on-chain USDC settlements and transactions</p>
        </div>

        {/* Filters */}
        <div className="card-orvion">
          <h3 className="font-bold text-lg mb-4">Filters</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-mono text-primary mb-2">Blockchain Network</label>
              <select
                className="input-orvion w-full"
                value={filterNetwork}
                onChange={(e) => setFilterNetwork(e.target.value)}
              >
                <option value="">All Networks</option>
                {networks.map((network) => (
                  <option key={network} value={network}>
                    {network}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-mono text-primary mb-2">Status</label>
              <select
                className="input-orvion w-full"
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
              >
                <option value="">All Statuses</option>
                {statuses.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Settlements Table */}
        <div className="card-orvion">
          <h3 className="font-bold text-lg mb-6">All Settlements ({filteredSettlements.length})</h3>
          <div className="overflow-x-auto">
            <table className="table-orvion">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Job</th>
                  <th>Agent</th>
                  <th>Amount</th>
                  <th>Network</th>
                  <th>Status</th>
                  <th>TX Hash</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {filteredSettlements.map((settlement) => (
                  <tr key={settlement.id}>
                    <td className="font-mono">#{settlement.id}</td>
                    <td className="font-mono">#{settlement.jobId}</td>
                    <td className="font-mono">#{settlement.agentId}</td>
                    <td className="font-bold text-primary">{settlement.amount} {settlement.currency}</td>
                    <td className="text-sm">{settlement.blockchainNetwork}</td>
                    <td>
                      <span className={`status-${settlement.status}`}>{settlement.status}</span>
                    </td>
                    <td className="font-mono text-xs text-muted-foreground">
                      {settlement.transactionHash ? settlement.transactionHash.slice(0, 10) + "..." : "-"}
                    </td>
                    <td className="text-sm text-muted-foreground">
                      {new Date(settlement.createdAt).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {filteredSettlements.length === 0 && (
              <div className="text-center py-8 text-muted-foreground">
                No settlements found matching the filters.
              </div>
            )}
          </div>
        </div>

        {/* Statistics */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="metric-card">
            <div className="metric-value mb-1">
              {filteredSettlements.filter((s) => s.status === "settled").length}
            </div>
            <div className="metric-label">Settled</div>
          </div>
          <div className="metric-card">
            <div className="metric-value mb-1">
              {filteredSettlements.filter((s) => s.status === "pending").length}
            </div>
            <div className="metric-label">Pending</div>
          </div>
          <div className="metric-card">
            <div className="metric-value mb-1">
              {filteredSettlements.filter((s) => s.status === "failed").length}
            </div>
            <div className="metric-label">Failed</div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
