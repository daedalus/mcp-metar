from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_requests_get() -> Generator[MagicMock, None, None]:
    """Fixture to mock requests.get."""
    with patch("mcp_metar._client.requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def sample_metar_response() -> list[dict[str, str]]:
    """Sample METAR response from API."""
    return [
        {
            "rawOb": "KJFK 261953Z 04018KT 10SM FEW040 BKN250 04/M02 A3008 RMK AO2 SLP268 T00441022",
            "icaoId": "KJFK",
            "reportTime": "2024-01-26T19:53:00Z",
        }
    ]


@pytest.fixture
def sample_taf_response() -> list[dict[str, str]]:
    """Sample TAF response from API."""
    return [
        {
            "rawOb": "KJFK 261600Z 2618/2718 04015G25KT P6SM BKN040 OVC100",
            "icaoId": "KJFK",
            "issueTime": "2024-01-26T16:00:00Z",
        }
    ]
