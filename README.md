# Pydantic AI + MCP Web Scraping Framework

**Current WebReconBot Status:** The chatbot successfully implements multi-AI support (OpenAI/Claude/Gemini), interactive chat with permission prompts, and domain-based memory that tracks previous findings. The header analysis tool uses curl fallback when shcheck fails, as shown by the test.com timeout. The bot correctly remembered example.com was already analyzed and avoided redundant checks. Core framework is operational with brave_search.py for web queries, python_tools.py for data processing, and recon_tools.py for security analysis. Memory persistence and permission system both work as designed.

