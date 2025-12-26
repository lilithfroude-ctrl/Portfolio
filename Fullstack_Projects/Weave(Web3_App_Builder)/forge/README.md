# 🔥 Forge

**Forge your dApp in minutes.** AI-powered Web3 development platform.

![Forge](https://img.shields.io/badge/Forge-Web3%20Builder-orange)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)

## Features

- 🤖 **AI-Powered Development** - Describe what you want, Forge builds it
- 🔗 **Multi-Chain Support** - Deploy to Base, Ethereum, or Polygon
- 👛 **Built-in Wallets** - Every project gets its own wallet
- ⛽ **Gas Sponsorship** - We handle gas so you can focus on building
- 📜 **One-Click Contracts** - Deploy ERC-20, ERC-721, and more
- 👁️ **Live Preview** - See changes in real-time

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **AI**: Anthropic Claude
- **Web3**: Thirdweb SDK + wagmi + viem
- **Auth**: Clerk
- **Database**: PostgreSQL (Prisma)

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm (recommended) or npm
- PostgreSQL database
- API keys (see below)

### Required API Keys

1. **Anthropic** - [Get API Key](https://console.anthropic.com/)
2. **Thirdweb** - [Get Client ID](https://thirdweb.com/dashboard)
3. **Clerk** - [Get Keys](https://clerk.com/dashboard)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/forge.git
cd forge

# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API keys

# Set up database
pnpm db:push

# Run development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) to see Forge.

## Project Structure

```
forge/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (dashboard)/        # Dashboard routes
│   │   ├── api/                # API routes
│   │   └── project/[id]/       # Project workbench
│   ├── components/
│   │   ├── chat/               # Chat interface
│   │   ├── editor/             # Code editor & preview
│   │   ├── ui/                 # shadcn/ui components
│   │   └── web3/               # Web3 components
│   ├── lib/
│   │   ├── ai/                 # AI client & prompts
│   │   ├── services/           # Web3 services
│   │   └── utils.ts            # Utilities
│   └── types/                  # TypeScript types
├── prisma/
│   └── schema.prisma           # Database schema
└── public/                     # Static assets
```

## Development Roadmap

### Phase 1: MVP ✅
- [x] Project structure
- [x] AI chat integration
- [x] Chain selector
- [x] Wallet panel UI
- [ ] File system integration
- [ ] Live preview

### Phase 2: Core Features
- [ ] Smart contract deployment
- [ ] Wallet creation & funding
- [ ] Contract verification
- [ ] Template library

### Phase 3: Polish
- [ ] Monaco editor integration
- [ ] Real-time preview
- [ ] Collaboration features
- [ ] Billing & subscriptions

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with 🔥 by the Forge team
