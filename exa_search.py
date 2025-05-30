from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from exa_py import Exa


load_dotenv(override=True)

# Initialize FastMCP
mcp = FastMCP(
    name="websearch", 
    version="1.0.0",
    description="Web search capability using Exa API"
)

# Initialize the Exa client
exa_api_key = os.getenv("EXA_API_KEY", "")
exa = Exa(api_key=exa_api_key)

# Default search configuration
websearch_config = {
    "parameters": {
        "default_num_results": 5,
        "include_domains": []
    }
}

@mcp.tool()
async def search_web(query: str, num_results: int = None) -> str:
    """Search the web using Exa API and return results as markdown formatted text."""
    try:
        search_args = {
            "num_results": num_results or websearch_config["parameters"]["default_num_results"]
        }
        
        search_results = exa.search_and_contents(
            query, 
            summary={"query": "Main points and key takeaways"},
            **search_args
        )
        
        return format_search_results(search_results)
    except Exception as e:
        return f"An error occurred while searching with Exa: {e}"

def format_search_results(search_results):
    if not search_results.results:
        return "No results found."

    markdown_results = "### Search Results:\n\n"
    for idx, result in enumerate(search_results.results, 1):
        title = result.title if hasattr(result, 'title') and result.title else "No title"
        url = result.url
        published_date = f" (Published: {result.published_date})" if hasattr(result, 'published_date') and result.published_date else ""
        
        markdown_results += f"**{idx}.** [{title}]({url}){published_date}\n"
        
        if hasattr(result, 'summary') and result.summary:
            markdown_results += f"> **Summary:** {result.summary}\n\n"
        else:
            markdown_results += "\n"
    
    return markdown_results

if __name__ == "__main__":
    mcp.run()