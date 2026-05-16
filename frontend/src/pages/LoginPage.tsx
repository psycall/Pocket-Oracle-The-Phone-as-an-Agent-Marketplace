import { motion } from "framer-motion";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GlassCard } from "../components/GlassCard";
import { GlowButton } from "../components/GlowButton";
import { GradientText } from "../components/GradientText";
import { useAuth } from "../hooks/useAuth";
import { Zap, AlertCircle } from "lucide-react";

declare global {
  interface Window {
    ethereum?: any;
  }
}

export function LoginPage() {
  const navigate = useNavigate();
  const { login, isLoading, error } = useAuth();
  const [localError, setLocalError] = useState<string | null>(null);

  const handleWalletLogin = async () => {
    setLocalError(null);

    try {
      // Check if wallet is available
      if (!window.ethereum) {
        throw new Error(
          "No wallet detected. Please install MetaMask or use Arc wallet."
        );
      }

      // Request account access
      const accounts = await window.ethereum.request({
        method: "eth_requestAccounts",
      });

      if (!accounts || accounts.length === 0) {
        throw new Error("No wallet accounts found");
      }

      const walletAddress = accounts[0];

      // Create message to sign
      const message = `Sign this message to login to ORVION\n\nWallet: ${walletAddress}\nTimestamp: ${Date.now()}`;

      // Request signature
      const signature = await window.ethereum.request({
        method: "personal_sign",
        params: [message, walletAddress],
      });

      // Login with signature
      await login(walletAddress, signature, message);

      // Navigate to dashboard
      navigate("/dashboard");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Login failed";
      setLocalError(errorMessage);
    }
  };

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
    <div className="min-h-screen bg-background flex items-center justify-center relative overflow-hidden">
      {/* Background gradient orbs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-float" style={{ animationDelay: "1s" }} />
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10 w-full max-w-md px-4"
      >
        {/* Logo */}
        <motion.div variants={itemVariants} className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
              <Zap className="w-7 h-7 text-white" />
            </div>
            <span className="text-3xl font-bold gradient-text">ORVION</span>
          </div>
          <p className="text-muted-foreground">
            The Agentic Settlement Layer
          </p>
        </motion.div>

        {/* Login Card */}
        <motion.div variants={itemVariants}>
          <GlassCard highlighted glowColor="primary" className="p-8">
            <h2 className="h3 mb-2">Welcome Back</h2>
            <p className="text-muted-foreground mb-8">
              Connect your Arc wallet to access the dashboard
            </p>

            {/* Error Message */}
            {(error || localError) && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-6 p-4 rounded-lg bg-danger/10 border border-danger/20 flex items-start gap-3"
              >
                <AlertCircle className="w-5 h-5 text-danger flex-shrink-0 mt-0.5" />
                <p className="text-sm text-danger">{error || localError}</p>
              </motion.div>
            )}

            {/* Login Button */}
            <GlowButton
              variant="primary"
              size="lg"
              className="w-full mb-4"
              onClick={handleWalletLogin}
              isLoading={isLoading}
              disabled={isLoading}
            >
              {isLoading ? "Connecting..." : "Connect Arc Wallet"}
            </GlowButton>

            {/* Alternative */}
            <p className="text-center text-sm text-muted-foreground mb-6">
              or
            </p>

            <GlowButton
              variant="outline"
              size="lg"
              className="w-full"
              disabled={isLoading}
            >
              Use MetaMask
            </GlowButton>

            {/* Info */}
            <div className="mt-8 p-4 rounded-lg bg-primary/10 border border-primary/20">
              <p className="text-sm text-foreground mb-2 font-medium">
                First time here?
              </p>
              <p className="text-xs text-muted-foreground">
                Your wallet will be automatically registered as an agent. You can manage your profile after login.
              </p>
            </div>
          </GlassCard>
        </motion.div>

        {/* Features */}
        <motion.div
          variants={itemVariants}
          className="mt-8 grid grid-cols-3 gap-4"
        >
          {[
            { icon: "🔒", label: "Secure" },
            { icon: "⚡", label: "Fast" },
            { icon: "🌐", label: "Decentralized" },
          ].map((feature, idx) => (
            <div key={idx} className="text-center">
              <div className="text-3xl mb-2">{feature.icon}</div>
              <p className="text-xs text-muted-foreground">{feature.label}</p>
            </div>
          ))}
        </motion.div>

        {/* Footer */}
        <motion.p
          variants={itemVariants}
          className="text-center text-xs text-muted-foreground mt-8"
        >
          By connecting your wallet, you agree to our{" "}
          <a href="#" className="text-primary hover:underline">
            Terms of Service
          </a>
        </motion.p>
      </motion.div>
    </div>
  );
}

export default LoginPage;
