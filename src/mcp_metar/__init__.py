"""MCP server for METAR/TAF aviation weather data."""

__version__ = "0.1.0"
__all__ = ["get_metar", "get_taf", "get_airport_weather"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_metar.core.models import WeatherData

from mcp_metar.core.models import get_airport_weather, get_metar, get_taf
