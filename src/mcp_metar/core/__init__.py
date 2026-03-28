"""Core domain logic for METAR/TAF data."""

from .models import (
    METAR_URL,
    TAF_URL,
    TIMEOUT,
    _validate_icao_code,
    get_airport_weather,
    get_metar,
    get_taf,
)
