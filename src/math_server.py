# Math dependency
import numpy as np

# Logging
import logging

from fastmcp import FastMCP


# Constants

# See: https://stackoverflow.com/questions/56514892/how-many-digits-can-float8-float16-float32-float64-and-float128-contain
SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES = np.finfo(np.float64).precision

# Note: Fast MCP cannot handle having numpy types in the function signature (it just sends None), so use float or int instead.
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
    """Adds a list of positive and/or negative numbers with 64 bit floating point precision and returns a 64 bit float.
       You need to provide them in the format of a list. For example, [1, 2, 3] would return 6.0.
       You can also use fractions if you want to, like [1/2, 1/3, 1/4].
    """

    if not numbers:
        logging.error("Received an empty list for addition.")
        raise ValueError("""The list of numbers cannot be empty. Try wrapping the numbers in brackets, like [1, 2, 3], if this is not the case.
        """)

    # Use numpy for fast addition
    result = np.round(np.sum(numbers, dtype=np.float64), decimals=SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES)
    logging.info(f"Adding numbers: {numbers} -> Result: {result}")
    return result

@mcp.tool
def multiply(
    numbers: list[int | float],
) -> float:
    """Multiplies a list of positive and/or negative numbers with 64 bit floating point precision and returns a 64 bit float.
       You need to provide them in the format of a list. For example, [1, 2, 3] would return 6.0.
       You can also use fractions if you want to, like [1/2, 1/3, 1/4].
    """

    if not numbers:
        logging.error("Received an empty list for multiplication.")
        raise ValueError("""The list of numbers cannot be empty. Try wrapping the numbers in brackets, like [1, 2, 3], if this is not the case.
        """)

    # Use numpy for fast multiplication
    result = np.round(np.prod(numbers, dtype=np.float64), decimals=SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES)
    logging.info(f"Multiplying numbers: {numbers} -> Result: {result}")
    return result

# Recommended best practice to ensure FastMCP server runs for all users & clients in a consistent way
if __name__ == "__main__":
    mcp.run() # Run the MCP server