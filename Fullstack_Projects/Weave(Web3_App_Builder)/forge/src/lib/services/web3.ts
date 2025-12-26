// Forge Web3 Service - Contract deployment and wallet management
import { ThirdwebSDK } from "@thirdweb-dev/sdk";
import { 
  Base, 
  BaseSepoliaTestnet,
  Ethereum,
  Sepolia,
  Polygon,
  PolygonAmoyTestnet 
} from "@thirdweb-dev/chains";
import { ethers } from "ethers";

// Chain mapping
const CHAINS = {
  "base-mainnet": Base,
  "base-testnet": BaseSepoliaTestnet,
  "ethereum-mainnet": Ethereum,
  "ethereum-testnet": Sepolia,
  "polygon-mainnet": Polygon,
  "polygon-testnet": PolygonAmoyTestnet,
} as const;

type ChainKey = keyof typeof CHAINS;

function getChainKey(chain: string, network: "mainnet" | "testnet"): ChainKey {
  return `${chain}-${network}` as ChainKey;
}

export interface DeployResult {
  success: boolean;
  contractAddress?: string;
  transactionHash?: string;
  explorerUrl?: string;
  error?: string;
}

export interface WalletInfo {
  address: string;
  balance: string;
  chain: string;
}

export class ForgeWeb3Service {
  private sdk: ThirdwebSDK;
  private chain: string;
  private network: "mainnet" | "testnet";

  constructor(
    privateKey: string,
    chain: string,
    network: "mainnet" | "testnet" = "testnet"
  ) {
    const chainKey = getChainKey(chain, network);
    const chainConfig = CHAINS[chainKey];
    
    if (!chainConfig) {
      throw new Error(`Unsupported chain: ${chain} ${network}`);
    }

    this.sdk = ThirdwebSDK.fromPrivateKey(privateKey, chainConfig, {
      clientId: process.env.NEXT_PUBLIC_THIRDWEB_CLIENT_ID,
      secretKey: process.env.THIRDWEB_SECRET_KEY,
    });
    
    this.chain = chain;
    this.network = network;
  }

  // Deploy ERC-20 Token
  async deployERC20(params: {
    name: string;
    symbol: string;
    initialSupply?: string;
    recipient?: string;
  }): Promise<DeployResult> {
    try {
      const walletAddress = await this.sdk.wallet.getAddress();
      
      const contractAddress = await this.sdk.deployer.deployToken({
        name: params.name,
        symbol: params.symbol,
        primary_sale_recipient: params.recipient || walletAddress,
      });

      // Mint initial supply if specified
      if (params.initialSupply) {
        const contract = await this.sdk.getContract(contractAddress);
        await contract.erc20.mint(params.initialSupply);
      }

      return {
        success: true,
        contractAddress,
        explorerUrl: this.getExplorerUrl(contractAddress),
      };
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      return { success: false, error: errorMessage };
    }
  }

  // Deploy ERC-721 NFT Collection
  async deployERC721(params: {
    name: string;
    symbol: string;
    royaltyBps?: number;
    recipient?: string;
  }): Promise<DeployResult> {
    try {
      const walletAddress = await this.sdk.wallet.getAddress();
      
      const contractAddress = await this.sdk.deployer.deployNFTCollection({
        name: params.name,
        symbol: params.symbol,
        primary_sale_recipient: params.recipient || walletAddress,
        seller_fee_basis_points: params.royaltyBps || 500,
        fee_recipient: params.recipient || walletAddress,
      });

      return {
        success: true,
        contractAddress,
        explorerUrl: this.getExplorerUrl(contractAddress),
      };
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      return { success: false, error: errorMessage };
    }
  }

  // Deploy ERC-1155 Multi-token
  async deployERC1155(params: {
    name: string;
    royaltyBps?: number;
    recipient?: string;
  }): Promise<DeployResult> {
    try {
      const walletAddress = await this.sdk.wallet.getAddress();
      
      const contractAddress = await this.sdk.deployer.deployEdition({
        name: params.name,
        primary_sale_recipient: params.recipient || walletAddress,
        seller_fee_basis_points: params.royaltyBps || 500,
        fee_recipient: params.recipient || walletAddress,
      });

      return {
        success: true,
        contractAddress,
        explorerUrl: this.getExplorerUrl(contractAddress),
      };
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      return { success: false, error: errorMessage };
    }
  }

