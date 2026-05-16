# ORVION Frontend Integration Guide

## Overview

The ORVION frontend is a React 19 + TypeScript application with professional design system based on SmartVault. It integrates seamlessly with the FastAPI backend for settlements, agents, reputation, and webhooks.

## Architecture

```
Frontend (React 19)
    ↓
API Client (axios)
    ↓
Backend (FastAPI)
    ↓
Database (PostgreSQL)
    ↓
Smart Contract (Solidity)
```

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_CHAIN_ID=5042002
REACT_APP_RPC_URL=https://rpc.testnet.arc.network
```

### 3. Start Development Server

```bash
npm run dev
```

Open http://localhost:5173

## File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── GlassCard.tsx          # Glassmorphism card component
│   │   ├── GlowButton.tsx         # Animated button component
│   │   └── GradientText.tsx       # Gradient text component
│   ├── hooks/
│   │   ├── useAuth.ts            # Authentication hook
│   │   └── useApi.ts             # API calls hook
│   ├── lib/
│   │   └── api.ts                # API client (axios)
│   ├── pages/
│   │   ├── LandingPage.tsx       # Hero + marketing
│   │   ├── LoginPage.tsx         # Wallet login
│   │   └── DashboardPage.tsx     # Settlement management
│   ├── App.tsx                   # Routes + auth protection
│   ├── index.css                 # Global styles (OKLCH)
│   └── main.tsx                  # Entry point
├── .env.example
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Key Features

### 1. Authentication (Arc Wallet)

```typescript
import { useAuth } from "./hooks/useAuth";

function MyComponent() {
  const { user, login, logout, isAuthenticated } = useAuth();

  const handleLogin = async () => {
    await login(walletAddress, signature, message);
  };

  return isAuthenticated ? <Dashboard /> : <LoginPage />;
}
```

### 2. API Calls

```typescript
import { useApi } from "./hooks/useApi";
import { apiClient } from "./lib/api";

function MyComponent() {
  // Query hook
  const { data, isLoading, error, refetch } = useApi(
    () => apiClient.getSettlements(10, 0),
    []
  );

  // Mutation hook
  const { mutate, isLoading: mutating } = useApiMutation(
    (data) => apiClient.createSettlement(data.agentId, data.jobId, data.amount)
  );

  return <div>{/* ... */}</div>;
}
```

### 3. Design System

**Colors (OKLCH)**:
- Primary: `#6366F1` (Indigo)
- Secondary: `#10B981` (Green)
- Danger: `#EF4444` (Red)
- Warning: `#F59E0B` (Amber)

**Components**:
- `<GlassCard>` - Glassmorphism card with hover lift
- `<GlowButton>` - Animated button with glow shadow
- `<GradientText>` - Text with brand gradient

**Utilities**:
- `.glass` - Glassmorphism effect
- `.gradient-text` - Gradient text
- `.smooth-transition` - Smooth animations
- `.glow-primary` - Glow shadow effect

## API Endpoints

### Authentication
- `POST /api/v1/auth/wallet-login` - Login with wallet signature
- `GET /api/v1/auth/me` - Get current user

### Settlements
- `GET /api/v1/settlement/settlements` - List settlements
- `GET /api/v1/settlement/settlements/{id}` - Get settlement
- `POST /api/v1/settlement/settlements` - Create settlement

### Agents
- `GET /api/v1/discovery/agents` - List agents
- `GET /api/v1/discovery/agents/{id}` - Get agent
- `POST /api/v1/discovery/agents` - Register agent

### Reputation
- `GET /api/v1/reputation/agents/{id}/reputation` - Get reputation
- `GET /api/v1/reputation/agents/top-rated` - Top rated agents
- `POST /api/v1/reputation/agents/{id}/feedback` - Submit feedback

### Webhooks
- `POST /api/v1/webhooks/subscribe` - Subscribe to events
- `GET /api/v1/webhooks/subscriptions` - Get subscriptions

### Disputes
- `POST /api/v1/disputes/create` - Create dispute
- `GET /api/v1/disputes/list` - List disputes

## Pages

### Landing Page (`/`)
- Hero section with animated background
- Features grid
- Benefits checklist
- Call-to-action buttons
- Responsive footer

### Login Page (`/login`)
- Wallet connection UI
- Arc wallet integration
- Error handling
- Feature highlights

### Dashboard (`/dashboard`)
- Protected route (requires authentication)
- Real-time stats cards
- Settlement trend chart
- Agent reputation pie chart
- Recent settlements table
- Responsive design

## Styling

### Tailwind CSS v4 with OKLCH

The project uses Tailwind CSS v4 with OKLCH color space for better color representation.

**Custom utilities**:
```css
.glass { /* Glassmorphism */ }
.gradient-text { /* Gradient text */ }
.smooth-transition { /* Smooth animations */ }
.flex-center { /* Flex center */ }
.grid-auto { /* Auto grid */ }
.hover-lift { /* Hover lift effect */ }
.animate-float { /* Float animation */ }
.animate-glow { /* Glow animation */ }
```

## Development Workflow

### 1. Create New Page

```typescript
// src/pages/MyPage.tsx
import { motion } from "framer-motion";
import { GlassCard } from "../components/GlassCard";
import { GlowButton } from "../components/GlowButton";

export function MyPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <GlassCard>
        <h1>My Page</h1>
        <GlowButton>Click me</GlowButton>
      </GlassCard>
    </motion.div>
  );
}
```

### 2. Add Route

```typescript
// src/App.tsx
<Route path="/my-page" element={<MyPage />} />
```

### 3. Use API

```typescript
import { useApi } from "../hooks/useApi";
import { apiClient } from "../lib/api";

const { data, isLoading, error } = useApi(
  () => apiClient.getSettlements(),
  []
);
```

## Testing

### Run Type Check
```bash
npm run type-check
```

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Deployment

### Build
```bash
npm run build
```

Output: `dist/` directory

### Deploy to Vercel
```bash
vercel deploy
```

### Deploy to Netlify
```bash
netlify deploy --prod --dir=dist
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:8000` |
| `REACT_APP_API_TIMEOUT` | API timeout (ms) | `10000` |
| `REACT_APP_CHAIN_ID` | Blockchain chain ID | `5042002` |
| `REACT_APP_RPC_URL` | Blockchain RPC URL | `https://rpc.testnet.arc.network` |
| `REACT_APP_ENABLE_WEBHOOKS` | Enable webhooks | `true` |
| `REACT_APP_ENABLE_DISPUTES` | Enable disputes | `true` |
| `REACT_APP_ENABLE_REPUTATION` | Enable reputation | `true` |

## Troubleshooting

### API Connection Failed
- Check `REACT_APP_API_URL` is correct
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend

### Wallet Connection Failed
- Install MetaMask or Arc wallet extension
- Ensure you're on the correct network (Arc testnet)
- Check wallet permissions

### Styling Issues
- Clear cache: `rm -rf node_modules .next dist`
- Reinstall: `npm install`
- Rebuild: `npm run build`

## Performance

- Lazy loading with React.lazy
- Code splitting with Vite
- Image optimization
- CSS minification
- Tree shaking

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Focus management
- Color contrast compliance

## Next Steps

1. Add more pages (Agent Management, Settings, etc.)
2. Implement real-time updates with WebSockets
3. Add notifications system
4. Create admin panel
5. Add analytics integration
6. Implement PWA features

## Support

For issues or questions, please refer to:
- Backend docs: `docs/API_UPDATED.md`
- Setup guide: `PRODUCTION_SETUP.md`
- Security guide: `docs/SECURITY_PRIVATE_KEY.md`
