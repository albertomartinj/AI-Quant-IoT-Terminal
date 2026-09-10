import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


def fetch_financial_news(query: str, api_key: str, limit: int = 5) -> list:
    """
    Fetches recent news headlines for a specific financial query using NewsAPI.

    Args:
        query (str): The keyword to search for (e.g., 'Apple', 'Uranium').
        api_key (str): Your NewsAPI key.
        limit (int): Maximum number of headlines to return.

    Returns:
        list: A list of string headlines.
    """
    # NewsAPI endpoint for everything matching the query, sorted by recency
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize={limit}&apiKey={api_key}"

    print(f"Fetching recent news for '{query}'...")
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        # Extract just the titles from the JSON response
        headlines = [article['title'] for article in articles if article['title']]
        return headlines
    else:
        print(f"Error fetching news: HTTP {response.status_code}")
        return []


def analyze_headlines_sentiment(headlines: list) -> list:
    """
    Analyzes the sentiment of a list of financial headlines using FinBERT.

    Args:
        headlines (list): A list of news headlines.

    Returns:
        list: A list of dictionaries containing the headline, sentiment label, and confidence score.
    """
    if not headlines:
        return []

    print("Loading FinBERT model (this might take a moment on the first run)...\n")

    # Load the pre-trained FinBERT tokenizer and model from Hugging Face
    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    results = []

    # Process each headline
    for headline in headlines:
        # Tokenize the text and convert to PyTorch tensors
        inputs = tokenizer(headline, return_tensors="pt", padding=True, truncation=True)

        # Disable gradient calculation for faster inference (we are not training)
        with torch.no_grad():
            outputs = model(**inputs)

        # Get the predicted class index (0: positive, 1: negative, 2: neutral)
        prediction_idx = torch.argmax(outputs.logits, dim=-1).item()

        # Map the index to the corresponding label
        labels = ['Positive', 'Negative', 'Neutral']
        sentiment = labels[prediction_idx]

        # Calculate confidence score using softmax
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        confidence = probabilities[0][prediction_idx].item()

        results.append({
            'Headline': headline,
            'Sentiment': sentiment,
            'Confidence': round(confidence * 100, 2)
        })

    return results


if __name__ == "__main__":
    # IMPORTANT: Replace this placeholder with your actual NewsAPI key
    fb65f574de0846318e071fa3c9dcfd37 = "YOUR_API_KEY_HERE"

    target_asset = "Apple stock"

    print("--- AI-Driven Quant Terminal: Sentiment Analysis Test ---")

    # 1. Fetch the news
    latest_headlines = fetch_financial_news(target_asset, fb65f574de0846318e071fa3c9dcfd37)

    # 2. Analyze the sentiment
    if latest_headlines:
        sentiment_results = analyze_headlines_sentiment(latest_headlines)

        print(f"--- FinBERT Sentiment Results for '{target_asset}' ---")
        for idx, result in enumerate(sentiment_results, 1):
            print(f"\n{idx}. {result['Headline']}")
            print(f"   => {result['Sentiment']} (Confidence: {result['Confidence']}%)")
    else:
        print("No headlines to analyze. Please check your API key.")