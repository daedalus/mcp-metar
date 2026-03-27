from unittest.mock import MagicMock

import pytest

from mcp_metar._client import (
    _validate_icao_code,
    get_airport_weather,
    get_metar,
    get_taf,
)


class TestValidateIcaoCode:
    """Tests for _validate_icao_code function."""

    def test_valid_icao_code(self) -> None:
        """Valid 4-letter codes should not raise."""
        _validate_icao_code("KJFK")
        _validate_icao_code("EGLL")
        _validate_icao_code("LFPG")

    def test_valid_icao_code_lowercase(self) -> None:
        """Lowercase codes should be accepted (normalized)."""
        _validate_icao_code("kjfk")

    def test_icao_code_with_spaces(self) -> None:
        """Codes with leading/trailing spaces should be accepted."""
        _validate_icao_code("  KJFK  ")

    def test_invalid_icao_code_too_short(self) -> None:
        """Code too short should raise ValueError."""
        with pytest.raises(ValueError, match="must be 4 characters"):
            _validate_icao_code("JFK")

    def test_invalid_icao_code_too_long(self) -> None:
        """Code too long should raise ValueError."""
        with pytest.raises(ValueError, match="must be 4 characters"):
            _validate_icao_code("KJFKX")

    def test_invalid_icao_code_with_numbers(self) -> None:
        """Code with numbers should raise ValueError."""
        with pytest.raises(ValueError, match="must contain only letters"):
            _validate_icao_code("KJ12")

    def test_invalid_icao_code_with_special_chars(self) -> None:
        """Code with special characters should raise ValueError."""
        with pytest.raises(ValueError, match="must be 4 characters"):
            _validate_icao_code("KJFK!")

    def test_not_a_string(self) -> None:
        """Non-string input should raise TypeError."""
        with pytest.raises(TypeError, match="must be a string"):
            _validate_icao_code(1234)  # type: ignore[arg-type]


class TestGetMetar:
    """Tests for get_metar function."""

    def test_get_metar_success(
        self,
        mock_requests_get: MagicMock,
        sample_metar_response: list[dict[str, str]],
    ) -> None:
        """Successful METAR fetch returns formatted data."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metar_response
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        result = get_metar("KJFK")

        assert "KJFK" in result
        mock_requests_get.assert_called_once()
        call_args = mock_requests_get.call_args
        assert call_args[1]["params"]["ids"] == "KJFK"

    def test_get_metar_no_data(self, mock_requests_get: MagicMock) -> None:
        """No METAR available returns appropriate message."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        result = get_metar("KJFK")
        assert result == "No METAR/TAF available"

    def test_get_metar_timeout(self, mock_requests_get: MagicMock) -> None:
        """Timeout raises RuntimeError."""
        import requests as req

        mock_requests_get.side_effect = req.Timeout()

        with pytest.raises(RuntimeError, match="timed out"):
            get_metar("KJFK")

    def test_get_metar_request_exception(self, mock_requests_get: MagicMock) -> None:
        """Request exception raises RuntimeError."""
        import requests as req

        mock_requests_get.side_effect = req.RequestException("Connection failed")

        with pytest.raises(RuntimeError, match="Request failed"):
            get_metar("KJFK")


class TestGetTaf:
    """Tests for get_taf function."""

    def test_get_taf_success(
        self,
        mock_requests_get: MagicMock,
        sample_taf_response: list[dict[str, str]],
    ) -> None:
        """Successful TAF fetch returns formatted data."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_taf_response
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        result = get_taf("KJFK")

        assert "KJFK" in result
        mock_requests_get.assert_called_once()
        call_args = mock_requests_get.call_args
        assert call_args[1]["params"]["ids"] == "KJFK"


class TestGetAirportWeather:
    """Tests for get_airport_weather function."""

    def test_get_airport_weather_success(
        self,
        mock_requests_get: MagicMock,
        sample_metar_response: list[dict[str, str]],
        sample_taf_response: list[dict[str, str]],
    ) -> None:
        """Combined METAR and TAF fetch returns both."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()

        def json_side_effect() -> list[dict[str, str]]:
            if mock_response.json.call_count == 1:
                return sample_metar_response
            return sample_taf_response

        mock_response.json.side_effect = json_side_effect
        mock_requests_get.return_value = mock_response

        result = get_airport_weather("KJFK")

        assert "metar" in result
        assert "taf" in result
        assert "KJFK" in result["metar"]
