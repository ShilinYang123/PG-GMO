#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的Word文档格式排版器
作者：雨俊
功能：优化PG管理手册的格式排版，提升文档专业性和可读性
"""

import os
import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.enum.section import WD_SECTION_START
from docx.oxml.shared import OxmlElement, qn
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from datetime import datetime
import re

def setup_document_styles(doc):
    """设置文档样式"""
    # 获取样式集合
    styles = doc.styles
    
    # 设置正文样式
    try:
        normal_style = styles['Normal']
        normal_font = normal_style.font
        normal_font.name = '宋体'
        normal_font.size = Pt(12)
        
        # 设置段落格式
        normal_para = normal_style.paragraph_format
        normal_para.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        normal_para.line_spacing = 1.5  # 1.5倍行距
        normal_para.space_after = Pt(6)  # 段后间距
        normal_para.first_line_indent = Pt(24)  # 首行缩进2字符
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
        heading1_font.color.rgb = RGBColor(0, 0, 0)
        
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
        heading2_font.color.rgb = RGBColor(0, 0, 0)
        
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
        heading3_font.color.rgb = RGBColor(0, 0, 0)
        
        heading3_para = heading3_style.paragraph_format
        heading3_para.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        heading3_para.space_before = Pt(12)
        heading3_para.space_after = Pt(6)
        heading3_para.first_line_indent = Pt(0)
        
    except Exception as e:
        print(f"设置标题样式时出错: {e}")

def create_professional_cover(doc, title="PG管理手册", subtitle="部门基础建设工作成果汇编"):
    """创建专业封面"""
    # 设置封面页边距
    section = doc.sections[0]
    section.top_margin = Inches(2)
    section.bottom_margin = Inches(2)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.5)
    
    # 主标题
    title_para = doc.add_paragraph()
    title_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_run = title_para.add_run(title)
    title_run.font.name = '微软雅黑'
    title_run.font.size = Pt(36)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0, 51, 102)  # 深蓝色
    
    # 添加装饰线
    line_para = doc.add_paragraph()
    line_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    line_run = line_para.add_run('━' * 20)
    line_run.font.name = '微软雅黑'
    line_run.font.size = Pt(14)
    line_run.font.color.rgb = RGBColor(0, 51, 102)
    
    # 添加空行
    for _ in range(8):
        doc.add_paragraph()
    
    # 副标题
    subtitle_para = doc.add_paragraph()
    subtitle_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    subtitle_run = subtitle_para.add_run(subtitle)
    subtitle_run.font.name = '微软雅黑'
    subtitle_run.font.size = Pt(20)
    subtitle_run.font.color.rgb = RGBColor(102, 102, 102)  # 灰色
    
    # 添加空行
    for _ in range(12):
        doc.add_paragraph()
    
    # 日期和版本信息
    date_para = doc.add_paragraph()
    date_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    date_run = date_para.add_run(f'{datetime.now().strftime("%Y年%m月")} 版本')
    date_run.font.name = '微软雅黑'
    date_run.font.size = Pt(16)
    date_run.font.color.rgb = RGBColor(102, 102, 102)
    
    # 添加分页符
    doc.add_page_break()

def create_enhanced_toc(doc, toc_entries):
    """创建增强版目录"""
    # 目录标题
    toc_title = doc.add_heading('目录', level=1)
    toc_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # 添加目录说明
    desc_para = doc.add_paragraph()
    desc_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    desc_run = desc_para.add_run('Contents')
    desc_run.font.name = 'Times New Roman'
    desc_run.font.size = Pt(12)
    desc_run.font.italic = True
    desc_run.font.color.rgb = RGBColor(102, 102, 102)
    
    doc.add_paragraph()  # 空行
    
    # 添加目录条目
    for entry in toc_entries:
        level = entry['level']
        title = entry['title']
        page = entry['page']
        
        toc_para = doc.add_paragraph()
        
        # 根据级别设置样式
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
        
        # 设置段落格式
        toc_para.paragraph_format.left_indent = Inches(indent)
        toc_para.paragraph_format.space_after = Pt(3)
        
        # 添加标题
        title_run = toc_para.add_run(title)
        title_run.font.name = '微软雅黑'
        title_run.font.size = font_size
        title_run.font.bold = is_bold
        title_run.font.color.rgb = color
        
        # 添加点线
        dots_length = max(5, 50 - len(title) - len(str(page)))
        dots_run = toc_para.add_run('·' * dots_length)
        dots_run.font.name = '微软雅黑'
        dots_run.font.size = Pt(10)
        dots_run.font.color.rgb = RGBColor(153, 153, 153)
        
        # 添加页码
        page_run = toc_para.add_run(str(page))
        page_run.font.name = 'Times New Roman'
        page_run.font.size = font_size
        page_run.font.bold = is_bold
        page_run.font.color.rgb = color
    
    # 添加分页符
    doc.add_page_break()

def setup_page_layout(doc):
    """设置页面布局"""
    for section in doc.sections:
        # 设置页边距
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1)
        
        # 设置页眉页脚
        header = section.header
        footer = section.footer
        
        # 清空默认内容
        for para in header.paragraphs:
            para.clear()
        for para in footer.paragraphs:
            para.clear()
        
        # 设置页脚页码
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        # 添加页码
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
        
        # 设置页码字体
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)

def format_paragraph_content(para, new_para):
    """格式化段落内容"""
    if not para.text.strip():
        return
    
    # 检查是否是列表项
    text = para.text.strip()
    if text.startswith(('•', '·', '-', '*')) or re.match(r'^\d+[.)、]', text):
        # 列表项格式
        new_para.paragraph_format.left_indent = Inches(0.5)
        new_para.paragraph_format.first_line_indent = Inches(-0.25)
        new_para.paragraph_format.space_after = Pt(3)
    else:
        # 普通段落格式
        new_para.paragraph_format.first_line_indent = Pt(24)  # 首行缩进
        new_para.paragraph_format.space_after = Pt(6)
    
    # 复制文本和格式
    for run in para.runs:
        new_run = new_para.add_run(run.text)
        if run.font.name:
            new_run.font.name = run.font.name
        else:
            new_run.font.name = '宋体'
        
        if run.font.size:
            new_run.font.size = run.font.size
        else:
            new_run.font.size = Pt(12)
        
        new_run.font.bold = run.font.bold
        new_run.font.italic = run.font.italic
        new_run.font.underline = run.font.underline

def improve_document_formatting(input_file, output_file):
    """改进文档格式"""
    try:
        # 打开原文档
        doc = Document(input_file)
        
        # 创建新文档
        new_doc = Document()
        
        # 设置文档样式
        setup_document_styles(new_doc)
        
        # 设置页面布局
        setup_page_layout(new_doc)
        
        print("正在改进文档格式...")
        
        # 收集目录信息
        toc_entries = []
        current_page = 3
        
        # 分析原文档结构
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading'):
                level = int(para.style.name.split()[-1])
                toc_entries.append({
                    'level': level,
                    'title': para.text,
                    'page': current_page
                })
                current_page += 1
        
        # 创建封面
        create_professional_cover(new_doc)
        
        # 创建目录
        create_enhanced_toc(new_doc, toc_entries)
        
        # 复制并格式化内容
        for para in doc.paragraphs:
            if para.text.strip():
                if para.style.name.startswith('Heading'):
                    # 标题
                    level = int(para.style.name.split()[-1])
                    new_heading = new_doc.add_heading(para.text, level=level)
                else:
                    # 普通段落
                    new_para = new_doc.add_paragraph()
                    format_paragraph_content(para, new_para)
        
        # 复制表格
        for table in doc.tables:
            new_table = new_doc.add_table(rows=len(table.rows), cols=len(table.columns))
            new_table.style = 'Table Grid'
            
            # 设置表格样式
            for i, row in enumerate(table.rows):
                for j, cell in enumerate(row.cells):
                    new_cell = new_table.cell(i, j)
                    new_cell.text = cell.text
                    
                    # 设置单元格字体
                    for para in new_cell.paragraphs:
                        for run in para.runs:
                            run.font.name = '宋体'
                            run.font.size = Pt(10)
        
        # 保存文档
        new_doc.save(output_file)
        print(f"✅ 格式改进完成: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 格式改进失败: {e}")
        return False

def main():
    """主函数"""
    print("=== Word文档格式排版改进器 ===")
    print("作者：雨俊")
    print("开始改进文档格式...\n")
    
    # 输入和输出文件
    input_file = "S:/PG-GMO/Output/PG管理手册.docx"
    output_file = "S:/PG-GMO/Output/PG管理手册_改进版.docx"
    
    if not os.path.exists(input_file):
        print(f"错误：输入文件不存在 {input_file}")
        return
    
    # 开始改进
    success = improve_document_formatting(input_file, output_file)
    
    if success:
        print("\n🎉 文档格式改进完成！")
        print(f"改进后文件: {output_file}")
        print("\n改进内容:")
        print("- 专业封面设计")
        print("- 增强版目录格式")
        print("- 统一字体和间距")
        print("- 优化标题样式")
        print("- 改进段落格式")
        print("- 美化表格样式")
        print("- 规范页码显示")
    else:
        print("\n❌ 文档格式改进失败")

if __name__ == "__main__":
    main()