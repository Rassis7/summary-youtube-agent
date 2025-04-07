import os
import requests
from dotenv import load_dotenv

load_dotenv()


def search_news(query, max_results=5):
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        print("🚨 News API Key not found")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": max_results,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("articles", [])
    else:
        print(f"🚨 Erro na busca de notícias: {response.content}")
        return []
