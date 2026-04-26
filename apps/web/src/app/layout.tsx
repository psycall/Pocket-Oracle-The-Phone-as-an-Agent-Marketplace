import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Orvion — Execution Layer",
  description: "The infrastructure for autonomous agent execution. Goal → Engine → Result.",
  openGraph: {
    title: "Orvion — Execution Layer for Autonomous Agents",
    description: "Give a goal. Orvion executes. Real AI, real results.",
    type: "website",
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
