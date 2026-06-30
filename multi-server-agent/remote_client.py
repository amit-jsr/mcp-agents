"""
Local + Remote MCP Servers Demo
================================
Connects to MCP servers using 3 transport patterns:

  math_server.py    → stdio                  (local subprocess)
  weather_server.py → streamable-http        (localhost:8000)
  kb_server.py      → streamable-http        (localhost:8001)
  GitHub MCP        → streamable-http REMOTE (api.githubcopilot.com, hosted by GitHub)
  Supabase MCP      → streamable-http REMOTE (mcp.supabase.com, hosted by Supabase)

Transport patterns:
  1. stdio       — client spawns server as subprocess, no port
  2. local http  — server runs on your machine, client hits localhost
  3. remote http — server hosted by a third party, client hits their URL + auth header

The first 3 servers are identical to local_client.py in this same folder —
this demo only adds the remote ones on top, so you can see exactly what
changes when a server moves from "you run it" to "someone else hosts it".

Run from the repo root:
  1. python demo-servers/weather_server.py        (terminal 1)
  2. python demo-servers/kb_server.py              (terminal 2)
  3. python multi-server-agent/remote_client.py    (terminal 3)

Env vars needed:
  OPENAI_API_KEY=sk-...
  GITHUB_TOKEN=ghp_...        (optional, enables the remote GitHub server)
  SUPABASE_ACCESS_TOKEN=...   (optional, enables the remote Supabase server)
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

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")                    # optional
SUPABASE_ACCESS_TOKEN = os.getenv("SUPABASE_ACCESS_TOKEN", "")  # optional
MATH_SERVER_PATH = str(Path(__file__).parent.parent / "demo-servers" / "math_server.py")

# ── Queries to demo all servers ───────────────────────────
DEMO_QUERIES = [
    # Uses math_server (stdio)
    "What is (7 + 3) raised to the power of 2, then divided by 5?",

    # Uses weather_server (local http)
    "Compare the weather in Delhi and London. Which is hotter?",

    # Uses kb_server (local http)
    "What is RAG and how does pgvector relate to it?",

    # Uses ALL local servers
    "Search knowledge base for MCP, then get Delhi weather, then calculate 38 + 15 * 2",

    # Uses the remote GitHub server (only runs if GITHUB_TOKEN is set)
    "List the top 3 repos in the octocat GitHub account",
]


async def run_agent():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=OPENAI_API_KEY,
        temperature=0
    )

    # ── Build server config ────────────────────────────────
    server_config = {

        # ── stdio ───────────────────────────────────────────
        # Client spawns math_server.py as a local subprocess.
        # No port. Communication via stdin/stdout pipes.
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": [MATH_SERVER_PATH],
        },

        # ── local streamable-http ───────────────────────────
        # Server runs independently on your machine (port 8000).
        "weather": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp",
        },

        # ── local streamable-http ───────────────────────────
        # Same pattern, second local server on port 8001.
        "knowledge_base": {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp",
        },
    }

    # ── remote streamable-http: GitHub ─────────────────────
    # Server is hosted by GitHub. Client hits their URL with an auth header.
    # You don't run this server — GitHub does.
    if GITHUB_TOKEN:
        server_config["github"] = {
            "transport": "streamable_http",
            "url": "https://api.githubcopilot.com/mcp/",
            "headers": {"Authorization": f"Bearer {GITHUB_TOKEN}"},
        }
        print("GitHub remote MCP server included")
    else:
        print("GITHUB_TOKEN not set — skipping remote GitHub server")
        print("  Set it to enable: export GITHUB_TOKEN=ghp_yourtoken")

    # ── remote streamable-http: Supabase ───────────────────
    # Server is hosted by Supabase. Same pattern as GitHub above.
    if SUPABASE_ACCESS_TOKEN:
        server_config["supabase"] = {
            "transport": "streamable_http",
            "url": "https://mcp.supabase.com/v1",
            "headers": {"Authorization": f"Bearer {SUPABASE_ACCESS_TOKEN}"},
        }
        print("Supabase remote MCP server included")
    else:
        print("SUPABASE_ACCESS_TOKEN not set — skipping remote Supabase server")
        print("  Set it to enable: export SUPABASE_ACCESS_TOKEN=your_token")
    print()

    # ── Connect to all configured servers ──────────────────
    async with MultiServerMCPClient(server_config) as client:

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

        # Run demo queries (the GitHub query only resolves if that server is connected)
        for i, query in enumerate(DEMO_QUERIES, 1):
            if "GitHub" in query and "github" not in server_config:
                continue

            print(f"{'=' * 60}")
            print(f"Query {i}: {query}")
            print("-" * 60)

            result = await agent.ainvoke({
                "messages": [{"role": "user", "content": query}]
            })

            for msg in result["messages"]:
                if msg.type == "tool":
                    print(f"  Tool called: {msg.name}")
                    print(f"  Result: {str(msg.content)[:100]}")
                elif msg.type == "ai" and msg.content:
                    print(f"\n  Answer: {msg.content}")
            print()


if __name__ == "__main__":
    asyncio.run(run_agent())
