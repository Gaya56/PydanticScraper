from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import requests
import json


load_dotenv(override=True)

# Initialize FastMCP
mcp = FastMCP(
    name="websearch", 
    version="1.0.0",
    description="Web search capability using Brave Search API"
)

# Initialize the Brave Search API
brave_api_key = os.getenv("BRAVE_API_KEY", "")
brave_search_url = "https://api.search.brave.com/res/v1/web/search"

# Default search configuration
websearch_config = {
    "parameters": {
        "default_num_results": 5,
        "include_domains": []
    }
}

@mcp.tool()
async def search_web(query: str, num_results: int = None) -> str:
    """Search the web using Brave Search API and return results as markdown formatted text."""
    try:
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": brave_api_key
        }
        
        params = {
            "q": query,
            "count": num_results or websearch_config["parameters"]["default_num_results"],
            "summary": 1,
            "freshness": "pw"  # past week for recent results
        }
        
        response = requests.get(brave_search_url, headers=headers, params=params)
        response.raise_for_status()
        
        search_results = response.json()
        return format_search_results(search_results)
    except Exception as e:
        return f"An error occurred while searching with Brave: {e}"

def format_search_results(search_results):
    web_results = search_results.get("web", {}).get("results", [])
    if not web_results:
        return "No results found."

    markdown_results = "### Search Results:\n\n"
    for idx, result in enumerate(web_results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        published_date = f" (Published: {result.get('age', '')})" if result.get('age') else ""
        
        markdown_results += f"**{idx}.** [{title}]({url}){published_date}\n"
        
        description = result.get("description", "")
        if description:
            markdown_results += f"> **Summary:** {description}\n\n"
        else:
            markdown_results += "\n"
    
    return markdown_results

if __name__ == "__main__":
    mcp.run()
