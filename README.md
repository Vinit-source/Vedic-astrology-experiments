# Vedic Astrology MCP Server

An MCP (Model Context Protocol) server for authentic Vedic astrology calculations using the [jyotishganit](https://github.com/northtara/jyotishganit) library. This server enables LLMs and CLI tools to perform precise astrological analysis based on birth data.

## Features

This MCP server provides comprehensive Vedic astrology tools including:

### Basic Birth Details
- Name, Date, Time, and Place of birth
- Latitude and Longitude coordinates
- Timezone information
- Sunrise and Sunset times
- Ayanamsha (sidereal offset) value

### Panchanga (Five-Limb Almanac)
- **Tithi** - Lunar day
- **Nakshatra** - Lunar constellation (with Pada/quarter)
- **Yoga** - Sun-Moon combination
- **Karana** - Half lunar day
- **Vaara** - Weekday

### Avakhada Details
- **Varna** - Social classification
- **Vashya** - Influence type
- **Yoni** - Animal nature
- **Gan** - Temperament (Deva/Manushya/Rakshasa)
- **Nadi** - Pulse/energy type
- **Sign** - Moon sign (Rashi)
- **Sign Lord** - Ruler of the Moon sign
- **Nakshatra-Charan** - Birth star with quarter

### Planetary Analysis
- Positions of all 9 Vedic planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
- Sign placement and degrees
- Nakshatra and Pada for each planet
- House placement
- Sign lords
- **Shadbala** - Six-fold planetary strength analysis:
  - Positional Strength (Sthanabala)
  - Temporal Strength (Kaalabala)
  - Directional Strength (Digbala)
  - Motional Strength (Cheshtabala)
  - Natural Strength (Naisargikabala)
  - Aspectual Strength (Drikbala)

### Vimshottari Dashas
- Current Mahadasha (major planetary period)
- Current Antardasha (sub-period)
- Upcoming Mahadasha periods with start and end dates

### Divisional Charts (Vargas)
Complete D1-D60 divisional chart calculations:
- **D1** - Rasi (General life and personality)
- **D2** - Hora (Wealth and finances)
- **D3** - Drekkana (Siblings and courage)
- **D4** - Chaturthamsa (Property and assets)
- **D7** - Saptamsa (Children and progeny)
- **D9** - Navamsa (Marriage and dharma)
- **D10** - Dasamsa (Career and profession)
- **D12** - Dwadasamsa (Parents and ancestors)
- **D16** - Shodasamsa (Vehicles and comforts)
- **D24** - Chaturvimsamsa (Education)
- **D27** - Bhamsha (Physical strength)
- **D30** - Trimsamsa (Misfortunes)
- **D60** - Shashtiamsa (Past life karma)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Vinit-source/Vedic-astrology-experiments.git
cd Vedic-astrology-experiments
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

The main dependencies are:
- `jyotishganit` - Professional Vedic astrology calculation library with NASA JPL ephemeris
- `mcp` - Model Context Protocol SDK

## Usage

### Running the MCP Server

The server communicates via stdio (standard input/output):

```bash
python vedic_astrology_server.py
```

### Using with Claude Desktop

To use this server with Claude Desktop, add it to your Claude configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "vedic-astrology": {
      "command": "python",
      "args": ["/absolute/path/to/vedic_astrology_server.py"]
    }
  }
}
```

Replace `/absolute/path/to/` with the actual path to the server file.

### Available Tools

#### 1. `calculate_complete_birth_chart`
Returns a comprehensive birth chart with all astrological details including panchanga, planetary positions, divisional charts, dashas, and more.

**Example:**
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

#### 2. `get_basic_details`
Returns basic birth information including name, date, time, place, coordinates, timezone, and ayanamsha.

#### 3. `get_panchanga_details`
Returns Panchanga elements (Tithi, Nakshatra, Yoga, Karana, Vaara) and Avakhada details (Varna, Vashya, Yoni, Gan, Nadi).

#### 4. `get_planetary_positions`
Returns detailed positions of all 9 Vedic planets with their sign, degrees, nakshatra, pada, house, and Shadbala strengths.

#### 5. `get_vimshottari_dashas`
Returns current and upcoming Vimshottari Dasha periods (Mahadasha and Antardasha).

#### 6. `get_divisional_charts`
Returns all divisional charts (D1-D60) with planetary positions in each chart.

### Example Usage with LLM

When connected to an LLM (like Claude), you can ask questions like:

- "Calculate the birth chart for a person born on July 4, 1996, at 9:10 AM in Karmala, India (18.404°N, 75.195°E)"
- "What is the current Mahadasha for someone born on..."
- "Show me the planetary positions and strengths for..."
- "What does the Navamsa chart show for..."
- "Get the Panchanga details for a birth at..."

## Timezone Reference

Common timezone offsets from UTC:
- **IST (India):** 5.5
- **EST (US East):** -5 (or -4 during DST)
- **PST (US West):** -8 (or -7 during DST)
- **GMT/UTC:** 0
- **CST (China):** 8
- **JST (Japan):** 9

## Technical Details

### Astronomical Accuracy
- Uses NASA JPL DE421 ephemeris data via Skyfield
- True Chitra Paksha Ayanamsa based on Spica star
- Precise planetary positions accurate to arc-seconds
- Traditional whole sign house system

### Calculation Methods
All calculations follow classical Vedic texts including:
- Brihat Parashara Hora Shastra
- Saravali
- Surya Siddhanta

### Data Storage
Ephemeris data is cached in platform-appropriate locations:
- **Windows:** `%LOCALAPPDATA%\jyotishganit\`
- **macOS:** `~/Library/Application Support/jyotishganit/`
- **Linux:** `~/.local/share/jyotishganit/`

## Development

### Project Structure
```
Vedic-astrology-experiments/
├── vedic_astrology_server.py   # Main MCP server implementation
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
└── package.json                 # Node.js metadata (optional)
```

### Testing the Server

You can test the server manually using a simple Python script:

```python
import asyncio
import json
from datetime import datetime
from jyotishganit import calculate_birth_chart, get_birth_chart_json

# Test birth data
birth_date = datetime(1996, 7, 4, 9, 10, 0)
chart = calculate_birth_chart(
    birth_date=birth_date,
    latitude=18.404,
    longitude=75.195,
    timezone_offset=5.5,
    name="Test Person"
)

# Print results
print(f"Ascendant: {chart.d1_chart.houses[0].sign}")
print(f"Moon Sign: {chart.d1_chart.planets[1].sign}")
print(f"Nakshatra: {chart.panchanga.nakshatra}")
print(f"Tithi: {chart.panchanga.tithi}")
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Areas for Enhancement
- Additional Dasha systems (Yogini, Chara, etc.)
- Ashtakavarga calculations
- Graha Drishti (planetary aspects)
- Yoga combinations detection
- Transit analysis
- Muhurta (electional astrology)

## License

ISC License

## Acknowledgments

- **jyotishganit** - Professional Vedic astrology library by [northtara](https://github.com/northtara)
- **MCP** - Model Context Protocol by Anthropic
- Built with reverence for the ancient science of Jyotisha

---

*॥ श्री कृष्णार्पणमस्तु ॥*
