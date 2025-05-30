from mcp.server.fastmcp import FastMCP
import io
import base64
import matplotlib.pyplot as plt
import sys
from io import StringIO
import traceback

mcp = FastMCP("python_tools")

class PythonREPL:
    def run(self, code):
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        try:
            exec(code, globals())
            sys.stdout = old_stdout
            return redirected_output.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            return f"Error: {str(e)}\n{traceback.format_exc()}"

repl = PythonREPL()

@mcp.tool()
async def python_repl(code: str) -> str:
    """Execute Python code."""
    return repl.run(code)

@mcp.tool()
async def data_visualization(code: str) -> str:
    """Execute Python code. Use matplotlib for visualization."""
    try:
        repl.run(code)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode()
        plt.close()  # Close the figure to free memory
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        return f"Error creating chart: {str(e)}"

if __name__ == "__main__":
    mcp.run()