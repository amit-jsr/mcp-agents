# MCP Playground

A working reference for building MCP (Model Context Protocol) servers and clients in Python — transports, OpenAI tool-calling integration, a function-calling comparison, Docker deployment, a real-world server example, and multi-server agent orchestration across local and remote MCP servers.

Background concepts (architecture, primitives, lifecycle, MCP vs. plain function calling) live in [docs/CONCEPTS.md](./docs/CONCEPTS.md). This README covers setup and points at the runnable code.

## Layout

Read in this order:

| # | Path | What it shows |
|---|---|---|
| 1 | [docs/CONCEPTS.md](./docs/CONCEPTS.md) | Architecture, transports, primitives, MCP vs. function calling, lifecycle management |
| 2 | [transports/](./transports) | A minimal server + client for each MCP transport: `stdio`, `sse`, `streamable-http` |
| 3 | [openai-integration/](./openai-integration) | A real OpenAI tool-calling loop backed by an MCP server (knowledge-base example) |
| 4 | [function-calling/](./function-calling) | The same knowledge-base tool, implemented as plain OpenAI function calling instead of MCP — for contrast |
| 5 | [docker/](./docker) | Packaging an MCP server + client into containers |
| 6 | [server/youtube/](./server/youtube) | A complete, production-shaped MCP server (YouTube transcript fetcher) |
| 7 | [multi-server-agent/local_client.py](./multi-server-agent/local_client.py) | A LangGraph agent connected to multiple MCP servers you run yourself (stdio + local HTTP) |
| 8 | [multi-server-agent/remote_client.py](./multi-server-agent/remote_client.py) | The same agent extended with MCP servers hosted by a third party (GitHub, Supabase) |

Both clients share their backing servers from [demo-servers/](./demo-servers) rather than each keeping a copy.

## Setup

```bash
python3 -m venv _venv
source _venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in OPENAI_API_KEY
```

## MCP CLI

The Python SDK ships CLI helpers useful during development:

```bash
mcp dev server.py        # run a server against the MCP Inspector (web UI)
mcp install server.py    # register a server with Claude Desktop
mcp run server.py        # run a server directly
```

## Next steps

- [Model Context Protocol docs](https://modelcontextprotocol.io)
- [MCP specification](https://spec.modelcontextprotocol.io)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Officially supported servers](https://github.com/modelcontextprotocol/servers)
