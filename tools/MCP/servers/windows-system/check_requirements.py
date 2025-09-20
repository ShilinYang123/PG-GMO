#!/usr/bin/env python3
"""
Check if required packages for Windows System MCP Server are available
"""

import sys
import os

# Add the project virtual environment to the path
sys.path.insert(0, "s:\\PG-GMO\\.venv\\Lib\\site-packages")

def check_package(package_name):
    """Check if a package is available"""
    try:
        __import__(package_name)
        print(f"✅ {package_name}: Available")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: Not available ({e})")
        return False

def main():
    print("Checking Windows System MCP Server requirements...")
    print("=" * 50)
    
    # Check required packages
    packages = [
        "mcp.server.fastmcp",
        "psutil",
        "win32api",
        "win32gui",
        "win32con",
        "win32process",
        "win32file"
    ]
    
    results = []
    for package in packages:
        results.append(check_package(package))
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All required packages are available!")
        print("You can now start the Windows System MCP Server.")
    else:
        print("❌ Some required packages are missing.")
        print("Please install the missing packages before starting the server.")
    
    return all(results)

if __name__ == "__main__":
    main()