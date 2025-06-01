import os
import asyncio
from dotenv import load_dotenv # Add this import
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel

load_dotenv() # Call this at the beginning of your script

# Use model based on environment variable
model_type = os.getenv("AI_MODEL", "openai").lower()

if model_type == "claude":
    model = AnthropicModel(model_name="claude-3-opus-20240229")
elif model_type == "gemini":
    model = GoogleModel(model_name="gemini-1.5-flash")
elif model_type == "deepseek":
    model = OpenAIModel(
        model_name="deepseek-chat",
        base_url="https://api.deepseek.com/v1"
    )
else:
    model = OpenAIModel(model_name="gpt-4o-mini")

# Define the MCP Servers
brave_server = MCPServerStdio(
    'python',
    ['brave_search.py']
)

python_tools_server = MCPServerStdio(
    'python',
    ['python_tools.py']
)

recon_tools_server = MCPServerStdio(
    'python',
    ['recon_tools.py']
)

# Define the Agent with all MCP servers
agent = Agent(
    model, 
    mcp_servers=[brave_server, python_tools_server, recon_tools_server],
    retries=3,
    system_prompt="""You are a security analysis assistant. Before running any security tools, 
    ALWAYS ask for permission using this format:
    'I'll need to run [tool_name] on [target]. This will [brief description]. Continue? (y/n)'
    
    Wait for user confirmation before proceeding with tool execution."""
)

# Main async function
async def main():
    async with agent.run_mcp_servers():
        print("Web Recon Chatbot Ready! Type 'exit' to quit.\n")
        
        conversation = []
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            
            conversation.append({"role": "user", "content": user_input})
            
            # Include last 4 messages for context
            context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation[-4:]])
            
            result = await agent.run(f"Previous context:\n{context}\n\nCurrent message: {user_input}")
            print(f"\nBot: {result.output}\n")
            
            conversation.append({"role": "assistant", "content": result.output})

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())