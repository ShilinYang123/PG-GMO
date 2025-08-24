#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采购部资料分析工具
清理和分析采购部提交的资料，生成结构化报告
"""

import pandas as pd
import os
from pathlib import Path
import logging
import json

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_dataframe(df):
    """清理DataFrame，移除空行和空列"""
    # 移除完全为空的行和列
    df = df.dropna(how='all').dropna(axis=1, how='all')
    # 重置索引
    df = df.reset_index(drop=True)
    return df

def analyze_responsibility_table():
    """分析职责分工表"""
    file_path = "S:/PG-GMO/office/采购部/五金和采购职责分工表.xlsx"
    
    try:
        # 读取第一个工作表
        df = pd.read_excel(file_path, sheet_name=0, header=None)
        df = clean_dataframe(df)
        
        logger.info(f"职责分工表原始数据形状: {df.shape}")
        
        # 尝试识别表头和数据结构
        responsibilities = []
        
        for i, row in df.iterrows():
            row_data = [str(cell) if pd.notna(cell) else '' for cell in row]
            if any(row_data):  # 如果行不为空
                responsibilities.append({
                    'row_index': i,
                    'content': ' | '.join(row_data)
                })
        
        return responsibilities
        
    except Exception as e:
        logger.error(f"分析职责分工表失败: {e}")
        return []

def analyze_performance_table():
    """分析绩效考核表"""
    file_path = "S:/PG-GMO/office/采购部/开发跟单采购员绩效考核表.xlsx"
    
    try:
        df = pd.read_excel(file_path, sheet_name=0, header=None)
        df = clean_dataframe(df)
        
        logger.info(f"绩效考核表原始数据形状: {df.shape}")
        
        performance_data = []
        
        for i, row in df.iterrows():
            row_data = [str(cell) if pd.notna(cell) else '' for cell in row]
            if any(row_data):  # 如果行不为空
                performance_data.append({
                    'row_index': i,
                    'content': ' | '.join(row_data)
                })
        
        return performance_data
        
    except Exception as e:
        logger.error(f"分析绩效考核表失败: {e}")
        return []

def generate_analysis_report():
    """生成分析报告"""
    report = {
        'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_directory': 'S:/PG-GMO/office/采购部',
        'responsibilities': analyze_responsibility_table(),
        'performance_data': analyze_performance_table()
    }
    
    # 保存JSON格式报告
    output_path = "S:/PG-GMO/Output/采购部资料分析报告.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"分析报告已保存到: {output_path}")
    
    # 生成可读性更好的文本报告
    text_report_path = "S:/PG-GMO/Output/采购部资料分析报告.md"
    
    with open(text_report_path, 'w', encoding='utf-8') as f:
        f.write("# 采购部资料分析报告\n\n")
        f.write(f"**分析时间**: {report['analysis_date']}\n\n")
        f.write(f"**数据源**: {report['source_directory']}\n\n")
        
        f.write("## 职责分工表分析\n\n")
        if report['responsibilities']:
            for item in report['responsibilities']:
                f.write(f"**第{item['row_index']+1}行**: {item['content']}\n\n")
        else:
            f.write("未找到有效的职责分工数据\n\n")
        
        f.write("## 绩效考核表分析\n\n")
        if report['performance_data']:
            for item in report['performance_data']:
                f.write(f"**第{item['row_index']+1}行**: {item['content']}\n\n")
        else:
            f.write("未找到有效的绩效考核数据\n\n")
    
    logger.info(f"文本报告已保存到: {text_report_path}")
    
    return report

def main():
    """主函数"""
    logger.info("开始分析采购部资料")
    
    try:
        report = generate_analysis_report()
        
        print("\n=== 采购部资料分析结果 ===")
        print(f"职责分工表数据行数: {len(report['responsibilities'])}")
        print(f"绩效考核表数据行数: {len(report['performance_data'])}")
        
        if report['responsibilities']:
            print("\n=== 职责分工表前5行 ===")
            for item in report['responsibilities'][:5]:
                print(f"第{item['row_index']+1}行: {item['content'][:100]}...")
        
        if report['performance_data']:
            print("\n=== 绩效考核表前5行 ===")
            for item in report['performance_data'][:5]:
                print(f"第{item['row_index']+1}行: {item['content'][:100]}...")
        
        logger.info("采购部资料分析完成")
        
    except Exception as e:
        logger.error(f"分析过程中出现错误: {e}")

if __name__ == "__main__":
    main()