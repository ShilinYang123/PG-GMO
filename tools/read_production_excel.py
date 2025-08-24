import pandas as pd
import sys

def read_excel_file(file_path):
    try:
        print(f"正在读取Excel文件: {file_path}")
        print("=" * 60)
        
        # 读取Excel文件的所有工作表
        excel_file = pd.ExcelFile(file_path)
        
        print(f"文件包含 {len(excel_file.sheet_names)} 个工作表:")
        for sheet_name in excel_file.sheet_names:
            print(f"  - {sheet_name}")
        
        print("\n" + "=" * 60)
        
        # 逐个读取每个工作表
        for sheet_name in excel_file.sheet_names:
            print(f"\n工作表: {sheet_name}")
            print("-" * 40)
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                print(f"行数: {len(df)}, 列数: {len(df.columns)}")
                
                if not df.empty:
                    print("\n列名:")
                    for i, col in enumerate(df.columns):
                        print(f"  {i+1}. {col}")
                    
                    print("\n数据内容:")
                    # 显示前10行数据
                    print(df.head(10).to_string())
                    
                    if len(df) > 10:
                        print(f"\n... (还有 {len(df) - 10} 行数据)")
                else:
                    print("该工作表为空")
                    
            except Exception as e:
                print(f"读取工作表 '{sheet_name}' 时出错: {e}")
        
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")

if __name__ == "__main__":
    file_path = "S:\\PG-GMO\\office\\装配部\\生产部生产流程图.xlsx"
    read_excel_file(file_path)