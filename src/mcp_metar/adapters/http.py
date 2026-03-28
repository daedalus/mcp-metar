"""HTTP adapter for NOAA Aviation Weather API."""

from typing import Any

import requests

from mcp_metar.core.models import METAR_URL, TAF_URL, TIMEOUT


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
        data: Any = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            raw_ob: str = data[0].get("rawOb", "No data available")
            return raw_ob
        return "No METAR/TAF available"

    except requests.Timeout:
        raise RuntimeError("Request timed out")
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")
    except ValueError:
        return "No data available"


def fetch_metar(icao_code: str) -> str:
    """Fetch METAR data from NOAA API.

    Args:
        icao_code: ICAO airport code.

    Returns:
        Raw METAR data or error message.
    """
    return _fetch_data(METAR_URL, icao_code)


def fetch_taf(icao_code: str) -> str:
    """Fetch TAF data from NOAA API.

    Args:
        icao_code: ICAO airport code.

    Returns:
        Raw TAF data or error message.
    """
    return _fetch_data(TAF_URL, icao_code)
