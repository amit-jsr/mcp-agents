# MCP Multi-Transport Demo
> Minimal end-to-end project covering all 3 MCP transport modes with OpenAI + LangGraph

---

## What this covers

| Server | Transport | Why |
|---|---|---|
| `math_server.py` | **stdio** | Local subprocess, no port, spawned by client |
| `weather_server.py` | **streamable-http** | Deployed service, client hits URL |
| `kb_server.py` | **streamable-http** | Second HTTP server, same pattern |

---

## Project Structure

```
mcp-demo/
├── servers/
│   ├── math_server.py      # stdio transport
│   ├── weather_server.py   # http on port 8000
│   └── kb_server.py        # http on port 8001
├── client/
│   └── agent.py            # connects all 3, runs LangGraph agent
└── requirements.txt
```

---

## Setup

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

---

## Run

Open 3 terminals:

```bash
# Terminal 1 — HTTP server (weather)
python servers/weather_server.py

# Terminal 2 — HTTP server (knowledge base)
python servers/kb_server.py

# Terminal 3 — Client agent (math runs automatically via stdio)
python client/agent.py
```

---

## Key Concepts

### Transport 1: stdio
```python
"math": {
    "transport": "stdio",
    "command": "python",
    "args": ["servers/math_server.py"],
}
```
- Client **spawns the server as a subprocess**
- Communication via stdin/stdout pipes
- No port, no network — pure local
- Best for: local tools, CLI tools, scripts

### Transport 2: streamable-http
```python
"weather": {
    "transport": "streamable_http",
    "url": "http://localhost:8000/mcp",
}
```
- Server runs **independently** as an HTTP service
- Client hits it via URL
- Can be hosted anywhere (local, cloud, Docker)
- Best for: deployed services, remote tools, production

### Tool Discovery
```python
tools = await client.get_tools()
# Returns ALL tools from ALL servers automatically
# No manual tool definitions needed
```

---

## Interview Talking Points

1. **Why MCP?** — N×M → N+M integration problem (same as Kafka for data pipelines)
2. **Transport choice** — stdio for local/subprocess, streamable-http for deployed/remote
3. **Tool discovery** — automatic, no manual schema writing
4. **Multi-server** — one `MultiServerMCPClient` connects to unlimited servers
5. **Agent is separate from tools** — LangGraph agent doesn't care where tools come from
