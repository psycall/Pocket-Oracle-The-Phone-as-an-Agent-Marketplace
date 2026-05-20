import { getDefaultConfig } from '@rainbow-me/rainbowkit';
import { mainnet, polygon, optimism, arbitrum, base } from 'wagmi/chains';

export const wagmiConfig = getDefaultConfig({
  appName: 'ORVION Agentic',
  projectId: 'YOUR_PROJECT_ID', // Substitua pelo seu Project ID do WalletConnect se tiver
  chains: [mainnet, polygon, optimism, arbitrum, base],
  ssr: false, 
});
