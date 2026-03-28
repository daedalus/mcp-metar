"""Tests for MCP server."""

import pytest
import pytest_mock
from mcp.types import TextContent

from mcp_metar.cli.server import call_tool, list_tools


class TestListTools:
    """Tests for list_tools function."""

    @pytest.mark.asyncio
    async def test_list_tools_returns_tools(self) -> None:
        """list_tools should return all available tools."""
        tools = await list_tools()

        assert len(tools) == 3
        tool_names = [t.name for t in tools]
        assert "get_metar" in tool_names
        assert "get_taf" in tool_names
        assert "get_airport_weather" in tool_names

    @pytest.mark.asyncio
    async def test_get_metar_tool_schema(self) -> None:
        """get_metar should have correct input schema."""
        tools = await list_tools()
        metar_tool = next(t for t in tools if t.name == "get_metar")

        assert metar_tool.inputSchema["type"] == "object"
        assert "icao_code" in metar_tool.inputSchema["properties"]
        assert metar_tool.inputSchema["required"] == ["icao_code"]


class TestCallTool:
    """Tests for call_tool function."""

    @pytest.mark.asyncio
    async def test_call_tool_get_metar(self, mocker: pytest_mock.MockerFixture) -> None:
        """call_tool should call get_metar and return result."""
        mock_get_metar = mocker.patch(
            "mcp_metar.cli.server.get_metar", return_value="KJFK METAR data"
        )

        result = await call_tool("get_metar", {"icao_code": "KJFK"})

        mock_get_metar.assert_called_once_with("KJFK")
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert result[0].text == "KJFK METAR data"

    @pytest.mark.asyncio
    async def test_call_tool_get_taf(self, mocker: pytest_mock.MockerFixture) -> None:
        """call_tool should call get_taf and return result."""
        mock_get_taf = mocker.patch(
            "mcp_metar.cli.server.get_taf", return_value="KJFK TAF data"
        )

        result = await call_tool("get_taf", {"icao_code": "KJFK"})

        mock_get_taf.assert_called_once_with("KJFK")
        assert len(result) == 1
        assert result[0].text == "KJFK TAF data"

    @pytest.mark.asyncio
    async def test_call_tool_get_airport_weather(
        self, mocker: pytest_mock.MockerFixture
    ) -> None:
        """call_tool should call get_airport_weather and format result."""
        mock_weather = mocker.patch(
            "mcp_metar.cli.server.get_airport_weather",
            return_value={"metar": "METAR data", "taf": "TAF data"},
        )

        result = await call_tool("get_airport_weather", {"icao_code": "KJFK"})

        mock_weather.assert_called_once_with("KJFK")
        assert len(result) == 1
        assert "METAR:" in result[0].text
        assert "TAF:" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_unknown_tool(self) -> None:
        """call_tool should raise ValueError for unknown tool."""
        with pytest.raises(ValueError, match="Unknown tool"):
            await call_tool("unknown_tool", {})

    @pytest.mark.asyncio
    async def test_call_tool_empty_icao(
        self, mocker: pytest_mock.MockerFixture
    ) -> None:
        """call_tool should pass empty string if icao_code not provided."""
        mock_get_metar = mocker.patch(
            "mcp_metar.cli.server.get_metar", return_value="data"
        )

        await call_tool("get_metar", {})

        mock_get_metar.assert_called_once_with("")
