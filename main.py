"""
AI-Driven Secure Quant & IoT Terminal - Main Master Orchestrator
Coordinates Module 1 (Data/NLP), Module 2 (C Math), Module 3 (IoT), and Module 4 (Dashboard DB).
"""
import os
import sys
import sqlite3
from datetime import datetime, timezone
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Load environment variables
load_dotenv()

# Setup Encryption (AES-256-GCM)
encryption_key_hex = os.getenv("ENCRYPTION_KEY")
if not encryption_key_hex:
    raise ValueError("CRITICAL: ENCRYPTION_KEY missing in .env file.")
encryption_key = bytes.fromhex(encryption_key_hex)
aesgcm = AESGCM(encryption_key)

def encrypt_data(data_str):
    """Encrypts a string using AES-256-GCM with a random nonce."""
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data_str.encode('utf-8'), None)
    return (nonce + ciphertext).hex()

# Add submodules to Python path so we can import them
sys.path.append(os.path.join(os.path.dirname(__file__), 'MODEL1'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'MODEL2'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'MODULE3'))

# Import Module 1 components (Data & NLP)
from market_data_ingestion import fetch_closing_prices
from news_sentiment import fetch_financial_news, analyze_headlines_sentiment
from trading_logic import evaluate_trading_signal

# Import Module 2 component (Hardware Risk Engine)
try:
    from bridge import QuantCoreBridge
except ImportError:
    QuantCoreBridge = None
    print("Warning: Could not find 'bridge.py' in the MODEL2 directory. Proceeding without hardware acceleration.")

# Import Module 3 component (IoT Trigger)
try:
    from iot_trigger import trigger_physical_alarm
except ImportError:
    def trigger_physical_alarm(asset, action, severity): pass

# Database path for Module 4 (React Dashboard)
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'quant_data.db'))

def save_to_dashboard_db(asset, current_price, entry_price, stop_loss_pct, sentiment_label, action_signal, severity):
    """
    Saves the processed metrics into SQLite for the Node.js API (Module 4) to consume in real-time.
    """
    current_time = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        # Encrypt sensitive financial metrics
        encrypted_current_price = encrypt_data(str(current_price))
        encrypted_entry_price = encrypt_data(str(entry_price))
        encrypted_stop_loss = encrypt_data(str(stop_loss_pct))
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO portfolio_metrics (
                timestamp, asset_symbol, current_price, entry_price, 
                stop_loss_threshold, sentiment_label, action_signal, alert_severity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            current_time, asset, encrypted_current_price, encrypted_entry_price,
            encrypted_stop_loss, sentiment_label, action_signal, severity
        ))
        conn.commit()
        conn.close()
        print(f"[Module 4] 💾 Saved encrypted {asset} metrics to quant_data.db for UI Dashboard.")
    except Exception as e:
        print(f"[Module 4 Error] Could not save {asset} data to database: {e}")

def main():
    print("="*60)
    print("🛡️  AI-Driven Secure Quant Terminal - Master Pipeline 🛡️")
    print("="*60)
    
    # 1. System Configuration
    portfolio = {
        'AAPL': {'entry_price': 330.00, 'stop_loss_pct': 5.0},
        'GLD': {'entry_price': 375.00, 'stop_loss_pct': 3.0},
        'URA': {'entry_price': 42.00, 'stop_loss_pct': 8.0}
    }
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        print("Warning: NEWS_API_KEY not found in .env. Sentiment analysis may fail.")
        NEWS_API_KEY = "dummy_key_if_none"
    
    target_tickers = list(portfolio.keys())
    historical_days = 252
    
    # ---------------------------------------------------------
    # MODULE 1: Data Ingestion
    # ---------------------------------------------------------
    print("\n>>> [MODULE 1] Fetching Market Prices...")
    # Using 10 days back to ensure we hit trading days even on weekends
    latest_prices_df = fetch_closing_prices(target_tickers, days_back=10)
    
    if latest_prices_df.empty:
        print("CRITICAL ERROR: No market data retrieved. Network/Proxy might be blocking.")
        return

    # Extract historical matrix for Module 2 and latest prices for logic
    returns_matrix = [latest_prices_df[ticker].pct_change().dropna().tolist() for ticker in target_tickers]
    current_prices = latest_prices_df.iloc[-1]
    
    # ---------------------------------------------------------
    # MODULE 2: Hardware Acceleration Risk Engine
    # ---------------------------------------------------------
    print("\n>>> [MODULE 2] Initializing C-Level Hardware Risk Engine...")
    if QuantCoreBridge:
        try:
            engine = QuantCoreBridge()
            # Feed real downloaded data to C Engine instead of mock data
            num_assets = len(target_tickers)
            # The C engine expects arrays of length 'historical_days'. 
            # We downloaded 10 days, so we pass the exact length we have.
            actual_days = len(returns_matrix[0])
            print(f"Delegating covariance calculations for {num_assets} assets over {actual_days} days to C engine...")
            
            cov_matrix = engine.get_covariance_matrix(returns_matrix, num_assets, actual_days)
            
            print("\n--- Portfolio Covariance Matrix (Hardware Accelerated) ---")
            for i, row in enumerate(cov_matrix):
                formatted_row = [f"{val:8.6f}" for val in row]
                print(f"{target_tickers[i]:<6} [{', '.join(formatted_row)}]")
        except Exception as e:
            print(f"[Module 2 Error]: {e}. Proceeding without hardware math.")
    else:
        print("Module 2 skipped.")

    # ---------------------------------------------------------
    # MODULE 1 & 3 & 4: NLP, Logic, IoT, and Dashboard
    # ---------------------------------------------------------
    print("\n>>> [MODULE 1, 3, 4] Analyzing Sentiment, Logic, and Broadcasting...\n")
    for asset in target_tickers:
        print(f"--- Analyzing {asset} ---")
        
        entry_price = portfolio[asset]['entry_price']
        current_price = current_prices[asset]
        stop_loss_pct = portfolio[asset]['stop_loss_pct']

        # FinBERT Sentiment
        print(f"[Module 1] Fetching NLP news sentiment for {asset}...")
        headlines = fetch_financial_news(query=asset, api_key=NEWS_API_KEY, limit=5)
        sentiment_results = analyze_headlines_sentiment(headlines)

        # Cross-reference price and sentiment
        signal_report = evaluate_trading_signal(
            asset_name=asset,
            entry_price=entry_price,
            current_price=current_price,
            stop_loss_pct=stop_loss_pct,
            sentiment_results=sentiment_results
        )

        action = signal_report['Action']
        sentiment_label = signal_report['Sentiment']
        print(f"-> SIGNAL: {action} (Reason: {signal_report['Reason']})")

        # Determine Severity
        severity = 'CRITICAL' if 'TRIGGER' in action else ('WARNING' if action != 'HOLD' else 'NORMAL')

        # MODULE 3: IoT Physical Trigger
        trigger_physical_alarm(asset, action, severity)

        # MODULE 4: Save to Dashboard Database
        save_to_dashboard_db(
            asset=asset, 
            current_price=current_price, 
            entry_price=entry_price, 
            stop_loss_pct=stop_loss_pct, 
            sentiment_label=sentiment_label, 
            action_signal=action, 
            severity=severity
        )
        print("")

    print("="*60)
    print("✅ System execution completed successfully. Pipeline sealed.")
    print("="*60)

if __name__ == "__main__":
    main()