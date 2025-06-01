from mcp.server.fastmcp import FastMCP
import subprocess
import json

mcp = FastMCP("recon_tools")

@mcp.tool()
async def check_security_headers(url: str) -> str:
    """Analyze website security headers using shcheck or curl."""
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        # Try shcheck first
        result = subprocess.run(
            ['python3', '-m', 'shcheck', '-j', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout:
            headers = json.loads(result.stdout)
            output = f"Security Header Analysis for {url}:\n\n"
            for header, status in headers.items():
                output += f"- {header}: {'✓ Present' if status else '✗ Missing'}\n"
            return output
    except:
        pass
    
    # Fallback to curl
    try:
        result = subprocess.run(
            ['curl', '-I', '-s', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return f"Headers for {url}:\n\n{result.stdout}"
        
        return f"Error fetching headers: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def detect_technologies(url: str) -> str:
    """Detect web technologies using webtech."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        result = subprocess.run(
            ['webtech', '-u', url, '--json'],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            tech_data = json.loads(result.stdout)
            output = f"Technologies detected on {url}:\n\n"
            
            for tech in tech_data.get('technologies', []):
                output += f"- {tech['name']} {tech.get('version', '')}\n"
            
            return output if tech_data.get('technologies') else f"No technologies detected on {url}"
        
        return f"Error analyzing {url}: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()