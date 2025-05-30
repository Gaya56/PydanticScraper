# PydanticScraper

AI-driven web scraping using Pydantic AI + Model Context Protocol. Search the web and analyze data with simple Python commands.

## Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add API keys to .env
OPENAI_API_KEY='your-key'
BRAVE_API_KEY='your-key'

# Run
python3 app.py
```

## Files to Edit

| File | What it does | Quick edit |
|------|-------------|------------|
| `app.py` | Main application | Change the AI prompt/task |
| `brave_search.py` | Web search | Modify search parameters |
| `python_tools.py` | Data processing | Add new analysis tools |

## Customize Search (brave_search.py)

**Change results count:**
```python
# Line ~22
"default_num_results": 10,  # Change from 5 to 10
```

**Restrict to specific sites:**
```python
# Line ~23  
"include_domains": ["github.com", "reddit.com"]
```

**Add news-only search:**
```python
# Add new function
@mcp.tool()
async def search_news(query: str) -> str:
    # Uses news endpoint instead of web
```

## Switch Search Engines

- `brave_search.py` - Current (Brave Search)
- `Extra_Tools/exa_search.py` - Alternative (Exa Search)

To switch: Update `app.py` line 16-18 to point to different search file.

## 📝 Contributing

This framework is designed for extensibility. Consider adding:
- Additional search engines (Google, Bing, DuckDuckGo)
- Specialized data sources (academic papers, financial APIs)
- Advanced visualization tools
- Database integration capabilities
- Real-time monitoring and alerts

---

**Built with** [Pydantic AI](https://github.com/pydantic/pydantic-ai) and [Model Context Protocol](https://modelcontextprotocol.io/)
