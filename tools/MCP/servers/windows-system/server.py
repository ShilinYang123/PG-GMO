from typing import Dict, List, Any
import subprocess
import os
import sys
import json
import psutil
import win32api
import win32gui
import win32con
import win32process
import win32file
from mcp.server.fastmcp import FastMCP

# Import configuration
from config import (
    FASTMCP_DEBUG,
    FASTMCP_LOG_LEVEL,
    FASTMCP_HOST,
    FASTMCP_PORT,
    FASTMCP_SSE_PATH,
    FASTMCP_MESSAGE_PATH,
)

# Create the MCP server with customized settings
mcp = FastMCP(
    'Windows System Controller',
    debug=FASTMCP_DEBUG,
    log_level=FASTMCP_LOG_LEVEL,
    host=FASTMCP_HOST,
    port=FASTMCP_PORT,
    sse_path=FASTMCP_SSE_PATH,
    message_path=FASTMCP_MESSAGE_PATH,
)


@mcp.tool()
def execute_command(command: str, shell: bool = True) -> Dict[str, Any]:
    '''
    Execute a Windows command and return the result.

    Args:
        command: The command to execute
        shell: Whether to use shell (default: True)

    Returns:
        A dictionary with stdout, stderr, and return code
    '''
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': 'Command timed out',
            'returncode': -1
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }


@mcp.tool()
def list_processes() -> List[Dict[str, Any]]:
    '''
    List all running processes on the system.

    Returns:
        A list of process information dictionaries
    '''
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'username': proc.info['username'],
                'memory_mb': round(proc.info['memory_info'].rss / 1024 / 1024, 2) if proc.info['memory_info'] else 0,
                'cpu_percent': proc.info['cpu_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Skip processes we can't access
            continue
    return processes


@mcp.tool()
def get_system_info() -> Dict[str, Any]:
    '''
    Get system information.

    Returns:
        A dictionary with system information
    '''
    try:
        # Get basic system info
        info = {
            'platform': sys.platform,
            'os_name': os.name,
            'python_version': sys.version,
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
            'disk_usage_gb': round(psutil.disk_usage('/').total / (1024**3), 2),
        }
        
        # Get Windows-specific info if available
        try:
            import platform
            info['system'] = platform.system()
            info['release'] = platform.release()
            info['version'] = platform.version()
            info['machine'] = platform.machine()
            info['processor'] = platform.processor()
        except:
            pass
            
        return info
    except Exception as e:
        return {'error': str(e)}


@mcp.tool()
def file_operations(operation: str, path: str, content: str = None) -> Dict[str, Any]:
    '''
    Perform file operations (read, write, delete).

    Args:
        operation: The operation to perform (read, write, delete)
        path: The file path
        content: Content to write (for write operation)

    Returns:
        A dictionary with operation result
    '''
    try:
        if operation == 'read':
            with open(path, 'r', encoding='utf-8') as f:
                return {'content': f.read()}
        elif operation == 'write':
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content or '')
            return {'status': 'success', 'message': f'File {path} written successfully'}
        elif operation == 'delete':
            os.remove(path)
            return {'status': 'success', 'message': f'File {path} deleted successfully'}
        else:
            return {'status': 'error', 'message': f'Unknown operation: {operation}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@mcp.tool()
def window_operations(operation: str, window_title: str = None) -> Dict[str, Any]:
    '''
    Perform window operations (list, minimize, maximize, close).

    Args:
        operation: The operation to perform (list, minimize, maximize, close)
        window_title: The window title to operate on (for minimize, maximize, close)

    Returns:
        A dictionary with operation result
    '''
    try:
        if operation == 'list':
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text:
                        windows.append({
                            'hwnd': hwnd,
                            'title': window_text,
                            'class': win32gui.GetClassName(hwnd)
                        })
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            return {'windows': windows}
        elif operation in ['minimize', 'maximize', 'close'] and window_title:
            # Find window by title
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                if operation == 'minimize':
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    return {'status': 'success', 'message': f'Window "{window_title}" minimized'}
                elif operation == 'maximize':
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    return {'status': 'success', 'message': f'Window "{window_title}" maximized'}
                elif operation == 'close':
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    return {'status': 'success', 'message': f'Window "{window_title}" closed'}
            else:
                return {'status': 'error', 'message': f'Window "{window_title}" not found'}
        else:
            return {'status': 'error', 'message': f'Invalid operation or missing window title'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    # Run the server - FastMCP already has host and port from initialization
    print(f"Windows System MCP Server starting on {FASTMCP_HOST}:{FASTMCP_PORT}")
    mcp.run()