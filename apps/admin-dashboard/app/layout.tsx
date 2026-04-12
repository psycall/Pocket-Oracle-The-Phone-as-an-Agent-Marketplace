import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'Pocket Oracle Admin Dashboard',
  description: 'Operational dashboard and demo metrics for Pocket Oracle.'
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
