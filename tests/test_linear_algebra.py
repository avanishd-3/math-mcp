import pytest
import logging

from fastmcp import FastMCP, Client, exceptions

# Set up logging for the tests
logger = logging.getLogger() # Using root logger for now
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Set up MCP server fixture
@pytest.fixture
def mcp_server():
    from src.math_server import math_mcp

    return math_mcp
"""
Matrix multiplication tests
"""

@pytest.mark.asyncio
# Using the mcp fixture to access the MCP server instance
async def test_matrix_multiplication_matrix_1_empty(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with an empty list to check for ToolError
        with pytest.raises(exceptions.ToolError):
            await client.call_tool("matrix_multiplication", {"matrix_1": [[]], "matrix_2": [[1]]})
            assert 'Received an empty matrix for multiplication.' in caplog.text

@pytest.mark.asyncio
async def test_matrix_multiplication_matrix_2_empty(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with an empty list to check for ToolError
        with pytest.raises(exceptions.ToolError):
            await client.call_tool("matrix_multiplication", {"matrix_1": [[1]], "matrix_2": [[]]})
            assert 'Received an empty matrix for multiplication.' in caplog.text

@pytest.mark.asyncio
async def test_matrix_multiplication_incompatible_dimensions(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with incompatible dimensions to check for ToolError
        with pytest.raises(exceptions.ToolError):
            await client.call_tool("matrix_multiplication", {"matrix_1": [[1, 2]], "matrix_2": [[1], [2], [3]]})
            assert 'Incompatible matrix dimensions for multiplication.' in caplog.text

@pytest.mark.asyncio
async def test_matrix_multiplication_valid_square(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with valid matrices
        result = await client.call_tool("matrix_multiplication", {"matrix_1": [[1, 2], [3, 4]], "matrix_2": [[5, 6], [7, 8]]})
        assert result.data == [[19.0, 22.0], [43.0, 50.0]]
        assert 'Multiplying matrices' in caplog.text

@pytest.mark.asyncio
async def test_matrix_multiplication_valid_rectangle(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with valid matrices
        result = await client.call_tool("matrix_multiplication", {"matrix_1": [[1, 2, 3], [4, 5, 6]], "matrix_2": [[7, 8], [9, 10], [11, 12]]})
        assert result.data == [[58.0, 64.0], [139.0, 154.0]]
        assert 'Multiplying matrices' in caplog.text