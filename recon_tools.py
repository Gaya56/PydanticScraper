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

@mcp.tool()
async def check_ssl_certificate(domain: str) -> str:
    """Analyze SSL certificate details."""
    domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
    
    try:
        # Simple approach - just get the text output
        result = subprocess.run(
            f'echo | openssl s_client -connect {domain}:443 -servername {domain} 2>/dev/null | openssl x509 -noout -dates -subject -issuer',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout:
            output = f"SSL Certificate for {domain}:\n\n{result.stdout}"
            
            # Basic checks
            if 'notAfter=' in result.stdout:
                output += "\n✓ Valid certificate found"
            if 'Let\'s Encrypt' in result.stdout:
                output += "\n→ Free certificate (Let's Encrypt)"
                
            return output
        
        return f"No SSL certificate found for {domain} (may not support HTTPS)"
        
    except Exception as e:
        return f"Error checking SSL: {str(e)}"

if __name__ == "__main__":
    mcp.run()