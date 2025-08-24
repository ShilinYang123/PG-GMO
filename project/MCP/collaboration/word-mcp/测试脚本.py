#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Office-Word-MCP-Server 功能测试脚本
作者：雨俊
用途：验证MCP Server的基本功能
"""

import subprocess
import sys
import time
import json
from pathlib import Path

def test_mcp_server():
    """测试MCP Server基本功能"""
    print("=== Office-Word-MCP-Server 功能测试 ===")
    print("技术负责人：雨俊")
    print(f"测试时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 检查Python环境
    print("[测试 1] 检查Python环境...")
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python版本：{result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Python检查失败：{e}")
        return False
    
    # 2. 检查依赖包
    print("\n[测试 2] 检查依赖包...")
    try:
        result = subprocess.run([sys.executable, "-c", "import fastmcp; print(f'FastMCP {fastmcp.__version__}')"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
        else:
            print(f"❌ FastMCP导入失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 依赖检查失败：{e}")
        return False
    
    # 3. 检查主服务器文件
    print("\n[测试 3] 检查服务器文件...")
    server_file = Path("word_mcp_server.py")
    if server_file.exists():
        print(f"✅ 服务器文件存在：{server_file.absolute()}")
    else:
        print(f"❌ 服务器文件不存在：{server_file.absolute()}")
        return False
    
    # 4. 测试服务器启动
    print("\n[测试 4] 测试服务器启动...")
    try:
        # 启动服务器进程
        process = subprocess.Popen(
            [sys.executable, "word_mcp_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待2秒检查启动状态
        time.sleep(2)
        
        if process.poll() is None:  # 进程仍在运行
            print("✅ MCP Server启动成功")
            process.terminate()  # 终止进程
            process.wait(timeout=5)  # 等待进程结束
            print("✅ 服务器正常关闭")
        else:
            stdout, stderr = process.communicate()
            print(f"❌ 服务器启动失败")
            print(f"错误输出：{stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 服务器测试失败：{e}")
        return False
    
    # 5. 检查配置文件
    print("\n[测试 5] 检查配置文件...")
    config_file = Path("claude_desktop_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            if "mcpServers" in config and "word-document-server" in config["mcpServers"]:
                print("✅ Claude配置文件格式正确")
            else:
                print("❌ 配置文件格式错误")
                return False
        except Exception as e:
            print(f"❌ 配置文件解析失败：{e}")
            return False
    else:
        print(f"❌ 配置文件不存在：{config_file.absolute()}")
        return False
    
    print("\n=== 测试完成 ===")
    print("✅ 所有测试通过，MCP Server可以正常使用")
    print("\n下一步：")
    print("1. 复制claude_desktop_config.json到Claude配置目录")
    print("2. 重启Claude Desktop")
    print("3. 在Claude中测试：'帮我创建一个Word文档'")
    
    return True

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)