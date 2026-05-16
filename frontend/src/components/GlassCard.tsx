import { motion } from "framer-motion";
import { ReactNode } from "react";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  hoverLift?: boolean;
  highlighted?: boolean;
  glowColor?: "primary" | "secondary" | "danger";
}

/**
 * Card com efeito glassmorphism + hover lift (assinatura ORVION/SmartVault)
 * Usa Framer Motion para animações suaves
 */
export function GlassCard({
  children,
  className = "",
  hoverLift = true,
  highlighted = false,
  glowColor = "primary",
}: GlassCardProps) {
  const glowClasses = {
    primary: "border-primary/50 shadow-lg shadow-primary/20",
    secondary: "border-secondary/50 shadow-lg shadow-secondary/20",
    danger: "border-danger/50 shadow-lg shadow-danger/20",
  };

  return (
    <motion.div
      whileHover={hoverLift ? { y: -5 } : undefined}
      className={`
        p-6 rounded-lg glass smooth-transition
        ${
          highlighted
            ? `border-2 ${glowClasses[glowColor]}`
            : "border border-white/10 hover:border-primary/50"
        }
        ${className}
      `}
    >
      {children}
    </motion.div>
  );
}
