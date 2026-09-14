# Module 5: Computer Systems Security & Cryptography 🛡️

This module implements the "Defense in Depth" architecture for the AI-Driven Secure Quant & IoT Terminal. 

Unlike previous modules, Module 5 does not run as a standalone script. Instead, it is a **cross-cutting security layer** injected directly into the core orchestration (`main.py`) and the Web API (`server.js`).

## 🔐 Key Security Features Implemented

### 1. Secrets Management (.env & .gitignore)
- All hardcoded API keys (e.g., Hugging Face, News APIs) and cryptographic keys were purged from the source code.
- Implemented `dotenv` for dynamic, memory-only loading of secrets in both Python and Node.js environments.
- Deployed a strict `.gitignore` to prevent credential and database leaks to public Git repositories.

### 2. Data at Rest (AES-256-GCM Cryptography)
- Evaluated `SQLCipher` vs Application-Level Encryption, selecting the latter to guarantee cross-platform compatibility and avoid C++ compilation (node-gyp) errors on Windows.
- The Python orchestrator (`main.py`) uses the `cryptography` library to encrypt sensitive financial metrics using **AES-256-GCM** (with a 32-byte key) before executing the SQLite `INSERT`.
- The SQLite database (`quant_data.db`) now stores only secure, authenticated ciphertexts (Nonce + Ciphertext + Auth Tag).
- The Node.js API (`server.js`) utilizes the native `crypto` module to decrypt the data in real-time in memory before serving it to the React Dashboard.

### 3. Network Security (MITM Vulnerability Patch)
- Identified and patched a critical vulnerability: the use of `NODE_TLS_REJECT_UNAUTHORIZED=0` exposed the Node.js server to Man-in-the-Middle (MITM) attacks by disabling certificate validation.
- The system is now configured to securely route through restrictive networks (like university proxies) by explicitly trusting the root CA certificate via the `NODE_EXTRA_CA_CERTS` environment variable, restoring strict TLS verification.
