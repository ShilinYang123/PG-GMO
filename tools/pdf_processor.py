#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF澶勭悊宸ュ叿
PG-GMO椤圭洰 - PDF鏂囨。澶勭悊宸ュ叿
浣滆€咃細闆ㄤ繆
鏃ユ湡锛?025-01-08
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# 閰嶇疆鏃ュ織
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """PDF澶勭悊鍣ㄧ被"""
    
    def __init__(self):
        self.name = "PDF澶勭悊宸ュ叿"
        self.version = "1.0.0"
        
    def open_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        鎵撳紑PDF鏂囦欢
        
        Args:
            file_path: PDF鏂囦欢璺緞
            
        Returns:
            鍖呭惈鎿嶄綔缁撴灉鐨勫瓧鍏?        """
        try:
            if not Path(file_path).exists():
                return {
                    "status": "error",
                    "message": f"PDF鏂囦欢涓嶅瓨鍦? {file_path}"
                }
            
            # 妫€鏌ユ枃浠舵墿灞曞悕
            if not file_path.lower().endswith('.pdf'):
                return {
                    "status": "error",
                    "message": f"鏂囦欢涓嶆槸PDF鏍煎紡: {file_path}"
                }
            
            # 浣跨敤绯荤粺榛樿绋嬪簭鎵撳紑PDF
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{file_path}"')
            else:
                os.system(f'xdg-open "{file_path}"')
            
            return {
                "status": "success",
                "message": f"PDF鏂囦欢宸叉墦寮€: {file_path}",
                "file_path": file_path
            }
            
        except Exception as e:
            logger.error(f"鎵撳紑PDF鏂囦欢澶辫触: {e}")
            return {
                "status": "error",
                "message": f"鎵撳紑PDF鏂囦欢澶辫触: {str(e)}"
            }
    
    def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """
        鑾峰彇PDF鏂囦欢淇℃伅
        
        Args:
            file_path: PDF鏂囦欢璺緞
            
        Returns:
            鍖呭惈PDF淇℃伅鐨勫瓧鍏?        """
        try:
            if not Path(file_path).exists():
                return {
                    "status": "error",
                    "message": f"PDF鏂囦欢涓嶅瓨鍦? {file_path}"
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
            logger.error(f"鑾峰彇PDF淇℃伅澶辫触: {e}")
            return {
                "status": "error",
                "message": f"鑾峰彇PDF淇℃伅澶辫触: {str(e)}"
            }
    
    def create_test_pdf(self, output_path: str) -> Dict[str, Any]:
        """
        鍒涘缓娴嬭瘯PDF鏂囦欢
        
        Args:
            output_path: 杈撳嚭鏂囦欢璺緞
            
        Returns:
            鍖呭惈鎿嶄綔缁撴灉鐨勫瓧鍏?        """
        try:
            # 鍒涘缓涓€涓畝鍗曠殑HTML鍐呭
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>娴嬭瘯PDF鏂囨。</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h1 { color: #333; }
                    .content { line-height: 1.6; }
                </style>
            </head>
            <body>
                <h1>PDF澶勭悊宸ュ叿娴嬭瘯鏂囨。</h1>
                <div class="content">
                    <p>杩欐槸涓€涓敱PDF澶勭悊宸ュ叿鍒涘缓鐨勬祴璇曟枃妗ｃ€?/p>
                    <p><strong>鍒涘缓鏃堕棿锛?/strong> 2025骞?鏈?鏃?/p>
                    <p><strong>宸ュ叿鐗堟湰锛?/strong> 1.0.0</p>
                    <p><strong>鍔熻兘鐗规€э細</strong></p>
                    <ul>
                        <li>PDF鏂囦欢鎵撳紑</li>
                        <li>PDF淇℃伅鑾峰彇</li>
                        <li>娴嬭瘯PDF鍒涘缓</li>
                    </ul>
                    <p><strong>娴嬭瘯缁撴灉锛?/strong> 閫氳繃</p>
                </div>
            </body>
            </html>
            """
            
            # 淇濆瓨HTML鏂囦欢
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
            logger.error(f"鍒涘缓娴嬭瘯PDF澶辫触: {e}")
            return {
                "status": "error",
                "message": f"鍒涘缓娴嬭瘯PDF澶辫触: {str(e)}"
            }
    
    def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """
        鑾峰彇PDF鏂囦欢淇℃伅
        
        Args:
            file_path: PDF鏂囦欢璺緞
            
        Returns:
            鍖呭惈PDF淇℃伅鐨勫瓧鍏?        """
        try:
            if not Path(file_path).exists():
                return {
                    "status": "error",
                    "message": f"PDF鏂囦欢涓嶅瓨鍦? {file_path}"
                }
            
            file_stat = Path(file_path).stat()
            
            return {
                "status": "success",
                "file_path": file_path,
                "file_size": file_stat.st_size,
                "file_size_mb": round(file_stat.st_size / (1024 * 1024), 2),
                "created_time": file_stat.st_ctime,
                "modified_time": file_stat.st_mtime,
                "message": "PDF淇℃伅鑾峰彇鎴愬姛"
            }
            
        except Exception as e:
            logger.error(f"鑾峰彇PDF淇℃伅澶辫触: {e}")
            return {
                "status": "error",
                "message": f"鑾峰彇PDF淇℃伅澶辫触: {str(e)}"
            }

