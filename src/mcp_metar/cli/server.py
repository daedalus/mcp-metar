"""MCP server for METAR/TAF weather data."""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from mcp_metar.core.models import get_airport_weather, get_metar, get_taf

app = Server("mcp-metar")


@app.list_tools()  # type: ignore[no-untyped-call,untyped-decorator]
async def list_tools() -> list[Tool]:
    """List available MCP tools.

    Returns:
        list[Tool]: List of available tools for METAR/TAF data retrieval.
    """
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


@app.call_tool()  # type: ignore[untyped-decorator]
async def call_tool(name: str, arguments: dict[str, object]) -> list[TextContent]:
    """Handle tool calls.

    Args:
        name: Name of the tool to call.
        arguments: Arguments to pass to the tool.

    Returns:
        list[TextContent]: List of text content results.

    Raises:
        ValueError: If unknown tool name.
    """
    if name == "get_metar":
        icao = str(arguments.get("icao_code", ""))
        result = get_metar(icao)
        return [TextContent(type="text", text=result)]
    elif name == "get_taf":
        icao = str(arguments.get("icao_code", ""))
        result = get_taf(icao)
        return [TextContent(type="text", text=result)]
    elif name == "get_airport_weather":
        icao = str(arguments.get("icao_code", ""))
        weather = get_airport_weather(icao)
        result = f"METAR:\n{weather['metar']}\n\nTAF:\n{weather['taf']}"
        return [TextContent(type="text", text=result)]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main() -> int:
    """Main entry point for the MCP server.

    Returns:
        int: Exit code (0 for success).
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )
    return 0
