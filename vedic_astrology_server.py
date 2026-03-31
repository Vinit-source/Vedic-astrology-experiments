#!/usr/bin/env python3
"""
MCP Server for Vedic Astrology Analysis using jyotishganit library.

This server provides tools to calculate and analyze Vedic birth charts, including:
- Basic birth details (Name, Date, Time, Place, etc.)
- Panchanga details (Tithi, Nakshatra, Yoga, Karana, etc.)
- Planetary positions and strengths
- Vimshottari Dashas
- All divisional charts (D1-D60)
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

try:
    from jyotishganit import calculate_birth_chart, get_birth_chart_json
except ImportError:
    print("Error: jyotishganit library not found. Please install it using: pip install jyotishganit")
    raise

# Create server instance
server = Server("vedic-astrology-server")


class BirthData(BaseModel):
    """Birth data required for astrological calculations."""
    name: str = Field(description="Name of the person")
    year: int = Field(description="Year of birth")
    month: int = Field(description="Month of birth (1-12)")
    day: int = Field(description="Day of birth")
    hour: int = Field(description="Hour of birth (0-23)")
    minute: int = Field(description="Minute of birth (0-59)")
    second: int = Field(default=0, description="Second of birth (0-59)")
    latitude: float = Field(description="Latitude of birth place")
    longitude: float = Field(description="Longitude of birth place")
    timezone_offset: float = Field(description="Timezone offset from UTC in hours (e.g., 5.5 for IST)")
    location_name: Optional[str] = Field(default=None, description="Name of birth place")


def parse_birth_data(arguments: Dict[str, Any]) -> BirthData:
    """Parse and validate birth data from arguments."""
    return BirthData(**arguments)


def get_birth_chart(birth_data: BirthData):
    """Calculate birth chart using jyotishganit."""
    birth_date = datetime(
        birth_data.year,
        birth_data.month,
        birth_data.day,
        birth_data.hour,
        birth_data.minute,
        birth_data.second
    )

    return calculate_birth_chart(
        birth_date=birth_date,
        latitude=birth_data.latitude,
        longitude=birth_data.longitude,
        timezone_offset=birth_data.timezone_offset,
        location_name=birth_data.location_name,
        name=birth_data.name
    )


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="calculate_complete_birth_chart",
            description=(
                "Calculate a complete Vedic birth chart with all astrological details. "
                "Returns comprehensive analysis including basic details, panchanga, "
                "planetary positions, divisional charts, dashas, and more. "
                "This is the most comprehensive tool and includes all information."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the person"},
                    "year": {"type": "integer", "description": "Year of birth"},
                    "month": {"type": "integer", "description": "Month of birth (1-12)"},
                    "day": {"type": "integer", "description": "Day of birth"},
                    "hour": {"type": "integer", "description": "Hour of birth (0-23)"},
                    "minute": {"type": "integer", "description": "Minute of birth (0-59)"},
                    "second": {"type": "integer", "description": "Second of birth (0-59)", "default": 0},
                    "latitude": {"type": "number", "description": "Latitude of birth place"},
                    "longitude": {"type": "number", "description": "Longitude of birth place"},
                    "timezone_offset": {
                        "type": "number",
                        "description": "Timezone offset from UTC in hours (e.g., 5.5 for IST, -5 for EST)"
                    },
                    "location_name": {
                        "type": "string",
                        "description": "Name of birth place (optional)"
                    }
                },
                "required": ["name", "year", "month", "day", "hour", "minute", "latitude", "longitude", "timezone_offset"]
            }
        ),
        Tool(
            name="get_basic_details",
            description=(
                "Get basic birth details including name, date, time, place, latitude, "
                "longitude, timezone, sunrise, sunset, and ayanamsha."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the person"},
                    "year": {"type": "integer", "description": "Year of birth"},
                    "month": {"type": "integer", "description": "Month of birth (1-12)"},
                    "day": {"type": "integer", "description": "Day of birth"},
                    "hour": {"type": "integer", "description": "Hour of birth (0-23)"},
                    "minute": {"type": "integer", "description": "Minute of birth (0-59)"},
                    "second": {"type": "integer", "description": "Second of birth (0-59)", "default": 0},
                    "latitude": {"type": "number", "description": "Latitude of birth place"},
                    "longitude": {"type": "number", "description": "Longitude of birth place"},
                    "timezone_offset": {"type": "number", "description": "Timezone offset from UTC in hours"},
                    "location_name": {"type": "string", "description": "Name of birth place (optional)"}
                },
                "required": ["name", "year", "month", "day", "hour", "minute", "latitude", "longitude", "timezone_offset"]
            }
        ),
        Tool(
            name="get_panchanga_details",
            description=(
                "Get Panchanga (five-limb almanac) details including Tithi, Nakshatra, "
                "Nakshatra Pada, Yoga, Karana, Vaara (weekday), Varna, Vashya, Yoni, "
                "Gan, Nadi, Sign, Sign Lord, and other Avakhada details."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the person"},
                    "year": {"type": "integer", "description": "Year of birth"},
                    "month": {"type": "integer", "description": "Month of birth (1-12)"},
                    "day": {"type": "integer", "description": "Day of birth"},
                    "hour": {"type": "integer", "description": "Hour of birth (0-23)"},
                    "minute": {"type": "integer", "description": "Minute of birth (0-59)"},
                    "second": {"type": "integer", "description": "Second of birth (0-59)", "default": 0},
                    "latitude": {"type": "number", "description": "Latitude of birth place"},
                    "longitude": {"type": "number", "description": "Longitude of birth place"},
                    "timezone_offset": {"type": "number", "description": "Timezone offset from UTC in hours"},
                    "location_name": {"type": "string", "description": "Name of birth place (optional)"}
                },
                "required": ["name", "year", "month", "day", "hour", "minute", "latitude", "longitude", "timezone_offset"]
            }
        ),
        Tool(
            name="get_planetary_positions",
            description=(
                "Get detailed planetary positions for all 9 Vedic planets (Sun, Moon, Mars, "
                "Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) including their sign, degrees, "
                "nakshatra, pada, house, dignities, and Shadbala (six-fold strength) calculations."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the person"},
                    "year": {"type": "integer", "description": "Year of birth"},
                    "month": {"type": "integer", "description": "Month of birth (1-12)"},
                    "day": {"type": "integer", "description": "Day of birth"},
                    "hour": {"type": "integer", "description": "Hour of birth (0-23)"},
                    "minute": {"type": "integer", "description": "Minute of birth (0-59)"},
                    "second": {"type": "integer", "description": "Second of birth (0-59)", "default": 0},
                    "latitude": {"type": "number", "description": "Latitude of birth place"},
                    "longitude": {"type": "number", "description": "Longitude of birth place"},
                    "timezone_offset": {"type": "number", "description": "Timezone offset from UTC in hours"},
                    "location_name": {"type": "string", "description": "Name of birth place (optional)"}
                },
                "required": ["name", "year", "month", "day", "hour", "minute", "latitude", "longitude", "timezone_offset"]
            }
        ),
        Tool(
            name="get_vimshottari_dashas",
            description=(
                "Get Vimshottari Dasha periods - the planetary time periods system used in "
                "Vedic astrology. Returns current Mahadasha, Antardasha, and upcoming periods."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the person"},
                    "year": {"type": "integer", "description": "Year of birth"},
                    "month": {"type": "integer", "description": "Month of birth (1-12)"},
                    "day": {"type": "integer", "description": "Day of birth"},
                    "hour": {"type": "integer", "description": "Hour of birth (0-23)"},
                    "minute": {"type": "integer", "description": "Minute of birth (0-59)"},
                    "second": {"type": "integer", "description": "Second of birth (0-59)", "default": 0},
                    "latitude": {"type": "number", "description": "Latitude of birth place"},
                    "longitude": {"type": "number", "description": "Longitude of birth place"},
                    "timezone_offset": {"type": "number", "description": "Timezone offset from UTC in hours"},
                    "location_name": {"type": "string", "description": "Name of birth place (optional)"}
                },
                "required": ["name", "year", "month", "day", "hour", "minute", "latitude", "longitude", "timezone_offset"]
            }
        ),
        Tool(
            name="get_divisional_charts",
            description=(
                "Get all divisional charts (Varga Chakras) from D1 to D60. Each divisional "
                "chart provides specific insights: D1 (general life), D2 (wealth), D3 (siblings), "
                "D4 (property), D7 (children), D9 (marriage/dharma), D10 (career), D12 (parents), "
                "D16 (vehicles), D24 (education), D27 (strength), D30 (misfortunes), D60 (karma)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the person"},
                    "year": {"type": "integer", "description": "Year of birth"},
                    "month": {"type": "integer", "description": "Month of birth (1-12)"},
                    "day": {"type": "integer", "description": "Day of birth"},
                    "hour": {"type": "integer", "description": "Hour of birth (0-23)"},
                    "minute": {"type": "integer", "description": "Minute of birth (0-59)"},
                    "second": {"type": "integer", "description": "Second of birth (0-59)", "default": 0},
                    "latitude": {"type": "number", "description": "Latitude of birth place"},
                    "longitude": {"type": "number", "description": "Longitude of birth place"},
                    "timezone_offset": {"type": "number", "description": "Timezone offset from UTC in hours"},
                    "location_name": {"type": "string", "description": "Name of birth place (optional)"}
                },
                "required": ["name", "year", "month", "day", "hour", "minute", "latitude", "longitude", "timezone_offset"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls."""
    try:
        birth_data = parse_birth_data(arguments)
        chart = get_birth_chart(birth_data)

        if name == "calculate_complete_birth_chart":
            # Return complete chart as JSON
            chart_json = get_birth_chart_json(chart)
            return [TextContent(
                type="text",
                text=json.dumps(chart_json, indent=2, default=str)
            )]

        elif name == "get_basic_details":
            # Extract basic details
            basic_details = {
                "name": birth_data.name,
                "date": f"{birth_data.year}-{birth_data.month:02d}-{birth_data.day:02d}",
                "time": f"{birth_data.hour:02d}:{birth_data.minute:02d}:{birth_data.second:02d}",
                "place": birth_data.location_name or f"Lat: {birth_data.latitude}, Lon: {birth_data.longitude}",
                "latitude": birth_data.latitude,
                "longitude": birth_data.longitude,
                "timezone_offset": birth_data.timezone_offset,
                "ayanamsha": chart.ayanamsa.value if hasattr(chart.ayanamsa, 'value') else str(chart.ayanamsa)
            }

            return [TextContent(
                type="text",
                text=json.dumps(basic_details, indent=2)
            )]

        elif name == "get_panchanga_details":
            # Extract panchanga and moon details
            moon = chart.d1_chart.planets[1]  # Moon is index 1

            panchanga_details = {
                "tithi": chart.panchanga.tithi,
                "nakshatra": chart.panchanga.nakshatra,
                "nakshatra_pada": moon.pada,
                "yoga": chart.panchanga.yoga,
                "karana": chart.panchanga.karana,
                "vaara": chart.panchanga.vaara,
                "moon_sign": moon.sign,
                "moon_sign_lord": moon.sign_lord,
                "moon_nakshatra": moon.nakshatra,
                "ascendant_sign": chart.d1_chart.houses[0].sign,
                "ascendant_lord": chart.d1_chart.houses[0].sign_lord
            }

            # Add Avakhada details if available
            if hasattr(moon, 'dignities'):
                dignities = moon.dignities
                if hasattr(dignities, 'varna'):
                    panchanga_details['varna'] = dignities.varna
                if hasattr(dignities, 'vashya'):
                    panchanga_details['vashya'] = dignities.vashya
                if hasattr(dignities, 'yoni'):
                    panchanga_details['yoni'] = dignities.yoni
                if hasattr(dignities, 'gan'):
                    panchanga_details['gan'] = dignities.gan
                if hasattr(dignities, 'nadi'):
                    panchanga_details['nadi'] = dignities.nadi

            return [TextContent(
                type="text",
                text=json.dumps(panchanga_details, indent=2)
            )]

        elif name == "get_planetary_positions":
            # Extract planetary positions
            planets_info = []

            for planet in chart.d1_chart.planets:
                planet_data = {
                    "planet": planet.celestial_body,
                    "sign": planet.sign,
                    "degrees": planet.sign_degrees,
                    "nakshatra": planet.nakshatra,
                    "pada": planet.pada,
                    "house": planet.house,
                    "sign_lord": planet.sign_lord,
                }

                # Add dignities if available
                if hasattr(planet, 'dignities'):
                    planet_data['dignity'] = planet.dignities.dignity if hasattr(planet.dignities, 'dignity') else str(planet.dignities)

                # Add Shadbala (six-fold strength) if available
                if hasattr(planet, 'shadbala') and planet.shadbala:
                    shadbala = planet.shadbala.get('Shadbala', {})
                    if shadbala:
                        planet_data['shadbala'] = {
                            'total': shadbala.get('Total'),
                            'rupas': shadbala.get('Rupas'),
                            'positional_strength': shadbala.get('Sthanabala'),
                            'temporal_strength': shadbala.get('Kaalabala'),
                            'directional_strength': shadbala.get('Digbala'),
                            'motional_strength': shadbala.get('Cheshtabala'),
                            'natural_strength': shadbala.get('Naisargikabala'),
                            'aspectual_strength': shadbala.get('Drikbala')
                        }

                planets_info.append(planet_data)

            return [TextContent(
                type="text",
                text=json.dumps(planets_info, indent=2, default=str)
            )]

        elif name == "get_vimshottari_dashas":
            # Extract Vimshottari Dasha information
            dashas_info = {
                "current_mahadasha": None,
                "current_antardasha": None,
                "upcoming_mahadashas": []
            }

            if hasattr(chart, 'dashas') and chart.dashas:
                dashas = chart.dashas

                # Get current and upcoming mahadashas
                if hasattr(dashas, 'current') and dashas.current:
                    current = dashas.current
                    if 'mahadasha' in current:
                        dashas_info['current_mahadasha'] = current['mahadasha']
                    if 'antardasha' in current:
                        dashas_info['current_antardasha'] = current['antardasha']

                if hasattr(dashas, 'upcoming') and dashas.upcoming:
                    upcoming = dashas.upcoming
                    if 'mahadashas' in upcoming:
                        mahadashas = upcoming['mahadashas']
                        for lord, md in list(mahadashas.items())[:5]:  # First 5 upcoming
                            dashas_info['upcoming_mahadashas'].append({
                                'lord': lord,
                                'start': str(md.get('start')),
                                'end': str(md.get('end'))
                            })

            return [TextContent(
                type="text",
                text=json.dumps(dashas_info, indent=2)
            )]

        elif name == "get_divisional_charts":
            # Extract divisional charts information
            charts_info = {}

            # D1 chart (main chart)
            charts_info['d1'] = extract_chart_data(chart.d1_chart, "D1 - Rasi (General Life)")

            # Other divisional charts
            if hasattr(chart, 'divisional_charts') and chart.divisional_charts:
                chart_names = {
                    'd2': 'D2 - Hora (Wealth)',
                    'd3': 'D3 - Drekkana (Siblings)',
                    'd4': 'D4 - Chaturthamsa (Property)',
                    'd7': 'D7 - Saptamsa (Children)',
                    'd9': 'D9 - Navamsa (Marriage/Dharma)',
                    'd10': 'D10 - Dasamsa (Career)',
                    'd12': 'D12 - Dwadasamsa (Parents)',
                    'd16': 'D16 - Shodasamsa (Vehicles)',
                    'd24': 'D24 - Chaturvimsamsa (Education)',
                    'd27': 'D27 - Bhamsha (Strength)',
                    'd30': 'D30 - Trimsamsa (Misfortunes)',
                    'd60': 'D60 - Shashtiamsa (Karma)'
                }

                for chart_key, chart_name in chart_names.items():
                    if chart_key in chart.divisional_charts:
                        div_chart = chart.divisional_charts[chart_key]
                        charts_info[chart_key] = extract_chart_data(div_chart, chart_name)

            return [TextContent(
                type="text",
                text=json.dumps(charts_info, indent=2)
            )]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


def extract_chart_data(chart_obj, chart_name: str) -> Dict:
    """Extract chart data in a readable format."""
    chart_data = {
        "chart_name": chart_name,
        "houses": [],
        "planets": []
    }

    # Extract house information
    for i, house in enumerate(chart_obj.houses, 1):
        house_info = {
            "house_number": i,
            "sign": house.sign,
            "sign_lord": house.sign_lord,
            "occupants": [p.celestial_body for p in house.occupants] if hasattr(house, 'occupants') else []
        }
        chart_data["houses"].append(house_info)

    # Extract planet positions
    for planet in chart_obj.planets:
        planet_info = {
            "planet": planet.celestial_body,
            "sign": planet.sign,
            "degrees": planet.sign_degrees,
            "house": planet.house
        }
        chart_data["planets"].append(planet_info)

    return chart_data


async def main():
    """Run the server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
