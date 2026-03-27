"""Client for fetching METAR and TAF weather data from NOAA."""

import re

import requests

METAR_URL = "https://aviationweather.gov/api/data/metar"
TAF_URL = "https://aviationweather.gov/api/data/taf"
TIMEOUT = 10


def _validate_icao_code(icao_code: str) -> None:
    """Validate ICAO airport code format.

    Args:
        icao_code: 4-letter ICAO airport code.

    Raises:
        ValueError: If code is invalid.
    """
    if not isinstance(icao_code, str):
        raise TypeError("icao_code must be a string")
    icao_code = icao_code.strip().upper()
    if len(icao_code) != 4:
        raise ValueError(f"Invalid ICAO code '{icao_code}': must be 4 characters")
    if not re.match(r"^[A-Z]{4}$", icao_code):
        raise ValueError(f"Invalid ICAO code '{icao_code}': must contain only letters")


def _fetch_data(url: str, icao_code: str) -> str:
    """Fetch data from NOAA API.

    Args:
        url: API endpoint URL.
        icao_code: ICAO airport code.

    Returns:
        Raw response data or error message.

    Raises:
        RuntimeError: On network failure.
    """
    icao_code = icao_code.strip().upper()
    params = {"ids": icao_code}

    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            return data[0].get("rawOb", "No data available")
        return "No METAR/TAF available"

    except requests.Timeout:
        raise RuntimeError("Request timed out")
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")
    except ValueError:
        return "No data available"


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
    _validate_icao_code(icao_code)
    return _fetch_data(METAR_URL, icao_code)


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
    _validate_icao_code(icao_code)
    return _fetch_data(TAF_URL, icao_code)


def get_airport_weather(icao_code: str) -> dict[str, str]:
    """Fetch both METAR and TAF for a given airport.

    Convenience function that retrieves both current METAR and forecast TAF
    data for the specified airport in a single call.

    Args:
        icao_code: 4-letter ICAO airport code (e.g., "KJFK", "EGLL", "LFPG").

    Returns:
        dict: Dictionary with "metar" and "taf" keys containing respective data.

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
