import PyPDF2
import os
import json
from pathlib import Path

def read_pdf_content(pdf_path):
    """读取PDF文件内容"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += f"\n--- 第{page_num + 1}页 ---\n"
                text_content += page.extract_text()
                
        return text_content
    except Exception as e:
        return f"读取PDF文件时出错: {str(e)}"

def read_quality_department_files():
    """读取品质部附件文件内容"""
    base_path = Path("S:/PG-GMO/Output/部门基础建设工作成果/品质部/附件")
    results = {}
    
    # 获取所有PDF文件
    pdf_files = list(base_path.glob("*.pdf"))
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    
    for pdf_file in pdf_files:
        print(f"正在读取: {pdf_file.name}")
        content = read_pdf_content(pdf_file)
        results[pdf_file.name] = {
            "文件路径": str(pdf_file),
            "文件大小": f"{pdf_file.stat().st_size} bytes",
            "内容": content[:2000] + "..." if len(content) > 2000 else content  # 限制长度
        }
    
    # 读取Excel文件
    excel_files = list(base_path.glob("*.xlsx"))
    if excel_files:
        try:
            import pandas as pd
            for excel_file in excel_files:
                print(f"正在读取Excel文件: {excel_file.name}")
                try:
                    # 读取所有工作表
                    excel_data = pd.read_excel(excel_file, sheet_name=None)
                    excel_content = {}
                    for sheet_name, df in excel_data.items():
                        excel_content[sheet_name] = df.to_string()
                    
                    results[excel_file.name] = {
                        "文件路径": str(excel_file),
                        "文件大小": f"{excel_file.stat().st_size} bytes",
                        "工作表数量": len(excel_data),
                        "内容": excel_content
                    }
                except Exception as e:
                    results[excel_file.name] = {
                        "文件路径": str(excel_file),
                        "错误": f"读取Excel文件时出错: {str(e)}"
                    }
        except ImportError:
            print("pandas未安装，跳过Excel文件读取")
    
    return results

if __name__ == "__main__":
    print("开始读取品质部附件文件...")
    results = read_quality_department_files()
    
    # 保存结果到JSON文件
    output_file = "S:/PG-GMO/Output/品质部附件内容分析.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n分析完成！结果已保存到: {output_file}")
    print(f"共处理了 {len(results)} 个文件")
    
    # 显示文件列表
    print("\n处理的文件列表:")
    for filename in results.keys():
        print(f"- {filename}")
    
    # 显示部分内容预览
    print("\n=== 内容预览 ===")
    for filename, data in list(results.items())[:3]:  # 只显示前3个文件的预览
        print(f"\n文件: {filename}")
        if "内容" in data:
            content = data["内容"]
            if isinstance(content, str):
                preview = content[:500] + "..." if len(content) > 500 else content
                print(f"内容预览: {preview}")
            else:
                print(f"内容类型: {type(content)}")
        print("-" * 50)