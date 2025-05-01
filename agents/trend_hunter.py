from utils.web_search import serpapi_search

def fetch_trending_topics(niche: str) -> list:
    query = f"{niche} trends"
    return serpapi_search(query)

