#!/usr/bin/env python3
"""
ModelScope Windows MCP Server
基于ModelScope的Windows系统集成MCP服务器
"""

import sys
from mcp.server.fastmcp import FastMCP
from mcp import Server, Notification, Resource, Tool
from mcp.types import (
    TextResourceContents,
    EmbeddedResource,
    PromptMessage,
    PromptMessageType,
    GetPromptResult,
)
import asyncio
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化MCP服务器
mcp_name = "ModelScope Windows MCP Server"
mcp = FastMCP(mcp_name, log_level="INFO")

# 注册工具函数
@mcp.tool()
def get_system_info() -> str:
    """获取Windows系统信息"""
    import platform
    system_info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    return str(system_info)

@mcp.tool()
def list_installed_programs() -> str:
    """列出已安装的程序"""
    try:
        import subprocess
        # 使用PowerShell获取已安装程序列表
        result = subprocess.run([
            "powershell", 
            "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher | Format-Table -AutoSize"
        ], capture_output=True, text=True, shell=True)
        
        return result.stdout
    except Exception as e:
        return f"Error listing programs: {str(e)}"

@mcp.tool()
def get_disk_info() -> str:
    """获取磁盘信息"""
    try:
        import shutil
        # 获取磁盘使用情况
        total, used, free = shutil.disk_usage("/")
        gb = 1024**3
        disk_info = {
            "total": f"{total/gb:.2f} GB",
            "used": f"{used/gb:.2f} GB", 
            "free": f"{free/gb:.2f} GB"
        }
        return str(disk_info)
    except Exception as e:
        return f"Error getting disk info: {str(e)}"

@mcp.tool()
def get_memory_info() -> str:
    """获取内存信息"""
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_info = {
            "total": f"{memory.total / (1024**3):.2f} GB",
            "available": f"{memory.available / (1024**3):.2f} GB",
            "percent": f"{memory.percent}%"
        }
        return str(memory_info)
    except ImportError:
        return "psutil not installed. Please install it with 'pip install psutil'"
    except Exception as e:
        return f"Error getting memory info: {str(e)}"

# 注册资源
@mcp.resource("windows/info")
def get_windows_info_resource() -> TextResourceContents:
    """获取Windows系统信息资源"""
    import platform
    info = f"""
Windows System Information:
- System: {platform.system()}
- Release: {platform.release()}
- Version: {platform.version()}
- Machine: {platform.machine()}
- Processor: {platform.processor()}
- Node: {platform.node()}
"""
    return TextResourceContents(
        uri="windows/info",
        text=info
    )

if __name__ == "__main__":
    # 运行MCP服务器
    print(f"{mcp_name} starting...", file=sys.stderr)
    mcp.run()