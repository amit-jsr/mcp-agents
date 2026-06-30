# Multi-Server Agent

A LangGraph ReAct agent wired up via `langchain-mcp-adapters`, connected to multiple MCP servers at once. Two client variants, same servers underneath:

| File | Servers it connects to |
|---|---|
| `local_client.py` | `math` (stdio), `weather` + `knowledge_base` (local streamable-http) — everything runs on your machine |
| `remote_client.py` | The same 3 local servers, plus optional `github` and `supabase` MCP servers hosted by third parties (streamable-http + auth header) |

The point of `remote_client.py`: moving a server from "you run it" to "someone else hosts it" only changes the client config — `url` points at their endpoint instead of `localhost`, and you add an `Authorization` header. Nothing about tool discovery or invocation changes. The remote servers are optional and only get added if their token env var is set.

Backing servers (`math_server.py`, `weather_server.py`, `kb_server.py`) live in [../demo-servers](../demo-servers), shared by both clients here.

## Setup

Run from the repo root:

```bash
pip install -r demo-servers/requirements.txt
export OPENAI_API_KEY=sk-...
export GITHUB_TOKEN=ghp_...               # optional — enables the GitHub example in remote_client.py
export SUPABASE_ACCESS_TOKEN=...          # optional — enables the Supabase example in remote_client.py
```

## Run

Open 3 terminals from the repo root:

```bash
# Terminal 1
python demo-servers/weather_server.py

# Terminal 2
python demo-servers/kb_server.py

# Terminal 3 — math runs automatically via stdio
python multi-server-agent/local_client.py
# or
python multi-server-agent/remote_client.py
```
