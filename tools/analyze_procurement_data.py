#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
閲囪喘閮ㄨ祫鏂欏垎鏋愬伐鍏?娓呯悊鍜屽垎鏋愰噰璐儴鎻愪氦鐨勮祫鏂欙紝鐢熸垚缁撴瀯鍖栨姤鍛?"""

import pandas as pd
import os
from pathlib import Path
import logging
import json

# 璁剧疆鏃ュ織
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_dataframe(df):
    """娓呯悊DataFrame锛岀Щ闄ょ┖琛屽拰绌哄垪"""
    # 绉婚櫎瀹屽叏涓虹┖鐨勮鍜屽垪
    df = df.dropna(how='all').dropna(axis=1, how='all')
    # 閲嶇疆绱㈠紩
    df = df.reset_index(drop=True)
    return df

def analyze_responsibility_table():
    """鍒嗘瀽鑱岃矗鍒嗗伐琛?""
    file_path = "S:/PG-GMO/office/閲囪喘閮?浜旈噾鍜岄噰璐亴璐ｅ垎宸ヨ〃.xlsx"
    
    try:
        # 璇诲彇绗竴涓伐浣滆〃
        df = pd.read_excel(file_path, sheet_name=0, header=None)
        df = clean_dataframe(df)
        
        logger.info(f"鑱岃矗鍒嗗伐琛ㄥ師濮嬫暟鎹舰鐘? {df.shape}")
        
        # 灏濊瘯璇嗗埆琛ㄥご鍜屾暟鎹粨鏋?        responsibilities = []
        
        for i, row in df.iterrows():
            row_data = [str(cell) if pd.notna(cell) else '' for cell in row]
            if any(row_data):  # 濡傛灉琛屼笉涓虹┖
                responsibilities.append({
                    'row_index': i,
                    'content': ' | '.join(row_data)
                })
        
        return responsibilities
        
    except Exception as e:
        logger.error(f"鍒嗘瀽鑱岃矗鍒嗗伐琛ㄥけ璐? {e}")
        return []

def analyze_performance_table():
    """鍒嗘瀽缁╂晥鑰冩牳琛?""
    file_path = "S:/PG-GMO/office/閲囪喘閮?寮€鍙戣窡鍗曢噰璐憳缁╂晥鑰冩牳琛?xlsx"
    
    try:
        df = pd.read_excel(file_path, sheet_name=0, header=None)
        df = clean_dataframe(df)
        
        logger.info(f"缁╂晥鑰冩牳琛ㄥ師濮嬫暟鎹舰鐘? {df.shape}")
        
        performance_data = []
        
        for i, row in df.iterrows():
            row_data = [str(cell) if pd.notna(cell) else '' for cell in row]
            if any(row_data):  # 濡傛灉琛屼笉涓虹┖
                performance_data.append({
                    'row_index': i,
                    'content': ' | '.join(row_data)
                })
        
        return performance_data
        
    except Exception as e:
        logger.error(f"鍒嗘瀽缁╂晥鑰冩牳琛ㄥけ璐? {e}")
        return []

def generate_analysis_report():
    """鐢熸垚鍒嗘瀽鎶ュ憡"""
    report = {
        'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_directory': 'S:/PG-GMO/office/閲囪喘閮?,
        'responsibilities': analyze_responsibility_table(),
        'performance_data': analyze_performance_table()
    }
    
    # 淇濆瓨JSON鏍煎紡鎶ュ憡
    output_path = "S:/PG-GMO/02-Output/閲囪喘閮ㄨ祫鏂欏垎鏋愭姤鍛?json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"鍒嗘瀽鎶ュ憡宸蹭繚瀛樺埌: {output_path}")
    
    # 鐢熸垚鍙鎬ф洿濂界殑鏂囨湰鎶ュ憡
    text_report_path = "S:/PG-GMO/02-Output/閲囪喘閮ㄨ祫鏂欏垎鏋愭姤鍛?md"
    
    with open(text_report_path, 'w', encoding='utf-8') as f:
        f.write("# 閲囪喘閮ㄨ祫鏂欏垎鏋愭姤鍛奬n\n")
        f.write(f"**鍒嗘瀽鏃堕棿**: {report['analysis_date']}\n\n")
        f.write(f"**鏁版嵁婧?*: {report['source_directory']}\n\n")
        
        f.write("## 鑱岃矗鍒嗗伐琛ㄥ垎鏋怽n\n")
        if report['responsibilities']:
            for item in report['responsibilities']:
                f.write(f"**绗瑊item['row_index']+1}琛?*: {item['content']}\n\n")
        else:
            f.write("鏈壘鍒版湁鏁堢殑鑱岃矗鍒嗗伐鏁版嵁\n\n")
        
        f.write("## 缁╂晥鑰冩牳琛ㄥ垎鏋怽n\n")
        if report['performance_data']:
            for item in report['performance_data']:
                f.write(f"**绗瑊item['row_index']+1}琛?*: {item['content']}\n\n")
        else:
            f.write("鏈壘鍒版湁鏁堢殑缁╂晥鑰冩牳鏁版嵁\n\n")
    
    logger.info(f"鏂囨湰鎶ュ憡宸蹭繚瀛樺埌: {text_report_path}")
    
    return report

def main():
    """涓诲嚱鏁?""
    logger.info("寮€濮嬪垎鏋愰噰璐儴璧勬枡")
    
    try:
        report = generate_analysis_report()
        
        print("\n=== 閲囪喘閮ㄨ祫鏂欏垎鏋愮粨鏋?===")
        print(f"鑱岃矗鍒嗗伐琛ㄦ暟鎹鏁? {len(report['responsibilities'])}")
        print(f"缁╂晥鑰冩牳琛ㄦ暟鎹鏁? {len(report['performance_data'])}")
        
        if report['responsibilities']:
            print("\n=== 鑱岃矗鍒嗗伐琛ㄥ墠5琛?===")
            for item in report['responsibilities'][:5]:
                print(f"绗瑊item['row_index']+1}琛? {item['content'][:100]}...")
        
        if report['performance_data']:
            print("\n=== 缁╂晥鑰冩牳琛ㄥ墠5琛?===")
            for item in report['performance_data'][:5]:
                print(f"绗瑊item['row_index']+1}琛? {item['content'][:100]}...")
        
        logger.info("閲囪喘閮ㄨ祫鏂欏垎鏋愬畬鎴?)
        
    except Exception as e:
        logger.error(f"鍒嗘瀽杩囩▼涓嚭鐜伴敊璇? {e}")

if __name__ == "__main__":
    main()
