#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部门管理手册提取工具
从完整版管理手册中提取每个部门的内容，生成独立的.md文件

作者: 雨俊
日期: 2025-08-13
"""

import os
import re
from datetime import datetime

def extract_department_content():
    """从完整版文件中提取各部门内容"""
    
    # 文件路径
    input_file = r"S:\PG-GMO\Output\PG管理手册_完整版.md"
    output_dir = r"S:\PG-GMO\Output\部门独立手册"
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 部门列表（按顺序）
    departments = [
        "总经办",
        "PMC部", 
        "业务部",
        "研发部",
        "品质部",
        "采购部",
        "五金部",
        "装配部",
        "行政部",
        "财务部"
    ]
    
    print(f"开始提取部门内容...")
    print(f"输入文件: {input_file}")
    print(f"输出目录: {output_dir}")
    print("-" * 60)
    
    try:
        # 读取完整文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计信息
        total_departments = len(departments)
        processed_count = 0
        
        for i, dept in enumerate(departments):
            print(f"正在处理: {dept}...")
            
            # 构建部门标题模式
            dept_pattern = f"# {dept}"
            
            # 找到当前部门的开始位置
            dept_start = content.find(dept_pattern)
            if dept_start == -1:
                print(f"  ⚠️  未找到部门: {dept}")
                continue
            
            # 找到下一个部门的开始位置（作为当前部门的结束位置）
            if i + 1 < len(departments):
                next_dept = departments[i + 1]
                next_dept_pattern = f"# {next_dept}"
                dept_end = content.find(next_dept_pattern, dept_start + 1)
            else:
                # 最后一个部门，找到文档信息部分
                dept_end = content.find("---\n\n## 文档信息", dept_start)
                if dept_end == -1:
                    dept_end = len(content)
            
            if dept_end == -1:
                dept_end = len(content)
            
            # 提取部门内容
            dept_content = content[dept_start:dept_end].strip()
            
            # 生成部门文件头部
            file_header = f"""# {dept}管理手册

**生成时间：** {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
**作者：** 雨俊
**版本：** v1.0
**来源：** PG管理手册完整版

---

"""
            
            # 处理内容（移除部门标题，因为已经在文件头部添加了）
            dept_content = dept_content.replace(f"# {dept}", "").strip()
            
            # 生成完整内容
            full_content = file_header + dept_content
            
            # 添加文档尾部
            file_footer = f"""

---

## 文档信息

- **生成时间：** {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
- **部门：** {dept}
- **技术负责人：** 雨俊
- **文档状态：** 已完成
"""
            
            full_content += file_footer
            
            # 保存部门文件
            output_file = os.path.join(output_dir, f"{dept}管理手册.md")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            processed_count += 1
            print(f"  ✅ 已生成: {output_file}")
            print(f"  📄 内容长度: {len(full_content):,} 字符")
        
        # 输出统计信息
        print("-" * 60)
        print(f"📊 处理统计:")
        print(f"  总部门数: {total_departments}")
        print(f"  成功处理: {processed_count}")
        print(f"  成功率: {processed_count/total_departments*100:.1f}%")
        print(f"  输出目录: {output_dir}")
        
        # 生成索引文件
        create_index_file(output_dir, departments, processed_count)
        
        print("\n🎉 部门管理手册提取完成！")
        
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {str(e)}")
        return False
    
    return True

def create_index_file(output_dir, departments, processed_count):
    """创建索引文件"""
    
    index_content = f"""# 部门管理手册索引

**生成时间：** {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
**作者：** 雨俊
**版本：** v1.0

---

## 概述

本目录包含PG公司各部门的独立管理手册，每个部门的管理制度、流程规范、岗位职责等内容已提取为独立的.md文件。

## 部门列表

"""
    
    for i, dept in enumerate(departments, 1):
        file_name = f"{dept}管理手册.md"
        file_path = os.path.join(output_dir, file_name)
        
        if os.path.exists(file_path):
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            size_kb = file_size / 1024
            
            index_content += f"{i}. [{dept}管理手册](./{file_name}) ({size_kb:.1f} KB)\n"
        else:
            index_content += f"{i}. {dept}管理手册 (未生成)\n"
    
    index_content += f"""

## 统计信息

- **总部门数：** {len(departments)}
- **成功生成：** {processed_count}
- **成功率：** {processed_count/len(departments)*100:.1f}%
- **生成时间：** {datetime.now().strftime('%Y年%m月%d日 %H:%M')}

## 使用说明

1. 每个部门的管理手册都是独立的.md文件
2. 文件内容包括部门架构、职责分工、管理制度、作业流程等
3. 所有文件采用UTF-8编码，可用任何支持Markdown的编辑器打开
4. 建议使用专业的Markdown编辑器查看，以获得最佳阅读体验

---

**技术负责人：** 雨俊  
**项目：** PG管理手册数字化  
**版本：** v1.0
"""
    
    # 保存索引文件
    index_file = os.path.join(output_dir, "README.md")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"  📋 已生成索引文件: {index_file}")

if __name__ == "__main__":
    print("=" * 60)
    print("PG管理手册 - 部门内容提取工具")
    print("=" * 60)
    
    success = extract_department_content()
    
    if success:
        print("\n✅ 所有任务已完成")
    else:
        print("\n❌ 任务执行失败")