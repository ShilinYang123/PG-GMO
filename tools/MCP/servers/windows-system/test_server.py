#!/usr/bin/env python3
"""
Test script for Windows System MCP Server
"""

import requests
import json
import time
import sys
import os

# Add the project virtual environment to the path
sys.path.insert(0, "s:\\PG-GMO\\.venv\\Lib\\site-packages")

# Server configuration
SERVER_URL = "http://127.0.0.1:8001"
SSE_URL = f"{SERVER_URL}/sse"
MESSAGES_URL = f"{SERVER_URL}/messages/"

def test_server_connection():
    """Test if the server is running"""
    try:
        response = requests.get(SERVER_URL)
        print(f"Server status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return False

def test_system_info():
    """Test getting system information"""
    try:
        # This is a simplified test - in reality, you'd use the MCP protocol
        print("Testing system info retrieval...")
        # We can't easily test the full MCP protocol here without proper client libraries
        print("System info test completed (manual verification needed)")
        return True
    except Exception as e:
        print(f"System info test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Windows System MCP Server")
    print("=" * 40)
    
    if test_server_connection():
        print("✅ Server connection test passed")
    else:
        print("❌ Server connection test failed")
        
    test_system_info()
    
    print("\nTo fully test the server:")
    print("1. Start the server: s:\\PG-GMO\\.venv\\Scripts\\python.exe server.py")
    print("2. Use an MCP client to connect to the server")
    print("3. Test the available tools")