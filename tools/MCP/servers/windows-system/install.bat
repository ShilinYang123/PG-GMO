@echo off
REM Windows System MCP Server Installation Script

echo Installing Windows System MCP Server...
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

echo Python version:
%PYTHON_PATH% --version

REM Install required packages
echo Installing required packages...
%PYTHON_PATH% -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install required packages
    echo Trying to install packages individually...
    
    echo Installing mcp...
    %PYTHON_PATH% -m pip install mcp
    
    echo Installing psutil...
    %PYTHON_PATH% -m pip install psutil
    
    echo Installing pywin32...
    %PYTHON_PATH% -m pip install pywin32
    
    if %errorlevel% neq 0 (
        echo Error: Failed to install packages
        pause
        exit /b 1
    )
)

echo Installation completed successfully!

echo.
echo To start the server, run:
echo   start_server.bat
echo.

pause