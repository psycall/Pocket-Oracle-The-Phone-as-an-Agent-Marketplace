import './globals.css';
import type { Metadata } from 'next';
import type { ReactNode } from 'react';

export const metadata: Metadata = {
  title: 'Orvion — Agent Commerce Layer',
  description:
    'Investor-ready landing page for the agent marketplace: execution, payments, proof and operator tooling.',
  openGraph: {
    title: 'Orvion — Agent Commerce Layer',
    description:
      'A polished overview of the marketplace, mobile operator surface, admin control plane and execution API.',
    type: 'website'
  }
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
