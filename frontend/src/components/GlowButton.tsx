import { motion } from "framer-motion";
import { ButtonHTMLAttributes, ReactNode } from "react";

interface GlowButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "danger";
  size?: "sm" | "md" | "lg";
  children: ReactNode;
  isLoading?: boolean;
}

/**
 * Botão da marca ORVION/SmartVault
 * - primary: fundo indigo + sombra glow indigo
 * - secondary: fundo green + sombra glow green
 * - outline: borda translúcida + hover bg-white/5
 * - danger: fundo red + sombra glow red
 */
export function GlowButton({
  variant = "primary",
  size = "md",
  className = "",
  children,
  isLoading = false,
  disabled,
  ...props
}: GlowButtonProps) {
  const variantClasses = {
    primary: "bg-primary text-primary-foreground hover:bg-primary/90 shadow-lg shadow-primary/50",
    secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/90 shadow-lg shadow-secondary/50",
    outline: "border border-white/20 hover:bg-white/5 text-foreground",
    danger: "bg-danger text-destructive-foreground hover:bg-danger/90 shadow-lg shadow-danger/50",
  };

  const sizeClasses = {
    sm: "px-3 py-2 text-sm",
    md: "px-6 py-3 text-base",
    lg: "px-8 py-4 text-lg",
  };

  return (
    <motion.button
      whileHover={!disabled ? { scale: 1.05 } : undefined}
      whileTap={!disabled ? { scale: 0.95 } : undefined}
      className={`
        inline-flex items-center justify-center rounded-md font-medium
        smooth-transition disabled:opacity-50 disabled:cursor-not-allowed
        ${sizeClasses[size]}
        ${variantClasses[variant]}
        ${className}
      `}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
          <span>Loading...</span>
        </div>
      ) : (
        children
      )}
    </motion.button>
  );
}
