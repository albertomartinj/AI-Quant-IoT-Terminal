def calculate_price_drop(entry_price: float, current_price: float) -> float:
    """
    Calculates the percentage drop from the entry price to the current price.

    Args:
        entry_price (float): The initial purchase price of the asset.
        current_price (float): The latest market closing price.

    Returns:
        float: The percentage drop (e.g., 5.0 for a 5% drop). Returns 0.0 if price increased.
    """
    if current_price >= entry_price:
        return 0.0

    drop_pct = ((entry_price - current_price) / entry_price) * 100
    return round(drop_pct, 2)


def aggregate_sentiment(sentiment_results: list) -> str:
    """
    Determines the overall market sentiment from a list of FinBERT results.

    Args:
        sentiment_results (list): List of dictionaries containing 'Sentiment' and 'Confidence'.

    Returns:
        str: 'PANIC', 'POSITIVE', or 'NEUTRAL'.
    """
    if not sentiment_results:
        return 'NEUTRAL'

    # Count occurrences of each sentiment
    negatives = sum(1 for r in sentiment_results if r['Sentiment'] == 'Negative')
    positives = sum(1 for r in sentiment_results if r['Sentiment'] == 'Positive')

    total_news = len(sentiment_results)

    # If more than 50% of the news is negative, we declare PANIC
    if (negatives / total_news) >= 0.5:
        return 'PANIC'
    elif (positives / total_news) >= 0.5:
        return 'POSITIVE'
    else:
        return 'NEUTRAL'


def evaluate_trading_signal(asset_name: str, entry_price: float, current_price: float,
                            stop_loss_pct: float, sentiment_results: list) -> dict:
    """
    Cross-references price drops with NLP sentiment to generate a trading signal.

    Args:
        asset_name (str): Name or ticker of the asset.
        entry_price (float): Price at which the asset was bought.
        current_price (float): Latest market price.
        stop_loss_pct (float): The maximum allowed loss percentage before triggering an alert.
        sentiment_results (list): Recent news sentiment analyzed by FinBERT.

    Returns:
        dict: A dictionary containing the final action ('HOLD', 'SELL', 'MONITOR') and reasoning.
    """
    drop = calculate_price_drop(entry_price, current_price)
    overall_sentiment = aggregate_sentiment(sentiment_results)

    signal = 'HOLD'
    reasoning = f"Price drop ({drop}%) is within safe limits. Sentiment is {overall_sentiment}."

    # Logic Cross-Reference
    if drop >= stop_loss_pct:
        if overall_sentiment == 'PANIC':
            signal = 'SELL / TRIGGER IOT ALERT'
            reasoning = f"CRITICAL: Stop-loss breached ({drop}%) AND market is in PANIC mode."
        else:
            signal = 'MONITOR'
            reasoning = f"WARNING: Stop-loss breached ({drop}%), but news sentiment is {overall_sentiment}. Possible false breakdown."

    return {
        'Asset': asset_name,
        'Action': signal,
        'Reason': reasoning,
        'Drop_Pct': drop,
        'Sentiment': overall_sentiment
    }


if __name__ == "__main__":
    # --- Simulated Test for the Logic ---
    print("--- AI-Driven Quant Terminal: Logic Cross-Reference Test ---\n")

    # Simulated scenario: Bought an asset at $100, it dropped to $90 (10% drop). Stop-loss is 8%.
    simulated_sentiment = [
        {'Headline': 'Market crashes due to rate hikes', 'Sentiment': 'Negative', 'Confidence': 98.5},
        {'Headline': 'CEO resigns unexpectedly', 'Sentiment': 'Negative', 'Confidence': 95.0},
        {'Headline': 'Company announces new product', 'Sentiment': 'Positive', 'Confidence': 80.0}
    ]

    result = evaluate_trading_signal(
        asset_name="Tech ETF",
        entry_price=100.0,
        current_price=90.0,
        stop_loss_pct=8.0,
        sentiment_results=simulated_sentiment
    )

    print(f"Asset: {result['Asset']}")
    print(f"Current Drop: {result['Drop_Pct']}%")
    print(f"Market Sentiment: {result['Sentiment']}")
    print(f"--> RECOMMENDED ACTION: {result['Action']}")
    print(f"--> REASONING: {result['Reason']}")