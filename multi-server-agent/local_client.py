"""
Local MCP Servers
==================
Connects to 3 MCP servers that all run on YOUR machine, using 2 transports:

  math_server.py    → stdio              (local subprocess, no port)
  weather_server.py → streamable-http    (localhost:8000)
  kb_server.py      → streamable-http    (localhost:8001)

This is the baseline pattern: every server here is something you start and
own. Compare with remote_client.py in this same folder, which adds
third-party hosted servers (GitHub, Supabase) into the same client.

Run from the repo root:
  1. python demo-servers/weather_server.py        (terminal 1)
  2. python demo-servers/kb_server.py              (terminal 2)
  3. python multi-server-agent/local_client.py     (terminal 3)
"""

import asyncio
import os
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# ── Config ────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

MATH_SERVER_PATH = str(Path(__file__).parent.parent / "demo-servers" / "math_server.py")

# ── Queries to demo all three servers ─────────────────────
QUERIES = [
    # Uses math_server (stdio)
    "What is (7 + 3) raised to the power of 2, then divided by 5?",

    # Uses weather_server (local http)
    "Compare the weather in Delhi and London. Which is hotter?",

    # Uses kb_server (local http)
    "What is RAG and how does pgvector relate to it?",

    # Uses ALL THREE servers
    "Search knowledge base for MCP, then get Delhi weather, then calculate 38 + 15 * 2",
]


async def run_agent():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=OPENAI_API_KEY,
        temperature=0
    )

    # ── Connect to all 3 local servers ─────────────────────
    async with MultiServerMCPClient({

        # LOCAL — stdio, spawns a subprocess on your machine, no port
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": [MATH_SERVER_PATH],
        },

        # LOCAL HTTP — server already running on your machine
        "weather": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp",
        },

        # LOCAL HTTP — second server, same pattern
        "knowledge_base": {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp",
        },

    }) as client:

        # Auto-discover ALL tools from ALL servers
        tools = await client.get_tools()

        print("=" * 60)
        print("Connected MCP Servers & Tools Discovered:")
        print("=" * 60)
        for t in tools:
            print(f"  - {t.name:<30} {t.description[:50]}")
        print()

        # Build LangGraph ReAct agent with all tools
        agent = create_react_agent(llm, tools)

        # Run demo queries
        for i, query in enumerate(QUERIES, 1):
            print(f"{'=' * 60}")
            print(f"Query {i}: {query}")
            print("-" * 60)

            result = await agent.ainvoke({
                "messages": [{"role": "user", "content": query}]
            })

            # Print tool calls and final answer
            for msg in result["messages"]:
                if msg.type == "tool":
                    print(f"  Tool called: {msg.name}")
                    print(f"  Result: {str(msg.content)[:100]}")
                elif msg.type == "ai" and msg.content:
                    print(f"\n  Answer: {msg.content}")
            print()


if __name__ == "__main__":
    asyncio.run(run_agent())
