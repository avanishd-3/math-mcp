import pytest
from fastmcp import FastMCP, Client, exceptions

@pytest.fixture
def mcp_server():
    from src.math_server import mcp

    return mcp

@pytest.mark.asyncio
# Using the mcp fixture to access the MCP server instance
async def test_add_valid_list(mcp_server: FastMCP):
    async with Client(mcp_server) as client:
        # Test with a valid list of numbers
        result = await client.call_tool("add", {"numbers": [1, 2, 3]})
        assert result.data == 6.0

@pytest.mark.asyncio
# Using the mcp fixture to access the MCP server instance
async def test_add_empty_list(mcp_server: FastMCP):
    async with Client(mcp_server) as client:
        # Test with an empty list to check for ToolError
        with pytest.raises(exceptions.ToolError):
            await client.call_tool("add", {"numbers": []})