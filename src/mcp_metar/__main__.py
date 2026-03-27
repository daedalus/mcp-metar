"""MCP server entry point for METAR/TAF weather data."""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from mcp_metar._client import get_airport_weather, get_metar, get_taf

app = Server("mcp-metar")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="get_metar",
            description="Fetch current METAR weather data for an airport by ICAO code",
            inputSchema={
                "type": "object",
                "properties": {
                    "icao_code": {
                        "type": "string",
                        "description": "4-letter ICAO airport code (e.g., KJFK, EGLL)",
                    }
                },
                "required": ["icao_code"],
            },
        ),
        Tool(
            name="get_taf",
            description="Fetch TAF (Terminal Aerodrome Forecast) for an airport by ICAO code",
            inputSchema={
                "type": "object",
                "properties": {
                    "icao_code": {
                        "type": "string",
                        "description": "4-letter ICAO airport code (e.g., KJFK, EGLL)",
                    }
                },
                "required": ["icao_code"],
            },
        ),
        Tool(
            name="get_airport_weather",
            description="Fetch both METAR and TAF for an airport by ICAO code",
            inputSchema={
                "type": "object",
                "properties": {
                    "icao_code": {
                        "type": "string",
                        "description": "4-letter ICAO airport code (e.g., KJFK, EGLL)",
                    }
                },
                "required": ["icao_code"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, object]) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_metar":
        icao = arguments.get("icao_code", "")
        result = get_metar(icao)
        return [TextContent(type="text", text=result)]
    elif name == "get_taf":
        icao = arguments.get("icao_code", "")
        result = get_taf(icao)
        return [TextContent(type="text", text=result)]
    elif name == "get_airport_weather":
        icao = arguments.get("icao_code", "")
        weather = get_airport_weather(icao)
        result = f"METAR:\n{weather['metar']}\n\nTAF:\n{weather['taf']}"
        return [TextContent(type="text", text=result)]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main() -> int:  # pragma: no cover
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
