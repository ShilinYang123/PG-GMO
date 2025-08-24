#!/usr/bin/env python3
"""
演示如何使用Word MCP工具的示例脚本
"""

import sys
import os
import asyncio
from mcp.server.fastmcp import FastMCP

# 添加项目路径到Python路径
sys.path.append(r"s:\PG-GMO\project\MCP\office\word-mcp")

async def demo_word_operations():
    """
    演示Word文档操作
    """
    try:
        # 导入Word文档工具
        from word_document_server.tools.document_tools import create_document
        from word_document_server.tools.content_tools import add_heading, add_paragraph
        
        # 创建新文档
        filename = "demo_document.docx"
        result = await create_document(filename, "演示文档", "AI助手")
        print(f"创建文档结果: {result}")
        
        # 添加标题
        result = await add_heading(filename, "欢迎使用Word MCP工具", 1)
        print(f"添加标题结果: {result}")
        
        # 添加段落
        result = await add_paragraph(filename, "这是使用MCP工具创建的第一个段落。MCP工具可以帮助我们自动化处理Word文档。")
        print(f"添加段落结果: {result}")
        
        print(f"文档已创建: {filename}")
        return True
        
    except Exception as e:
        print(f"操作过程中出现错误: {e}")
        return False

async def main():
    print("开始演示Word MCP工具操作...")
    success = await demo_word_operations()
    if success:
        print("演示完成!")
    else:
        print("演示失败!")

if __name__ == "__main__":
    asyncio.run(main())