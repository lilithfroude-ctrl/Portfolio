"use client";

import { useState } from "react";
import { 
  Wallet, 
  Plus, 
  Copy, 
  ExternalLink, 
  RefreshCw,
  FileCode,
  ChevronRight,
  Loader2
} from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

interface WalletPanelProps {
  projectId: string;
  chain: string;
  network: "mainnet" | "testnet";
}

interface ProjectWallet {
  address: string;
  balance: string;
}

interface DeployedContract {
  address: string;
  name: string;
  type: string;
}

export function WalletPanel({ projectId, chain, network }: WalletPanelProps) {
  const [wallet, setWallet] = useState<ProjectWallet | null>(null);
  const [contracts, setContracts] = useState<DeployedContract[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const explorerUrls: Record<string, Record<string, string>> = {
    base: {
      testnet: "https://sepolia.basescan.org",
      mainnet: "https://basescan.org",
    },
    ethereum: {
      testnet: "https://sepolia.etherscan.io",
      mainnet: "https://etherscan.io",
    },
    polygon: {
      testnet: "https://amoy.polygonscan.com",
      mainnet: "https://polygonscan.com",
    },
  };

  const getExplorerUrl = (address: string) => {
    return `${explorerUrls[chain]?.[network]}/address/${address}`;
  };

  const createWallet = async () => {
    setIsCreating(true);
    try {
      const response = await fetch(`/api/projects/${projectId}/wallet`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chain }),
      });

      if (!response.ok) throw new Error("Failed to create wallet");

      const data = await response.json();
      setWallet(data);
      toast.success("Project wallet created!");
    } catch (error) {
      console.error(error);
      toast.error("Failed to create wallet");
    } finally {
      setIsCreating(false);
    }
  };

  const copyAddress = () => {
    if (wallet?.address) {
      navigator.clipboard.writeText(wallet.address);
      toast.success("Address copied!");
    }
  };

  const refreshBalance = async () => {
    if (!wallet) return;
    setIsLoading(true);
    try {
      const response = await fetch(`/api/projects/${projectId}/wallet`);
      if (response.ok) {
        const data = await response.json();
        setWallet(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-6">
      {/* Wallet Section */}
      <section>
        <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-3">
          Project Wallet
        </h3>

        {wallet ? (
          <div className="bg-muted rounded-xl p-4 space-y-4">
            {/* Address */}
            <div>
              <p className="text-xs text-muted-foreground mb-1">Address</p>
              <div className="flex items-center gap-2">
                <code className="text-sm font-mono">
                  {wallet.address.slice(0, 6)}...{wallet.address.slice(-4)}
                </code>
                <button
                  onClick={copyAddress}
                  className="p-1 rounded hover:bg-accent transition"
                >
                  <Copy className="w-3.5 h-3.5" />
                </button>
                <a
                  href={getExplorerUrl(wallet.address)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-1 rounded hover:bg-accent transition"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>

            {/* Balance */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <p className="text-xs text-muted-foreground">Balance</p>
                <button
                  onClick={refreshBalance}
                  disabled={isLoading}
                  className="p-1 rounded hover:bg-accent transition"
                >
                  <RefreshCw className={cn(
                    "w-3.5 h-3.5",
                    isLoading && "animate-spin"
                  )} />
                </button>
              </div>
              <p className="text-lg font-semibold font-mono">
                {wallet.balance} ETH
              </p>
            </div>

            {/* Fund Button */}
            <button className="w-full py-2 rounded-lg border border-forge-500 text-forge-500 hover:bg-forge-500/10 transition text-sm font-medium">
              Add Gas
            </button>
          </div>
        ) : (
          <button
            onClick={createWallet}
            disabled={isCreating}
            className="w-full flex items-center justify-center gap-2 p-4 rounded-xl border-2 border-dashed border-border hover:border-forge-500/50 hover:bg-accent/30 transition"
          >
            {isCreating ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <>
                <Plus className="w-5 h-5" />
                <span>Create Wallet</span>
              </>
            )}
          </button>
        )}
      </section>

      {/* Deployed Contracts */}
      <section>
        <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-3">
          Deployed Contracts
        </h3>

        {contracts.length > 0 ? (
          <div className="space-y-2">
            {contracts.map((contract) => (
              <ContractCard
                key={contract.address}
                contract={contract}
                explorerUrl={getExplorerUrl(contract.address)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <FileCode className="w-10 h-10 text-muted-foreground/50 mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">
              No contracts deployed yet
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              Ask Forge to deploy a contract
            </p>
          </div>
        )}
      </section>

      {/* Quick Actions */}
      <section>
        <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-3">
          Quick Deploy
        </h3>
        <div className="space-y-2">
          <QuickDeployButton type="ERC-721" description="NFT Collection" />
          <QuickDeployButton type="ERC-20" description="Fungible Token" />
          <QuickDeployButton type="NFT Drop" description="Claimable NFTs" />
        </div>
      </section>
    </div>
  );
}

function ContractCard({ 
  contract, 
  explorerUrl 
}: { 
  contract: DeployedContract;
  explorerUrl: string;
}) {
  return (
    <a
      href={explorerUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center justify-between p-3 rounded-lg bg-muted hover:bg-accent transition group"
    >
      <div>
        <p className="font-medium text-sm">{contract.name}</p>
        <p className="text-xs text-muted-foreground">
          {contract.type} • {contract.address.slice(0, 6)}...{contract.address.slice(-4)}
        </p>
      </div>
      <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-foreground transition" />
    </a>
  );
}

function QuickDeployButton({ 
  type, 
  description 
}: { 
  type: string;
  description: string;
}) {
  return (
    <button className="w-full flex items-center justify-between p-3 rounded-lg border border-border hover:border-forge-500/50 hover:bg-accent/30 transition text-left">
      <div>
        <p className="font-medium text-sm">{type}</p>
        <p className="text-xs text-muted-foreground">{description}</p>
      </div>
      <ChevronRight className="w-4 h-4 text-muted-foreground" />
    </button>
  );
}
