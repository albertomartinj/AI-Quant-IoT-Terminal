"""
Main pipeline execution script for the AI-Driven Secure Quant & IoT Terminal.
Orchestrates data ingestion, sentiment analysis, and trading logic.
"""

# Import the modules we created
from MODEL1.market_data_ingestion import fetch_closing_prices
from MODEL1.news_sentiment import fetch_financial_news, analyze_headlines_sentiment
from MODEL1.trading_logic import evaluate_trading_signal

import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../quant_data.db'))


def run_quant_pipeline():
    """
    Executes the main ETL and analysis pipeline.
    1. Fetches market data.
    2. Fetches and analyzes news sentiment.
    3. Cross-references data to generate actionable trading signals.
    """
    # 1. Configuration and Portfolio Setup
    # Simulating our portfolio with entry prices and stop-loss limits
    portfolio = {
        'AAPL': {'entry_price': 330.00, 'stop_loss_pct': 5.0},
        'GLD': {'entry_price': 375.00, 'stop_loss_pct': 3.0},
        'URA': {'entry_price': 42.00, 'stop_loss_pct': 8.0}
    }

    # IMPORTANT: Insert your actual NewsAPI key here
    NEWS_API_KEY = "fb65f574de0846318e071fa3c9dcfd37"

    print("=== STARTING QUANT PIPELINE RUN ===\n")

    # 2. Extract Market Data
    target_tickers = list(portfolio.keys())
    print(">>> STEP 1: Fetching Market Prices...")
    latest_prices_df = fetch_closing_prices(target_tickers, days_back=7)

    # Check if we got data successfully
    if latest_prices_df.empty:
        print("CRITICAL ERROR: No market data retrieved. Aborting pipeline.")
        return

    # Get the most recent closing prices (the last row of the DataFrame)
    current_prices = latest_prices_df.iloc[-1]
    print("\nLatest Closing Prices:")
    print(current_prices)
    print("\n" + "-" * 40 + "\n")

    # 3. Process Each Asset in the Portfolio
    print(">>> STEP 2 & 3: Analyzing Sentiment and Generating Signals...\n")

    for asset in target_tickers:
        print(f"Analyzing {asset}...")

        entry_price = portfolio[asset]['entry_price']
        current_price = current_prices[asset]
        stop_loss_pct = portfolio[asset]['stop_loss_pct']

        # Fetch news and calculate sentiment
        headlines = fetch_financial_news(query=asset, api_key=NEWS_API_KEY, limit=5)
        sentiment_results = analyze_headlines_sentiment(headlines)

        # Cross-reference price and sentiment using our logic engine
        signal_report = evaluate_trading_signal(
            asset_name=asset,
            entry_price=entry_price,
            current_price=current_price,
            stop_loss_pct=stop_loss_pct,
            sentiment_results=sentiment_results
        )

        # 4. Output the Final Decision
        print(f"[{asset}] SIGNAL: {signal_report['Action']}")
        print(f"[{asset}] REASON: {signal_report['Reason']}\n")
        
        # 5. Save to Dashboard Database
        current_time = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        severity = 'CRITICAL' if 'TRIGGER' in signal_report['Action'] else ('WARNING' if signal_report['Action'] != 'HOLD' else 'NORMAL')
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO portfolio_metrics (
                    timestamp, asset_symbol, current_price, entry_price, 
                    stop_loss_threshold, sentiment_label, action_signal, alert_severity
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                current_time,
                asset,
                float(current_price),
                float(entry_price),
                float(stop_loss_pct),
                signal_report['Sentiment'],
                signal_report['Action'],
                severity
            ))
            conn.commit()
            conn.close()
            print(f"[DB] Saved {asset} metrics to quant_data.db")
        except Exception as e:
            print(f"[DB Error] Could not save {asset} data: {e}")


if __name__ == "__main__":
    run_quant_pipeline()