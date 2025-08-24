#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF处理工具
高效办公助手系统 - PDF文档处理工具
作者：雨俊
日期：2025-01-08
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """PDF处理器类"""
    
    def __init__(self):
        self.name = "PDF处理工具"
        self.version = "1.0.0"
        
    def open_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        打开PDF文件
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            包含操作结果的字典
        """
        try:
            if not Path(file_path).exists():
                return {
                    "status": "error",
                    "message": f"PDF文件不存在: {file_path}"
                }
            
            # 检查文件扩展名
            if not file_path.lower().endswith('.pdf'):
                return {
                    "status": "error",
                    "message": f"文件不是PDF格式: {file_path}"
                }
            
            # 使用系统默认程序打开PDF
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{file_path}"')
            else:
                os.system(f'xdg-open "{file_path}"')
            
            return {
                "status": "success",
                "message": f"PDF文件已打开: {file_path}",
                "file_path": file_path
            }
            
        except Exception as e:
            logger.error(f"打开PDF文件失败: {e}")
            return {
                "status": "error",
                "message": f"打开PDF文件失败: {str(e)}"
            }
    
    def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取PDF文件信息
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            包含PDF信息的字典
        """
        try:
            if not Path(file_path).exists():
                return {
                    "status": "error",
                    "message": f"PDF文件不存在: {file_path}"
                }
            
            file_stat = Path(file_path).stat()
            
            return {
                "status": "success",
                "info": {
                    "file_path": file_path,
                    "file_name": Path(file_path).name,
                    "file_size": file_stat.st_size,
                    "file_size_mb": round(file_stat.st_size / (1024 * 1024), 2),
                    "created_time": file_stat.st_ctime,
                    "modified_time": file_stat.st_mtime
                }
            }
            
        except Exception as e:
            logger.error(f"获取PDF信息失败: {e}")
            return {
                "status": "error",
                "message": f"获取PDF信息失败: {str(e)}"
            }
    
    def create_test_pdf(self, output_path: str) -> Dict[str, Any]:
        """
        创建测试PDF文件
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            包含操作结果的字典
        """
        try:
            # 创建一个简单的HTML内容
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>测试PDF文档</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h1 { color: #333; }
                    .content { line-height: 1.6; }
                </style>
            </head>
            <body>
                <h1>PDF处理工具测试文档</h1>
                <div class="content">
                    <p>这是一个由PDF处理工具创建的测试文档。</p>
                    <p><strong>创建时间：</strong> 2025年1月8日</p>
                    <p><strong>工具版本：</strong> 1.0.0</p>
                    <p><strong>功能特性：</strong></p>
                    <ul>
                        <li>PDF文件打开</li>
                        <li>PDF信息获取</li>
                        <li>测试PDF创建</li>
                    </ul>
                    <p><strong>测试结果：</strong> 通过</p>
                </div>
            </body>
            </html>
            """
            
            # 保存HTML文件
            html_path = output_path.replace('.pdf', '.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                "status": "success",
                "message": f"测试HTML文件已创建: {html_path}（可手动转换为PDF）",
                "html_path": html_path,
                "note": "请使用浏览器打开HTML文件，然后打印为PDF"
            }
            
        except Exception as e:
            logger.error(f"创建测试PDF失败: {e}")
            return {
                "status": "error",
                "message": f"创建测试PDF失败: {str(e)}"
            }
    
    def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取PDF文件信息
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            包含PDF信息的字典
        """
        try:
            if not Path(file_path).exists():
                return {
                    "status": "error",
                    "message": f"PDF文件不存在: {file_path}"
                }
            
            file_stat = Path(file_path).stat()
            
            return {
                "status": "success",
                "file_path": file_path,
                "file_size": file_stat.st_size,
                "file_size_mb": round(file_stat.st_size / (1024 * 1024), 2),
                "created_time": file_stat.st_ctime,
                "modified_time": file_stat.st_mtime,
                "message": "PDF信息获取成功"
            }
            
        except Exception as e:
            logger.error(f"获取PDF信息失败: {e}")
            return {
                "status": "error",
                "message": f"获取PDF信息失败: {str(e)}"
            }

# 便捷函数
def create_test_pdf(output_path: str = None) -> str:
    """
    创建测试PDF文件的便捷函数
    
    Args:
        output_path: 输出路径，默认为Output目录
        
    Returns:
        创建的文件路径
    """
    if output_path is None:
        output_dir = Path(r'S:\PG-GMO\Output')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / "PDF功能测试报告.html")
    
    processor = PDFProcessor()
    result = processor.create_test_pdf(output_path)
    
    if result["status"] == "success":
        return result["html_path"]
    else:
        raise Exception(result["message"])

def get_pdf_info(file_path: str) -> Dict[str, Any]:
    """
    获取PDF信息的便捷函数
    
    Args:
        file_path: PDF文件路径
        
    Returns:
        PDF信息字典
    """
    processor = PDFProcessor()
    return processor.get_pdf_info(file_path)

def main():
    """主函数"""
    processor = PDFProcessor()
    
    print(f"=== {processor.name} v{processor.version} ===")
    print("可用功能：")
    print("1. 打开PDF文件")
    print("2. 获取PDF信息")
    print("3. 创建测试PDF")
    
    while True:
        choice = input("\n请选择功能 (1-3, q退出): ")
        
        if choice.lower() == 'q':
            break
        elif choice == '1':
            file_path = input("请输入PDF文件路径: ")
            result = processor.open_pdf(file_path)
            print(f"结果: {result}")
        elif choice == '2':
            file_path = input("请输入PDF文件路径: ")
            result = processor.get_pdf_info(file_path)
            print(f"结果: {result}")
        elif choice == '3':
            output_path = input("请输入输出文件路径 (如: test.pdf): ")
            result = processor.create_test_pdf(output_path)
            print(f"结果: {result}")
        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main()