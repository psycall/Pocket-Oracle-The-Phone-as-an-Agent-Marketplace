import { ReactNode } from "react";

interface GradientTextProps {
  children: ReactNode;
  className?: string;
  variant?: "brand" | "primary" | "secondary" | "danger";
  animate?: boolean;
}

/**
 * Texto com gradiente (indigo → green → indigo)
 * Pode ser estático ou animado
 */
export function GradientText({
  children,
  className = "",
  variant = "brand",
  animate = false,
}: GradientTextProps) {
  const gradientClasses = {
    brand: "bg-gradient-to-r from-primary via-secondary to-primary",
    primary: "bg-gradient-to-r from-primary to-primary/60",
    secondary: "bg-gradient-to-r from-secondary to-secondary/60",
    danger: "bg-gradient-to-r from-danger to-danger/60",
  };

  return (
    <span
      className={`
        bg-clip-text text-transparent
        ${gradientClasses[variant]}
        ${animate ? "animate-pulse" : ""}
        ${className}
      `}
    >
      {children}
    </span>
  );
}
