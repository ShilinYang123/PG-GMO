import pandas as pd
import os

# 采购部Excel文件路径
excel_files = [
    r'S:\PG-GMO\office\采购部\五金和采购职责分工表.xlsx',
    r'S:\PG-GMO\office\采购部\开发跟单采购员绩效考核表.xlsx',
    r'S:\PG-GMO\office\采购部\采购部部门架构.xlsx'
]

print("开始读取采购部所有Excel文件...")
print("=" * 60)

for file_path in excel_files:
    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        print(f"\n=== 文件: {filename} ===")
        
        try:
            # 读取Excel文件的所有工作表
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            print(f"工作表数量: {len(sheet_names)}")
            print(f"工作表名称: {sheet_names}")
            
            for sheet_name in sheet_names:
                print(f"\n--- 工作表: {sheet_name} ---")
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    print(f"行数: {len(df)}, 列数: {len(df.columns)}")
                    print(f"列名: {list(df.columns)}")
                    
                    print("\n数据内容:")
                    if len(df) > 0:
                        # 显示前20行数据
                        print(df.head(20).to_string())
                        if len(df) > 20:
                            print(f"\n... 还有 {len(df) - 20} 行数据 ...")
                    else:
                        print("工作表为空")
                        
                except Exception as e:
                    print(f"读取工作表 {sheet_name} 时出错: {str(e)}")
                    
            print(f"成功读取文件: {filename}")
            
        except Exception as e:
            print(f"读取文件 {filename} 时出错: {str(e)}")
            
        print("\n" + "=" * 60)
    else:
        print(f"文件不存在: {file_path}")

print("\nExcel文件读取完成")