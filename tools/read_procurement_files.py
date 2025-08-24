#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采购部资料读取工具
用于读取采购部提交的各种格式文件
"""

import pandas as pd
import os
from pathlib import Path
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_excel_file(file_path):
    """读取Excel文件内容"""
    try:
        # 读取所有工作表
        excel_file = pd.ExcelFile(file_path)
        sheets_data = {}
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            sheets_data[sheet_name] = df
            logger.info(f"成功读取工作表: {sheet_name}, 行数: {len(df)}, 列数: {len(df.columns)}")
            
        return sheets_data
    except Exception as e:
        logger.error(f"读取Excel文件失败: {e}")
        return None

def analyze_procurement_structure():
    """分析采购部组织架构"""
    base_path = Path("S:/PG-GMO/office/采购部")
    
    # 读取部门架构Excel文件
    structure_file = base_path / "采购部部门架构.xlsx"
    if structure_file.exists():
        logger.info(f"正在读取部门架构文件: {structure_file}")
        structure_data = read_excel_file(structure_file)
        
        if structure_data:
            print("\n=== 采购部部门架构 ===")
            for sheet_name, df in structure_data.items():
                print(f"\n工作表: {sheet_name}")
                print(df.to_string(index=False))
    
    # 读取职责分工表
    responsibility_file = base_path / "五金和采购职责分工表.xlsx"
    if responsibility_file.exists():
        logger.info(f"正在读取职责分工表: {responsibility_file}")
        responsibility_data = read_excel_file(responsibility_file)
        
        if responsibility_data:
            print("\n=== 五金和采购职责分工表 ===")
            for sheet_name, df in responsibility_data.items():
                print(f"\n工作表: {sheet_name}")
                print(df.to_string(index=False))
    
    # 读取绩效考核表
    performance_file = base_path / "开发跟单采购员绩效考核表.xlsx"
    if performance_file.exists():
        logger.info(f"正在读取绩效考核表: {performance_file}")
        performance_data = read_excel_file(performance_file)
        
        if performance_data:
            print("\n=== 开发跟单采购员绩效考核表 ===")
            for sheet_name, df in performance_data.items():
                print(f"\n工作表: {sheet_name}")
                print(df.to_string(index=False))

def main():
    """主函数"""
    logger.info("开始分析采购部提交的资料")
    
    try:
        analyze_procurement_structure()
        logger.info("采购部资料分析完成")
    except Exception as e:
        logger.error(f"分析过程中出现错误: {e}")

if __name__ == "__main__":
    main()