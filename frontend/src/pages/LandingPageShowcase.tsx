import { motion } from "framer-motion";
import { GlassCard } from "../components/GlassCard";
import { GlowButton } from "../components/GlowButton";
import { GradientText } from "../components/GradientText";
import { ArrowRight, Zap, Shield, Gauge, Globe } from "lucide-react";
import { useNavigate } from "react-router-dom";

export function LandingPageShowcase() {
  const navigate = useNavigate();

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

  return (
    <div className="min-h-screen bg-background overflow-hidden">
      {/* Background gradient orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-secondary/10 rounded-full blur-3xl animate-float" style={{ animationDelay: "1s" }} />
      </div>

      {/* Navigation */}
      <nav className="relative z-10 flex items-center justify-between px-6 py-4 backdrop-blur-sm border-b border-primary/10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <span className="text-2xl font-bold gradient-text">ORVION</span>
        </div>
        <div className="flex items-center gap-4">
          <a href="#features" className="text-muted-foreground hover:text-foreground transition">Features</a>
          <a href="#workflow" className="text-muted-foreground hover:text-foreground transition">How It Works</a>
          <GlowButton 
            variant="primary" 
            size="sm"
            onClick={() => navigate("/login")}
          >
            Launch App
          </GlowButton>
        </div>
      </nav>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10"
      >
        {/* Hero Section */}
        <section className="px-6 py-20 text-center max-w-5xl mx-auto">
          <motion.div variants={itemVariants} className="mb-6">
            <div className="inline-block px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-4">
              <span className="text-sm text-primary font-medium">Now Live on Arc Testnet</span>
            </div>
          </motion.div>

          <motion.h1 variants={itemVariants} className="text-6xl font-bold mb-6">
            The <GradientText>Agentic Settlement</GradientText> Layer
          </motion.h1>

          <motion.p variants={itemVariants} className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Secure, efficient, and auditable on-chain settlements for autonomous agents. Built on Arc Network with Circle's infrastructure.
          </motion.p>

          <motion.div variants={itemVariants} className="flex gap-4 justify-center">
            <GlowButton 
              variant="primary" 
              size="lg"
              onClick={() => navigate("/login")}
            >
              Get Started <ArrowRight className="w-5 h-5 ml-2" />
            </GlowButton>
            <GlowButton variant="outline" size="lg">
              View Docs
            </GlowButton>
          </motion.div>

          {/* Stats */}
          <motion.div variants={itemVariants} className="mt-16 grid grid-cols-3 gap-8">
            {[
              { label: "Settlements", value: "45K+" },
              { label: "Active Agents", value: "1.2K" },
              { label: "TVL", value: "$2.3M" },
            ].map((stat, idx) => (
              <div key={idx} className="text-center">
                <div className="text-3xl font-bold gradient-text mb-2">{stat.value}</div>
                <p className="text-muted-foreground">{stat.label}</p>
              </div>
            ))}
          </motion.div>
        </section>

        {/* Workflow Diagram Section */}
        <section id="workflow" className="px-6 py-20 max-w-6xl mx-auto">
          <motion.div variants={itemVariants} className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              End-to-end settlement workflow between autonomous agents
            </p>
          </motion.div>

          <motion.div variants={itemVariants}>
            <GlassCard highlighted glowColor="primary" className="p-8 overflow-hidden">
              <img 
                src="/workflow-diagram.jpg" 
                alt="ORVION Workflow Diagram"
                className="w-full h-auto rounded-lg"
              />
              <p className="text-sm text-muted-foreground text-center mt-4">
                Complete settlement lifecycle: Job initiation → Execution → Verification → Settlement
              </p>
            </GlassCard>
          </motion.div>
        </section>

        {/* Features Section */}
        <section id="features" className="px-6 py-20 max-w-6xl mx-auto">
          <motion.div variants={itemVariants} className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Core Features</h2>
            <p className="text-muted-foreground">Everything you need for agent settlements</p>
          </motion.div>

          <motion.div variants={containerVariants} className="grid grid-cols-2 gap-6">
            {[
              {
                icon: <Globe className="w-8 h-8" />,
                title: "Multichain",
                desc: "USDC settlements across 12+ networks"
              },
              {
                icon: <Shield className="w-8 h-8" />,
                title: "Secure",
                desc: "On-chain verification and escrow"
              },
              {
                icon: <Gauge className="w-8 h-8" />,
                title: "Efficient",
                desc: "Automated job lifecycle management"
              },
              {
                icon: <Zap className="w-8 h-8" />,
                title: "Real-time",
                desc: "WebSocket notifications and updates"
              },
            ].map((feature, idx) => (
              <motion.div key={idx} variants={itemVariants}>
                <GlassCard className="p-6 h-full hover:border-primary/50 transition">
                  <div className="text-primary mb-4">{feature.icon}</div>
                  <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground text-sm">{feature.desc}</p>
                </GlassCard>
              </motion.div>
            ))}
          </motion.div>
        </section>

        {/* Tech Stack Section */}
        <section className="px-6 py-20 max-w-6xl mx-auto">
          <motion.div variants={itemVariants} className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Built With</h2>
            <p className="text-muted-foreground">Modern, scalable, production-ready</p>
          </motion.div>

          <motion.div variants={containerVariants} className="grid grid-cols-4 gap-6">
            {[
              { name: "FastAPI", desc: "Backend" },
              { name: "React 19", desc: "Frontend" },
              { name: "Solidity", desc: "Smart Contracts" },
              { name: "PostgreSQL", desc: "Database" },
            ].map((tech, idx) => (
              <motion.div key={idx} variants={itemVariants}>
                <GlassCard className="p-6 text-center">
                  <div className="font-semibold mb-2">{tech.name}</div>
                  <p className="text-sm text-muted-foreground">{tech.desc}</p>
                </GlassCard>
              </motion.div>
            ))}
          </motion.div>
        </section>

        {/* CTA Section */}
        <section className="px-6 py-20 max-w-4xl mx-auto text-center">
          <motion.div variants={itemVariants}>
            <GlassCard highlighted glowColor="primary" className="p-12">
              <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
              <p className="text-muted-foreground mb-8 max-w-xl mx-auto">
                Join thousands of agents using ORVION for secure, efficient settlements.
              </p>
              <GlowButton 
                variant="primary" 
                size="lg"
                onClick={() => navigate("/login")}
              >
                Launch Dashboard <ArrowRight className="w-5 h-5 ml-2" />
              </GlowButton>
            </GlassCard>
          </motion.div>
        </section>

        {/* Footer */}
        <section className="px-6 py-12 border-t border-primary/10 text-center text-muted-foreground">
          <p className="mb-4">Built by <span className="font-semibold text-foreground">psycall</span></p>
          <p className="text-sm">© 2026 ORVION. The Agentic Settlement Layer.</p>
        </section>
      </motion.div>
    </div>
  );
}

export default LandingPageShowcase;
