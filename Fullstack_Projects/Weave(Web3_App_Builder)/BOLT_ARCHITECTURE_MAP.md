# 🔥 Bolt.new Architecture Map for Web3 Integration

## Overview

This document maps Bolt.new's key components so you can integrate Web3 features. Based on the prompts.ts file and typical Bolt.new structure.

---

## 📁 Key File Locations

### 1. **System Prompt** ⭐ MOST IMPORTANT
**Location:** `app/utils/prompts.ts` (or `app/lib/prompts.ts`)

**What it does:**
- Defines Bolt's personality and capabilities
- Contains artifact format instructions (`<boltArtifact>`, `<boltAction>`)
- Sets coding standards and constraints

**Current structure:**
```typescript
export const getSystemPrompt = (cwd: string = WORK_DIR) => `
  You are Bolt, an expert AI assistant...
  
  <artifact_info>
    <artifact_instructions>
      // How to create artifacts
    </artifact_instructions>
  </artifact_info>
`;
```

**Where to inject Web3:**
- Add `<web3_capabilities>` section
- Add Web3 tool definitions
- Add contract deployment instructions
- Add chain configuration info

---

### 2. **Artifact Parser & Executor**
**Location:** `app/lib/artifact-parser.ts` or `app/utils/artifact-handler.ts`

**What it does:**
- Parses `<boltArtifact>` XML from AI responses
- Extracts `<boltAction>` elements (type="file" or type="shell")
- Executes file writes and shell commands
- Manages WebContainer file system

**How it works:**
```typescript
// Pseudo-code structure
function parseArtifact(xml: string) {
  // Extract <boltArtifact id="..." title="...">
  // Extract <boltAction type="file" filePath="...">
  // Extract <boltAction type="shell">
  // Return structured actions
}

function executeActions(actions: Action[]) {
  // Write files to WebContainer
  // Run shell commands in WebContainer
  // Update file tree UI
}
```

**Where to add Web3:**
- Add new action type: `type="web3-deploy"`
- Add handler for contract deployment
- Add handler for wallet creation
- Add handler for funding wallets

---

### 3. **Chat Message Handler**
**Location:** `app/api/chat/route.ts` or `app/routes/api/chat.ts`

**What it does:**
- Receives user messages from chat UI
- Calls Claude API with system prompt
- Returns AI response with artifacts
- Streams responses for real-time UI

**Current flow:**
```
User Message → API Route → Claude API → Parse Artifacts → Execute → Update UI
```

**Where to inject Web3:**
- Add project context (chain, network, wallet address)
- Add Web3 tool definitions to Claude call
- Parse Web3-specific artifacts
- Route Web3 actions to handlers

---

### 4. **Chat UI Component**
**Location:** `app/components/chat/BaseChat.tsx` or `app/components/Chat.tsx`

**What it does:**
- Renders chat messages
- Handles user input
- Shows streaming AI responses
- Displays artifact execution status

**Where to add Web3:**
- Add chain selector dropdown
- Add wallet status indicator
- Show contract deployment status
- Display transaction hashes

---

### 5. **File System / WebContainer Integration**
**Location:** `packages/bolt/src/runtime/` or `app/lib/webcontainer.ts`

**What it does:**
- Manages virtual file system
- Executes npm commands
- Runs dev servers (Vite)
- Provides live preview

**Where to add Web3:**
- Add Web3 package installation
- Add contract compilation support
- Add deployment scripts
- Add RPC provider configuration

---

### 6. **State Management**
**Location:** `app/lib/stores/` or `app/stores/`

**What it does:**
- Manages project files
- Tracks chat history
- Stores UI state
- Manages WebContainer instance

**Where to add Web3:**
- Add chain/network state
- Add wallet address state
- Add deployed contracts state
- Add transaction history

---

## 🔗 How Components Connect

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Chat UI    │  │  File Tree   │  │   Live Preview   │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘   │
│         │                 │                    │             │
└─────────┼─────────────────┼────────────────────┼─────────────┘
          │                 │                    │
          ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                  API LAYER                                  │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  /api/chat                                             │ │
│  │  1. Receives user message                             │ │
│  │  2. Calls Claude with system prompt                   │ │
│  │  3. Parses <boltArtifact> from response              │ │
│  │  4. Returns artifacts to frontend                     │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              ARTIFACT EXECUTOR                               │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  parseArtifact()                                     │ │
│  │  - Extracts <boltAction type="file">                 │ │
│  │  - Extracts <boltAction type="shell">                │ │
│  │  - Extracts <boltAction type="web3-deploy"> ⭐ NEW   │ │
│  └──────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  executeActions()                                     │ │
│  │  - Writes files to WebContainer                      │ │
│  │  - Runs shell commands                               │ │
│  │  - Calls Web3 API handlers ⭐ NEW                    │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              WEB3 HANDLERS ⭐ NEW                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  Deploy      │  │  Create       │  │  Fund Wallet     │ │
│  │  Contract    │  │  Wallet      │  │                  │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Integration Points for Web3

