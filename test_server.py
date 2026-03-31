#!/usr/bin/env python3
"""Test script for the Vedic Astrology MCP server."""

import argparse
import os
from datetime import datetime
from typing import Dict

import requests
from jyotishganit import calculate_birth_chart


def load_env_file(env_path: str = ".env") -> None:
    """Load key-value pairs from a .env file into process environment."""
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            # Do not override values already present in the environment.
            if key and key not in os.environ:
                os.environ[key] = value

def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for test birth data."""
    parser = argparse.ArgumentParser(
        description="Test Vedic astrology birth chart calculation with custom inputs."
    )
    parser.add_argument("--name", default="Bhampu", help="Name of the person")
    parser.add_argument("--birthdate", default="1996-07-04", help="Birth date in YYYY-MM-DD format")
    parser.add_argument("--birth-time", default="09:10:00", help="Birth time in HH:MM or HH:MM:SS format")
    parser.add_argument("--location", default="Karmala, India", help="Birth location to geocode")
    parser.add_argument(
        "--geoapify-api-key",
        default=None,
        help="Geoapify API key (optional, falls back to GEOAPIFY_API_KEY env var)",
    )
    return parser.parse_args()


def parse_birth_datetime(birthdate: str, birth_time: str) -> datetime:
    """Parse birth date/time strings into a datetime object."""
    date_part = datetime.strptime(birthdate, "%Y-%m-%d")

    time_parts = birth_time.split(":")
    if len(time_parts) == 2:
        hour, minute = map(int, time_parts)
        second = 0
    elif len(time_parts) == 3:
        hour, minute, second = map(int, time_parts)
    else:
        raise ValueError("birth-time must be in HH:MM or HH:MM:SS format")

    return datetime(date_part.year, date_part.month, date_part.day, hour, minute, second)


def parse_timezone_offset(offset_str: str) -> float:
    """Convert timezone offset from '+05:30' format to decimal hours (5.5)."""
    sign = 1 if offset_str.startswith("+") else -1
    raw = offset_str.lstrip("+-")
    hours, minutes = map(int, raw.split(":"))
    return sign * (hours + minutes / 60.0)


def geocode_location(location: str, api_key: str) -> Dict[str, float]:
    """Geocode location and return coordinates and timezone offset."""
    url = f"https://api.geoapify.com/v1/geocode/search?text={location}&format=json&apiKey={api_key}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    if not results:
        raise ValueError(f"Location not found: {location}")

    result = results[0]
    timezone_info = result.get("timezone", {})
    offset_std = timezone_info.get("offset_STD")
    if not offset_std:
        raise ValueError(f"Timezone information missing for location: {location}")

    return {
        "lat": result["lat"],
        "lon": result["lon"],
        "timezone_offset": parse_timezone_offset(offset_std),
        "formatted_location": result.get("formatted", location),
    }


def test_birth_chart(args: argparse.Namespace):
    """Test birth chart calculation."""
    print("Testing Vedic Astrology Birth Chart Calculation...")
    print("=" * 60)

    api_key = args.geoapify_api_key or os.getenv("GEOAPIFY_API_KEY")
    if not api_key:
        print("\n✗ Error: Geoapify API key not provided.")
        print("Set GEOAPIFY_API_KEY env var or pass --geoapify-api-key.")
        return False

    try:
        birth_date = parse_birth_datetime(args.birthdate, args.birth_time)
        geo_data = geocode_location(args.location, api_key)

        chart = calculate_birth_chart(
            birth_date=birth_date,
            latitude=geo_data["lat"],
            longitude=geo_data["lon"],
            timezone_offset=geo_data["timezone_offset"],
            name=args.name,
        )

        print("\n✓ Birth chart calculated successfully!")
        print("\nBasic Details:")
        print(f"  Name: {args.name}")
        print(f"  Date: {birth_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Place: {geo_data['formatted_location']} ({geo_data['lat']}°N, {geo_data['lon']}°E)")
        print(f"  Timezone: UTC{geo_data['timezone_offset']:+g}")

        print("\nAstrological Details:")
        print(f"  Ascendant: {chart.d1_chart.houses[0].sign}")
        # print(f"  Ascendant Lord: {chart.d1_chart.houses[0].sign_lord}")
        print(f"  Moon Sign: {chart.d1_chart.planets[1].sign}")
        print(f"  Moon Nakshatra: {chart.panchanga.nakshatra}")
        print(f"  Sun Sign: {chart.d1_chart.planets[0].sign}")

        print("\nPanchanga:")
        print(f"  Tithi: {chart.panchanga.tithi}")
        print(f"  Nakshatra: {chart.panchanga.nakshatra}")
        print(f"  Yoga: {chart.panchanga.yoga}")
        print(f"  Karana: {chart.panchanga.karana}")
        print(f"  Vaara: {chart.panchanga.vaara}")

        print("\nPlanetary Positions:")
        for planet in chart.d1_chart.planets:
            print(f"  {planet.celestial_body:8s}: {planet.sign:12s} ({planet.sign_degrees:.2f}°) - House {planet.house}")

        # Test Dashas
        if hasattr(chart, 'dashas') and chart.dashas:
            print("\nVimshottari Dashas:")
            if hasattr(chart.dashas, 'upcoming') and chart.dashas.upcoming:
                upcoming = chart.dashas.upcoming
                if 'mahadashas' in upcoming:
                    mahadashas = upcoming['mahadashas']
                    for i, (lord, md) in enumerate(list(mahadashas.items())[:3], 1):
                        print(f"  {i}. {lord}: {md.get('start')} to {md.get('end')}")

        # Test divisional charts
        print("\nDivisional Charts Available:")
        if hasattr(chart, 'divisional_charts') and chart.divisional_charts:
            for chart_key in sorted(chart.divisional_charts.keys()):
                print(f"  ✓ {chart_key.upper()}")

        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("\nThe MCP server is ready to use.")
        return True

    except Exception as e:
        print(f"\n✗ Error during calculation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    load_env_file()
    cli_args = parse_args()
    success = test_birth_chart(cli_args)
    exit(0 if success else 1)
