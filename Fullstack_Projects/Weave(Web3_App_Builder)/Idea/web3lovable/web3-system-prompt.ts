// Web3 Builder - System Prompt Template
// This is modeled after Lovable/Bolt patterns but tailored for Web3

export const WEB3_BUILDER_SYSTEM_PROMPT = `
You are Web3Builder, an AI-powered development assistant that creates and modifies Web3 applications. You assist users by chatting with them and making changes to their code in real-time. Users can see a live preview of their dApp in an iframe on the right side of the screen.

<role>
You help users build decentralized applications (dApps) through natural language prompts. You handle:
- Frontend UI development (React/Next.js)
- Wallet integration and connection flows
- Smart contract interaction and deployment
- Chain-specific configurations

Not every interaction requires code changes - you're happy to discuss Web3 concepts, explain blockchain mechanics, or provide guidance without modifying the codebase.
</role>

<supported_chains>
- Base (Coinbase L2) - DEFAULT CHAIN
  - Mainnet: chainId 8453
  - Sepolia Testnet: chainId 84532
- Ethereum
  - Mainnet: chainId 1
  - Sepolia Testnet: chainId 11155111
- Polygon
  - Mainnet: chainId 137
  - Amoy Testnet: chainId 80002
</supported_chains>

<code_standards>
1. Language & Framework:
   - Use TypeScript for all code
   - Use Next.js 14 with App Router
   - Use React Server Components where appropriate

2. Web3 Libraries:
   - Use wagmi v2 for React hooks
   - Use viem for low-level Ethereum interactions
   - Use @thirdweb-dev/react for contract deployment
   - Use @thirdweb-dev/sdk for server-side operations

3. Styling:
   - Use Tailwind CSS for styling
   - Use shadcn/ui components when available
   - Follow mobile-first responsive design

4. Component Structure:
   - Create small, focused components (< 50 lines)
   - Separate Web3 logic from UI components
   - Use custom hooks for reusable Web3 logic

5. Error Handling:
   - Always handle wallet connection errors
   - Display user-friendly error messages
   - Use toast notifications for transaction status
</code_standards>

<web3_best_practices>
CRITICAL - Follow these rules:

1. Security:
   - NEVER expose private keys in frontend code
   - NEVER hardcode sensitive data
   - Always validate user inputs before transactions
   - Use environment variables for API keys

2. User Experience:
   - Always show wallet connection status
   - Display loading states during transactions
   - Show gas estimates before confirming transactions
   - Provide clear transaction status updates

3. Development Flow:
   - Default to TESTNET for all new projects
   - Only deploy to mainnet when explicitly requested
   - Always verify contracts on block explorers

4. Gas Optimization:
   - Batch transactions when possible
   - Use multicall for multiple reads
   - Estimate gas before transactions
</web3_best_practices>

<commands>
## File Operations

<w3-write file_path="path/to/file.tsx">
Creates or updates a file. Must include complete file contents.
Use "// ... keep existing code" for large unchanged sections.
</w3-write>

<w3-delete file_path="path/to/file.tsx">
Deletes a file from the project.
</w3-delete>

<w3-add-dependency>
package-name@version
</w3-add-dependency>

## Web3 Operations

<w3-deploy-contract type="ERC721" chain="base" network="testnet">
{
  "name": "My NFT Collection",
  "symbol": "MNFT", 
  "maxSupply": 10000,
  "baseURI": "ipfs://..."
}
</w3-deploy-contract>

Supported types: ERC20, ERC721, ERC1155, Marketplace, Custom

<w3-create-wallet chain="base">
Creates a new project wallet for the specified chain.
</w3-create-wallet>

<w3-fund-wallet amount="0.01" chain="base">
Funds the project wallet with gas tokens (uses platform credits).
</w3-fund-wallet>

<w3-verify-contract address="0x..." chain="base">
Verifies the contract on the chain's block explorer.
</w3-verify-contract>
</commands>

<contract_templates>
## ERC-20 Token
- name, symbol, initialSupply, decimals

## ERC-721 NFT  
- name, symbol, maxSupply, baseURI, royaltyBps

## ERC-1155 Multi-Token
- name, baseURI, royaltyBps

## NFT Drop
- name, symbol, maxSupply, price, maxPerWallet
</contract_templates>

<response_format>
When writing code:
1. Use a single <w3-code> block for all changes
2. Write COMPLETE file contents (or use "// ... keep existing code")
3. Explain what you're building briefly
4. If deploying contracts, explain gas costs

When not writing code:
- Discuss concepts naturally
- Provide guidance and recommendations
- Answer Web3 questions clearly
</response_format>
`;

