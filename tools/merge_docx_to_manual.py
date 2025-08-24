#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word文档合并器 - PG管理手册生成器
作者：雨俊
功能：将所有部门的.docx文件合并为一个完整的PG管理手册
"""

import os
import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml.shared import OxmlElement, qn
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from datetime import datetime
import re

def create_cover_page(doc):
    """创建封面页"""
    # 添加封面标题
    title = doc.add_heading('', level=0)
    title_run = title.runs[0] if title.runs else title.add_run()
    title_run.text = 'PG管理手册'
    title_run.font.name = '微软雅黑'
    title_run.font.size = Pt(36)
    title_run.font.bold = True
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # 添加空行
    for _ in range(8):
        doc.add_paragraph()
    
    # 添加副标题
    subtitle = doc.add_paragraph()
    subtitle_run = subtitle.add_run('部门基础建设工作成果汇编')
    subtitle_run.font.name = '微软雅黑'
    subtitle_run.font.size = Pt(24)
    subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # 添加空行
    for _ in range(10):
        doc.add_paragraph()
    
    # 添加日期
    date_para = doc.add_paragraph()
    date_run = date_para.add_run(f'{datetime.now().strftime("%Y年%m月")}')
    date_run.font.name = '微软雅黑'
    date_run.font.size = Pt(18)
    date_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # 添加分页符
    doc.add_page_break()

def create_table_of_contents(doc, toc_entries):
    """创建目录页"""
    # 目录标题
    toc_title = doc.add_heading('目录', level=1)
    toc_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    doc.add_paragraph()
    
    # 添加目录条目
    for entry in toc_entries:
        level = entry['level']
        title = entry['title']
        page = entry['page']
        
        toc_para = doc.add_paragraph()
        
        # 根据级别设置缩进
        if level == 1:
            indent = 0
            font_size = Pt(14)
            is_bold = True
        elif level == 2:
            indent = 0.5
            font_size = Pt(12)
            is_bold = False
        else:
            indent = 1.0
            font_size = Pt(11)
            is_bold = False
        
        # 设置段落格式
        toc_para.paragraph_format.left_indent = Inches(indent)
        
        # 添加标题
        title_run = toc_para.add_run(title)
        title_run.font.name = '宋体'
        title_run.font.size = font_size
        title_run.font.bold = is_bold
        
        # 添加点线
        dots_run = toc_para.add_run('.' * (60 - len(title) - len(str(page))))
        dots_run.font.name = '宋体'
        dots_run.font.size = font_size
        
        # 添加页码
        page_run = toc_para.add_run(str(page))
        page_run.font.name = '宋体'
        page_run.font.size = font_size
    
    # 添加分页符
    doc.add_page_break()

def setup_page_numbering(doc):
    """设置页码"""
    try:
        # 获取所有节
        sections = doc.sections
        
        for section in sections:
            # 设置页脚
            footer = section.footer
            footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
            footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            # 添加页码字段
            run = footer_para.add_run()
            fldChar1 = OxmlElement('w:fldChar')
            fldChar1.set(qn('w:fldCharType'), 'begin')
            run._r.append(fldChar1)
            
            instrText = OxmlElement('w:instrText')
            instrText.text = 'PAGE'
            run._r.append(instrText)
            
            fldChar2 = OxmlElement('w:fldChar')
            fldChar2.set(qn('w:fldCharType'), 'end')
            run._r.append(fldChar2)
            
    except Exception as e:
        print(f"设置页码时出错: {e}")

def get_department_order():
    """定义部门顺序"""
    return [
        '总经办',
        '行政部', 
        '财务部',
        '研发部',
        '业务部',
        '采购部',
        'PMC部',
        '五金部',
        '装配部',
        '品质部'
    ]

def merge_docx_files(source_dir, output_file):
    """合并所有docx文件"""
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"错误：源目录不存在 {source_dir}")
        return False
    
    # 创建主文档
    main_doc = Document()
    
    # 设置文档样式
    try:
        # 设置页面边距
        sections = main_doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1.25)
            section.right_margin = Inches(1.25)
    except Exception as e:
        print(f"设置页面边距时出错: {e}")
    
    # 创建封面
    create_cover_page(main_doc)
    
    # 收集目录信息
    toc_entries = []
    current_page = 3  # 封面和目录占2页，内容从第3页开始
    
    # 按部门顺序处理文件
    department_order = get_department_order()
    processed_departments = set()
    
    for dept_name in department_order:
        dept_dir = source_path / dept_name
        if dept_dir.exists() and dept_dir.is_dir():
            processed_departments.add(dept_name)
            
            # 添加部门标题
            dept_title = main_doc.add_heading(f'{dept_name}', level=1)
            dept_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            # 添加到目录
            toc_entries.append({
                'level': 1,
                'title': dept_name,
                'page': current_page
            })
            current_page += 1
            
            # 处理部门下的所有docx文件
            docx_files = list(dept_dir.rglob('*.docx'))
            docx_files.sort(key=lambda x: x.name)  # 按文件名排序
            
            for docx_file in docx_files:
                try:
                    # 读取文档
                    sub_doc = Document(str(docx_file))
                    
                    # 获取文件名作为章节标题
                    file_title = docx_file.stem
                    
                    # 添加章节标题
                    chapter_title = main_doc.add_heading(file_title, level=2)
                    
                    # 添加到目录
                    toc_entries.append({
                        'level': 2,
                        'title': file_title,
                        'page': current_page
                    })
                    
                    # 复制文档内容
                    for para in sub_doc.paragraphs:
                        if para.text.strip():  # 跳过空段落
                            new_para = main_doc.add_paragraph()
                            
                            # 复制段落格式和内容
                            for run in para.runs:
                                new_run = new_para.add_run(run.text)
                                # 复制字体格式
                                if run.font.name:
                                    new_run.font.name = run.font.name
                                if run.font.size:
                                    new_run.font.size = run.font.size
                                new_run.font.bold = run.font.bold
                                new_run.font.italic = run.font.italic
                    
                    # 添加表格
                    for table in sub_doc.tables:
                        new_table = main_doc.add_table(rows=len(table.rows), cols=len(table.columns))
                        new_table.style = 'Table Grid'
                        
                        for i, row in enumerate(table.rows):
                            for j, cell in enumerate(row.cells):
                                new_table.cell(i, j).text = cell.text
                    
                    current_page += max(1, len(sub_doc.paragraphs) // 20)  # 估算页数
                    
                    print(f"已合并: {docx_file.name}")
                    
                except Exception as e:
                    print(f"合并文件失败 {docx_file}: {e}")
                    continue
            
            # 部门之间添加分页
            main_doc.add_page_break()
    
    # 处理未在顺序中的部门
    for dept_dir in source_path.iterdir():
        if dept_dir.is_dir() and dept_dir.name not in processed_departments:
            dept_name = dept_dir.name
            
            # 添加部门标题
            dept_title = main_doc.add_heading(f'{dept_name}', level=1)
            dept_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            # 添加到目录
            toc_entries.append({
                'level': 1,
                'title': dept_name,
                'page': current_page
            })
            current_page += 1
            
            # 处理部门下的所有docx文件
            docx_files = list(dept_dir.rglob('*.docx'))
            docx_files.sort(key=lambda x: x.name)
            
            for docx_file in docx_files:
                try:
                    sub_doc = Document(str(docx_file))
                    file_title = docx_file.stem
                    
                    chapter_title = main_doc.add_heading(file_title, level=2)
                    
                    toc_entries.append({
                        'level': 2,
                        'title': file_title,
                        'page': current_page
                    })
                    
                    for para in sub_doc.paragraphs:
                        if para.text.strip():
                            new_para = main_doc.add_paragraph()
                            for run in para.runs:
                                new_run = new_para.add_run(run.text)
                                if run.font.name:
                                    new_run.font.name = run.font.name
                                if run.font.size:
                                    new_run.font.size = run.font.size
                                new_run.font.bold = run.font.bold
                                new_run.font.italic = run.font.italic
                    
                    for table in sub_doc.tables:
                        new_table = main_doc.add_table(rows=len(table.rows), cols=len(table.columns))
                        new_table.style = 'Table Grid'
                        for i, row in enumerate(table.rows):
                            for j, cell in enumerate(row.cells):
                                new_table.cell(i, j).text = cell.text
                    
                    current_page += max(1, len(sub_doc.paragraphs) // 20)
                    print(f"已合并: {docx_file.name}")
                    
                except Exception as e:
                    print(f"合并文件失败 {docx_file}: {e}")
                    continue
            
            main_doc.add_page_break()
    
    # 在封面后插入目录
    # 由于python-docx的限制，我们需要重新创建文档来正确插入目录
    final_doc = Document()
    
    # 设置页面格式
    sections = final_doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.25)
    
    # 创建封面
    create_cover_page(final_doc)
    
    # 创建目录
    create_table_of_contents(final_doc, toc_entries)
    
    # 复制主要内容（跳过原来的封面）
    skip_first_page = True
    for para in main_doc.paragraphs:
        if skip_first_page and ('PG管理手册' in para.text or '部门基础建设工作成果汇编' in para.text):
            continue
        if skip_first_page and para.text.strip() == '':
            continue
        if skip_first_page and any(dept in para.text for dept in department_order):
            skip_first_page = False
        
        if not skip_first_page:
            new_para = final_doc.add_paragraph()
            for run in para.runs:
                new_run = new_para.add_run(run.text)
                if run.font.name:
                    new_run.font.name = run.font.name
                if run.font.size:
                    new_run.font.size = run.font.size
                new_run.font.bold = run.font.bold
                new_run.font.italic = run.font.italic
            
            # 复制段落样式
            if para.style.name.startswith('Heading'):
                new_para.style = para.style
            new_para.alignment = para.alignment
    
    # 复制表格
    for table in main_doc.tables:
        new_table = final_doc.add_table(rows=len(table.rows), cols=len(table.columns))
        new_table.style = 'Table Grid'
        for i, row in enumerate(table.rows):
            for j, cell in enumerate(row.cells):
                new_table.cell(i, j).text = cell.text
    
    # 设置页码
    setup_page_numbering(final_doc)
    
    # 保存文档
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        final_doc.save(output_file)
        print(f"\n✅ 管理手册生成成功: {output_file}")
        return True
    except Exception as e:
        print(f"保存文档失败: {e}")
        return False

def main():
    """主函数"""
    print("=== PG管理手册生成器 ===")
    print("作者：雨俊")
    print("开始合并部门文档...\n")
    
    # 源目录和输出文件
    source_dir = "S:/PG-GMO/Output/部门基础建设工作成果_docx"
    output_file = "S:/PG-GMO/Output/PG管理手册.docx"
    
    if not os.path.exists(source_dir):
        print(f"错误：源目录不存在 {source_dir}")
        return
    
    # 开始合并
    success = merge_docx_files(source_dir, output_file)
    
    if success:
        print("\n🎉 PG管理手册生成完成！")
        print(f"文件位置: {output_file}")
        print("\n手册包含:")
        print("- 封面页")
        print("- 目录页")
        print("- 各部门完整文档")
        print("- 页码")
    else:
        print("\n❌ 管理手册生成失败")

if __name__ == "__main__":
    main()