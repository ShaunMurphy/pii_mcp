import pytest
from fastmcp import FastMCP
from main import mcp

@pytest.fixture(scope="module")
def client():
    from fastmcp import Client
    return Client(mcp)

def extract_data(result):
    # FastMCP returns a CallToolResult object, extract the actual string
    if hasattr(result, "data"):
        return result.data
    if hasattr(result, "structured_content") and isinstance(result.structured_content, dict):
        return next(iter(result.structured_content.values()))
    if hasattr(result, "content") and result.content:
        return result.content[0].text
    return result

def test_orchestrator_plugin_echo(client):
    data = {"input": "Echo this text"}
    import asyncio
    async def run():
        async with client:
            result = await client.call_tool("orchestrator_tool", data)
            output = extract_data(result)
            assert output == "Echo this text"
    asyncio.run(run())