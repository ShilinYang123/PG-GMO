import PyPDF2
import os
import json
from pathlib import Path

def read_pdf_content(pdf_path):
    """璇诲彇PDF鏂囦欢鍐呭"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += f"\n--- 绗瑊page_num + 1}椤?---\n"
                text_content += page.extract_text()
                
        return text_content
    except Exception as e:
        return f"璇诲彇PDF鏂囦欢鏃跺嚭閿? {str(e)}"

def read_quality_department_files():
    """璇诲彇鍝佽川閮ㄩ檮浠舵枃浠跺唴瀹?""
    base_path = Path("S:/PG-GMO/02-Output/閮ㄩ棬鍩虹寤鸿宸ヤ綔鎴愭灉/鍝佽川閮?闄勪欢")
    results = {}
    
    # 鑾峰彇鎵€鏈塒DF鏂囦欢
    pdf_files = list(base_path.glob("*.pdf"))
    
    print(f"鎵惧埌 {len(pdf_files)} 涓狿DF鏂囦欢")
    
    for pdf_file in pdf_files:
        print(f"姝ｅ湪璇诲彇: {pdf_file.name}")
        content = read_pdf_content(pdf_file)
        results[pdf_file.name] = {
            "鏂囦欢璺緞": str(pdf_file),
            "鏂囦欢澶у皬": f"{pdf_file.stat().st_size} bytes",
            "鍐呭": content[:2000] + "..." if len(content) > 2000 else content  # 闄愬埗闀垮害
        }
    
    # 璇诲彇Excel鏂囦欢
    excel_files = list(base_path.glob("*.xlsx"))
    if excel_files:
        try:
            import pandas as pd
            for excel_file in excel_files:
                print(f"姝ｅ湪璇诲彇Excel鏂囦欢: {excel_file.name}")
                try:
                    # 璇诲彇鎵€鏈夊伐浣滆〃
                    excel_data = pd.read_excel(excel_file, sheet_name=None)
                    excel_content = {}
                    for sheet_name, df in excel_data.items():
                        excel_content[sheet_name] = df.to_string()
                    
                    results[excel_file.name] = {
                        "鏂囦欢璺緞": str(excel_file),
                        "鏂囦欢澶у皬": f"{excel_file.stat().st_size} bytes",
                        "宸ヤ綔琛ㄦ暟閲?: len(excel_data),
                        "鍐呭": excel_content
                    }
                except Exception as e:
                    results[excel_file.name] = {
                        "鏂囦欢璺緞": str(excel_file),
                        "閿欒": f"璇诲彇Excel鏂囦欢鏃跺嚭閿? {str(e)}"
                    }
        except ImportError:
            print("pandas鏈畨瑁咃紝璺宠繃Excel鏂囦欢璇诲彇")
    
    return results

if __name__ == "__main__":
    print("寮€濮嬭鍙栧搧璐ㄩ儴闄勪欢鏂囦欢...")
    results = read_quality_department_files()
    
    # 淇濆瓨缁撴灉鍒癑SON鏂囦欢
    output_file = "S:/PG-GMO/02-Output/鍝佽川閮ㄩ檮浠跺唴瀹瑰垎鏋?json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n鍒嗘瀽瀹屾垚锛佺粨鏋滃凡淇濆瓨鍒? {output_file}")
    print(f"鍏卞鐞嗕簡 {len(results)} 涓枃浠?)
    
    # 鏄剧ず鏂囦欢鍒楄〃
    print("\n澶勭悊鐨勬枃浠跺垪琛?")
    for filename in results.keys():
        print(f"- {filename}")
    
    # 鏄剧ず閮ㄥ垎鍐呭棰勮
    print("\n=== 鍐呭棰勮 ===")
    for filename, data in list(results.items())[:3]:  # 鍙樉绀哄墠3涓枃浠剁殑棰勮
        print(f"\n鏂囦欢: {filename}")
        if "鍐呭" in data:
            content = data["鍐呭"]
            if isinstance(content, str):
                preview = content[:500] + "..." if len(content) > 500 else content
                print(f"鍐呭棰勮: {preview}")
            else:
                print(f"鍐呭绫诲瀷: {type(content)}")
        print("-" * 50)
