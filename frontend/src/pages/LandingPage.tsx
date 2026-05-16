import { motion } from "framer-motion";
import { GlassCard } from "../components/GlassCard";
import { GlowButton } from "../components/GlowButton";
import { GradientText } from "../components/GradientText";
import {
  Zap,
  Shield,
  TrendingUp,
  Users,
  ArrowRight,
  CheckCircle,
} from "lucide-react";

const features = [
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Settle transactions in milliseconds with our optimized layer",
  },
  {
    icon: Shield,
    title: "Secure",
    description: "Enterprise-grade security with multi-signature verification",
  },
  {
    icon: TrendingUp,
    title: "Scalable",
    description: "Handle millions of settlements per second",
  },
  {
    icon: Users,
    title: "Agent Native",
    description: "Built for autonomous agents and decentralized systems",
  },
];

const benefits = [
  "Real-time settlement processing",
  "Multi-chain support (Arc, Ethereum, Polygon, etc)",
  "Reputation-based agent scoring",
  "Automated dispute resolution",
  "Cross-chain USDC transfers via Circle",
  "Webhook notifications for integrations",
];

export function LandingPage() {
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
      {/* Navigation */}
      <motion.nav
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="fixed top-0 w-full z-50 border-b border-border/50 backdrop-blur-md"
      >
        <div className="container py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold gradient-text">ORVION</span>
          </div>
          <GlowButton variant="primary">
            Get Started
            <ArrowRight className="w-4 h-4 ml-2" />
          </GlowButton>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="relative min-h-screen flex items-center justify-center pt-20"
      >
        {/* Background gradient orbs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-float" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-float" style={{ animationDelay: "1s" }} />
        </div>

        <div className="container relative z-10">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="max-w-4xl mx-auto text-center"
          >
            {/* Badge */}
            <motion.div variants={itemVariants} className="mb-6">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
                <div className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
                <span className="text-sm font-medium text-primary">
                  Now Live on Arc Testnet
                </span>
              </div>
            </motion.div>

            {/* Main Heading */}
            <motion.h1 variants={itemVariants} className="h1 mb-6">
              The Agentic <GradientText>Settlement Layer</GradientText>
            </motion.h1>

            {/* Subheading */}
            <motion.p
              variants={itemVariants}
              className="subtitle mb-8 max-w-2xl mx-auto"
            >
              Lightning-fast, secure settlement infrastructure for autonomous
              agents. Built for the future of decentralized systems.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              variants={itemVariants}
              className="flex flex-col sm:flex-row gap-4 justify-center mb-12"
            >
              <GlowButton variant="primary" size="lg">
                Launch Dashboard
                <ArrowRight className="w-5 h-5 ml-2" />
              </GlowButton>
              <GlowButton variant="outline" size="lg">
                Read Documentation
              </GlowButton>
            </motion.div>

            {/* Stats */}
            <motion.div
              variants={itemVariants}
              className="grid grid-cols-3 gap-6 pt-8 border-t border-border/50"
            >
              <div>
                <p className="text-2xl font-bold gradient-text">45K+</p>
                <p className="text-sm text-muted-foreground">Settlements</p>
              </div>
              <div>
                <p className="text-2xl font-bold gradient-text">1.2K</p>
                <p className="text-sm text-muted-foreground">Active Agents</p>
              </div>
              <div>
                <p className="text-2xl font-bold gradient-text">$2.3M</p>
                <p className="text-sm text-muted-foreground">TVL</p>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="py-20 border-t border-border"
      >
        <div className="container">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            <motion.div variants={itemVariants} className="text-center mb-12">
              <h2 className="h2 mb-4">Powerful Features</h2>
              <p className="subtitle max-w-2xl mx-auto">
                Everything you need to build and scale settlement infrastructure
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {features.map((feature, idx) => {
                const Icon = feature.icon;
                return (
                  <motion.div
                    key={idx}
                    variants={itemVariants}
                    className="group"
                  >
                    <GlassCard
                      hoverLift
                      className="h-full flex flex-col"
                    >
                      <div className="p-3 rounded-lg bg-primary/10 w-fit mb-4 group-hover:bg-primary/20 smooth-transition">
                        <Icon className="w-6 h-6 text-primary" />
                      </div>
                      <h3 className="font-bold mb-2">{feature.title}</h3>
                      <p className="text-sm text-muted-foreground">
                        {feature.description}
                      </p>
                    </GlassCard>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        </div>
      </motion.section>

      {/* Benefits Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="py-20 border-t border-border"
      >
        <div className="container">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="max-w-3xl mx-auto"
          >
            <motion.h2 variants={itemVariants} className="h2 mb-12 text-center">
              Why Choose ORVION?
            </motion.h2>

            <GlassCard highlighted glowColor="secondary">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {benefits.map((benefit, idx) => (
                  <motion.div
                    key={idx}
                    variants={itemVariants}
                    className="flex items-start gap-3"
                  >
                    <CheckCircle className="w-5 h-5 text-secondary flex-shrink-0 mt-0.5" />
                    <span className="text-foreground">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </motion.section>

      {/* CTA Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="py-20 border-t border-border"
      >
        <div className="container">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="max-w-2xl mx-auto text-center"
          >
            <motion.h2 variants={itemVariants} className="h2 mb-6">
              Ready to Build?
            </motion.h2>
            <motion.p
              variants={itemVariants}
              className="subtitle mb-8"
            >
              Join the future of autonomous settlement infrastructure
            </motion.p>
            <motion.div
              variants={itemVariants}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <GlowButton variant="primary" size="lg">
                Get Started Now
              </GlowButton>
              <GlowButton variant="outline" size="lg">
                Schedule Demo
              </GlowButton>
            </motion.div>
          </motion.div>
        </div>
      </motion.section>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="border-t border-border py-12 bg-card/50"
      >
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="font-bold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground smooth-transition">Features</a></li>
                <li><a href="#" className="hover:text-foreground smooth-transition">Pricing</a></li>
                <li><a href="#" className="hover:text-foreground smooth-transition">Security</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Developers</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground smooth-transition">Docs</a></li>
                <li><a href="#" className="hover:text-foreground smooth-transition">API</a></li>
                <li><a href="#" className="hover:text-foreground smooth-transition">SDK</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground smooth-transition">About</a></li>
                <li><a href="#" className="hover:text-foreground smooth-transition">Blog</a></li>
                <li><a href="#" className="hover:text-foreground smooth-transition">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground smooth-transition">Privacy</a></li>
                <li><a href="#" className="hover:text-foreground smooth-transition">Terms</a></li>
                <li><a href="#" className="hover:text-foreground smooth-transition">License</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-border pt-8 flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              © 2026 ORVION. All rights reserved.
            </p>
            <div className="flex items-center gap-4">
              <a href="#" className="text-muted-foreground hover:text-foreground smooth-transition">Twitter</a>
              <a href="#" className="text-muted-foreground hover:text-foreground smooth-transition">Discord</a>
              <a href="#" className="text-muted-foreground hover:text-foreground smooth-transition">GitHub</a>
            </div>
          </div>
        </div>
      </motion.footer>
    </div>
  );
}

export default LandingPage;
