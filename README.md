# mcp-metar

> MCP server for METAR/TAF aviation weather data

[![PyPI](https://img.shields.io/pypi/v/mcp-metar.svg)](https://pypi.org/project/mcp-metar/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-metar.svg)](https://pypi.org/project/mcp-metar/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install mcp-metar
```

## Usage

```python
from mcp_metar import get_metar, get_taf, get_airport_weather

# Get current METAR for an airport
metar = get_metar("KJFK")
print(metar)

# Get TAF forecast
taf = get_taf("KJFK")
print(taf)

# Get both METAR and TAF
weather = get_airport_weather("KJFK")
print(weather["metar"])
print(weather["taf"])
```

## MCP Server

This package provides an MCP server that can be used with MCP-compatible clients. Configure your client with:

```json
{
  "mcpServers": {
    "mcp-metar": {
      "command": "mcp-metar",
      "env": {}
    }
  }
}
```

### Available Tools

- `get_metar`: Fetch current METAR weather data for an airport by ICAO code
- `get_taf`: Fetch TAF (Terminal Aerodrome Forecast) for an airport by ICAO code
- `get_airport_weather`: Fetch both METAR and TAF for an airport by ICAO code

## Development

```bash
git clone https://github.com/daedalus/mcp-metar.git
cd mcp-metar
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```

## License

MIT