from mcp.server.fastmcp import FastMCP
import subprocess
import json

mcp = FastMCP("recon_tools")

@mcp.tool()
async def check_security_headers(url: str) -> str:
    """Analyze website security headers using shcheck."""
    try:
        # Run shcheck with JSON output
        result = subprocess.run(
            ['shcheck', '-j', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return f"Error running shcheck: {result.stderr}"
        
        # Parse JSON output
        headers = json.loads(result.stdout)
        
        # Format results for AI interpretation
        output = f"Security Header Analysis for {url}:\n\n"
        for header, status in headers.items():
            output += f"- {header}: {'✓ Present' if status else '✗ Missing'}\n"
        
        return output
    except Exception as e:
        return f"Error analyzing headers: {str(e)}"

if __name__ == "__main__":
    mcp.run()