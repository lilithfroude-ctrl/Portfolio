"use client";

import { useState } from "react";
import { 
  ChevronRight, 
  ChevronDown, 
  File, 
  Folder,
  FolderOpen
} from "lucide-react";
import { cn } from "@/lib/utils";

interface FileTreeProps {
  files: string[];
  selectedFile: string;
  onSelectFile: (file: string) => void;
}

interface TreeNode {
  name: string;
  path: string;
  type: "file" | "folder";
  children?: TreeNode[];
}

export function FileTree({ files, selectedFile, onSelectFile }: FileTreeProps) {
  // Build tree structure from flat file list
  const buildTree = (files: string[]): TreeNode[] => {
    const root: TreeNode[] = [];
    
    files.forEach((filePath) => {
      const parts = filePath.split("/");
      let current = root;
      
      parts.forEach((part, index) => {
        const isFile = index === parts.length - 1;
        const existingNode = current.find((n) => n.name === part);
        
        if (existingNode) {
          if (!isFile && existingNode.children) {
            current = existingNode.children;
          }
        } else {
          const newNode: TreeNode = {
            name: part,
            path: parts.slice(0, index + 1).join("/"),
            type: isFile ? "file" : "folder",
            children: isFile ? undefined : [],
          };
          current.push(newNode);
          if (!isFile && newNode.children) {
            current = newNode.children;
          }
        }
      });
    });
    
    return root;
  };

  const tree = buildTree(files);

  return (
    <div className="w-60 border-r border-[#3c3c3c] bg-[#252526] overflow-y-auto">
      <div className="p-2 text-xs text-gray-500 uppercase tracking-wide">
        Explorer
      </div>
      <div className="px-2">
        {tree.map((node) => (
          <TreeNodeComponent
            key={node.path}
            node={node}
            selectedFile={selectedFile}
            onSelectFile={onSelectFile}
            depth={0}
          />
        ))}
      </div>
    </div>
  );
}

interface TreeNodeComponentProps {
  node: TreeNode;
  selectedFile: string;
  onSelectFile: (file: string) => void;
  depth: number;
}

function TreeNodeComponent({ 
  node, 
  selectedFile, 
  onSelectFile, 
  depth 
}: TreeNodeComponentProps) {
  const [isOpen, setIsOpen] = useState(true);
  const isSelected = node.type === "file" && node.path === selectedFile;
  
  const getFileIcon = (filename: string) => {
    if (filename.endsWith(".tsx") || filename.endsWith(".ts")) {
      return <span className="text-blue-400">TS</span>;
    }
    if (filename.endsWith(".css")) {
      return <span className="text-purple-400">#</span>;
    }
    if (filename.endsWith(".json")) {
      return <span className="text-yellow-400">{"{}"}</span>;
    }
    return <File className="w-4 h-4" />;
  };

  if (node.type === "folder") {
    return (
      <div>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center gap-1 py-1 px-2 hover:bg-[#2a2d2e] rounded text-sm text-gray-300"
          style={{ paddingLeft: `${depth * 12 + 8}px` }}
        >
          {isOpen ? (
            <ChevronDown className="w-4 h-4 text-gray-500" />
          ) : (
            <ChevronRight className="w-4 h-4 text-gray-500" />
          )}
          {isOpen ? (
            <FolderOpen className="w-4 h-4 text-yellow-500" />
          ) : (
            <Folder className="w-4 h-4 text-yellow-500" />
          )}
          <span>{node.name}</span>
        </button>
        
        {isOpen && node.children && (
          <div>
            {node.children.map((child) => (
              <TreeNodeComponent
                key={child.path}
                node={child}
                selectedFile={selectedFile}
                onSelectFile={onSelectFile}
                depth={depth + 1}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <button
      onClick={() => onSelectFile(node.path)}
      className={cn(
        "w-full flex items-center gap-2 py-1 px-2 rounded text-sm",
        isSelected 
          ? "bg-[#094771] text-white" 
          : "text-gray-300 hover:bg-[#2a2d2e]"
      )}
      style={{ paddingLeft: `${depth * 12 + 28}px` }}
    >
      <span className="w-4 h-4 flex items-center justify-center text-xs">
        {getFileIcon(node.name)}
      </span>
      <span>{node.name}</span>
    </button>
  );
}
