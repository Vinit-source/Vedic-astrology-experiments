@echo off
REM Setup script for Vedic Astrology MCP Server (Windows)

echo ==================================================
echo Vedic Astrology MCP Server - Setup
echo ==================================================
echo.

REM Check Python version
echo Checking Python version...
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% detected
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Test the installation
echo Testing jyotishganit library...
python -c "import jyotishganit; print('jyotishganit library imported successfully')" > nul 2>&1
if errorlevel 1 (
    echo Failed to import jyotishganit
    exit /b 1
)
echo jyotishganit library OK

python -c "import mcp; print('MCP SDK imported successfully')" > nul 2>&1
if errorlevel 1 (
    echo Failed to import MCP SDK
    exit /b 1
)
echo MCP SDK OK

echo.
echo ==================================================
echo Setup Complete!
echo ==================================================
echo.
echo Next steps:
echo.
echo 1. Configure Claude Desktop to use this server:
echo    Add the following to your claude_desktop_config.json:
echo.
echo    {
echo      "mcpServers": {
echo        "vedic-astrology": {
echo          "command": "python",
echo          "args": ["%CD%\\vedic_astrology_server.py"]
echo        }
echo      }
echo    }
echo.
echo 2. Configuration file location:
echo    %%APPDATA%%\Claude\claude_desktop_config.json
echo.
echo 3. Restart Claude Desktop after adding the configuration
echo.
echo 4. Test the server with sample queries from EXAMPLES.md
echo.
echo For more information, see README.md
echo.
pause