  // Deploy NFT Drop (claimable NFTs)
  async deployNFTDrop(params: {
    name: string;
    symbol: string;
    maxSupply?: number;
    royaltyBps?: number;
    recipient?: string;
  }): Promise<DeployResult> {
    try {
      const walletAddress = await this.sdk.wallet.getAddress();
      
      const contractAddress = await this.sdk.deployer.deployNFTDrop({
        name: params.name,
        symbol: params.symbol,
        primary_sale_recipient: params.recipient || walletAddress,
        seller_fee_basis_points: params.royaltyBps || 500,
        fee_recipient: params.recipient || walletAddress,
      });

      return {
        success: true,
        contractAddress,
        explorerUrl: this.getExplorerUrl(contractAddress),
      };
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      return { success: false, error: errorMessage };
    }
  }

  // Deploy Marketplace
  async deployMarketplace(params: {
    name: string;
    recipient?: string;
  }): Promise<DeployResult> {
    try {
      const walletAddress = await this.sdk.wallet.getAddress();
      
      const contractAddress = await this.sdk.deployer.deployMarketplaceV3({
        name: params.name,
        platform_fee_recipient: params.recipient || walletAddress,
        platform_fee_basis_points: 250, // 2.5%
      });

      return {
        success: true,
        contractAddress,
        explorerUrl: this.getExplorerUrl(contractAddress),
      };
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      return { success: false, error: errorMessage };
    }
  }

  // Get wallet info
  async getWalletInfo(): Promise<WalletInfo> {
    const address = await this.sdk.wallet.getAddress();
    const balance = await this.sdk.wallet.balance();
    
    return {
      address,
      balance: balance.displayValue,
      chain: `${this.chain}-${this.network}`,
    };
  }

  // Get explorer URL for contract
  private getExplorerUrl(address: string): string {
    const explorers: Record<string, string> = {
      "base-mainnet": "https://basescan.org",
      "base-testnet": "https://sepolia.basescan.org",
      "ethereum-mainnet": "https://etherscan.io",
      "ethereum-testnet": "https://sepolia.etherscan.io",
      "polygon-mainnet": "https://polygonscan.com",
      "polygon-testnet": "https://amoy.polygonscan.com",
    };
    
    const baseUrl = explorers[getChainKey(this.chain, this.network)];
    return `${baseUrl}/address/${address}`;
  }
}

// Wallet generation utilities
export function generateWallet(): { address: string; privateKey: string } {
  const wallet = ethers.Wallet.createRandom();
  return {
    address: wallet.address,
    privateKey: wallet.privateKey,
  };
}

// Get wallet balance
export async function getWalletBalance(
  address: string,
  chain: string,
  network: "mainnet" | "testnet"
): Promise<string> {
  const rpcUrls: Record<string, string> = {
    "base-mainnet": "https://mainnet.base.org",
    "base-testnet": "https://sepolia.base.org",
    "ethereum-mainnet": "https://eth.llamarpc.com",
    "ethereum-testnet": "https://rpc.sepolia.org",
    "polygon-mainnet": "https://polygon-rpc.com",
    "polygon-testnet": "https://rpc-amoy.polygon.technology",
  };
  
  const rpc = rpcUrls[getChainKey(chain, network)];
  const provider = new ethers.providers.JsonRpcProvider(rpc);
  const balance = await provider.getBalance(address);
  
  return ethers.utils.formatEther(balance);
}

// Fund a wallet (from platform wallet)
export async function fundWallet(
  toAddress: string,
  amount: string,
  chain: string,
  network: "mainnet" | "testnet"
): Promise<{ success: boolean; txHash?: string; error?: string }> {
  const platformKey = process.env.PLATFORM_WALLET_KEY;
  if (!platformKey) {
    return { success: false, error: "Platform wallet not configured" };
  }
  
  const rpcUrls: Record<string, string> = {
    "base-mainnet": "https://mainnet.base.org",
    "base-testnet": "https://sepolia.base.org",
    "ethereum-mainnet": "https://eth.llamarpc.com",
    "ethereum-testnet": "https://rpc.sepolia.org",
    "polygon-mainnet": "https://polygon-rpc.com",
    "polygon-testnet": "https://rpc-amoy.polygon.technology",
  };
  
  try {
    const rpc = rpcUrls[getChainKey(chain, network)];
    const provider = new ethers.providers.JsonRpcProvider(rpc);
    const wallet = new ethers.Wallet(platformKey, provider);
    
    const tx = await wallet.sendTransaction({
      to: toAddress,
      value: ethers.utils.parseEther(amount),
    });
    
    await tx.wait();
    
    return { success: true, txHash: tx.hash };
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : "Unknown error";
    return { success: false, error: errorMessage };
  }
}