# 渚挎嵎鍑芥暟
def create_test_pdf(output_path: str = None) -> str:
    """
    鍒涘缓娴嬭瘯PDF鏂囦欢鐨勪究鎹峰嚱鏁?    
    Args:
        output_path: 杈撳嚭璺緞锛岄粯璁や负Output鐩綍
        
    Returns:
        鍒涘缓鐨勬枃浠惰矾寰?    """
    if output_path is None:
        output_dir = Path(r'S:\\PG-GMO\\02-Output')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / "PDF鍔熻兘娴嬭瘯鎶ュ憡.html")
    
    processor = PDFProcessor()
    result = processor.create_test_pdf(output_path)
    
    if result["status"] == "success":
        return result["html_path"]
    else:
        raise Exception(result["message"])

def get_pdf_info(file_path: str) -> Dict[str, Any]:
    """
    鑾峰彇PDF淇℃伅鐨勪究鎹峰嚱鏁?    
    Args:
        file_path: PDF鏂囦欢璺緞
        
    Returns:
        PDF淇℃伅瀛楀吀
    """
    processor = PDFProcessor()
    return processor.get_pdf_info(file_path)

def main():
    """涓诲嚱鏁?""
    processor = PDFProcessor()
    
    print(f"=== {processor.name} v{processor.version} ===")
    print("鍙敤鍔熻兘锛?)
    print("1. 鎵撳紑PDF鏂囦欢")
    print("2. 鑾峰彇PDF淇℃伅")
    print("3. 鍒涘缓娴嬭瘯PDF")
    
    while True:
        choice = input("\n璇烽€夋嫨鍔熻兘 (1-3, q閫€鍑?: ")
        
        if choice.lower() == 'q':
            break
        elif choice == '1':
            file_path = input("璇疯緭鍏DF鏂囦欢璺緞: ")
            result = processor.open_pdf(file_path)
            print(f"缁撴灉: {result}")
        elif choice == '2':
            file_path = input("璇疯緭鍏DF鏂囦欢璺緞: ")
            result = processor.get_pdf_info(file_path)
            print(f"缁撴灉: {result}")
        elif choice == '3':
            output_path = input("璇疯緭鍏ヨ緭鍑烘枃浠惰矾寰?(濡? test.pdf): ")
            result = processor.create_test_pdf(output_path)
            print(f"缁撴灉: {result}")
        else:
            print("鏃犳晥閫夋嫨锛岃閲嶈瘯")

if __name__ == "__main__":
    main()
