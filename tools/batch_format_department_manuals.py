#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量改进部门管理手册格式
作者：雨俊
功能：批量优化所有部门管理手册的格式排版
"""

import os
import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.enum.section import WD_SECTION_START
from docx.oxml.shared import OxmlElement, qn
from datetime import datetime
import re
import glob

def setup_document_styles(doc):
    """设置文档样式"""
    styles = doc.styles
    
    # 设置正文样式
    try:
        normal_style = styles['Normal']
        normal_font = normal_style.font
        normal_font.name = '宋体'
        normal_font.size = Pt(12)
        
        normal_para = normal_style.paragraph_format
        normal_para.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        normal_para.line_spacing = 1.5
        normal_para.space_after = Pt(6)
        normal_para.first_line_indent = Pt(24)
    except:
        pass
    
    # 设置标题样式
    try:
        # 一级标题
        heading1_style = styles['Heading 1']
        heading1_font = heading1_style.font
        heading1_font.name = '微软雅黑'
        heading1_font.size = Pt(18)
        heading1_font.bold = True
        heading1_font.color.rgb = RGBColor(0, 51, 102)
        
        heading1_para = heading1_style.paragraph_format
        heading1_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        heading1_para.space_before = Pt(18)
        heading1_para.space_after = Pt(12)
        heading1_para.keep_with_next = True
        
        # 二级标题
        heading2_style = styles['Heading 2']
        heading2_font = heading2_style.font
        heading2_font.name = '微软雅黑'
        heading2_font.size = Pt(16)
        heading2_font.bold = True
        heading2_font.color.rgb = RGBColor(0, 51, 102)
        
        heading2_para = heading2_style.paragraph_format
        heading2_para.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        heading2_para.space_before = Pt(12)
        heading2_para.space_after = Pt(6)
        heading2_para.keep_with_next = True
        
        # 三级标题
        heading3_style = styles['Heading 3']
        heading3_font = heading3_style.font
        heading3_font.name = '微软雅黑'
        heading3_font.size = Pt(14)
        heading3_font.bold = True
        heading3_font.color.rgb = RGBColor(51, 51, 51)
        
        heading3_para = heading3_style.paragraph_format
        heading3_para.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        heading3_para.space_before = Pt(12)
        heading3_para.space_after = Pt(6)
        heading3_para.first_line_indent = Pt(0)
        
    except Exception as e:
        print(f"设置标题样式时出错: {e}")

def create_department_cover(doc, department_name):
    """创建部门专业封面"""
    section = doc.sections[0]
    section.top_margin = Inches(2)
    section.bottom_margin = Inches(2)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.5)
    
    # 主标题
    title_para = doc.add_paragraph()
    title_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_run = title_para.add_run('PG管理手册')
    title_run.font.name = '微软雅黑'
    title_run.font.size = Pt(32)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0, 51, 102)
    
    # 装饰线
    line_para = doc.add_paragraph()
    line_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    line_run = line_para.add_run('━' * 15)
    line_run.font.name = '微软雅黑'
    line_run.font.size = Pt(12)
    line_run.font.color.rgb = RGBColor(0, 51, 102)
    
    # 空行
    for _ in range(4):
        doc.add_paragraph()
    
    # 部门名称
    dept_para = doc.add_paragraph()
    dept_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    dept_run = dept_para.add_run(department_name)
    dept_run.font.name = '微软雅黑'
    dept_run.font.size = Pt(24)
    dept_run.font.bold = True
    dept_run.font.color.rgb = RGBColor(204, 0, 0)  # 红色突出部门
    
    # 空行
    for _ in range(6):
        doc.add_paragraph()
    
    # 副标题
    subtitle_para = doc.add_paragraph()
    subtitle_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    subtitle_run = subtitle_para.add_run('部门基础建设工作成果')
    subtitle_run.font.name = '微软雅黑'
    subtitle_run.font.size = Pt(18)
    subtitle_run.font.color.rgb = RGBColor(102, 102, 102)
    
    # 空行
    for _ in range(10):
        doc.add_paragraph()
    
    # 日期
    date_para = doc.add_paragraph()
    date_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    date_run = date_para.add_run(f'{datetime.now().strftime("%Y年%m月")} 版本')
    date_run.font.name = '微软雅黑'
    date_run.font.size = Pt(14)
    date_run.font.color.rgb = RGBColor(102, 102, 102)
    
    doc.add_page_break()

def create_department_toc(doc, toc_entries, department_name):
    """创建部门目录"""
    # 目录标题
    toc_title = doc.add_heading(f'{department_name} - 目录', level=1)
    toc_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    doc.add_paragraph()
    
    # 添加目录条目
    for entry in toc_entries:
        level = entry['level']
        title = entry['title']
        page = entry['page']
        
        toc_para = doc.add_paragraph()
        
        if level == 1:
            indent = 0
            font_size = Pt(14)
            is_bold = True
            color = RGBColor(0, 51, 102)
        elif level == 2:
            indent = 0.5
            font_size = Pt(12)
            is_bold = False
            color = RGBColor(0, 0, 0)
        else:
            indent = 1.0
            font_size = Pt(11)
            is_bold = False
            color = RGBColor(102, 102, 102)
        
        toc_para.paragraph_format.left_indent = Inches(indent)
        toc_para.paragraph_format.space_after = Pt(3)
        
        # 标题
        title_run = toc_para.add_run(title)
        title_run.font.name = '微软雅黑'
        title_run.font.size = font_size
        title_run.font.bold = is_bold
        title_run.font.color.rgb = color
        
        # 点线
        dots_length = max(5, 45 - len(title) - len(str(page)))
        dots_run = toc_para.add_run('·' * dots_length)
        dots_run.font.name = '微软雅黑'
        dots_run.font.size = Pt(10)
        dots_run.font.color.rgb = RGBColor(153, 153, 153)
        
        # 页码
        page_run = toc_para.add_run(str(page))
        page_run.font.name = 'Times New Roman'
        page_run.font.size = font_size
        page_run.font.bold = is_bold
        page_run.font.color.rgb = color
    
    doc.add_page_break()

def setup_page_layout(doc):
    """设置页面布局"""
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1)
        
        # 设置页脚页码
        footer = section.footer
        for para in footer.paragraphs:
            para.clear()
        
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
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
        
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)

def format_paragraph_enhanced(para, new_para):
    """增强段落格式化"""
    if not para.text.strip():
        return
    
    text = para.text.strip()
    
    # 检查列表项
    if text.startswith(('•', '·', '-', '*')) or re.match(r'^\d+[.)、]', text):
        new_para.paragraph_format.left_indent = Inches(0.5)
        new_para.paragraph_format.first_line_indent = Inches(-0.25)
        new_para.paragraph_format.space_after = Pt(3)
    else:
        new_para.paragraph_format.first_line_indent = Pt(24)
        new_para.paragraph_format.space_after = Pt(6)
    
    # 设置行距
    new_para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    new_para.paragraph_format.line_spacing = 1.5
    
    # 复制内容和格式
    for run in para.runs:
        new_run = new_para.add_run(run.text)
        new_run.font.name = run.font.name or '宋体'
        new_run.font.size = run.font.size or Pt(12)
        new_run.font.bold = run.font.bold
        new_run.font.italic = run.font.italic
        new_run.font.underline = run.font.underline

def improve_department_manual(input_file, output_file):
    """改进部门管理手册格式"""
    try:
        # 从文件名提取部门名称
        filename = Path(input_file).stem
        department_name = filename.replace('PG管理手册-', '').replace('.docx', '')
        
        doc = Document(input_file)
        new_doc = Document()
        
        setup_document_styles(new_doc)
        setup_page_layout(new_doc)
        
        # 收集目录信息
        toc_entries = []
        current_page = 3
        
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading'):
                level = int(para.style.name.split()[-1])
                toc_entries.append({
                    'level': level,
                    'title': para.text,
                    'page': current_page
                })
                current_page += 1
        
        # 创建封面和目录
        create_department_cover(new_doc, department_name)
        create_department_toc(new_doc, toc_entries, department_name)
        
        # 复制内容
        for para in doc.paragraphs:
            if para.text.strip():
                if para.style.name.startswith('Heading'):
                    level = int(para.style.name.split()[-1])
                    new_heading = new_doc.add_heading(para.text, level=level)
                else:
                    new_para = new_doc.add_paragraph()
                    format_paragraph_enhanced(para, new_para)
        
        # 复制表格
        for table in doc.tables:
            new_table = new_doc.add_table(rows=len(table.rows), cols=len(table.columns))
            new_table.style = 'Table Grid'
            
            for i, row in enumerate(table.rows):
                for j, cell in enumerate(row.cells):
                    new_cell = new_table.cell(i, j)
                    new_cell.text = cell.text
                    
                    for para in new_cell.paragraphs:
                        for run in para.runs:
                            run.font.name = '宋体'
                            run.font.size = Pt(10)
        
        new_doc.save(output_file)
        print(f"✅ {department_name} 格式改进完成")
        return True
        
    except Exception as e:
        print(f"❌ {input_file} 格式改进失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 批量部门管理手册格式改进器 ===")
    print("作者：雨俊")
    print("开始批量改进部门管理手册格式...\n")
    
    # 查找所有部门管理手册
    input_dir = "S:/PG-GMO/Output"
    pattern = os.path.join(input_dir, "PG管理手册-*.docx")
    manual_files = glob.glob(pattern)
    
    if not manual_files:
        print("未找到部门管理手册文件")
        return
    
    success_count = 0
    total_count = len(manual_files)
    
    print(f"找到 {total_count} 个部门管理手册文件")
    print("开始批量处理...\n")
    
    for input_file in manual_files:
        # 生成输出文件名
        filename = Path(input_file).stem
        output_file = os.path.join(input_dir, f"{filename}_改进版.docx")
        
        print(f"正在处理: {Path(input_file).name}")
        
        if improve_department_manual(input_file, output_file):
            success_count += 1
    
    print(f"\n=== 批量处理完成 ===")
    print(f"总文件数: {total_count}")
    print(f"成功处理: {success_count}")
    print(f"失败数量: {total_count - success_count}")
    
    if success_count == total_count:
        print("\n🎉 所有部门管理手册格式改进完成！")
        print("\n改进内容:")
        print("- 专业部门封面设计")
        print("- 个性化目录格式")
        print("- 统一字体和间距")
        print("- 优化标题层次")
        print("- 改进段落排版")
        print("- 美化表格样式")
        print("- 规范页码显示")
        print("\n改进版文件已保存，文件名后缀'_改进版'")
    else:
        print(f"\n⚠️ 部分文件处理失败，请检查错误信息")

if __name__ == "__main__":
    main()