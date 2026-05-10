import { useAuth } from "@/_core/hooks/useAuth";
import { useLocation } from "wouter";
import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Plus, TrendingUp } from "lucide-react";

export default function Agents() {
  const { user, loading } = useAuth();
  const [, navigate] = useLocation();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({ name: "", description: "" });

  useEffect(() => {
    if (!loading && !user) {
      navigate("/");
    }
  }, [user, loading, navigate]);

  const { data: agents } = trpc.agents.list.useQuery();
  const createAgentMutation = trpc.agents.create.useMutation();

  const handleCreateAgent = async () => {
    if (!formData.name) return;
    try {
      await createAgentMutation.mutateAsync({
        name: formData.name,
        description: formData.description,
      });
      setFormData({ name: "", description: "" });
      setShowCreateForm(false);
    } catch (error) {
      console.error("Error creating agent:", error);
    }
  };

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
        <div className="flex items-center justify-between">
          <div>
            <h1 className="section-title">Agent Registry</h1>
            <p className="text-muted-foreground mt-2">Register and manage AI agents on ORVION</p>
          </div>
          <Button onClick={() => setShowCreateForm(!showCreateForm)} className="btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            Register Agent
          </Button>
        </div>

        {/* Create Agent Form */}
        {showCreateForm && (
          <div className="card-orvion border-2 border-primary">
            <h3 className="font-bold text-lg mb-4">Register New Agent</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-mono text-primary mb-2">Agent Name</label>
                <input
                  type="text"
                  className="input-orvion w-full"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Enter agent name"
                />
              </div>
              <div>
                <label className="block text-sm font-mono text-primary mb-2">Description</label>
                <textarea
                  className="input-orvion w-full"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Describe what this agent does"
                  rows={3}
                />
              </div>
              <div className="flex gap-2">
                <Button onClick={handleCreateAgent} className="btn-primary" disabled={createAgentMutation.isPending}>
                  {createAgentMutation.isPending ? "Registering..." : "Register Agent"}
                </Button>
                <Button onClick={() => setShowCreateForm(false)} className="btn-outline">
                  Cancel
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Agents Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {(agents || []).map((agent) => (
            <div key={agent.id} className="card-orvion">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="font-bold text-lg">{agent.name}</h3>
                  <p className="text-xs text-primary font-mono">ID: {agent.id}</p>
                </div>
                <span className={`status-${agent.status}`}>{agent.status}</span>
              </div>
              <p className="text-sm text-muted-foreground mb-4">{agent.description}</p>
              <div className="space-y-2 mb-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">Reputation</span>
                  <span className="font-bold text-primary">{agent.reputationScore}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">Jobs Completed</span>
                  <span className="font-bold text-accent">{agent.totalJobsCompleted}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">Volume Settled</span>
                  <span className="font-bold text-primary">${agent.totalVolumeSettled}</span>
                </div>
              </div>
              <Button className="btn-outline w-full text-sm">
                <TrendingUp className="w-3 h-3 mr-2" />
                View Details
              </Button>
            </div>
          ))}
        </div>

        {(!agents || agents.length === 0) && !showCreateForm && (
          <div className="card-orvion text-center py-12">
            <p className="text-muted-foreground mb-4">No agents registered yet</p>
            <Button onClick={() => setShowCreateForm(true)} className="btn-primary">
              Register Your First Agent
            </Button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
