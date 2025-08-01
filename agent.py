import asyncio
import os
import logging
import mlflow
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

async def test_tool_connectivity():
    fastmcp_url = os.getenv("FASTMCP_URL", "http://localhost:8000/mcp")
    logger.info(f"Connecting to FastMCP server at {fastmcp_url}")
    try:
        client = MultiServerMCPClient(
            {
                "sfmc": {
                    "url": fastmcp_url,
                    "transport": "streamable_http",
                }
            }
        )
        with mlflow.start_run(run_name="test_tool_connectivity"):
            try:
                tools = await client.get_tools()
                logger.info(f"Available tools: {tools}")
                mlflow.log_text(str(tools), "available_tools.txt")
            except Exception as e:
                logger.error(f"Error fetching tools: {e}")
                mlflow.log_param("error_fetching_tools", str(e))
                return

            # Try invoking each tool with appropriate args
            for tool in tools:
                tool_name = getattr(tool, "name", str(tool))
                logger.info(f"Testing tool: {tool_name}")
                try:
                    args = {}
                    # Provide required input for demo_echo tool
                    if tool_name == "demo_echo":
                        args = {"input": "test input"}
                    result = await tool.ainvoke(args)
                    logger.info(f"Result from {tool_name}: {result}")
                    mlflow.log_text(str(result), f"{tool_name}_result.txt")
                except Exception as e:
                    logger.error(f"Error invoking {tool_name}: {e}")
                    mlflow.log_param(f"error_{tool_name}", str(e))
    except Exception as e:
        logger.error(f"Failed to connect to FastMCP server: {e}")

if __name__ == "__main__":
    asyncio.run(test_tool_connectivity())