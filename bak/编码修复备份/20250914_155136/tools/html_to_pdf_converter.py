#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML转PDF工具（使用浏览器打印功能）
高效办公助手系统 - HTML文档转PDF工具
作者：雨侠
日期：2025-01-08
"""

import os
import sys
import time
import subprocess
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLToPDFConverter:
    """HTML转PDF转换器类"""
    
    def __init__(self):
        self.name = "HTML转PDF工具"
        self.version = "1.0.0"
        
    def convert_html_to_pdf_chrome(self, html_file: str, output_pdf: str = None) -> dict:
        """
        使用Chrome浏览器的无头模式将HTML转换为PDF
        
        Args:
            html_file: HTML文件路径
            output_pdf: 输出PDF文件路径（可选）
            
        Returns:
            包含操作结果的字典
        """
        try:
            # 检查输入文件
            if not Path(html_file).exists():
                return {
                    "status": "error",
                    "message": f"HTML文件不存在: {html_file}"
                }
            
            # 确定输出文件路径
            if output_pdf is None:
                output_pdf = str(Path(html_file).with_suffix('.pdf'))
            
            # 将路径转换为绝对路径和file://协议
            html_path = Path(html_file).resolve()
            pdf_path = Path(output_pdf).resolve()
            file_url = f"file:///{str(html_path).replace(os.sep, '/')}"
            
            # Chrome命令行参数
            chrome_args = [
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--print-to-pdf=" + str(pdf_path),
                "--print-to-pdf-no-header",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=5000",
                file_url
            ]
            
            # 尝试找到Chrome可执行文件
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
                "chrome",  # 如果在PATH中
                "google-chrome",  # Linux
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # macOS
            ]
            
            chrome_exe = None
            for path in chrome_paths:
                if os.path.exists(path) or path in ["chrome", "google-chrome"]:
                    chrome_exe = path
                    break
            
            if not chrome_exe:
                return {
                    "status": "error",
                    "message": "未找到Chrome浏览器，请确保已安装Chrome"
                }
            
            # 执行Chrome命令
            cmd = [chrome_exe] + chrome_args
            logger.info(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and Path(output_pdf).exists():
                return {
                    "status": "success",
                    "message": f"PDF文件已生成: {output_pdf}",
                    "input_file": html_file,
                    "output_file": output_pdf
                }
            else:
                return {
                    "status": "error",
                    "message": f"PDF生成失败。返回码: {result.returncode}\n错误信息: {result.stderr}"
                }
                
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "message": "Chrome执行超时，请检查HTML文件是否过大或复杂"
            }
        except Exception as e:
            logger.error(f"转换失败: {e}")
            return {
                "status": "error",
                "message": f"转换失败: {str(e)}"
            }
    
    def open_html_for_manual_print(self, html_file: str) -> dict:
        """
        在浏览器中打开HTML文件，供用户手动打印为PDF
        
        Args:
            html_file: HTML文件路径
            
        Returns:
            包含操作结果的字典
        """
        try:
            if not Path(html_file).exists():
                return {
                    "status": "error",
                    "message": f"HTML文件不存在: {html_file}"
                }
            
            # 在默认浏览器中打开HTML文件
            if os.name == 'nt':  # Windows
                os.startfile(html_file)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.run(['open', html_file] if sys.platform == 'darwin' else ['xdg-open', html_file])
            
            return {
                "status": "success",
                "message": f"HTML文件已在浏览器中打开: {html_file}\n请使用浏览器的打印功能（Ctrl+P）保存为PDF",
                "input_file": html_file
            }
            
        except Exception as e:
            logger.error(f"打开文件失败: {e}")
            return {
                "status": "error",
                "message": f"打开文件失败: {str(e)}"
            }

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  自动转换: python html_to_pdf_converter.py <html_file> [output_pdf]")
        print("  手动打印: python html_to_pdf_converter.py <html_file> --manual")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    converter = HTMLToPDFConverter()
    
    # 检查是否是手动模式
    if len(sys.argv) > 2 and sys.argv[2] == "--manual":
        result = converter.open_html_for_manual_print(html_file)
    else:
        output_pdf = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "--manual" else None
        result = converter.convert_html_to_pdf_chrome(html_file, output_pdf)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")
        # 如果自动转换失败，尝试手动模式
        if "Chrome" in result["message"] or "chrome" in result["message"]:
            print("\n🔄 尝试手动模式...")
            manual_result = converter.open_html_for_manual_print(html_file)
            if manual_result["status"] == "success":
                print(f"✅ {manual_result['message']}")
            else:
                print(f"❌ {manual_result['message']}")
                sys.exit(1)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()