import { getDefaultConfig } from '@rainbow-me/rainbowkit';
import { http } from 'wagmi';
import { arbitrum, arbitrumSepolia } from 'wagmi/chains';

const arcTestnet = {
  id: 5042002,
  name: 'Arc Testnet',
  nativeCurrency: { name: 'USDC', symbol: 'USDC', decimals: 6 },
  rpcUrls: { default: { http: ['https://rpc.testnet.arc.network'] } },
  blockExplorers: { default: { name: 'ArcScan', url: 'https://testnet.arcscan.app' } },
  testnet: true,
};

export const wagmiConfig = getDefaultConfig({
  appName: 'ORVION Agentic',
  projectId: 'YOUR_PROJECT_ID', // Substitua pelo seu Project ID do WalletConnect se tiver
  chains: [arcTestnet, arbitrum, arbitrumSepolia],
  ssr: true,
  transports: {
    [arcTestnet.id]: http('https://rpc.testnet.arc.network'),
  },
});
