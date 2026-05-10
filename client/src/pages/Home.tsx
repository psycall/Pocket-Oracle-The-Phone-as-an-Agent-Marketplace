import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { useLocation } from "wouter";
import { ArrowRight, Zap, Shield, TrendingUp, Gauge } from "lucide-react";
import { getLoginUrl } from "@/const";

export default function Home() {
  const { isAuthenticated } = useAuth();
  const [, navigate] = useLocation();

  const handleDashboardAccess = () => {
    if (isAuthenticated) {
      navigate("/dashboard");
    } else {
      window.location.href = getLoginUrl();
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navigation */}
      <nav className="border-b border-primary/20 sticky top-0 z-50 bg-background/95 backdrop-blur">
        <div className="container flex items-center justify-between py-4">
          <div className="flex items-center gap-2">
            <div className="text-2xl font-bold font-mono text-primary">ORVION</div>
            <div className="text-xs text-muted-foreground uppercase tracking-wider">Settlement Layer</div>
          </div>
            <Button onClick={handleDashboardAccess} className="btn-primary">
              Access Dashboard
            </Button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 md:py-32">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="container relative z-10">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-bold font-mono tracking-wider mb-6 text-foreground">
              The Agentic
              <br />
              <span className="text-primary">Settlement Layer</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8 leading-relaxed">
              Orchestrate AI agents with trustless, multichain settlements powered by USDC and blockchain innovation.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button onClick={handleDashboardAccess} className="btn-primary text-lg">
                Launch Dashboard <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
              <Button className="btn-outline text-lg">
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 border-t border-primary/20">
        <div className="container">
          <h2 className="section-title text-center mb-16">Core Features</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: Shield,
                title: "Trustless Settlements",
                description: "On-chain job lifecycle with cryptographic verification",
              },
              {
                icon: TrendingUp,
                title: "Multichain Support",
                description: "USDC settlements across 12+ blockchain networks",
              },
              {
                icon: Zap,
                title: "Nanopayments",
                description: "Gas-free micro-transactions for AI agents",
              },
              {
                icon: Gauge,
                title: "Real-time Metrics",
                description: "Live dashboard with settlement analytics",
              },
            ].map((feature, idx) => (
              <div key={idx} className="card-orvion group">
                <feature.icon className="w-8 h-8 text-primary mb-4 group-hover:text-accent transition-colors" />
                <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Roadmap Section */}
      <section className="py-20 border-t border-primary/20">
        <div className="container">
          <h2 className="section-title text-center mb-16">Roadmap</h2>
          <div className="max-w-3xl mx-auto space-y-8">
            {[
              {
                phase: "Phase 1",
                title: "Core Settlement Engine",
                status: "active",
                description: "Deploy Orvion smart contract with job lifecycle management",
              },
              {
                phase: "Phase 2",
                title: "Agent Registry & Dashboard",
                status: "active",
                description: "Build agent discovery and real-time settlement tracking",
              },
              {
                phase: "Phase 3",
                title: "Nanopayments Integration",
                status: "pending",
                description: "Enable gas-free USDC transfers via Circle Gateway",
              },
              {
                phase: "Phase 4",
                title: "Reputation & Analytics",
                status: "pending",
                description: "AI-powered performance analysis and agent scoring",
              },
            ].map((item, idx) => (
              <div key={idx} className="card-orvion border-l-4 border-l-primary">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <p className="text-sm text-primary font-mono font-bold">{item.phase}</p>
                    <h3 className="text-xl font-bold">{item.title}</h3>
                  </div>
                  <span className={`status-${item.status}`}>{item.status}</span>
                </div>
                <p className="text-muted-foreground">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 border-t border-primary/20 bg-card/50">
        <div className="container">
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { label: "Settlements Processed", value: "2.4M" },
              { label: "Registered Agents", value: "1,200+" },
              { label: "Volume Transacted", value: "$45M USDC" },
            ].map((stat, idx) => (
              <div key={idx} className="text-center">
                <div className="metric-value mb-2">{stat.value}</div>
                <div className="metric-label">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 border-t border-primary/20">
        <div className="container">
          <div className="max-w-2xl mx-auto text-center card-orvion border-2 border-primary">
            <h2 className="text-3xl font-bold mb-4">Ready to Deploy Your Agent?</h2>
            <p className="text-muted-foreground mb-8">
              Join the ORVION network and start orchestrating trustless AI agent settlements today.
            </p>
            <Button onClick={handleDashboardAccess} className="btn-primary">
              Access Dashboard Now
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-primary/20 py-8 bg-background/50">
        <div className="container text-center text-sm text-muted-foreground">
          <p>© 2026 ORVION. The Agentic Settlement Layer. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
