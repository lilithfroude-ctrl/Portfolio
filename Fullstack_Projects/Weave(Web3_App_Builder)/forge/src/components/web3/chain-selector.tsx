"use client";

import { useState } from "react";
import { Check, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

const CHAINS = [
  { id: "base", name: "Base", icon: "🔵" },
  { id: "ethereum", name: "Ethereum", icon: "⟠" },
  { id: "polygon", name: "Polygon", icon: "💜" },
];

interface ChainSelectorProps {
  chain: string;
  network: "mainnet" | "testnet";
  onChainChange: (chain: string) => void;
  onNetworkChange: (network: "mainnet" | "testnet") => void;
}

export function ChainSelector({
  chain,
  network,
  onChainChange,
  onNetworkChange,
}: ChainSelectorProps) {
  const [open, setOpen] = useState(false);
  const selectedChain = CHAINS.find((c) => c.id === chain);

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-border bg-card hover:bg-accent transition"
      >
        <span className="text-base">{selectedChain?.icon}</span>
        <span className="text-sm font-medium">{selectedChain?.name}</span>
        <span
          className={cn(
            "px-2 py-0.5 text-xs rounded-full",
            network === "testnet"
              ? "bg-yellow-500/10 text-yellow-500"
              : "bg-green-500/10 text-green-500"
          )}
        >
          {network}
        </span>
        <ChevronDown className="w-4 h-4 text-muted-foreground" />
      </button>

      {open && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setOpen(false)}
          />
          
          {/* Dropdown */}
          <div className="absolute top-full right-0 mt-2 w-64 bg-card border border-border rounded-xl shadow-xl z-50 overflow-hidden">
            {/* Network Toggle */}
            <div className="p-3 border-b border-border">
              <p className="text-xs text-muted-foreground mb-2">Network</p>
              <div className="flex gap-2">
                <button
                  onClick={() => onNetworkChange("testnet")}
                  className={cn(
                    "flex-1 py-2 text-sm rounded-lg transition font-medium",
                    network === "testnet"
                      ? "bg-yellow-500 text-white"
                      : "bg-muted hover:bg-accent"
                  )}
                >
                  Testnet
                </button>
                <button
                  onClick={() => onNetworkChange("mainnet")}
                  className={cn(
                    "flex-1 py-2 text-sm rounded-lg transition font-medium",
                    network === "mainnet"
                      ? "bg-green-500 text-white"
                      : "bg-muted hover:bg-accent"
                  )}
                >
                  Mainnet
                </button>
              </div>
              {network === "mainnet" && (
                <p className="text-xs text-yellow-500 mt-2">
                  ⚠️ Real funds will be used on mainnet
                </p>
              )}
            </div>

            {/* Chain List */}
            <div className="p-2">
              <p className="text-xs text-muted-foreground px-2 mb-2">Chain</p>
              {CHAINS.map((c) => (
                <button
                  key={c.id}
                  onClick={() => {
                    onChainChange(c.id);
                    setOpen(false);
                  }}
                  className={cn(
                    "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition",
                    chain === c.id
                      ? "bg-forge-500/10 text-forge-500"
                      : "hover:bg-accent"
                  )}
                >
                  <span className="text-lg">{c.icon}</span>
                  <span className="font-medium">{c.name}</span>
                  {chain === c.id && (
                    <Check className="w-4 h-4 ml-auto" />
                  )}
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
