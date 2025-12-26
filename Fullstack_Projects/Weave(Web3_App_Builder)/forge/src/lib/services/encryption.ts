// Simple encryption for private keys
// In production, use AWS KMS, Google Cloud KMS, or similar
import crypto from "crypto";

const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || crypto.randomBytes(32).toString("hex");
const ALGORITHM = "aes-256-gcm";

// For production, this should use a proper KMS service
// This is a simple implementation for development
export function encryptPrivateKey(privateKey: string): string {
  try {
    // In production, use AWS KMS or similar
    // For now, use a simple encryption with a key derived from ENV
    const key = crypto.scryptSync(ENCRYPTION_KEY, "salt", 32);
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv("aes-256-cbc", key, iv);
    
    let encrypted = cipher.update(privateKey, "utf8", "hex");
    encrypted += cipher.final("hex");
    
    // Return IV + encrypted data
    return iv.toString("hex") + ":" + encrypted;
  } catch (error) {
    console.error("Encryption error:", error);
    throw new Error("Failed to encrypt private key");
  }
}

export function decryptPrivateKey(encryptedKey: string): string {
  try {
    const [ivHex, encrypted] = encryptedKey.split(":");
    if (!ivHex || !encrypted) {
      throw new Error("Invalid encrypted key format");
    }
    
    const key = crypto.scryptSync(ENCRYPTION_KEY, "salt", 32);
    const iv = Buffer.from(ivHex, "hex");
    const decipher = crypto.createDecipheriv("aes-256-cbc", key, iv);
    
    let decrypted = decipher.update(encrypted, "hex", "utf8");
    decrypted += decipher.final("utf8");
    
    return decrypted;
  } catch (error) {
    console.error("Decryption error:", error);
    throw new Error("Failed to decrypt private key");
  }
}

