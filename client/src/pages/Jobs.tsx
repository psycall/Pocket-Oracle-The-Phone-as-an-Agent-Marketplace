import { useAuth } from "@/_core/hooks/useAuth";
import { useLocation } from "wouter";
import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export default function Jobs() {
  const { user, loading } = useAuth();
  const [, navigate] = useLocation();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({ title: "", description: "", agentId: 1 });

  useEffect(() => {
    if (!loading && !user) {
      navigate("/");
    }
  }, [user, loading, navigate]);

  const { data: jobs } = trpc.jobs.list.useQuery();
  const { data: agents } = trpc.agents.list.useQuery();
  const createJobMutation = trpc.jobs.create.useMutation();

  const handleCreateJob = async () => {
    if (!formData.title) return;
    try {
      await createJobMutation.mutateAsync({
        agentId: formData.agentId,
        title: formData.title,
        description: formData.description,
      });
      setFormData({ title: "", description: "", agentId: 1 });
      setShowCreateForm(false);
    } catch (error) {
      console.error("Error creating job:", error);
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
            <h1 className="section-title">Jobs Management</h1>
            <p className="text-muted-foreground mt-2">Create and monitor AI agent jobs</p>
          </div>
          <Button onClick={() => setShowCreateForm(!showCreateForm)} className="btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            New Job
          </Button>
        </div>

        {/* Create Job Form */}
        {showCreateForm && (
          <div className="card-orvion border-2 border-primary">
            <h3 className="font-bold text-lg mb-4">Create New Job</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-mono text-primary mb-2">Job Title</label>
                <input
                  type="text"
                  className="input-orvion w-full"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Enter job title"
                />
              </div>
              <div>
                <label className="block text-sm font-mono text-primary mb-2">Description</label>
                <textarea
                  className="input-orvion w-full"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Enter job description"
                  rows={3}
                />
              </div>
              <div>
                <label className="block text-sm font-mono text-primary mb-2">Agent</label>
                <select
                  className="input-orvion w-full"
                  value={formData.agentId}
                  onChange={(e) => setFormData({ ...formData, agentId: parseInt(e.target.value) })}
                >
                  {(agents || []).map((agent) => (
                    <option key={agent.id} value={agent.id}>
                      {agent.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex gap-2">
                <Button onClick={handleCreateJob} className="btn-primary" disabled={createJobMutation.isPending}>
                  {createJobMutation.isPending ? "Creating..." : "Create Job"}
                </Button>
                <Button onClick={() => setShowCreateForm(false)} className="btn-outline">
                  Cancel
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Jobs Table */}
        <div className="card-orvion">
          <h3 className="font-bold text-lg mb-6">All Jobs</h3>
          <div className="overflow-x-auto">
            <table className="table-orvion">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Title</th>
                  <th>Agent</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Execution Time</th>
                </tr>
              </thead>
              <tbody>
                {(jobs || []).map((job) => (
                  <tr key={job.id}>
                    <td className="font-mono">#{job.id}</td>
                    <td className="font-semibold">{job.title}</td>
                    <td>Agent {job.agentId}</td>
                    <td>
                      <span className={`status-${job.status}`}>{job.status}</span>
                    </td>
                    <td className="text-sm text-muted-foreground">
                      {new Date(job.createdAt).toLocaleDateString()}
                    </td>
                    <td className="text-sm">{job.executionTime ? `${job.executionTime}ms` : "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {(!jobs || jobs.length === 0) && (
              <div className="text-center py-8 text-muted-foreground">
                No jobs yet. Create one to get started.
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
