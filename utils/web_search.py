import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

def serpapi_search(query: str) -> list:
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return [res['title'] for res in results.get('organic_results', [])[:5]]
