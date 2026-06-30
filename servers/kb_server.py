# ============================================================
# TRANSPORT 2b: streamable-http (second HTTP server, port 8001)
# Simulates a "Knowledge Base" domain expert
# Start with: python kb_server.py
# Runs on: http://localhost:8001/mcp
# ============================================================

from fastmcp import FastMCP

mcp = FastMCP("KnowledgeBaseExpert")

# Simulated knowledge base
KB = {
    "mcp": "Model Context Protocol is an open standard by Anthropic that connects LLMs to external tools via a client-server architecture.",
    "langgraph": "LangGraph is a framework for building stateful, multi-actor agentic systems using a graph-based approach.",
    "rag": "Retrieval Augmented Generation combines vector search with LLM generation to answer questions from a knowledge base.",
    "fastapi": "FastAPI is a modern Python web framework for building APIs with automatic OpenAPI docs and high performance.",
    "pgvector": "pgvector is a Postgres extension for storing and querying vector embeddings, enabling semantic search.",
    "langsmith": "LangSmith is an observability platform for tracing, evaluating and monitoring LLM applications.",
}

@mcp.tool()
def search_knowledge(query: str) -> str:
    """Search the knowledge base for a topic"""
    query_lower = query.lower()
    results = []
    for key, value in KB.items():
        if key in query_lower or query_lower in key:
            results.append(f"[{key.upper()}]: {value}")
    if results:
        return "\n\n".join(results)
    return f"No knowledge found for '{query}'. Available topics: {', '.join(KB.keys())}"

@mcp.tool()
def list_topics() -> list:
    """List all available topics in the knowledge base"""
    return list(KB.keys())

@mcp.tool()
def add_knowledge(topic: str, content: str) -> str:
    """Add a new topic to the knowledge base"""
    KB[topic.lower()] = content
    return f"Added topic '{topic}' to knowledge base"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)
