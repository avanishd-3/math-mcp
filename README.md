# Math MCP Server

## Overview

This is an MCP (Model Context Protocol) server that can do basic arithmetic in 64 bit precision, along with matrix multiplication.

## Features
- Addition 
- Subtraction 
- Multiplication
- Division

- Matrix multiplication

## Installation

### Prerequisities
Ensure you have the following installed:
- Python 3.13+
- uv

#### Installing UV
See [installation guide](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) for all options.

##### Unix/MacOS

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or

```
brew install uv
```
##### Windows

```
winget install --id=astral-sh.uv  -e
```

### Clone the Repository
```
git clone https://github.com/avanishd-3/math-mcp.git
cd math-mcp-server
uv sync
```

## Integration with Clients

### Claude Code
fastmcp install claude-code src/math_server.py:math_mcp

### Claude Desktop
fastmcp install claude-desktop src/math_server.py:math_mcp

### Cursor
fastmcp install cursor src/math_server.py:math_mcp

### VS Code
Add the following .vscode/mcp.json and use your actual path.

```
{
  "servers": {
    "Math MCP Server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "--with",
        "numpy",
        "fastmcp",
        "run",
        "/absolute/path/Desktop/to/math-mcp-server/src/math_server.py:math_mcp"
      ]
    }
  },
}
```

## Contributing
1. Fork the repository

2. Create a new branch:
```
git checkout -b add-feature
```

3. Make changes and commit (remember to add unit tests in test/ directory)
```
git commit -m "Added a new feature"
```

4. Push to your fork
git push origin add-feature

5. Open a pull request.

## Project Structure
```text
/
├── src
│   └── math_server.py
├── tests
│   ├── test_arithmetic.py
│   │   └── astro.svg
│   ├── test_linear_algebra.py
├── pytest.ini
├── pyproject.toml
└── uv.lock
```

### Architecture
This MCP server uses [Fast MCP 2.0](https://gofastmcp.com/getting-started/welcome), which provides many more features than
Fast MCP 1.0, which is what the official Python SDK for MCP uses.

Also, the unit tests are written with Pytest, which is what Fast MCP 2.0 recommends. 

Lastly, if you don't know, uv is a much faster version of pip that also provides a lockfile for project dependencies (this will be familiar if you've used npm or cargo before). The MCP Python SDK itself uses uv, and I use it for all new Python projects, because it's 10-100x faster than pip, and the lockfile makes dependency version management much simpler.