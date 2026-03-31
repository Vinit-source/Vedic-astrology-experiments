# Example Queries for Vedic Astrology MCP Server

This document provides example queries and use cases for the Vedic Astrology MCP server.

**Note:** The server now uses location-based geocoding. Simply provide location names (e.g., "Chennai", "Mumbai") instead of coordinates and timezone. The Geoapify API automatically converts locations to precise coordinates and timezone information.

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
  "location": "Karmala, India"
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
  "location": "New Delhi, India"
}
```

### Example 3: Mumbai Birth
```json
{
  "name": "Test Person",
  "year": 1985,
  "month": 3,
  "day": 20,
  "hour": 6,
  "minute": 45,
  "second": 0,
  "location": "Mumbai"
}
```

## Example Queries to Ask Claude

Once the MCP server is configured with Claude Desktop, you can ask questions like:

### Complete Birth Chart Analysis
```
Calculate the complete birth chart for a person named Bhampu, born on July 4, 1996,
at 9:10 AM in Karmala, India
```

### Basic Details Query
```
Get the basic birth details for someone born on January 15, 1990, at 2:30 PM
in New Delhi, India
```

### Panchanga Details
```
What are the Panchanga details (Tithi, Nakshatra, Yoga, Karana) for a person
born on July 4, 1996, at 9:10 AM in Karmala, India?
```

### Planetary Positions and Strengths
```
Show me the planetary positions and Shadbala strengths for a birth on
July 4, 1996, at 9:10 AM in Karmala, India
```

### Vimshottari Dashas
```
What is the current Mahadasha and upcoming Dasha periods for someone born on
July 4, 1996, at 9:10 AM in Karmala, India?
```

### Divisional Charts
```
Get the Navamsa (D9) chart for a person born on July 4, 1996, at 9:10 AM
in Karmala, India
```

### Comprehensive Analysis Questions
```
Analyze the birth chart of Bhampu (born July 4, 1996, 9:10 AM, Karmala, India) and tell me about:
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
  "place": "Karmala, Maharashtra, India",
  "latitude": 18.404,
  "longitude": 75.195,
  "timezone_offset": 5.5,
  "ayanamsha": "23.88..."
}
```

**Note:** Latitude, longitude, and timezone_offset are automatically geocoded from the location name.

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

## Common Location Examples

You can use any of these location names with the server (automatic geocoding):

| City | Example Usage |
|------|---------------|
| Mumbai | "Mumbai", "Mumbai, India" |
| Delhi | "Delhi", "New Delhi", "New Delhi, India" |
| Bangalore | "Bangalore", "Bengaluru", "Bangalore, Karnataka" |
| Chennai | "Chennai", "Chennai, Tamil Nadu" |
| Kolkata | "Kolkata", "Kolkata, West Bengal" |
| Pune | "Pune", "Pune, Maharashtra" |
| Hyderabad | "Hyderabad", "Hyderabad, Telangana" |
| Ahmedabad | "Ahmedabad", "Ahmedabad, Gujarat" |
| Jaipur | "Jaipur", "Jaipur, Rajasthan" |
| Varanasi | "Varanasi", "Varanasi, Uttar Pradesh" |

## Tips for Best Results

1. **Always provide complete birth data**: Name, date, time, and location name
2. **Use clear location names**: e.g., "Mumbai, India" or "New Delhi" for better geocoding accuracy
3. **No need for coordinates**: The server automatically geocodes location names
4. **No need for timezone**: Timezone is automatically detected from the location
5. **Be specific** in your questions - ask for particular aspects of the chart
6. **Interpret results** - Ask Claude to explain what the astrological data means

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
