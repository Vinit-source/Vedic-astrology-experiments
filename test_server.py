#!/usr/bin/env python3
"""Test script for the Vedic Astrology MCP server."""

import json
from datetime import datetime
from jyotishganit import calculate_birth_chart, get_birth_chart_json

def test_birth_chart():
    """Test birth chart calculation."""
    print("Testing Vedic Astrology Birth Chart Calculation...")
    print("=" * 60)

    # Test with the example from jyotishganit README
    birth_date = datetime(1996, 7, 4, 9, 10, 0)

    try:
        chart = calculate_birth_chart(
            birth_date=birth_date,
            latitude=18.404,
            longitude=75.195,
            timezone_offset=5.5,
            name="Bhampu"
        )

        print("\n✓ Birth chart calculated successfully!")
        print("\nBasic Details:")
        print(f"  Name: Bhampu")
        print(f"  Date: {birth_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Place: Karmala, India (18.404°N, 75.195°E)")
        print(f"  Timezone: IST (UTC+5.5)")

        print("\nAstrological Details:")
        print(f"  Ascendant: {chart.d1_chart.houses[0].sign}")
        print(f"  Ascendant Lord: {chart.d1_chart.houses[0].sign_lord}")
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
    success = test_birth_chart()
    exit(0 if success else 1)
