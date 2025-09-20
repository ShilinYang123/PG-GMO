# Windows System MCP Server

## Overview
This MCP (Model Context Protocol) server provides direct Windows system control capabilities, allowing AI assistants to execute commands, manage processes, and interact with the Windows operating system.

## Features
- Execute Windows commands and scripts
- List and monitor running processes
- Retrieve system information (CPU, memory, disk usage)
- File operations (read, write, delete)
- Window management (list, minimize, maximize, close)

## Installation

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. The server requires Python for Windows Extensions (pywin32) which may need separate installation:
   ```bash
   pip install pywin32
   ```

## Configuration
The server can be configured using environment variables:

- `FASTMCP_HOST`: Host to bind to (default: 127.0.0.1)
- `FASTMCP_PORT`: Port to listen on (default: 8001)
- `FASTMCP_DEBUG`: Enable debug mode (default: false)
- `FASTMCP_LOG_LEVEL`: Logging level (default: INFO)

## Usage

Start the server:
```bash
python server.py
```

The server will start on `http://127.0.0.1:8001` by default.

## Available Tools

### execute_command
Execute a Windows command and return the result.

### list_processes
List all running processes on the system.

### get_system_info
Get system information including CPU, memory, and disk usage.

### file_operations
Perform file operations (read, write, delete).

### window_operations
Perform window operations (list, minimize, maximize, close).

## Security Notes
⚠️ **Warning**: This server provides direct system access and should only be used in trusted environments. 
Ensure proper firewall rules and access controls are in place when running this server.