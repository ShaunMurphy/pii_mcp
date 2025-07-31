import pytest
from fastmcp import Client

@pytest.fixture(scope="module")
def client():
    # Connect to the running HTTP server
    return Client("http://127.0.0.1:8000/mcp/")

def extract_data(result):
    # FastMCP returns a CallToolResult object, extract the actual string or dict
    if hasattr(result, "data"):
        return result.data
    if hasattr(result, "structured_content") and isinstance(result.structured_content, dict):
        return result.structured_content
    if hasattr(result, "content") and result.content:
        return result.content[0].text
    return result

def test_pii_redaction(client):
    pii_text = {
        "input": (
            "My name is John Doe. My email is john.doe@example.com. "
            "My SSN is 123-45-6789. My credit card is 4111-1111-1111-1111. "
            "My password is hunter2."
        )
    }
    import asyncio
    async def run():
        async with client:
            result = await client.call_tool("demo_echo", pii_text)
            output = extract_data(result)
            # Should redact email, SSN, credit card
            assert "john.doe@example.com" not in output
            assert "123-45-6789" not in output
            assert "4111-1111-1111-1111" not in output
            # Password and name may not be redacted by default
    asyncio.run(run())

def test_no_pii(client):
    text = {"input": "Hello, this is a safe message."}
    import asyncio
    async def run():
        async with client:
            result = await client.call_tool("demo_echo", text)
            output = extract_data(result)
            assert output["result"] == "Hello, this is a safe message."
    asyncio.run(run())