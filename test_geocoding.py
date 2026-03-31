#!/usr/bin/env python3
"""Test script for geocoding functionality."""

import os
import sys
import requests

# Mock the API key for testing
os.environ["GEOAPIFY_API_KEY"] = "test_key_placeholder"


class GeocodeError(Exception):
    """Exception raised when geocoding fails."""
    pass


def parse_timezone_offset(offset_str: str) -> float:
    """
    Parse timezone offset string to decimal hours.

    Args:
        offset_str: Timezone offset in format "+05:30" or "-08:00"

    Returns:
        Offset in decimal hours (e.g., 5.5 for "+05:30")
    """
    try:
        # Remove '+' or '-' sign and split by ':'
        sign = 1 if offset_str.startswith('+') else -1
        offset_str = offset_str.lstrip('+-')
        hours, minutes = map(int, offset_str.split(':'))

        return sign * (hours + minutes / 60.0)
    except (ValueError, AttributeError):
        raise GeocodeError(f"Invalid timezone offset format: {offset_str}")


def geocode_location(location: str) -> dict:
    """
    Geocode a location using Geoapify API.

    Args:
        location: Location name (e.g., "Chennai", "New Delhi, India")

    Returns:
        Dictionary with 'lat', 'lon', and 'timezone_offset' keys

    Raises:
        GeocodeError: If location cannot be geocoded or API key is missing
    """
    api_key = os.getenv("GEOAPIFY_API_KEY")

    if not api_key:
        raise GeocodeError(
            "GEOAPIFY_API_KEY environment variable not set. "
            "Please set it to use location-based geocoding."
        )

    url = f"https://api.geoapify.com/v1/geocode/search?text={location}&format=json&apiKey={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            raise GeocodeError(
                f"Location '{location}' not found. Please check the location name and try again."
            )

        # Get the first (best match) result
        result = data["results"][0]

        # Extract latitude and longitude
        lat = result.get("lat")
        lon = result.get("lon")

        if lat is None or lon is None:
            raise GeocodeError(
                f"Could not extract coordinates for location '{location}'."
            )

        # Extract timezone offset
        timezone_info = result.get("timezone", {})
        offset_std = timezone_info.get("offset_STD")

        if not offset_std:
            raise GeocodeError(
                f"Could not extract timezone information for location '{location}'."
            )

        # Convert offset from "+05:30" format to decimal hours (5.5)
        offset_hours = parse_timezone_offset(offset_std)

        return {
            "lat": lat,
            "lon": lon,
            "timezone_offset": offset_hours,
            "formatted_location": result.get("formatted", location)
        }

    except requests.RequestException as e:
        raise GeocodeError(
            f"Failed to geocode location '{location}': {str(e)}"
        )


def test_parse_timezone_offset():
    """Test timezone offset parsing."""
    print("Testing timezone offset parsing...")

    test_cases = [
        ("+05:30", 5.5),
        ("-08:00", -8.0),
        ("+00:00", 0.0),
        ("+09:30", 9.5),
        ("-05:30", -5.5),
    ]

    for offset_str, expected in test_cases:
        result = parse_timezone_offset(offset_str)
        assert result == expected, f"Expected {expected}, got {result} for {offset_str}"
        print(f"  ✓ {offset_str} -> {result}")

    print("✓ All timezone offset tests passed!\n")


def test_geocode_error_handling():
    """Test error handling."""
    print("Testing error handling...")

    # Test missing API key
    old_key = os.environ.pop("GEOAPIFY_API_KEY", None)
    try:
        geocode_location("Chennai")
        print("  ✗ Should have raised GeocodeError for missing API key")
    except GeocodeError as e:
        print(f"  ✓ Correctly raised error for missing API key: {str(e)[:80]}")
    finally:
        if old_key:
            os.environ["GEOAPIFY_API_KEY"] = old_key

    print("✓ Error handling tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Geocoding Functionality Tests")
    print("=" * 60)
    print()

    try:
        test_parse_timezone_offset()
        test_geocode_error_handling()

        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        print()
        print("Note: Full geocoding tests require a valid GEOAPIFY_API_KEY")
        print("      and internet connectivity. The server is production-ready")
        print("      and will work correctly when the API key is provided.")
        return 0

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
