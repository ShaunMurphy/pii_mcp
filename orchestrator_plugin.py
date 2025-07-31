# No longer using FastAPI or Plugin base class.
# Instead, register as a tool with FastMCP directly.

def register_tool(mcp):
    @mcp.tool
    def orchestrator_tool(input: str) -> str:
        # Stub: echo input
        return input