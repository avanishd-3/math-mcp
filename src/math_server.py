# Math dependency
import numpy as np

# Type annotation and input validation dependencies
from typing import Final

# Logging
import logging

from fastmcp import FastMCP


# Constants

# See: https://stackoverflow.com/questions/56514892/how-many-digits-can-float8-float16-float32-float64-and-float128-contain
SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES: Final[int] = np.finfo(np.float64).precision

"""
Notes about Fast MCP:

Cannot handle having numpy types in the function signature (it just sends None), so use float or int instead.

Server composition breaks MCP inspector (at least in 2.11.1), so use a single server for now. I even tried their own
example for server composition, but you cannot use a dev server with it. The main server lists no tools if you call it directly,
but you can run dev with the sub servers and they work.

It finding the server on dev is also broken, so you need to do fastmcp dev src/math_server.py:math_mcp to run it.

"""

math_mcp = FastMCP(
    name="Math MCP Server",
    instructions="This server provides basic arithmetic operations and matrix multiplication in 64 bit floating point precision.",
    dependencies=["numpy"],
)

# Can't really have higher than 64 bit precision on a 64-bit system
@math_mcp.tool
def add(
    numbers: list[int | float],
) -> float:
    """Adds a list of positive and/or negative numbers with 64 bit floating point precision and returns a 64 bit float.
       You need to provide them in the format of a list. For example, [1, 2, 3] would return 6.0.
       You can also use fractions if you want to, like [1/2, 1/3, 1/4].
    """

    # This is technically allowed by Fast MCP, but it is an error here
    if not numbers:
        logging.error("Received an empty list for addition.")
        raise ValueError("""The list of numbers cannot be empty. Try wrapping the numbers in brackets, like [1, 2, 3], if this is not the case.
        """)

    # Use numpy for fast addition
    result = np.round(np.sum(numbers, dtype=np.float64), decimals=SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES)
    logging.info(f"Adding numbers: {numbers} -> Result: {result}")
    return result

@math_mcp.tool
def subtract(
    number_1: int | float,
    number_2: int | float,
) -> float:
    """Subtracts two numbers with 64 bit floating point precision and returns a 64 bit float.
       For example, subtracting 5 from 10 would return 5.0.
       You can also use fractions if you want to, like 1/2 for number_1 and 1/3 for number_2.
    """
    result = np.round(np.float64(number_1) - np.float64(number_2), decimals=SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES)
    logging.info(f"Doing subtraction: {number_1} - {number_2} -> Result: {result}")
    return result

@math_mcp.tool
def multiply(
    numbers: list[int | float],
) -> float:
    """Multiplies a list of positive and/or negative numbers with 64 bit floating point precision and returns a 64 bit float.
       You need to provide them in the format of a list. For example, [1, 2, 3] would return 6.0.
       You can also use fractions if you want to, like [1/2, 1/3, 1/4].
    """

    # This is technically allowed by Fast MCP, but it is an error here
    if not numbers:
        logging.error("Received an empty list for multiplication.")
        raise ValueError("""The list of numbers cannot be empty. Try wrapping the numbers in brackets, like [1, 2, 3], if this is not the case.
        """)

    # Use numpy for fast multiplication
    result = np.round(np.prod(numbers, dtype=np.float64), decimals=SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES)
    logging.info(f"Multiplying numbers: {numbers} -> Result: {result}")
    return result

@math_mcp.tool
def divide(
    number_1: int | float,
    number_2: int | float,
) -> float:
    """Divides two numbers with 64 bit floating point precision and returns a 64 bit float.
       For example, dividing 10 by 2 would return 5.0.
       You can also use fractions if you want to, like 1/2 for number_1 and 1/3 for number_2.
    """
    if number_2 == 0:
        logging.error("Division by zero error.")
        raise ValueError("Division by zero is not allowed.")
    result = np.round(np.float64(number_1) / np.float64(number_2), decimals=SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES)
    logging.info(f"Doing division: {number_1} / {number_2} -> Result: {result}")
    return result

@math_mcp.tool
def matrix_multiplication(
    matrix_1: list[list[int | float]],
    matrix_2: list[list[int | float]],
) -> list[list[float]]:
    """Multiplies two matrices with 64 bit floating point precision and returns the result as a matrix.
       You need to provide them in the format of nested lists. For example, [[1, 2], [3, 4]] would represent a 2x2 matrix.
       Each sub list represents a row in the matrix, and each element in the sub list represents a column.
       The matrices must be compatible for multiplication, meaning the number of columns in the first matrix must equal the number of rows in the second matrix.
       You can also use fractions for individual elements if you want to, like [1/2, 1/3, 1/4].
    """

    # Convert matrices to numpy arrays for efficient multiplication
    matrix_1 = np.array(matrix_1, dtype=np.float64)
    matrix_2 = np.array(matrix_2, dtype=np.float64)

    # This is technically allowed by Fast MCP, but it is an error here
    if not matrix_1.size:
        logging.error("Matrix 1 is empty.")
        raise ValueError("Matrix 1 cannot be empty.")
    if not matrix_2.size:
        logging.error("Matrix 2 is empty.")
        raise ValueError("Matrix 2 cannot be empty.")
    
    # Check if matrices have compatible dimensions for multiplication
    if len(matrix_1[0]) != len(matrix_2):
        logging.error("Incompatible matrix dimensions for multiplication.")
        raise ValueError("Incompatible matrix dimensions.")
    
    

    # Use numpy for fast matrix multiplication
    result = np.round(np.matmul(matrix_1, matrix_2), decimals=SIXTY_FOUR_BIT_FLOAT_DECIMAL_PLACES)
    logging.info(f"Multiplying matrices: {matrix_1} * {matrix_2} -> Result: {result}")

    # Convert result to list of lists so Fast MCP can serialize it properly
    result = result.tolist()
    return result

# Recommended best practice to ensure FastMCP server runs for all users & clients in a consistent way
if __name__ == "__main__":
    math_mcp.run()