# Web3 Builder - Implementation Roadmap

## Quick Start: What to Build First

Based on how Lovable and Bolt achieved fast success, here's the optimal build order:

---

## Phase 1: Fork & Foundation (Week 1)

### Step 1: Clone Bolt.new

```bash
git clone https://github.com/stackblitz/bolt.new.git web3-builder
cd web3-builder
npm install
```

### Step 2: Study the Core Files

The key files to understand:

```
bolt.new/
├── app/
│   ├── lib/
│   │   └── stores/         # State management
│   ├── components/
│   │   ├── chat/           # Chat interface
│   │   ├── editor/         # Monaco code editor
│   │   └── workbench/      # File tree, preview
│   └── utils/
│       └── prompts.ts      # ⭐ THE SYSTEM PROMPT
├── packages/
│   └── bolt/
│       └── src/
│           └── runtime/    # WebContainer execution
```

### Step 3: Modify the System Prompt

Replace `app/utils/prompts.ts` with your Web3-enhanced version:

```typescript
// app/utils/prompts.ts
import { WORK_DIR } from '~/utils/constants';

export const getSystemPrompt = (cwd: string = WORK_DIR) => `
You are Web3Builder, an expert AI assistant for building decentralized applications.

<system_constraints>
  You are operating in WebContainer, a browser-based Node.js runtime.
  
  IMPORTANT: This environment supports:
  - React/Next.js frontend development
  - Web3 libraries (wagmi, viem, thirdweb SDK)
  - Smart contract compilation (solc)
  
  This environment does NOT support:
  - Direct blockchain node connections (use RPC providers)
  - Native binaries or system-level operations
</system_constraints>

<web3_capabilities>
  You can help users:
  1. Build dApp frontends with wallet integration
  2. Generate and deploy smart contracts via thirdweb
  3. Interact with deployed contracts
  4. Configure multi-chain support
  
  Supported Chains: Base, Ethereum, Polygon
  Default Chain: Base Sepolia (testnet)
</web3_capabilities>

<artifact_instructions>
  // ... keep existing Bolt artifact instructions ...
  
  ADDITIONAL WEB3 RULES:
  - Always include thirdweb Provider in the root layout
  - Default all deployments to testnet
  - Include wallet connection UI in initial setup
  - Use environment variables for API keys
</artifact_instructions>

// ... rest of your system prompt
`;
```

---

## Phase 2: Web3 Infrastructure (Week 2)

### Step 1: Set Up Thirdweb Integration

Create a new service for contract deployment:

```typescript
// app/lib/services/web3.ts
import { ThirdwebSDK } from "@thirdweb-dev/sdk";
import { BaseSepoliaTestnet, Base, Ethereum, Polygon } from "@thirdweb-dev/chains";

const CHAINS = {
  'base-testnet': BaseSepoliaTestnet,
  'base': Base,
  'ethereum': Ethereum,
  'polygon': Polygon,
};

export class Web3Service {
  private sdk: ThirdwebSDK;
  
  constructor(chain: keyof typeof CHAINS, secretKey: string) {
    this.sdk = ThirdwebSDK.fromPrivateKey(
      secretKey, // Project wallet private key
      CHAINS[chain],
      {
        clientId: process.env.THIRDWEB_CLIENT_ID,
        secretKey: process.env.THIRDWEB_SECRET_KEY,
      }
    );
  }
  
  async deployERC721(params: {
    name: string;
    symbol: string;
    royaltyBps?: number;
    primarySaleRecipient: string;
  }) {
    const contract = await this.sdk.deployer.deployNFTCollection({
      name: params.name,
      symbol: params.symbol,
      primary_sale_recipient: params.primarySaleRecipient,
      seller_fee_basis_points: params.royaltyBps || 500,
      fee_recipient: params.primarySaleRecipient,
    });
    
    return {
      address: contract,
      explorerUrl: `https://sepolia.basescan.org/address/${contract}`,
    };
  }
  
  async deployERC20(params: {
    name: string;
    symbol: string;
    initialSupply: string;
  }) {
    const contract = await this.sdk.deployer.deployToken({
      name: params.name,
      symbol: params.symbol,
      primary_sale_recipient: await this.sdk.wallet.getAddress(),
    });
    
    // Mint initial supply
    const token = await this.sdk.getContract(contract);
    await token.erc20.mint(params.initialSupply);
    
    return {
      address: contract,
      explorerUrl: `https://sepolia.basescan.org/address/${contract}`,
    };
  }
}
```

### Step 2: Add Web3 Tools to AI

Create custom tool handlers:

```typescript
// app/lib/tools/web3-tools.ts
import { Web3Service } from '../services/web3';

