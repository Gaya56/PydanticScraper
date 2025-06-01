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
    
    Wait for user confirmation before proceeding with tool execution.
    
    When asked about a domain, FIRST check 'Previous findings' in the context before using any tools. 
    Only search or run new tools if no previous data exists."""
)

# Main async function
async def main():
    async with agent.run_mcp_servers():
        print("Web Recon Chatbot Ready! Type 'exit' to quit.\n")
        
        conversation = []
        findings = {}  # Store findings by domain
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            
            conversation.append({"role": "user", "content": user_input})
            
            # Include findings in context
            findings_summary = "\n".join([f"{domain}: {info}" for domain, info in findings.items()])
            context = f"Previous findings:\n{findings_summary}\n\nRecent messages:\n"
            context += "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation[-4:]])
            
            result = await agent.run(f"{context}\n\nCurrent message: {user_input}")
            print(f"\nBot: {result.output}\n")
            
            # Extract domain and update findings (simple pattern matching)
            if "Headers for" in result.output or "Security Header Analysis" in result.output:
                import re
                domain_match = re.search(r'headers for `?(?:https?://)?([a-zA-Z0-9.-]+)`?', result.output, re.IGNORECASE)
                if domain_match:
                    domain = domain_match.group(1)
                    findings[domain] = findings.get(domain, "") + f"Headers checked (HSTS, CSP, etc). "
            
            conversation.append({"role": "assistant", "content": result.output})

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())