import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

deepseek_chat_model = OpenAIModel( #define the base as open AI
    'deepseek-chat',
    base_url='https://api.deepseek.com',
    api_key=os.environ["DEEPSEEK_API_KEY"],
)

# Define the MCP Servers
exa_server = MCPServerStdio(
    'python',
    ['exa_search.py']
)

python_tools_server = MCPServerStdio(
    'python',
    ['python_tools.py']
)

# Define the Agent with both MCP servers
agent = Agent(
    deepseek_chat_model, 
    mcp_servers=[exa_server, python_tools_server],
    retries=3
)

# Main async function
async def main():
    async with agent.run_mcp_servers():
        result = await agent.run("""
        I need to analyze some climate data. First, search for recent climate change statistics.
        Then, create a bar chart showing the increase in global temperature over the last decade.
        Use Python for the data visualization.
        """)
        print(result)

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())