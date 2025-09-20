#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOC到DOCX批量转换工具
将.doc文件批量转换为.docx格式，以便后续分析处理
"""

import os
import sys
from pathlib import Path
from win32com.client import Dispatch
import pythoncom
from datetime import datetime

class DocToDocxConverter:
    def __init__(self, input_dir, output_dir=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 统计信息
        self.converted_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.conversion_log = []
        
    def find_doc_files(self):
        """查找所有.doc文件"""
        doc_files = []
        for root, dirs, files in os.walk(self.input_dir):
            for file in files:
                if file.lower().endswith('.doc') and not file.lower().endswith('.docx'):
                    doc_files.append(Path(root) / file)
        return doc_files
    
    def convert_single_file(self, doc_path):
        """转换单个.doc文件为.docx"""
        try:
            # 初始化COM
            pythoncom.CoInitialize()
            
            # 创建Word应用程序对象
            word_app = Dispatch('Word.Application')
            word_app.Visible = False
            word_app.DisplayAlerts = False
            
            # 构建输出文件路径
            relative_path = doc_path.relative_to(self.input_dir)
            output_path = self.output_dir / relative_path.with_suffix('.docx')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 检查输出文件是否已存在
            if output_path.exists():
                print(f"跳过已存在文件: {output_path.name}")
                self.skipped_count += 1
                self.conversion_log.append(f"跳过: {doc_path.name} -> 已存在")
                return True
            
            print(f"正在转换: {doc_path.name} -> {output_path.name}")
            
            # 打开.doc文件
            doc = word_app.Documents.Open(str(doc_path))
            
            # 保存为.docx格式 (格式代码16表示docx)
            doc.SaveAs2(str(output_path), FileFormat=16)
            
            # 关闭文档
            doc.Close()
            
            # 关闭Word应用程序
            word_app.Quit()
            
            # 清理COM
            pythoncom.CoUninitialize()
            
            self.converted_count += 1
            self.conversion_log.append(f"成功: {doc_path.name} -> {output_path.name}")
            print(f"✅ 转换成功: {output_path.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ 转换失败: {doc_path.name} - {str(e)}")
            self.failed_count += 1
            self.conversion_log.append(f"失败: {doc_path.name} -> {str(e)}")
            
            # 确保清理资源
            try:
                if 'word_app' in locals():
                    word_app.Quit()
                pythoncom.CoUninitialize()
            except:
                pass
            
            return False
    
    def batch_convert(self):
        """批量转换所有.doc文件"""
        print("=== DOC到DOCX批量转换工具 ===")
        print(f"输入目录: {self.input_dir}")
        print(f"输出目录: {self.output_dir}")
        print()
        
        # 查找所有.doc文件
        doc_files = self.find_doc_files()
        
        if not doc_files:
            print("未找到.doc文件")
            return
        
        print(f"找到 {len(doc_files)} 个.doc文件")
        print("开始批量转换...\n")
        
        # 逐个转换
        for i, doc_file in enumerate(doc_files, 1):
            print(f"[{i}/{len(doc_files)}] ", end="")
            self.convert_single_file(doc_file)
        
        # 生成转换报告
        self.generate_report()
    
    def generate_report(self):
        """生成转换报告"""
        total_files = self.converted_count + self.failed_count + self.skipped_count
        
        report_content = f"""# DOC到DOCX转换报告

**转换时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 转换统计

- **总文件数**: {total_files} 个
- **转换成功**: {self.converted_count} 个
- **转换失败**: {self.failed_count} 个
- **跳过文件**: {self.skipped_count} 个
- **成功率**: {(self.converted_count / total_files * 100):.1f}%

## 转换详情

"""
        
        for log_entry in self.conversion_log:
            report_content += f"- {log_entry}\n"
        
        report_content += f"""\n## 说明

- 输入目录: `{self.input_dir}`
- 输出目录: `{self.output_dir}`
- 转换后的.docx文件保持原有的目录结构
- 已存在的.docx文件会被跳过，不会覆盖

## 后续操作

转换完成后，可以使用部门角色分析脚本重新分析所有文档：
```bash
python department_role_analyzer.py
```
"""
        
        report_path = self.output_dir / "DOC转换报告.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n=== 批量转换完成 ===")
        print(f"✅ 转换成功: {self.converted_count} 个")
        print(f"❌ 转换失败: {self.failed_count} 个")
        print(f"⏭️ 跳过文件: {self.skipped_count} 个")
        print(f"📊 转换报告: {report_path}")

def main():
    """主函数"""
    input_dir = "S:/PG-GMO/01-Input/原始文档/PG-ISO文件"
    output_dir = "S:/PG-GMO/01-Input/原始文档/PG-ISO文件_docx"
    
    print("杨老师，开始批量转换.doc文件为.docx格式...")
    
    converter = DocToDocxConverter(input_dir, output_dir)
    converter.batch_convert()
    
    print("\n转换完成！现在可以重新运行部门角色分析脚本了。")

if __name__ == "__main__":
    main()