#!/bin/bash
# Setup script for Vedic Astrology MCP Server

set -e

echo "=================================================="
echo "Vedic Astrology MCP Server - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "Error: Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✓ Dependencies installed successfully!"
echo ""

# Test the installation
echo "Testing jyotishganit library..."
python3 -c "import jyotishganit; print('✓ jyotishganit library imported successfully')" || {
    echo "✗ Failed to import jyotishganit"
    exit 1
}

python3 -c "import mcp; print('✓ MCP SDK imported successfully')" || {
    echo "✗ Failed to import MCP SDK"
    exit 1
}

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure Claude Desktop to use this server:"
echo "   Add the following to your claude_desktop_config.json:"
echo ""
echo "   {"
echo "     \"mcpServers\": {"
echo "       \"vedic-astrology\": {"
echo "         \"command\": \"python\","
echo "         \"args\": [\"$(pwd)/vedic_astrology_server.py\"]"
echo "       }"
echo "     }"
echo "   }"
echo ""
echo "2. Configuration file locations:"
echo "   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   Windows: %APPDATA%/Claude/claude_desktop_config.json"
echo ""
echo "3. Restart Claude Desktop after adding the configuration"
echo ""
echo "4. Test the server with sample queries from EXAMPLES.md"
echo ""
echo "For more information, see README.md"
echo ""
