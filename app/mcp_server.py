from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

from app.agents.sql_agent import run_sql_agent
from app.agents.docs_agent import run_docs_agent
from app.graph import run_workflow


# ---------------------------------------------------------
# Create FastMCP server
# ---------------------------------------------------------
mcp = FastMCP(
    name="SupportAssistant",
    json_response=True,   # ensures clean JSON output for clients
)


# ---------------------------------------------------------
# SQL Agent Tool
# ---------------------------------------------------------
@mcp.tool()
def sql_agent(query: str) -> str:
    """
    Run the SQL agent on a natural-language query.
    """
    result = run_sql_agent(query)
    return result


# ---------------------------------------------------------
# Docs Agent Tool
# ---------------------------------------------------------
@mcp.tool()
def docs_agent(query: str) -> str:
    """
    Run the Docs agent (vectorstore retrieval + summary).
    """
    result = run_docs_agent(query)
    return result


# ---------------------------------------------------------
# Workflow Tool (LangGraph)
# ---------------------------------------------------------
@mcp.tool()
def workflow(query: str) -> str:
    """
    Run the full LangGraph workflow (router → SQL or Docs).
    """
    result = run_workflow(query)
    return result


# ---------------------------------------------------------
# Run server (HTTP transport recommended)
# ---------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="streamable-http")