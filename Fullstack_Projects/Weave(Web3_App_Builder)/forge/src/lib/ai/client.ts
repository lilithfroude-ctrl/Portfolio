// Forge AI Client - Handles communication with Claude
import Anthropic from "@anthropic-ai/sdk";
import { FORGE_SYSTEM_PROMPT, FORGE_TOOLS } from "./system-prompt";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY!,
});

export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface ToolCall {
  name: string;
  input: Record<string, unknown>;
}

export interface ForgeResponse {
  content: string;
  toolCalls: ToolCall[];
}

// Parse tool calls from Claude's response
function parseToolCalls(content: string): ToolCall[] {
  const toolCalls: ToolCall[] = [];
  
  // Parse forge-write blocks
  const writeRegex = /<forge-write path="([^"]+)">([\s\S]*?)<\/forge-write>/g;
  let match;
  while ((match = writeRegex.exec(content)) !== null) {
    toolCalls.push({
      name: "forge-write",
      input: { path: match[1], content: match[2].trim() }
    });
  }
  
  // Parse forge-delete blocks
  const deleteRegex = /<forge-delete path="([^"]+)"\s*\/>/g;
  while ((match = deleteRegex.exec(content)) !== null) {
    toolCalls.push({
      name: "forge-delete",
      input: { path: match[1] }
    });
  }
  
  // Parse forge-install blocks
  const installRegex = /<forge-install>([\s\S]*?)<\/forge-install>/g;
  while ((match = installRegex.exec(content)) !== null) {
    toolCalls.push({
      name: "forge-install",
      input: { package: match[1].trim() }
    });
  }
  
  // Parse forge-deploy blocks
  const deployRegex = /<forge-deploy\s+([\s\S]*?)\/>/g;
  while ((match = deployRegex.exec(content)) !== null) {
    const attrs = match[1];
    const input: Record<string, unknown> = {};
    
    // Parse attributes
    const attrRegex = /(\w+)=["']([^"']+)["']/g;
    let attrMatch;
    while ((attrMatch = attrRegex.exec(attrs)) !== null) {
      const key = attrMatch[1];
      let value: unknown = attrMatch[2];
      
      // Parse JSON for params
      if (key === "params") {
        try {
          value = JSON.parse(value as string);
        } catch {
          // Keep as string if not valid JSON
        }
      }
      input[key] = value;
    }
    
    toolCalls.push({
      name: "forge-deploy",
      input
    });
  }
  
  // Parse forge-wallet blocks
  const walletRegex = /<forge-wallet chain="([^"]+)"\s*\/>/g;
  while ((match = walletRegex.exec(content)) !== null) {
    toolCalls.push({
      name: "forge-wallet",
      input: { chain: match[1] }
    });
  }
  
  // Parse forge-fund blocks
  const fundRegex = /<forge-fund amount="([^"]+)" chain="([^"]+)"\s*\/>/g;
  while ((match = fundRegex.exec(content)) !== null) {
    toolCalls.push({
      name: "forge-fund",
      input: { amount: match[1], chain: match[2] }
    });
  }
  
  return toolCalls;
}

// Clean response content (remove tool tags for display)
function cleanContent(content: string): string {
  return content
    .replace(/<forge-write[\s\S]*?<\/forge-write>/g, "")
    .replace(/<forge-delete[^>]*\/>/g, "")
    .replace(/<forge-install>[\s\S]*?<\/forge-install>/g, "")
    .replace(/<forge-deploy[\s\S]*?\/>/g, "")
    .replace(/<forge-wallet[^>]*\/>/g, "")
    .replace(/<forge-fund[^>]*\/>/g, "")
    .replace(/<forge-verify[^>]*\/>/g, "")
    .trim();
}

export async function chat(
  messages: Message[],
  projectContext?: {
    files: Record<string, string>;
    chain: string;
    network: "mainnet" | "testnet";
    walletAddress?: string;
  }
): Promise<ForgeResponse> {
  // Build context string
  let contextAddition = "";
  
  if (projectContext) {
    contextAddition = `
<project_context>
Chain: ${projectContext.chain}
Network: ${projectContext.network}
${projectContext.walletAddress ? `Project Wallet: ${projectContext.walletAddress}` : "No project wallet created yet"}

Current Files:
${Object.keys(projectContext.files).map(f => `- ${f}`).join("\n")}
</project_context>
`;
  }
  
  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 8096,
    system: FORGE_SYSTEM_PROMPT + contextAddition,
    messages: messages.map(m => ({
      role: m.role,
      content: m.content
    }))
  });
  
  // Extract text content
  const textContent = response.content
    .filter(block => block.type === "text")
    .map(block => (block as { type: "text"; text: string }).text)
    .join("\n");
  
  // Parse tool calls from the response
  const toolCalls = parseToolCalls(textContent);
  
  // Clean content for display
  const cleanedContent = cleanContent(textContent);
  
  return {
    content: cleanedContent,
    toolCalls
  };
}

// Stream chat for real-time responses
export async function* streamChat(
  messages: Message[],
  projectContext?: {
    files: Record<string, string>;
    chain: string;
    network: "mainnet" | "testnet";
    walletAddress?: string;
  }
): AsyncGenerator<string> {
  let contextAddition = "";
  
  if (projectContext) {
    contextAddition = `
<project_context>
Chain: ${projectContext.chain}
Network: ${projectContext.network}
${projectContext.walletAddress ? `Project Wallet: ${projectContext.walletAddress}` : "No project wallet created yet"}

Current Files:
${Object.keys(projectContext.files).map(f => `- ${f}`).join("\n")}
</project_context>
`;
  }
  
  const stream = await anthropic.messages.stream({
    model: "claude-sonnet-4-20250514",
    max_tokens: 8096,
    system: FORGE_SYSTEM_PROMPT + contextAddition,
    messages: messages.map(m => ({
      role: m.role,
      content: m.content
    }))
  });
  
  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      yield event.delta.text;
    }
  }
}