export interface Web3ToolResult {
  success: boolean;
  data?: any;
  error?: string;
}

export async function handleW3DeployContract(
  params: {
    contractType: 'ERC20' | 'ERC721' | 'ERC1155';
    chain: string;
    network: 'mainnet' | 'testnet';
    constructorArgs: Record<string, any>;
  },
  projectWalletKey: string
): Promise<Web3ToolResult> {
  const chainKey = params.network === 'testnet' 
    ? `${params.chain}-testnet` 
    : params.chain;
    
  const web3 = new Web3Service(chainKey as any, projectWalletKey);
  
  try {
    let result;
    
    switch (params.contractType) {
      case 'ERC721':
        result = await web3.deployERC721({
          name: params.constructorArgs.name,
          symbol: params.constructorArgs.symbol,
          royaltyBps: params.constructorArgs.royaltyBps,
          primarySaleRecipient: params.constructorArgs.recipient,
        });
        break;
        
      case 'ERC20':
        result = await web3.deployERC20({
          name: params.constructorArgs.name,
          symbol: params.constructorArgs.symbol,
          initialSupply: params.constructorArgs.initialSupply,
        });
        break;
        
      default:
        throw new Error(`Unsupported contract type: ${params.contractType}`);
    }
    
    return {
      success: true,
      data: {
        contractAddress: result.address,
        explorerUrl: result.explorerUrl,
        chain: params.chain,
        network: params.network,
      }
    };
  } catch (error: any) {
    return {
      success: false,
      error: error.message,
    };
  }
}
```

---

## Phase 3: Wallet Management (Week 3)

### Step 1: Project Wallet System

Each project gets its own wallet. Store encrypted in your database.

```typescript
// app/lib/services/wallet-service.ts
import { Wallet } from 'ethers';
import { encrypt, decrypt } from '../utils/crypto';

interface ProjectWallet {
  id: string;
  projectId: string;
  address: string;
  encryptedPrivateKey: string;
  chain: string;
  createdAt: Date;
}

export class WalletService {
  // Create new wallet for a project
  static async createProjectWallet(
    projectId: string,
    chain: string,
    encryptionKey: string
  ): Promise<{ address: string }> {
    // Generate new wallet
    const wallet = Wallet.createRandom();
    
    // Encrypt private key before storing
    const encryptedKey = await encrypt(wallet.privateKey, encryptionKey);
    
    // Store in database
    await db.projectWallets.create({
      projectId,
      address: wallet.address,
      encryptedPrivateKey: encryptedKey,
      chain,
    });
    
    return { address: wallet.address };
  }
  
  // Get wallet for deployment
  static async getProjectWallet(
    projectId: string,
    decryptionKey: string
  ): Promise<string> {
    const walletRecord = await db.projectWallets.findUnique({
      where: { projectId }
    });
    
    if (!walletRecord) {
      throw new Error('Project wallet not found');
    }
    
    return decrypt(walletRecord.encryptedPrivateKey, decryptionKey);
  }
}
```

### Step 2: Gas Sponsorship

Use a paymaster or fund wallets directly:

```typescript
// app/lib/services/gas-service.ts
import { ethers } from 'ethers';

export class GasService {
  private platformWallet: ethers.Wallet;
  private provider: ethers.JsonRpcProvider;
  
  constructor() {
    this.provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
    this.platformWallet = new ethers.Wallet(
      process.env.PLATFORM_WALLET_KEY!,
      this.provider
    );
  }
  
  // Fund a project wallet
  async fundProjectWallet(
    toAddress: string,
    amountEth: string,
    userId: string
  ) {
    // Check user has credits
    const user = await db.users.findUnique({ where: { id: userId } });
    const requiredCredits = parseFloat(amountEth) * 100; // 1 ETH = 100 credits
    
    if (user.credits < requiredCredits) {
      throw new Error('Insufficient credits');
    }
    
    // Send gas
    const tx = await this.platformWallet.sendTransaction({
      to: toAddress,
      value: ethers.parseEther(amountEth),
    });
    
    await tx.wait();
    
    // Deduct credits
    await db.users.update({
      where: { id: userId },
      data: { credits: { decrement: requiredCredits } }
    });
    
    return {
      txHash: tx.hash,
      amount: amountEth,
      creditsUsed: requiredCredits,
    };
  }
}
```

---

## Phase 4: UI Components (Week 4)

### Step 1: Chain Selector

```tsx
// app/components/chain-selector.tsx
"use client";

