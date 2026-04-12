import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'Pocket Oracle Mobile PWA',
  description: 'Mobile-first operator surface for Pocket Oracle.'
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
