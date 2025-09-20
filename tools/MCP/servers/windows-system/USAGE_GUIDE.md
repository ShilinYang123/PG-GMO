# Windows System MCP Server Usage Guide

## Overview
The Windows System MCP Server provides direct Windows system control capabilities through the Model Context Protocol, allowing AI assistants to execute commands, manage processes, and interact with the Windows operating system.

## Prerequisites
- Python 3.7+ (available in the project's virtual environment)
- Windows operating system
- Properly configured development environment

## Installation

### 1. Check Requirements
Run the requirements check script to verify that all required packages are available:
```cmd
s:\PG-GMO\.venv\Scripts\python.exe check_requirements.py
```

### 2. Install Missing Packages (if needed)
If any packages are missing, install them using:
```cmd
s:\PG-GMO\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Or install individual packages:
```cmd
s:\PG-GMO\.venv\Scripts\python.exe -m pip install mcp
s:\PG-GMO\.venv\Scripts\python.exe -m pip install psutil
s:\PG-GMO\.venv\Scripts\python.exe -m pip install pywin32
```

## Starting the Server

### Method 1: Using the Start Script
Run the provided start script:
```cmd
s:\PG-GMO\tools\MCP\servers\windows-system\start_server.bat
```

### Method 2: Direct Execution
Navigate to the server directory and run:
```cmd
cd s:\PG-GMO\tools\MCP\servers\windows-system
s:\PG-GMO\.venv\Scripts\python.exe server.py
```

The server will start on `http://127.0.0.1:8010` by default.

## Available Tools

### 1. execute_command
Execute a Windows command and return the result.

**Parameters:**
- `command` (string): The command to execute
- `shell` (boolean, optional): Whether to use shell (default: True)

**Returns:**
A dictionary with stdout, stderr, and return code.

### 2. list_processes
List all running processes on the system.

**Returns:**
A list of process information dictionaries.

### 3. get_system_info
Get system information including CPU, memory, and disk usage.

**Returns:**
A dictionary with system information.

### 4. file_operations
Perform file operations (read, write, delete).

**Parameters:**
- `operation` (string): The operation to perform (read, write, delete)
- `path` (string): The file path
- `content` (string, optional): Content to write (for write operation)

**Returns:**
A dictionary with operation result.

### 5. window_operations
Perform window operations (list, minimize, maximize, close).

**Parameters:**
- `operation` (string): The operation to perform (list, minimize, maximize, close)
- `window_title` (string, optional): The window title to operate on (for minimize, maximize, close)

**Returns:**
A dictionary with operation result.

## Integration with Claude Desktop

To use the Windows System MCP Server with Claude Desktop:

1. Add the server configuration to Claude Desktop's MCP servers configuration:
```json
{
  "mcpServers": {
    "windows-system": {
      "command": "s:\\PG-GMO\\.venv\\Scripts\\python.exe",
      "args": [
        "s:\\PG-GMO\\tools\\MCP\\servers\\windows-system\\server.py"
      ],
      "env": {
        "FASTMCP_HOST": "127.0.0.1",
        "FASTMCP_PORT": "8010",
        "FASTMCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

2. Restart Claude Desktop to load the new server configuration.

## Security Considerations

⚠️ **Warning**: This server provides direct system access and should only be used in trusted environments.

### Best Practices:
1. Only run the server when needed
2. Ensure proper firewall rules are in place
3. Consider network access restrictions
4. Be cautious with command execution tools
5. Regularly review security practices

### Risks:
- Unauthorized command execution
- System file modification
- Process manipulation
- Window management access

## Troubleshooting

### Common Issues:

1. **Python not found**: Ensure you're using the Python from the project's virtual environment
2. **Missing packages**: Run the installation script or install packages manually
3. **Port conflicts**: Change the port in the configuration
4. **Permission errors**: Run as administrator if needed for certain operations

### Debugging:
1. Check server logs for error messages
2. Verify all required packages are installed
3. Test connectivity with the test script
4. Ensure proper firewall configuration

## Testing

Use the provided test script to verify basic functionality:
```cmd
s:\PG-GMO\.venv\Scripts\python.exe test_server.py
```

## Maintenance

### Updates:
1. Regularly update dependencies
2. Monitor server logs for issues
3. Review security practices periodically

### Monitoring:
1. Check system resource usage
2. Review command execution logs
3. Monitor network connections

## Support

For issues with the Windows System MCP Server, please:
1. Check the documentation and troubleshooting guide
2. Verify all prerequisites are met
3. Contact the development team for assistance