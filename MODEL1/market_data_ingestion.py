import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_closing_prices(tickers: list, days_back: int = 7) -> pd.DataFrame:
    """
    Fetches the daily closing prices for a list of financial assets.

    Args:
        tickers (list): A list of ticker symbols (e.g., ['AAPL', 'GLD', 'URA']).
        days_back (int): Number of days to look back for historical data.

    Returns:
        pd.DataFrame: A DataFrame containing the 'Close' prices for the specified tickers.
    """
    # Calculate the date range
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days_back)

    # Format dates as strings for the API
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    print(f"Fetching data from {start_str} to {end_str}...\n")

    # Initialize an empty DataFrame to store the results
    prices_df = pd.DataFrame()

    for ticker in tickers:
        try:
            # Download data using yfinance
            asset_data = yf.download(ticker, start=start_str, end=end_str, progress=False)

            # Extract only the 'Close' column and rename it to the ticker symbol
            if not asset_data.empty:
                prices_df[ticker] = asset_data['Close']
                print(f"Successfully downloaded data for {ticker}")
            else:
                print(f"Warning: No data found for {ticker}")

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    # Drop any rows with NaN values (e.g., weekends or market holidays)
    prices_df.dropna(inplace=True)

    return prices_df


if __name__ == "__main__":
    # Test the function with a Tech Stock (Apple), a Commodity (Gold ETF), and a Uranium ETF
    # Note: Using GLD for Gold and URA for Uranium as standard ETF proxies
    target_assets = ['AAPL', 'GLD', 'URA']

    print("--- AI-Driven Quant Terminal: Data Ingestion Test ---")
    closing_prices = fetch_closing_prices(target_assets, days_back=14)

    print("\n--- Downloaded Closing Prices ---")
    print(closing_prices)