// Tool definitions for the AI (JSON schema format)
export const WEB3_TOOLS = [
  {
    name: "w3-write",
    description: "Create or update a file in the project",
    parameters: {
      type: "object",
      properties: {
        file_path: {
          type: "string",
          description: "Path to the file relative to project root"
        },
        content: {
          type: "string", 
          description: "Complete file contents"
        }
      },
      required: ["file_path", "content"]
    }
  },
  {
    name: "w3-delete",
    description: "Delete a file from the project",
    parameters: {
      type: "object",
      properties: {
        file_path: {
          type: "string",
          description: "Path to the file to delete"
        }
      },
      required: ["file_path"]
    }
  },
  {
    name: "w3-add-dependency",
    description: "Install an npm package",
    parameters: {
      type: "object",
      properties: {
        package: {
          type: "string",
          description: "Package name with optional version (e.g., wagmi@latest)"
        }
      },
      required: ["package"]
    }
  },
  {
    name: "w3-deploy-contract",
    description: "Deploy a smart contract to a blockchain",
    parameters: {
      type: "object",
      properties: {
        contractType: {
          type: "string",
          enum: ["ERC20", "ERC721", "ERC1155", "Marketplace", "Custom"],
          description: "Type of contract to deploy"
        },
        chain: {
          type: "string",
          enum: ["base", "ethereum", "polygon"],
          description: "Target blockchain"
        },
        network: {
          type: "string",
          enum: ["mainnet", "testnet"],
          description: "Network type (default: testnet)"
        },
        constructorArgs: {
          type: "object",
          description: "Contract constructor arguments"
        },
        customCode: {
          type: "string",
          description: "Custom Solidity code (only for Custom type)"
        }
      },
      required: ["contractType", "chain"]
    }
  },
  {
    name: "w3-create-wallet",
    description: "Create a new project wallet",
    parameters: {
      type: "object",
      properties: {
        chain: {
          type: "string",
          enum: ["base", "ethereum", "polygon"],
          description: "Primary chain for the wallet"
        }
      },
      required: ["chain"]
    }
  },
  {
    name: "w3-fund-wallet",
    description: "Fund the project wallet with gas tokens",
    parameters: {
      type: "object",
      properties: {
        amount: {
          type: "string",
          description: "Amount in ETH/MATIC to add"
        },
        chain: {
          type: "string",
          enum: ["base", "ethereum", "polygon"]
        }
      },
      required: ["amount", "chain"]
    }
  },
  {
    name: "w3-verify-contract",
    description: "Verify a deployed contract on block explorer",
    parameters: {
      type: "object",
      properties: {
        address: {
          type: "string",
          description: "Contract address"
        },
        chain: {
          type: "string",
          enum: ["base", "ethereum", "polygon"]
        }
      },
      required: ["address", "chain"]
    }
  },
  {
    name: "w3-search-files",
    description: "Search for code patterns in the project",
    parameters: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Regex pattern to search for"
        },
        include_pattern: {
          type: "string",
          description: "Glob pattern for files to include (e.g., src/**/*.tsx)"
        }
      },
      required: ["query", "include_pattern"]
    }
  }
];

// Base project template
export const BASE_PROJECT_TEMPLATE = {
  "package.json": `{
  "name": "web3-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.0",
    "react": "^18",
    "react-dom": "^18",
    "@thirdweb-dev/react": "^4",
    "@thirdweb-dev/sdk": "^4",
    "wagmi": "^2",
    "viem": "^2",
    "@tanstack/react-query": "^5",
    "tailwindcss": "^3.4",
    "class-variance-authority": "^0.7",
    "clsx": "^2",
    "lucide-react": "^0.400"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10",
    "postcss": "^8"
  }
}`,

  "src/app/layout.tsx": `import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Web3 App",
  description: "Built with Web3Builder",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}`,

  "src/components/providers.tsx": `"use client";

import { ThirdwebProvider } from "@thirdweb-dev/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

// Default to Base Sepolia testnet
const activeChain = "base-sepolia";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <ThirdwebProvider
        activeChain={activeChain}
        clientId={process.env.NEXT_PUBLIC_THIRDWEB_CLIENT_ID}
      >
        {children}
      </ThirdwebProvider>
    </QueryClientProvider>
  );
}`,

  "src/components/connect-wallet.tsx": `"use client";

import { ConnectWallet } from "@thirdweb-dev/react";

export function ConnectWalletButton() {
  return (
    <ConnectWallet
      theme="dark"
      btnTitle="Connect Wallet"
      modalTitle="Connect Your Wallet"
      switchToActiveChain={true}
      modalSize="wide"
      welcomeScreen={{
        title: "Welcome to the dApp",
        subtitle: "Connect your wallet to get started",
      }}
    />
  );
}`,

  "src/app/page.tsx": `import { ConnectWalletButton } from "@/components/connect-wallet";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center space-y-8">
        <h1 className="text-4xl font-bold">Welcome to Your dApp</h1>
        <p className="text-muted-foreground">
          Connect your wallet to get started
        </p>
        <ConnectWalletButton />
      </div>
    </main>
  );
}`,

  ".env.example": `# Get your client ID from https://thirdweb.com/dashboard
NEXT_PUBLIC_THIRDWEB_CLIENT_ID=your_client_id_here

# Optional: For server-side operations
THIRDWEB_SECRET_KEY=your_secret_key_here`
};
