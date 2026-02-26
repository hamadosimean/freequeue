from tavily import TavilyClient
from general_settings.settings import env

# -----------------------------
# Load environment variables
# -----------------------------

TAVILY_API_KEY = env("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("Missing TAVILY_API_KEY in environment")


# -----------------------------
# Initialize Tavily client
# -----------------------------
tavily = TavilyClient(api_key=TAVILY_API_KEY)


# -----------------------------
# Web search using Tavily
# -----------------------------
def web_search(query: str, max_results: int = 8):
    """
    Search the web using Tavily and return the results.

    Args:
        query: search query
        max_results: maximum number of results

    Returns:
        List of results
    """

    response = tavily.search(
        query=query,
        search_depth="basic",
        max_results=max_results,
    )

    results = response.get("results", [])

    return results
