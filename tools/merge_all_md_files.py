#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PG管理手册 - 所有.md文件合并工具
作者：雨俊
功能：将S:\PG-GMO\Output\部门基础建设工作成果目录下的所有.md文件合并成一个完整的.md文件
"""

import os
import glob
from pathlib import Path
from datetime import datetime

def read_md_file(file_path):
    """读取markdown文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"读取文件失败: {file_path} - {e}")
        return f"# 文件读取失败\n\n文件路径: {file_path}\n错误信息: {e}"

def create_toc_entry(title, level=1):
    """创建目录条目"""
    indent = "  " * (level - 1)
    anchor = title.lower().replace(" ", "-").replace("部", "bu").replace("办", "ban")
    return f"{indent}- [{title}](#{anchor})"

def merge_all_md_files():
    """合并所有.md文件"""
    
    # 定义部门顺序
    department_order = [
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
    
    # 源目录和输出文件
    source_dir = Path("S:/PG-GMO/Output/部门基础建设工作成果")
    output_file = Path("S:/PG-GMO/Output/PG管理手册_完整版.md")
    
    print("=== PG管理手册 - 所有.md文件合并工具 ===")
    print(f"源目录: {source_dir}")
    print(f"输出文件: {output_file}")
    print()
    
    # 开始构建合并内容
    merged_content = []
    toc_entries = []
    
    # 添加文档头部
    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    header = f"""# PG管理手册 - 完整版

**生成时间：** {current_time}  
**作者：** 雨俊  
**版本：** v1.0

---

## 目录
"""
    
    merged_content.append(header)
    
    # 按部门顺序处理
    total_files = 0
    processed_files = 0
    
    for dept_name in department_order:
        dept_dir = source_dir / dept_name
        
        if not dept_dir.exists():
            print(f"⚠️  部门目录不存在: {dept_name}")
            continue
            
        print(f"📁 处理部门: {dept_name}")
        
        # 添加部门标题到目录
        toc_entries.append(create_toc_entry(dept_name, 1))
        
        # 获取部门下的所有.md文件
        md_files = list(dept_dir.glob("*.md"))
        
        # 处理子目录（如PMC部下的仓储部）
        subdirs = [d for d in dept_dir.iterdir() if d.is_dir() and d.name != "附件"]
        
        # 按文件名排序
        md_files.sort(key=lambda x: x.name)
        
        if md_files:
            # 添加部门章节
            dept_section = f"\n\n---\n\n# {dept_name}\n\n"
            merged_content.append(dept_section)
            
            # 处理部门主要文件
            for md_file in md_files:
                total_files += 1
                print(f"  📄 处理文件: {md_file.name}")
                
                # 提取章节标题
                section_title = md_file.stem
                if section_title.startswith("0") and "-" in section_title:
                    section_title = section_title.split("-", 1)[1]
                
                # 添加到目录
                toc_entries.append(create_toc_entry(section_title, 2))
                
                # 读取文件内容
                content = read_md_file(md_file)
                
                if content:
                    # 添加章节标题和内容
                    section = f"\n## {section_title}\n\n{content}\n"
                    merged_content.append(section)
                    processed_files += 1
                else:
                    print(f"    ❌ 文件内容为空: {md_file.name}")
        
        # 处理子部门
        for subdir in subdirs:
            if subdir.name == "仓储部":  # PMC部下的仓储部
                print(f"  📁 处理子部门: {subdir.name}")
                toc_entries.append(create_toc_entry(f"{dept_name}-{subdir.name}", 2))
                
                # 添加子部门章节
                subdept_section = f"\n\n## {dept_name}-{subdir.name}\n\n"
                merged_content.append(subdept_section)
                
                # 处理子部门的.md文件
                sub_md_files = list(subdir.glob("*.md"))
                sub_md_files.sort(key=lambda x: x.name)
                
                for sub_md_file in sub_md_files:
                    total_files += 1
                    print(f"    📄 处理子文件: {sub_md_file.name}")
                    
                    # 提取章节标题
                    sub_section_title = sub_md_file.stem
                    if sub_section_title.startswith("0") and "-" in sub_section_title:
                        sub_section_title = sub_section_title.split("-", 1)[1]
                    
                    # 添加到目录
                    toc_entries.append(create_toc_entry(sub_section_title, 3))
                    
                    # 读取文件内容
                    sub_content = read_md_file(sub_md_file)
                    
                    if sub_content:
                        # 添加子章节标题和内容
                        sub_section = f"\n### {sub_section_title}\n\n{sub_content}\n"
                        merged_content.append(sub_section)
                        processed_files += 1
                    else:
                        print(f"      ❌ 子文件内容为空: {sub_md_file.name}")
    
    # 构建完整的目录
    toc_content = "\n".join(toc_entries)
    
    # 组装最终内容
    final_content = merged_content[0] + toc_content + "\n\n---\n" + "".join(merged_content[1:])
    
    # 添加文档尾部
    footer = f"\n\n---\n\n## 文档信息\n\n- **生成时间：** {current_time}\n- **总文件数：** {total_files}\n- **成功处理：** {processed_files}\n- **成功率：** {processed_files/total_files*100:.1f}%\n- **技术负责人：** 雨俊\n\n---\n\n*本文档由PG管理手册合并工具自动生成*"
    
    final_content += footer
    
    # 写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"\n✅ 合并完成！")
        print(f"📄 输出文件: {output_file}")
        print(f"📊 处理统计:")
        print(f"   - 总文件数: {total_files}")
        print(f"   - 成功处理: {processed_files}")
        print(f"   - 成功率: {processed_files/total_files*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")
        return False

def main():
    """主函数"""
    try:
        success = merge_all_md_files()
        if success:
            print("\n🎉 所有.md文件合并完成！")
        else:
            print("\n❌ 合并过程中出现错误")
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")

if __name__ == "__main__":
    main()