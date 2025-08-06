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
    from src.math_server import mcp

    return mcp

""" 
Add tests
"""

@pytest.mark.asyncio
# Using the mcp fixture to access the MCP server instance
async def test_add_positive_list(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a valid list containing positive numbers
        result = await client.call_tool("add", {"numbers": [1, 2, 3]})
        assert result.data == 6.0
        assert 'Adding numbers: [1, 2, 3] -> Result: 6.0' in caplog.text

@pytest.mark.asyncio
async def test_add_negative_list(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a list containing negative numbers
        result = await client.call_tool("add", {"numbers": [-1, -2, -3]})
        assert result.data == -6.0
        assert 'Adding numbers: [-1, -2, -3] -> Result: -6.0' in caplog.text

@pytest.mark.asyncio
async def test_add_fractional_list(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a list containing fractional numbers
        result = await client.call_tool("add", {"numbers": [1/2, 1/3, 1/4]})
        assert result.data == pytest.approx(1.083333333333333, rel=1e-9)
        print(caplog.text)
        assert 'Adding numbers: [0.5, 0.3333333333333333, 0.25] -> Result: 1.083333333333333' in caplog.text

@pytest.mark.asyncio
# Using the mcp fixture to access the MCP server instance
async def test_add_empty_list(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with an empty list to check for ToolError
        with pytest.raises(exceptions.ToolError):
            await client.call_tool("add", {"numbers": []})
            assert 'Received an empty list for addition.' in caplog.text

"""
Multiply tests
"""

@pytest.mark.asyncio
# Using the mcp fixture to access the MCP server instance
async def test_multiply_positive_list(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a valid list containing positive numbers
        result = await client.call_tool("multiply", {"numbers": [1, 1, 1]})
        assert result.data == 1.0
        assert 'Multiplying numbers: [1, 1, 1] -> Result: 1.0' in caplog.text

@pytest.mark.asyncio
async def test_multiply_negative_list(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a list containing negative numbers
        result = await client.call_tool("multiply", {"numbers": [-1, -2, -3]})
        assert result.data == -6.0
        assert 'Multiplying numbers: [-1, -2, -3] -> Result: -6.0' in caplog.text

@pytest.mark.asyncio
async def test_multiply_fractional_list(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a list containing fractional numbers
        result = await client.call_tool("multiply", {"numbers": [1/2, 1/3, 1/4]})
        assert result.data == pytest.approx(1/24, rel=1e-9)
        assert 'Multiplying numbers: [0.5, 0.3333333333333333, 0.25] -> Result: 0.041666666666667' in caplog.text

@pytest.mark.asyncio
# Using the mcp fixture to access the MCP server instance
async def test_multiply_empty_list(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with an empty list to check for ToolError
        with pytest.raises(exceptions.ToolError):
            await client.call_tool("multiply", {"numbers": []})
            assert 'Received an empty list for multiplication.' in caplog.text


"""
Subtract tests
"""

@pytest.mark.asyncio
# Using the mcp fixture to access the MCP server instance
async def test_subtract_positive_numbers(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a valid list containing positive numbers
        result = await client.call_tool("subtract", {"number_1": 5, "number_2": 3})
        assert result.data == 2.0
        assert 'Doing subtraction: 5 - 3 -> Result: 2.0' in caplog.text

@pytest.mark.asyncio
async def test_subtract_negative_numbers(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a list containing negative numbers
        result = await client.call_tool("subtract", {"number_1": -5, "number_2": -3})
        assert result.data == -2.0
        assert 'Doing subtraction: -5 - -3 -> Result: -2.0' in caplog.text

@pytest.mark.asyncio
async def test_subtract_fractional_numbers(mcp_server: FastMCP, caplog: pytest.LogCaptureFixture):
    async with Client(mcp_server) as client:
        # Test with a list containing fractional numbers
        result = await client.call_tool("subtract", {"number_1": 1/2, "number_2": 1/3})
        assert result.data == pytest.approx(1/6, rel=1e-9)
        assert 'Doing subtraction: 0.5 - 0.3333333333333333 -> Result: 0.166666666666667' in caplog.text