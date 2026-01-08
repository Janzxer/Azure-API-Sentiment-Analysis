import pandas as pd
import requests
from key_loader import API_KEY, AZURE_API_KEY, AZURE_END
from newsapi import NewsApiClient


#--- Configuration ----
SENTIMENT_URL = f"{AZURE_END}text/analytics/v3.0/sentiment"
HEADERS ={
    "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
    "Content-Type": "application/json"
}

def fetch_news_articles(topic = 'ai regulation', days_back = 7):
    newsapi = NewsApiClient(api_key = API_KEY)

    # To make this work, the start date would need to be calculated based on "days_back"
    all_articles = newsapi.get_everything(
        q = topic,
        language ='en',
        sort_by ='publishedAt',
        page_size = 20,
        page = 1
    )
    return all_articles.get("articles", [])

def parse_articles(articles):
    parsed_articles = []
    for idx, a in enumerate(articles, start =1):
        source = a.get("source") or {}
        parsed_articles.append({
            "id": str(idx), # ID is needed for azure matching
            "source_name": source.get("name") or "",
            "title": a.get("title") or "",
            "description": a.get("description") or "",
            "url": a.get("url") or "",
            "publishedAt": a.get("publishedAt") or "",
            "content": a.get("content") or "",
        })
    return parsed_articles

def chunk_data(items, size = 10):
    for i in range(0, len(items), size):
        yield items[i:i + size]

def analyze_sentiment(parsed_data):
    sentiment_map = {}
    
    documents = [{"id": item["id"], "language": "en", "text":item["title"]} for item in parsed_data]

    for chunk in chunk_data(documents):
        try:
            response = requests.post(SENTIMENT_URL, headers=HEADERS, json={"documents": chunk})
            response.raise_for_status()
            data = response.json()

            for item in data.get("documents", []):
                sentiment_map[item["id"]] = item["sentiment"]
        except Exception as e:
            print(f"Error connecting to Azure: {e}")
    return sentiment_map

def main():
    raw_articles = fetch_news_articles()

    if not raw_articles:
        print("No articles found.")
        return

    clean_articles = parse_articles(raw_articles)

    sentiment_results = analyze_sentiment(clean_articles)

    for article in clean_articles:
        article["title_sentiment"] = sentiment_results.get(article["id"], "N/A")
        print(f"{article['title'][:50]}... | {article['title_sentiment']}")

    df = pd.DataFrame(clean_articles)
    df = df[["title", "source_name", "title_sentiment", "url"]]
    df.to_excel("news_sentiment.xlsx", index=False)

if __name__ == "__main__":
    main()