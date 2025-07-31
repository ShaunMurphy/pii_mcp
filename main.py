from fastmcp import FastMCP
from middleware import GuardrailsMiddleware
from orchestrator_plugin import register_tool

# Instantiate FastMCP server
mcp = FastMCP("PII Redacting Salesforce MCP Server")

# Register Guardrails Middleware
mcp.add_middleware(GuardrailsMiddleware())

# Register Orchestrator Plugin as a tool
register_tool(mcp)

# Demo/test tool for PII redaction
@mcp.tool
def demo_echo(input: str) -> dict:
    # Return a dict so the middleware can redact outgoing responses
    return {"result": input}

if __name__ == "__main__":
    # Use FastMCP's built-in HTTP server, not Uvicorn/FastAPI
    mcp.run(transport="http", host="127.0.0.1", port=8000)