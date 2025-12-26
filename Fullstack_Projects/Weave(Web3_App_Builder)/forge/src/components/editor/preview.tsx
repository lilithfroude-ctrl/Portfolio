"use client";

import { RefreshCw, ExternalLink, Smartphone, Monitor, Tablet } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

type ViewportSize = "mobile" | "tablet" | "desktop";

const viewportSizes: Record<ViewportSize, { width: string; icon: React.ReactNode }> = {
  mobile: { width: "375px", icon: <Smartphone className="w-4 h-4" /> },
  tablet: { width: "768px", icon: <Tablet className="w-4 h-4" /> },
  desktop: { width: "100%", icon: <Monitor className="w-4 h-4" /> },
};

export function Preview() {
  const [viewport, setViewport] = useState<ViewportSize>("desktop");
  const [key, setKey] = useState(0);

  const refresh = () => setKey((k) => k + 1);

  return (
    <div className="h-full flex flex-col bg-muted/30">
      {/* Toolbar */}
      <div className="h-10 border-b border-border flex items-center justify-between px-4 bg-card">
        <div className="flex items-center gap-1">
          {(Object.keys(viewportSizes) as ViewportSize[]).map((size) => (
            <button
              key={size}
              onClick={() => setViewport(size)}
              className={cn(
                "p-1.5 rounded transition",
                viewport === size 
                  ? "bg-accent text-foreground" 
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              {viewportSizes[size].icon}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={refresh}
            className="p-1.5 rounded hover:bg-accent transition"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <button className="p-1.5 rounded hover:bg-accent transition">
            <ExternalLink className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Preview Frame */}
      <div className="flex-1 flex items-start justify-center p-4 overflow-auto">
        <div 
          className={cn(
            "bg-white rounded-lg shadow-xl overflow-hidden transition-all duration-300",
            viewport === "desktop" ? "w-full h-full" : "h-[600px]"
          )}
          style={{ 
            width: viewportSizes[viewport].width,
            maxWidth: "100%"
          }}
        >
          {/* In production, this would be an iframe pointing to the dev server */}
          <div 
            key={key}
            className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100"
          >
            <div className="text-center p-8">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-orange-500 to-amber-500 mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl">⚡</span>
              </div>
              <h2 className="text-xl font-semibold text-gray-800 mb-2">
                Preview Ready
              </h2>
              <p className="text-gray-500 text-sm max-w-xs">
                Your dApp preview will appear here. Start by describing what you want to build in the chat.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
