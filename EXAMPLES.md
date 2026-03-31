# Example Queries for Vedic Astrology MCP Server

This document provides example queries and use cases for the Vedic Astrology MCP server.

## Sample Birth Data

Here are some sample birth details you can use for testing:

### Example 1: Bhampu (from jyotishganit documentation)
```json
{
  "name": "Bhampu",
  "year": 1996,
  "month": 7,
  "day": 4,
  "hour": 9,
  "minute": 10,
  "second": 0,
  "latitude": 18.404,
  "longitude": 75.195,
  "timezone_offset": 5.5,
  "location_name": "Karmala, India"
}
```

### Example 2: Sample Delhi Birth
```json
{
  "name": "Sample Person",
  "year": 1990,
  "month": 1,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "second": 0,
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone_offset": 5.5,
  "location_name": "New Delhi, India"
}
```

## Example Queries to Ask Claude

Once the MCP server is configured with Claude Desktop, you can ask questions like:

### Complete Birth Chart Analysis
```
Calculate the complete birth chart for a person named Bhampu, born on July 4, 1996,
at 9:10 AM in Karmala, India (latitude: 18.404, longitude: 75.195, timezone: IST/UTC+5.5)
```

### Basic Details Query
```
Get the basic birth details for someone born on January 15, 1990, at 2:30 PM
in New Delhi (28.6139°N, 77.2090°E, IST)
```

### Panchanga Details
```
What are the Panchanga details (Tithi, Nakshatra, Yoga, Karana) for a person
born on July 4, 1996, at 9:10 AM in Karmala, India (18.404°N, 75.195°E, IST)?
```

### Planetary Positions and Strengths
```
Show me the planetary positions and Shadbala strengths for a birth on
July 4, 1996, at 9:10 AM in Karmala, India (18.404°N, 75.195°E, UTC+5.5)
```

### Vimshottari Dashas
```
What is the current Mahadasha and upcoming Dasha periods for someone born on
July 4, 1996, at 9:10 AM in Karmala, India (18.404°N, 75.195°E, IST)?
```

### Divisional Charts
```
Get the Navamsa (D9) chart for a person born on July 4, 1996, at 9:10 AM
in Karmala, India (18.404°N, 75.195°E, IST)
```

### Comprehensive Analysis Questions
```
Analyze the birth chart of Bhampu (born July 4, 1996, 9:10 AM, Karmala, India,
18.404°N, 75.195°E, IST) and tell me about:
- The ascendant and moon sign
- The planetary strengths (Shadbala)
- The current Dasha period
- What the Navamsa chart reveals
```

## Expected Response Format

The server returns data in JSON format. Here's what you can expect:

### Basic Details Response
```json
{
  "name": "Bhampu",
  "date": "1996-07-04",
  "time": "09:10:00",
  "place": "Karmala, India",
  "latitude": 18.404,
  "longitude": 75.195,
  "timezone_offset": 5.5,
  "ayanamsha": "23.88..."
}
```

### Panchanga Details Response
```json
{
  "tithi": "Krishna Chaturthi",
  "nakshatra": "Dhanishta",
  "nakshatra_pada": 2,
  "yoga": "Priti",
  "karana": "Balava",
  "vaara": "Thursday",
  "moon_sign": "Aquarius",
  "moon_sign_lord": "Saturn",
  "ascendant_sign": "Leo",
  "ascendant_lord": "Sun"
}
```

### Planetary Position Sample
```json
{
  "planet": "Jupiter",
  "sign": "Sagittarius",
  "degrees": 15.42,
  "nakshatra": "Purva Ashadha",
  "pada": 2,
  "house": 5,
  "sign_lord": "Jupiter",
  "dignity": "own sign",
  "shadbala": {
    "total": 587.09,
    "rupas": 9.79,
    "positional_strength": 130.87,
    "temporal_strength": 222.92,
    "directional_strength": 48.78,
    "motional_strength": 117.13,
    "natural_strength": 60.00,
    "aspectual_strength": 7.39
  }
}
```

## Common Locations and Coordinates

For convenience, here are coordinates for major Indian cities:

| City | Latitude | Longitude |
|------|----------|-----------|
| Mumbai | 19.0760 | 72.8777 |
| Delhi | 28.6139 | 77.2090 |
| Bangalore | 12.9716 | 77.5946 |
| Chennai | 13.0827 | 80.2707 |
| Kolkata | 22.5726 | 88.3639 |
| Pune | 18.5204 | 73.8567 |
| Hyderabad | 17.3850 | 78.4867 |
| Ahmedabad | 23.0225 | 72.5714 |
| Jaipur | 26.9124 | 75.7873 |
| Varanasi | 25.3176 | 82.9739 |

## Timezone Reference

Common timezone offsets:
- **IST (India Standard Time)**: 5.5
- **EST (Eastern Standard Time)**: -5 (or -4 during DST)
- **PST (Pacific Standard Time)**: -8 (or -7 during DST)
- **GMT/UTC**: 0
- **CST (China Standard Time)**: 8
- **JST (Japan Standard Time)**: 9
- **AEDT (Australian Eastern Daylight Time)**: 11

## Tips for Best Results

1. **Always provide complete birth data**: Name, date, time, location coordinates, and timezone
2. **Use decimal degrees** for latitude and longitude (not degrees/minutes/seconds)
3. **Timezone offset** should be in decimal hours from UTC (e.g., 5.5 for IST, not 5:30)
4. **Be specific** in your questions - ask for particular aspects of the chart
5. **Interpret results** - Ask Claude to explain what the astrological data means

## Advanced Queries

### Comparative Analysis
```
Compare the planetary strengths in the D1 chart versus the D9 chart for
Bhampu (July 4, 1996, 9:10 AM, Karmala, India)
```

### Specific Planet Analysis
```
What is the strength and position of Jupiter in all divisional charts for
someone born on July 4, 1996, at 9:10 AM in Karmala, India?
```

### Dasha Interpretation
```
Based on the current Mahadasha for Bhampu (born July 4, 1996), what can you
tell me about this planetary period?
```
