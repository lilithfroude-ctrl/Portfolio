"use client";

import { useEffect, useRef } from "react";

interface CodeEditorProps {
  file: string;
  content: string;
  onChange?: (content: string) => void;
  readOnly?: boolean;
}

export function CodeEditor({ 
  file, 
  content, 
  onChange,
  readOnly = false 
}: CodeEditorProps) {
  const editorRef = useRef<HTMLDivElement>(null);

  // In production, you'd use Monaco Editor here
  // For MVP, we'll use a simple textarea with syntax highlighting
  
  const getLanguage = (filename: string) => {
    if (filename.endsWith(".tsx") || filename.endsWith(".ts")) return "typescript";
    if (filename.endsWith(".jsx") || filename.endsWith(".js")) return "javascript";
    if (filename.endsWith(".css")) return "css";
    if (filename.endsWith(".json")) return "json";
    if (filename.endsWith(".md")) return "markdown";
    return "plaintext";
  };

  const language = getLanguage(file);

  return (
    <div className="flex-1 flex flex-col bg-[#1e1e1e] overflow-hidden">
      {/* File Tab */}
      <div className="h-10 bg-[#252526] border-b border-[#3c3c3c] flex items-center px-4">
        <span className="text-sm text-gray-300">{file}</span>
      </div>

      {/* Editor Content */}
      <div ref={editorRef} className="flex-1 overflow-auto p-4">
        <pre className="text-sm font-mono leading-relaxed">
          <code className={`language-${language}`}>
            {content.split("\n").map((line, i) => (
              <div key={i} className="flex">
                <span className="w-12 text-right pr-4 text-gray-600 select-none">
                  {i + 1}
                </span>
                <span className="text-gray-300">{line || " "}</span>
              </div>
            ))}
          </code>
        </pre>
      </div>
    </div>
  );
}