### Point 1: System Prompt (`app/utils/prompts.ts`)

**Add this section:**
```typescript
<web3_capabilities>
  You can help users:
  - Deploy smart contracts (ERC20, ERC721, ERC1155)
  - Create project wallets
  - Fund wallets with gas
  - Integrate wallet connections
  - Configure multi-chain support
</web3_capabilities>

<web3_tools>
  <boltAction type="web3-deploy" contractType="ERC721" chain="base" network="testnet">
    {
      "name": "My NFT",
      "symbol": "MNFT",
      "maxSupply": 10000
    }
  </boltAction>
  
  <boltAction type="web3-wallet" chain="base" />
  
  <boltAction type="web3-fund" amount="0.01" chain="base" />
</web3_tools>
```

---

### Point 2: Artifact Parser (`app/lib/artifact-parser.ts`)

**Add Web3 action parsing:**
```typescript
// In parseArtifact function
const web3DeployRegex = /<boltAction type="web3-deploy"([^>]*)>([\s\S]*?)<\/boltAction>/g;
const web3WalletRegex = /<boltAction type="web3-wallet"([^>]*)\/>/g;
const web3FundRegex = /<boltAction type="web3-fund"([^>]*)\/>/g;

// Extract attributes and add to actions array
```

---

### Point 3: Web3 Action Executor (`app/lib/web3-executor.ts`) ⭐ NEW FILE

**Create this file:**
```typescript
import { deployContract } from '@/lib/services/web3';
import { createWallet } from '@/lib/services/wallet';
import { fundWallet } from '@/lib/services/funding';

export async function executeWeb3Action(action: Web3Action) {
  switch (action.type) {
    case 'web3-deploy':
      return await deployContract(action.params);
    case 'web3-wallet':
      return await createWallet(action.chain);
    case 'web3-fund':
      return await fundWallet(action.amount, action.chain);
  }
}
```

---

### Point 4: Chat API Route (`app/api/chat/route.ts`)

**Add Web3 context:**
```typescript
// Fetch project context from database
const project = await db.project.findUnique({ where: { id: projectId } });

const projectContext = {
  files: project.files,
  chain: project.chain,
  network: project.network,
  walletAddress: project.wallet?.address,
};

// Pass to Claude API call
const response = await chat(messages, projectContext);
```

---

### Point 5: Chat UI Component (`app/components/chat/BaseChat.tsx`)

**Add Web3 UI elements:**
```typescript
// Add chain selector
<ChainSelector 
  value={chain} 
  onChange={setChain}
/>

// Add wallet status
<WalletStatus 
  address={walletAddress}
  balance={balance}
/>

// Show deployment status
{deploymentStatus && (
  <DeploymentStatus 
    contractAddress={deploymentStatus.address}
    txHash={deploymentStatus.txHash}
  />
)}
```

---

## 📋 Integration Checklist

- [ ] **Replace system prompt** with Web3-enhanced version
- [ ] **Add Web3 action types** to artifact parser
- [ ] **Create Web3 executor** module
- [ ] **Add Web3 API routes** (`/api/web3/deploy`, `/api/web3/wallet`, etc.)
- [ ] **Update chat API** to include Web3 context
- [ ] **Add Web3 UI components** (chain selector, wallet panel)
- [ ] **Add Web3 state management** (Zustand store)
- [ ] **Test artifact parsing** with Web3 actions
- [ ] **Test contract deployment** end-to-end
- [ ] **Add error handling** for Web3 operations

---

## 🚀 Next Steps

1. **Find Bolt.new's actual codebase** (should be in a separate directory)
2. **Locate the exact file paths** mentioned above
3. **Replace system prompt** with your Web3 version
4. **Add Web3 action parsing** to artifact handler
5. **Create Web3 executor** that calls your API routes
6. **Add UI components** for chain/wallet management

---

## 🔍 How to Find Bolt.new Files

If Bolt.new is in a different location:

```bash
# Search for key files
find . -name "prompts.ts" -type f
find . -name "*artifact*" -type f
find . -name "*webcontainer*" -type f
find . -name "BaseChat*" -type f
```

Look for:
- `app/` or `src/app/` directory structure
- `packages/bolt/` for WebContainer integration
- `app/utils/prompts.ts` for system prompt
- `app/components/chat/` for chat UI

---

**Once you find Bolt.new's actual codebase, update this map with the exact file paths!** 🔥

