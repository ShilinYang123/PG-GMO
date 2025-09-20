#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分批生成剩余ISO流程图脚本
每次生成5个，避免内存问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from complete_batch_flowchart_generator import CompleteBatchFlowchartGenerator
from pathlib import Path

def generate_batch(start_index, batch_size=5):
    """分批生成流程图"""
    # 所有需要生成的文档
    all_docs = [
        'HQ-QP-09', 'HQ-QP-10', 'HQ-QP-11', 'HQ-QP-12', 'HQ-QP-13', 'HQ-QP-14',
        'HQ-QP-15', 'HQ-QP-16', 'HQ-QP-17', 'HQ-QP-18', 'HQ-QP-19', 'HQ-QP-20',
        'HQ-QP-21', 'HQ-QP-22', 'HQ-QP-23', 'HQ-QP-24', 'HQ-QP-25', 'HQ-QP-26',
        'HQ-QP-27', 'HQ-QP-28', 'HQ-QP-29', 'HQ-QP-30', 'HQ-QP-31', 'HQ-QP-32'
    ]
    
    # 检查已生成的文件
    output_dir = Path("S:/PG-GMO/02-Output/品高ISO流程图")
    existing_files = set()
    for file in output_dir.glob("*.drawio"):
        if file.stat().st_size > 0:  # 只计算非空文件
            doc_code = file.name.split(' ')[0]
            existing_files.add(doc_code)
    
    # 过滤出未生成的文档
    remaining_docs = [doc for doc in all_docs if doc not in existing_files]
    
    print(f"发现 {len(remaining_docs)} 个未生成的文档")
    
    if not remaining_docs:
        print("所有流程图都已生成完成！")
        return [], []
    
    # 选择本批次要生成的文档
    end_index = min(start_index + batch_size, len(remaining_docs))
    current_batch = remaining_docs[start_index:end_index]
    
    print(f"本批次生成: {current_batch}")
    
    generator = CompleteBatchFlowchartGenerator()
    generated_files = []
    failed_files = []
    
    for i, doc_code in enumerate(current_batch, 1):
        try:
            doc_name = generator.doc_names.get(doc_code, doc_code)
            print(f"[{i}/{len(current_batch)}] 正在生成: {doc_code} {doc_name}")
            
            # 获取流程步骤
            steps = generator.get_process_steps(doc_code)
            
            # 生成流程图
            xml_element = generator.generate_drawio_xml(doc_code, steps)
            
            # 保存文件
            filename = f"{doc_code} {doc_name}.drawio"
            output_path = generator.save_flowchart(xml_element, filename)
            generated_files.append(str(output_path))
            print(f"✅ 成功生成: {filename}")
            
        except Exception as e:
            print(f"❌ 生成失败: {doc_code} - {str(e)}")
            failed_files.append(doc_code)
    
    return generated_files, failed_files

def main():
    print("=== 分批生成剩余ISO流程图 ===")
    
    # 第一批：HQ-QP-09到HQ-QP-13
    print("\n开始第一批生成...")
    batch1_generated, batch1_failed = generate_batch(0, 5)
    
    print(f"\n第一批完成: 成功 {len(batch1_generated)} 个，失败 {len(batch1_failed)} 个")
    
    if batch1_generated:
        print("第一批生成的文件:")
        for file_path in batch1_generated:
            print(f"  - {Path(file_path).name}")
    
    return batch1_generated, batch1_failed

if __name__ == "__main__":
    main()