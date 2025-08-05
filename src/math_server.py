# Math dependency
import numpy as np

# Logging
import logging

from fastmcp import FastMCP

mcp = FastMCP(
    name="Math MCP Server",
    instructions="This server provides basic arithmetic operations in 64 bit floating point precision.",
    dependencies=["numpy"],
)

# Can't really have higher than 64 bit precision on a 64-bit system
@mcp.tool
def add(
    numbers: list[int | float],
) -> float:
    """Adds a list of numbers with 64 bit floating point precision and returns a 64 bit float.
       You need to provide them in the format of a list. For example, [1, 2, 3] would return 6.0.
    """

    if not numbers:
        logging.error("Received an empty list for addition.")
        raise ValueError("""The list of numbers cannot be empty. Try wrapping the numbers in brackets, like [1, 2, 3], if this is not the case.
        """)

    # Use numpy for fast addition
    result = float(np.sum(numbers, dtype=np.float64))
    logging.info(f"Adding numbers: {numbers} -> Result: {result}")
    return result

# Recommended best practice to ensure FastMCP server runs for all users & clients in a consistent way
if __name__ == "__main__":
    mcp.run() # Run the MCP server