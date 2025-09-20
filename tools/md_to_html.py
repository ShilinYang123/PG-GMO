#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Markdown文件转换为HTML并打开
简单实用的Markdown转HTML工具，不依赖外部工具
"""

import os
import sys
from pathlib import Path
import logging
import webbrowser

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import markdown
except ImportError:
    logger.info("正在安装markdown模块...")
    os.system("pip install markdown")
    import markdown

def convert_md_to_html(md_file_path, output_html_path=None):
    """
    将Markdown文件转换为HTML
    
    Args:
        md_file_path: Markdown文件路径
        output_html_path: 输出HTML文件路径，如果为None则使用相同文件名
        
    Returns:
        转换结果信息
    """
    try:
        md_path = Path(md_file_path)
        
        # 检查文件是否存在
        if not md_path.exists():
            return {"status": "error", "message": f"Markdown文件不存在: {md_file_path}"}
        
        # 如果未指定输出路径，则使用相同文件名
        if output_html_path is None:
            output_html_path = str(md_path.with_suffix('.html'))
        
        # 确保输出目录存在
        output_dir = Path(output_html_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 读取Markdown内容
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 转换为HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # 添加HTML头部和样式
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{md_path.stem}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; max-width: 900px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }}
                h2 {{ color: #444; margin-top: 30px; }}
                h3 {{ color: #555; }}
                code {{ background-color: #f5f5f5; padding: 2px 5px; border-radius: 3px; font-family: monospace; }}
                pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                pre code {{ background-color: transparent; padding: 0; }}
                blockquote {{ border-left: 4px solid #ddd; padding-left: 15px; color: #777; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                img {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # 保存HTML文件
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        # 检查HTML是否成功生成
        if not Path(output_html_path).exists():
            return {"status": "error", "message": f"HTML生成失败: {output_html_path}"}
        
        # 使用默认浏览器打开HTML
        webbrowser.open(f"file://{os.path.abspath(output_html_path)}")
        
        return {"status": "success", "message": f"Markdown已成功转换为HTML并打开: {output_html_path}", "html_path": output_html_path}
        
    except Exception as e:
        logger.error(f"转换过程中发生错误: {e}")
        return {"status": "error", "message": f"转换过程中发生错误: {str(e)}"}

def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("使用方法: python md_to_html.py <Markdown文件路径> [输出HTML路径]")
        sys.exit(1)
    
    md_file_path = sys.argv[1]
    output_html_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = convert_md_to_html(md_file_path, output_html_path)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        sys.exit(0)
    else:
        print(f"❌ {result['message']}")
        sys.exit(1)

if __name__ == "__main__":
    main()