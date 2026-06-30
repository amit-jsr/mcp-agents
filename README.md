# MCP Playground

A working reference for building MCP (Model Context Protocol) servers and clients in Python — transports, OpenAI tool-calling integration, a function-calling comparison, and Docker deployment.

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
