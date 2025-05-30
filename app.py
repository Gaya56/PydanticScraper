import os
import asyncio
from dotenv import load_dotenv # Add this import
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel

load_dotenv() # Call this at the beginning of your script

# Set OpenAI environment variables to use DeepSeek
os.environ["OPENAI_API_KEY"] = os.environ["DEEPSEEK_API_KEY"]
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"

deepseek_chat_model = OpenAIModel( #define the base as open AI
    model_name="deepseek-v3.1" # use the deepseek model and correct parameter name
)

# Define the MCP Servers
brave_server = MCPServerStdio(
    'python',
    ['brave_search.py']
)

python_tools_server = MCPServerStdio(
    'python',
    ['python_tools.py']
)

# Define the Agent with both MCP servers
agent = Agent(
    deepseek_chat_model, 
    mcp_servers=[brave_server, python_tools_server],
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