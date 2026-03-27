# SPEC.md — mcp-metar

## Purpose

An MCP (Model Context Protocol) server that provides tools for fetching METAR (Meteorological Terminal Air Report) and TAF (Terminal Aerodrome Forecast) aviation weather data from NOAA/NWS APIs. It enables AI assistants to retrieve current weather conditions and forecasts for airports worldwide.

## Scope

### In Scope
- METAR data retrieval by ICAO airport code
- TAF data retrieval by ICAO airport code
- Parse and format METAR/TAF responses into human-readable output
- Support for US and international airports
- Error handling for invalid codes and network failures

### Not in Scope
- Historical data retrieval
- Real-time weather updates/polling
- Graphical weather maps
- Integration with other weather services (NOAA only)

## Public API / Interface

### MCP Server
The server implements the MCP stdio protocol with the following tools:

#### `get_metar`
Fetches current METAR for a given airport.

- **Arguments:**
  - `icao_code` (str): 4-letter ICAO airport code (e.g., "KJFK", "EGLL")
- **Returns:** str - Formatted METAR report or error message
- **Raises:** ValueError if invalid ICAO code format

#### `get_taf`
Fetches TAF forecast for a given airport.

- **Arguments:**
  - `icao_code` (str): 4-letter ICAO airport code (e.g., "KJFK", "EGLL")
- **Returns:** str - Formatted TAF report or error message
- **Raises:** ValueError if invalid ICAO code format

#### `get_airport_weather`
Fetches both METAR and TAF for a given airport.

- **Arguments:**
  - `icao_code` (str): 4-letter ICAO airport code
- **Returns:** dict with "metar" and "taf" keys

## Data Formats

### Input
- ICAO codes: 4-character strings (letters only, uppercase preferred)

### Output
- METAR: Raw NOAA METAR string with basic formatting
- TAF: Raw NOAA TAF string with basic formatting

### API Endpoints
- METAR: `https://aviationweather.gov/api/data/metar?ids={icao_code}`
- TAF: `https://aviationweather.gov/api/data/taf?ids={icao_code}`

## Edge Cases

1. Invalid ICAO code (wrong length, invalid characters) - raise ValueError
2. Airport not found (no data returned) - return "No METAR/TAF available"
3. Network timeout - raise RuntimeError
4. Empty response - return "No data available"
5. International airports with different format - handle gracefully

## Performance & Constraints

- HTTP timeout: 10 seconds
- No caching (fetch fresh data each request)
- Single request per tool call
- Minimal dependencies (requests only)

## Implementation Details

- Use `mcp-server` library for MCP protocol handling
- Use `requests` for HTTP calls
- Type hints throughout
- Verbose docstrings on all functions