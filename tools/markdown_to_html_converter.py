#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转HTML工具
高效办公助手系统 - Markdown文档转HTML工具
作者：雨侠
日期：2025-01-08
"""

import os
import sys
from pathlib import Path
import markdown
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarkdownToHTMLConverter:
    """Markdown转HTML转换器类"""
    
    def __init__(self):
        self.name = "Markdown转HTML工具"
        self.version = "1.0.0"
        
    def convert_markdown_to_html(self, markdown_file: str, output_html: str = None) -> dict:
        """
        将Markdown文件转换为HTML
        
        Args:
            markdown_file: Markdown文件路径
            output_html: 输出HTML文件路径（可选）
            
        Returns:
            包含操作结果的字典
        """
        try:
            # 检查输入文件
            if not Path(markdown_file).exists():
                return {
                    "status": "error",
                    "message": f"Markdown文件不存在: {markdown_file}"
                }
            
            # 确定输出文件路径
            if output_html is None:
                output_html = str(Path(markdown_file).with_suffix('.html'))
            
            # 读取Markdown文件
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # 转换Markdown为HTML
            md = markdown.Markdown(extensions=['tables', 'toc', 'codehilite', 'fenced_code'])
            html_content = md.convert(markdown_content)
            
            # 创建完整的HTML文档
            full_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>N8N国际市场拓展方案实施分析报告</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", "SimSun", Arial, sans-serif;
            line-height: 1.8;
            margin: 0;
            padding: 40px;
            color: #333;
            background-color: #fff;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-top: 40px;
            margin-bottom: 30px;
            font-size: 2.2em;
            text-align: center;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
            margin-top: 35px;
            margin-bottom: 20px;
            font-size: 1.6em;
        }}
        
        h3 {{
            color: #2c3e50;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        h4 {{
            color: #7f8c8d;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
            text-indent: 2em;
        }}
        
        ul, ol {{
            margin-bottom: 20px;
            padding-left: 30px;
        }}
        
        li {{
            margin-bottom: 8px;
            line-height: 1.6;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 25px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        code {{
            background-color: #f8f9fa;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: "Consolas", "Monaco", monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding-left: 25px;
            color: #7f8c8d;
            font-style: italic;
        }}
        
        .header-info {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }}
        
        .print-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #3498db;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            z-index: 1000;
        }}
        
        .print-button:hover {{
            background-color: #2980b9;
        }}
        
        @media print {{
            body {{
                padding: 20px;
                font-size: 12pt;
            }}
            
            .print-button {{
                display: none;
            }}
            
            h1 {{
                font-size: 18pt;
                page-break-after: avoid;
            }}
            
            h2 {{
                font-size: 14pt;
                page-break-after: avoid;
            }}
            
            h3 {{
                font-size: 12pt;
                page-break-after: avoid;
            }}
            
            table {{
                page-break-inside: avoid;
            }}
            
            @page {{
                margin: 2cm;
                @bottom-right {{
                    content: "第 " counter(page) " 页";
                }}
            }}
        }}
    </style>
</head>
<body>
    <button class="print-button" onclick="window.print()">打印/保存为PDF</button>
    
    <div class="header-info">
        <h1 style="margin: 0; border: none; padding: 0;">N8N国际市场拓展方案实施分析报告</h1>
        <p style="margin: 10px 0 0 0; text-indent: 0;">生成时间：{{
            import datetime
            datetime.datetime.now().strftime('%Y年%m月%d日')
        }}</p>
    </div>
    
    {html_content}
    
    <script>
        // 自动调整表格宽度
        document.addEventListener('DOMContentLoaded', function() {{
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {{
                table.style.fontSize = '0.9em';
            }});
        }});
    </script>
</body>
</html>
            """
            
            # 写入HTML文件
            with open(output_html, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            return {
                "status": "success",
                "message": f"HTML文件已生成: {output_html}",
                "input_file": markdown_file,
                "output_file": output_html
            }
            
        except Exception as e:
            logger.error(f"转换失败: {e}")
            return {
                "status": "error",
                "message": f"转换失败: {str(e)}"
            }

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python markdown_to_html_converter.py <markdown_file> [output_html]")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_html = sys.argv[2] if len(sys.argv) > 2 else None
    
    converter = MarkdownToHTMLConverter()
    result = converter.convert_markdown_to_html(markdown_file, output_html)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        print("💡 提示：打开HTML文件后，可以使用浏览器的打印功能保存为PDF")
    else:
        print(f"❌ {result['message']}")
        sys.exit(1)

if __name__ == "__main__":
    main()