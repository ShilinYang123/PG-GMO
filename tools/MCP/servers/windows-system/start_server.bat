@echo off
REM Windows System MCP Server Start Script

echo Starting Windows System MCP Server...
echo ======================================

REM Use Python from the project's virtual environment
set PYTHON_PATH=s:\PG-GMO\.venv\Scripts\python.exe

REM Check if Python is available
%PYTHON_PATH% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed in the project virtual environment
    echo Please ensure the project virtual environment is properly set up
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking for required packages...
%PYTHON_PATH% -c "import mcp.server.fastmcp; import psutil; import win32api" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    %PYTHON_PATH% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Error: Failed to install required packages
        pause
        exit /b 1
    )
)

echo Starting server on http://127.0.0.1:8001
echo Press Ctrl+C to stop the server
echo.

%PYTHON_PATH% server.py

pause