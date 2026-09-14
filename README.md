# 📈 AI-Driven Secure Quant & IoT Terminal

An end-to-end Algorithmic Trading and Risk Management platform that integrates financial data ingestion, AI-driven sentiment analysis, C-level hardware risk calculations, physical IoT alerts, and military-grade cryptography, all visualized through a real-time React Dashboard.

## 🚀 Project Architecture (The 5 Modules)

### 1. Data Ingestion & NLP (Artificial Intelligence)
- Fetches real-time financial market data (via Yahoo Finance).
- Uses **FinBERT** (a Hugging Face NLP model) to analyze breaking financial news and classify market sentiment as Positive, Negative, or Neutral.

### 2. Hardware Risk Engine (C-Level Acceleration)
- Calculates the portfolio's covariance matrix for risk assessment.
- Uses a **Python-to-C Bridge** to delegate heavy mathematical calculations to a low-level C engine, simulating hardware-accelerated High-Frequency Trading (HFT) environments.

### 3. IoT Physical Trigger (The Physical World)
- Translates digital trading signals into physical alerts.
- Evaluates critical market drops combined with negative AI sentiment to trigger physical hardware alarms (e.g., flashing LEDs via IoT protocols).

### 4. React & Node.js Dashboard (User Interface)
- A modern, accessible web interface acting as the visual control center.
- A Node.js backend serves an API consumed by a React frontend to display portfolio metrics, prices, and AI sentiment analysis in real-time.

### 5. Computer Systems Security (The Cryptographic Shield)
- **Secrets Management:** Implements `dotenv` to securely manage API keys and cryptographic secrets outside the source code.
- **Data at Rest:** Secures the SQLite database using Application-Level Encryption (**AES-256-GCM**). Sensitive metrics are encrypted in Python before storage and decrypted in Node.js on the fly.
- **Network Security:** Mitigates Man-in-the-Middle (MITM) vulnerabilities by strictly enforcing SSL/TLS certificate verification across network requests.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.x (with a virtual environment)
- Node.js & npm

### 1. Clone the repository and configure secrets
```bash
git clone https://github.com/albertomartinj/AI-Quant-IoT-Terminal.git
cd AI-Quant-IoT-Terminal
```
Create a `.env` file in the root directory (do not commit this file):
```env
NEWS_API_KEY=your_news_api_key_here
HF_TOKEN=your_huggingface_token_here
ENCRYPTION_KEY=your_32_byte_hex_encryption_key_here
```

### 2. Python Backend Setup
```bash
# Create and activate virtual environment (Linux/WSL example)
python3 -m venv wsl-env
source wsl-env/bin/activate

# Install dependencies
pip install python-dotenv cryptography
```

### 3. Node.js Frontend Setup
```bash
cd MODULE4-Dashboard
npm install
```

---

## 🖥️ Execution Guide

To run the terminal, you need to execute both the Backend (Python) and the Frontend (Node.js) concurrently.

### Terminal 1: Start the Quant Engine (Backend)
Activate your virtual environment and run the orchestrator:
```bash
source wsl-env/bin/activate
python main.py
```
> *Watch the console as the AI reads news, the C engine calculates risk, IoT alarms are evaluated, and data is encrypted to the SQLite database.*

### Terminal 2: Start the Dashboard (Frontend)
Open a new terminal, navigate to the Dashboard folder, and start the server:
```powershell
cd MODULE4-Dashboard
node server.js
```
> *The server will connect to the database, decrypt the data in memory, and listen on port 3000.*

### View Results
Open your web browser and navigate to:
👉 **`http://localhost:3000`**

---
*Developed as a comprehensive showcase of Software Engineering, Artificial Intelligence, Hardware Integration, Web Development, and Cybersecurity.*