import { useState } from 'react';
import { Check, ChevronDown } from 'lucide-react';

const CHAINS = [
  { id: 'base', name: 'Base', icon: '🔵', testnet: 'base-sepolia' },
  { id: 'ethereum', name: 'Ethereum', icon: '⟠', testnet: 'sepolia' },
  { id: 'polygon', name: 'Polygon', icon: '💜', testnet: 'amoy' },
];

interface ChainSelectorProps {
  value: string;
  onChange: (chain: string) => void;
  network: 'mainnet' | 'testnet';
  onNetworkChange: (network: 'mainnet' | 'testnet') => void;
}

export function ChainSelector({ 
  value, 
  onChange, 
  network,
  onNetworkChange 
}: ChainSelectorProps) {
  const [open, setOpen] = useState(false);
  const selected = CHAINS.find(c => c.id === value);
  
  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition"
      >
        <span>{selected?.icon}</span>
        <span>{selected?.name}</span>
        <span className={`text-xs px-2 py-0.5 rounded ${
          network === 'testnet' ? 'bg-yellow-600' : 'bg-green-600'
        }`}>
          {network}
        </span>
        <ChevronDown className="w-4 h-4" />
      </button>
      
      {open && (
        <div className="absolute top-full mt-2 w-64 bg-gray-800 rounded-lg shadow-xl z-50">
          <div className="p-2 border-b border-gray-700">
            <div className="flex gap-2">
              <button
                onClick={() => onNetworkChange('testnet')}
                className={`flex-1 py-1 rounded text-sm ${
                  network === 'testnet' ? 'bg-yellow-600' : 'bg-gray-700'
                }`}
              >
                Testnet
              </button>
              <button
                onClick={() => onNetworkChange('mainnet')}
                className={`flex-1 py-1 rounded text-sm ${
                  network === 'mainnet' ? 'bg-green-600' : 'bg-gray-700'
                }`}
              >
                Mainnet
              </button>
            </div>
          </div>
          
          <div className="p-2">
            {CHAINS.map(chain => (
              <button
                key={chain.id}
                onClick={() => {
                  onChange(chain.id);
                  setOpen(false);
                }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded hover:bg-gray-700"
              >
                <span>{chain.icon}</span>
                <span>{chain.name}</span>
                {value === chain.id && <Check className="w-4 h-4 ml-auto" />}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

### Step 2: Wallet Dashboard

```tsx
// app/components/wallet-dashboard.tsx
"use client";

import { useEffect, useState } from 'react';
import { Wallet, ArrowUpRight, Copy, Plus } from 'lucide-react';

interface WalletDashboardProps {
  projectId: string;
}

export function WalletDashboard({ projectId }: WalletDashboardProps) {
  const [wallet, setWallet] = useState<{
    address: string;
    balance: string;
    chain: string;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchWallet();
  }, [projectId]);
  
  async function fetchWallet() {
    const res = await fetch(`/api/projects/${projectId}/wallet`);
    if (res.ok) {
      setWallet(await res.json());
    }
    setLoading(false);
  }
  
  async function createWallet() {
    const res = await fetch(`/api/projects/${projectId}/wallet`, {
      method: 'POST',
      body: JSON.stringify({ chain: 'base' }),
    });
    if (res.ok) {
      setWallet(await res.json());
    }
  }
  
  if (loading) {
    return <div className="animate-pulse h-24 bg-gray-800 rounded-lg" />;
  }
  
  if (!wallet) {
    return (
      <button
        onClick={createWallet}
        className="w-full flex items-center justify-center gap-2 p-4 border-2 border-dashed border-gray-600 rounded-lg hover:border-blue-500 transition"
      >
        <Plus className="w-5 h-5" />
        <span>Create Project Wallet</span>
      </button>
    );
  }
  
  return (
    <div className="bg-gray-800 rounded-lg p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Wallet className="w-5 h-5 text-blue-400" />
          <span className="font-medium">Project Wallet</span>
        </div>
        <span className="text-xs px-2 py-1 bg-blue-600 rounded">
          {wallet.chain}
        </span>
      </div>
      
      <div className="flex items-center gap-2 text-sm text-gray-400">
        <code>{wallet.address.slice(0, 6)}...{wallet.address.slice(-4)}</code>
        <button
          onClick={() => navigator.clipboard.writeText(wallet.address)}
          className="hover:text-white transition"
        >
          <Copy className="w-4 h-4" />
        </button>
        <a
          href={`https://sepolia.basescan.org/address/${wallet.address}`}
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-white transition"
        >
          <ArrowUpRight className="w-4 h-4" />
        </a>
      </div>
      
      <div className="flex items-center justify-between pt-2 border-t border-gray-700">
        <span className="text-gray-400">Balance</span>
        <span className="font-mono">{wallet.balance} ETH</span>
      </div>
    </div>
  );
}
```

---

## Phase 5: Polish & Launch (Week 5-6)

### Key Features to Add

1. **Contract Templates Gallery**
   - NFT Collection (ERC-721)
   - Token (ERC-20)
   - NFT Drop with allowlist
   - Marketplace
   - Staking

2. **Example Projects**
   - NFT Minting Page
   - Token Dashboard
   - Simple DEX Interface
   - NFT Gallery

3. **Infrastructure Provider Selection**
   - Let users choose: Alchemy vs QuickNode
   - Let users bring their own API keys

4. **Deployment Confirmation Modal**
   - Show gas estimate
   - Show network (testnet/mainnet)
   - Require explicit confirmation for mainnet

---

## Database Schema (Prisma)

```prisma
// prisma/schema.prisma

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  credits   Float    @default(100)  // Gas funding credits
  plan      String   @default("free")
  projects  Project[]
  createdAt DateTime @default(now())
}

model Project {
  id          String   @id @default(cuid())
  name        String
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  chain       String   @default("base")
  network     String   @default("testnet")
  wallet      ProjectWallet?
  contracts   DeployedContract[]
  files       Json     // Store file system state
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model ProjectWallet {
  id                  String   @id @default(cuid())
  projectId           String   @unique
  project             Project  @relation(fields: [projectId], references: [id])
  address             String
  encryptedPrivateKey String   // Encrypted with KMS
  chain               String
  createdAt           DateTime @default(now())
}

model DeployedContract {
  id          String   @id @default(cuid())
  projectId   String
  project     Project  @relation(fields: [projectId], references: [id])
  address     String
  type        String   // ERC20, ERC721, etc.
  chain       String
  network     String
  name        String
  verified    Boolean  @default(false)
  txHash      String
  createdAt   DateTime @default(now())
}
```

---

## API Routes

```typescript
// Key API endpoints to implement

// POST /api/projects
// Create new project with optional chain selection

// GET /api/projects/:id
// Get project with files, wallet, contracts

// POST /api/projects/:id/wallet
// Create project wallet

// POST /api/projects/:id/wallet/fund
// Fund wallet with platform credits

// POST /api/projects/:id/deploy
// Deploy smart contract

// POST /api/projects/:id/verify
// Verify contract on block explorer

// POST /api/ai/chat
// Main AI chat endpoint - processes messages and returns tool calls
```

---

## Environment Variables

```bash
# .env

# AI
ANTHROPIC_API_KEY=sk-ant-...
# or
OPENAI_API_KEY=sk-...

# Thirdweb
THIRDWEB_CLIENT_ID=...
THIRDWEB_SECRET_KEY=...

# RPC Providers
ALCHEMY_API_KEY=...
# or
QUICKNODE_URL=...

# Database
DATABASE_URL=postgresql://...

# Encryption
ENCRYPTION_KEY=...  # For wallet private keys
AWS_KMS_KEY_ID=...  # Optional: Use KMS instead

# Platform Wallet (for gas sponsorship)
PLATFORM_WALLET_KEY=...

# Auth (Clerk recommended)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
CLERK_SECRET_KEY=...
```

---

## Quick Win: Start Here

If you want to see something working TODAY:

1. Clone Bolt.new
2. Replace the system prompt with Web3 instructions
3. Add thirdweb SDK to the base template
4. Add wagmi + wallet connection component
5. Test with: "Create an NFT minting page"

The AI will generate a working Web3 app using existing libraries. The more complex features (deployment, wallet management) can be added incrementally.

---

## Resources

- **Bolt.new Source**: https://github.com/stackblitz/bolt.new
- **Thirdweb Docs**: https://portal.thirdweb.com/
- **wagmi Docs**: https://wagmi.sh/
- **Base Docs**: https://docs.base.org/
- **WebContainer API**: https://webcontainers.io/
