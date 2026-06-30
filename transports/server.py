import os

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
    stateless_http=True,
)


# Add a simple calculator tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


# Run the server
# Switch transports without editing this file: TRANSPORT=sse python server.py
if __name__ == "__main__":
    transport = os.getenv("TRANSPORT", "stdio")
    if transport not in ("stdio", "sse", "streamable-http"):
        raise ValueError(f"Unknown transport: {transport}")

    print(f"Running server with {transport} transport")
    mcp.run(transport=transport)
