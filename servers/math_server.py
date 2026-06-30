# ============================================================
# TRANSPORT 1: stdio
# Runs as a local subprocess — client spawns this process
# and communicates via stdin/stdout
# ============================================================

from fastmcp import FastMCP

mcp = FastMCP("MathExpert")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent"""
    return base ** exponent

if __name__ == "__main__":
    mcp.run(transport="stdio")  # <-- STDIO: reads from stdin, writes to stdout
