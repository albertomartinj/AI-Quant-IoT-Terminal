"""
AI-Driven Secure Quant & IoT Terminal - Main Entry Point
Connects Module 1 (Financial Data/NLP) with Module 2 (C Hardware Acceleration).
"""
import os
import sys
import random

# Add MODEL2 to the Python path so we can import our C bridge
sys.path.append(os.path.join(os.path.dirname(__file__), 'MODEL2'))

try:
    from bridge import QuantCoreBridge
except ImportError:
    print("Error: Could not find 'bridge.py' in the MODEL2 directory.")
    sys.exit(1)

def get_module1_returns(assets: list, days: int) -> list:
    """
    Simulates Module 1 fetching historical returns via APIs (e.g., yfinance).
    TODO: Replace this mock function with your actual Module 1 API calls.
    """
    print(f"[Module 1] Fetching historical market data for {len(assets)} assets over {days} days...")
    
    # Generating mock daily returns between -2% and +2% for demonstration
    # The output is a 2D list: [asset_1_returns, asset_2_returns, ...]
    return [[random.uniform(-0.02, 0.02) for _ in range(days)] for _ in assets]

def main():
    print("=== AI-Driven Secure Quant Terminal ===")
    
    # 1. System Configuration
    portfolio_assets = ['AAPL', 'MSFT', 'GOOGL']
    historical_days = 252 # Typical number of trading days in a single year
    
    # 2. Data Ingestion (Module 1)
    returns_data = get_module1_returns(portfolio_assets, historical_days)
    num_assets = len(portfolio_assets)
    
    # 3. Initialize Hardware Acceleration Engine (Module 2)
    try:
        engine = QuantCoreBridge()
    except RuntimeError as e:
        print(f"\n[Hardware Engine Error]: {e}")
        print("Please ensure libquant_core.so is compiled in the MODEL2 folder.")
        return

    print("[Module 2] Delegating covariance calculations to C engine...")
    
    # 4. Execute Low-Level Risk Calculations
    cov_matrix = engine.get_covariance_matrix(returns_data, num_assets, historical_days)
    
    # 5. Display the Final System Output
    print("\n--- Portfolio Covariance Matrix (Hardware Accelerated) ---")
    for i, row in enumerate(cov_matrix):
        formatted_row = [f"{val:8.6f}" for val in row]
        print(f"{portfolio_assets[i]:<6} [{', '.join(formatted_row)}]")
        
    print("\nSystem execution completed successfully.")

if __name__ == "__main__":
    main()