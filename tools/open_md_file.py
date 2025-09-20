#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打开Markdown文件并显示内容
简单实用的Markdown查看工具
"""

import os
import sys
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_markdown_file(file_path):
    """
    读取Markdown文件内容
    
    Args:
        file_path: Markdown文件路径
        
    Returns:
        文件内容字符串
    """
    try:
        path = Path(file_path)
        
        # 检查文件是否存在
        if not path.exists():
            logger.error(f"文件不存在: {file_path}")
            return None
        
        # 检查文件扩展名
        if path.suffix.lower() != '.md':
            logger.warning(f"文件可能不是Markdown格式: {file_path}")
        
        # 读取文件内容
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
        
    except Exception as e:
        logger.error(f"读取文件时发生错误: {e}")
        return None

def display_markdown_content(content):
    """
    显示Markdown内容
    
    Args:
        content: Markdown内容字符串
    """
    if not content:
        print("没有内容可显示")
        return
    
    print("\n" + "=" * 80)
    print("Markdown文件内容:")
    print("=" * 80)
    print(content)
    print("\n" + "=" * 80)
    print("文件显示完成")
    print("=" * 80)

def main():
    """
    主函数
    """
    if len(sys.argv) != 2:
        print("使用方法: python open_md_file.py <Markdown文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    content = read_markdown_file(file_path)
    
    if content:
        display_markdown_content(content)
        print(f"✅ 成功读取并显示文件: {file_path}")
        sys.exit(0)
    else:
        print(f"❌ 无法读取文件: {file_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()