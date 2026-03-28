"""Core domain models and functions for METAR/TAF data."""

import re
from typing import TypedDict

METAR_URL = "https://aviationweather.gov/api/data/metar"
TAF_URL = "https://aviationweather.gov/api/data/taf"
TIMEOUT = 10


class WeatherData(TypedDict):
    """Weather data dictionary with METAR and TAF."""

    metar: str
    taf: str


def _validate_icao_code(icao_code: str) -> None:
    """Validate ICAO airport code format.

    Args:
        icao_code: 4-letter ICAO airport code.

    Raises:
        ValueError: If code is invalid.
        TypeError: If icao_code is not a string.
    """
    if not isinstance(icao_code, str):
        raise TypeError("icao_code must be a string")
    icao_code = icao_code.strip().upper()
    if len(icao_code) != 4:
        raise ValueError(f"Invalid ICAO code '{icao_code}': must be 4 characters")
    if not re.match(r"^[A-Z]{4}$", icao_code):
        raise ValueError(f"Invalid ICAO code '{icao_code}': must contain only letters")


def get_metar(icao_code: str) -> str:
    """Fetch current METAR for a given airport.

    Retrieves the current METAR (Meteorological Terminal Air Report) for the
    specified airport from the NOAA Aviation Weather API.

    Args:
        icao_code: 4-letter ICAO airport code (e.g., "KJFK", "EGLL", "LFPG").

    Returns:
        str: Formatted METAR report, or "No METAR available" if not found.

    Raises:
        ValueError: If icao_code is invalid (not 4 letters).
        RuntimeError: On network timeout or failure.

    Examples:
        >>> get_metar("KJFK")
        'KJFK 261953Z 04018KT 10SM FEW040 BKN250 04/M02 A3008 RMK AO2 SLP268 T00441022'
    """
    from mcp_metar.adapters.http import fetch_metar

    _validate_icao_code(icao_code)
    return fetch_metar(icao_code)


def get_taf(icao_code: str) -> str:
    """Fetch TAF forecast for a given airport.

    Retrieves the TAF (Terminal Aerodrome Forecast) for the specified airport
    from the NOAA Aviation Weather API.

    Args:
        icao_code: 4-letter ICAO airport code (e.g., "KJFK", "EGLL", "LFPG").

    Returns:
        str: Formatted TAF report, or "No TAF available" if not found.

    Raises:
        ValueError: If icao_code is invalid (not 4 letters).
        RuntimeError: On network timeout or failure.

    Examples:
        >>> get_taf("KJFK")
        'KJFK 261600Z 2618/2718 04015G25KT P6SM BKN040 OVC100'
    """
    from mcp_metar.adapters.http import fetch_taf

    _validate_icao_code(icao_code)
    return fetch_taf(icao_code)


def get_airport_weather(icao_code: str) -> WeatherData:
    """Fetch both METAR and TAF for a given airport.

    Convenience function that retrieves both current METAR and forecast TAF
    data for the specified airport in a single call.

    Args:
        icao_code: 4-letter ICAO airport code (e.g., "KJFK", "EGLL", "LFPG").

    Returns:
        WeatherData: Dictionary with "metar" and "taf" keys containing respective data.

    Raises:
        ValueError: If icao_code is invalid (not 4 letters).
        RuntimeError: On network timeout or failure.

    Examples:
        >>> weather = get_airport_weather("KJFK")
        >>> weather["metar"]
        'KJFK 261953Z 04018KT 10SM FEW040 BKN250 04/M02 A3008 ...'
    """
    _validate_icao_code(icao_code)
    return {
        "metar": get_metar(icao_code),
        "taf": get_taf(icao_code),
    }
