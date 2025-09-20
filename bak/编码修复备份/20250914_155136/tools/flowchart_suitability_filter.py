#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第二阶段：流程图适用性筛选工具
根据任务书筛选标准，识别适合生成流程图的文档类型
"""

import json
import os
from pathlib import Path

def load_analysis_results():
    """加载第一阶段的分析结果"""
    results_file = Path("S:/PG-GMO/02-Output/ISO文档分析结果.json")
    if not results_file.exists():
        print(f"❌ 分析结果文件不存在: {results_file}")
        return []
    
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def apply_task_book_criteria(documents):
    """根据任务书标准进行精确筛选"""
    
    # 任务书明确要求的适合类型
    suitable_types = {
        '工作流程类': ['工作流程', '作业流程', '操作流程', '业务流程'],
        '操作程序类': ['操作程序', '作业程序', '工艺程序', '生产程序'],
        '审批流程类': ['审批流程', '评审程序', '审核程序', '批准程序'],
        '质量控制类': ['质量控制', '品质控制', '检验程序', '测试程序'],
        '检验程序类': ['检验程序', '检测程序', '试验程序', '验证程序'],
        '管理流程类': ['管理程序', '控制程序', '管理流程', '控制流程']
    }
    
    # 需要排除的类型
    exclude_types = {
        '纯表单类': ['表单', '记录表', '登记表', '统计表', '清单'],
        '纯制度类': ['制度', '规定', '办法', '条例', '准则', '标准']
    }
    
    filtered_results = []
    category_stats = {}
    
    for doc in documents:
        filename = doc['filename']
        original_category = doc['analysis']['category']
        
        # 重新分类和筛选
        new_category = None
        is_suitable = False
        exclusion_reason = None
        
        # 检查是否属于排除类型
        for exclude_cat, keywords in exclude_types.items():
            if any(keyword in filename for keyword in keywords):
                exclusion_reason = f"属于{exclude_cat}，不适合生成流程图"
                break
        
        if not exclusion_reason:
            # 检查是否属于适合类型
            for suit_cat, keywords in suitable_types.items():
                if any(keyword in filename for keyword in keywords):
                    new_category = suit_cat
                    is_suitable = True
                    break
        
        # 更新文档信息
        doc['analysis']['task_book_suitable'] = is_suitable
        doc['analysis']['task_book_category'] = new_category
        doc['analysis']['exclusion_reason'] = exclusion_reason
        
        if is_suitable:
            filtered_results.append(doc)
            category_stats[new_category] = category_stats.get(new_category, 0) + 1
    
    return filtered_results, category_stats

def generate_filter_report(original_docs, filtered_docs, category_stats):
    """生成筛选报告"""
    report = []
    report.append("# 第二阶段：流程图适用性筛选报告")
    report.append("")
    report.append(f"## 筛选结果统计")
    report.append(f"- 原始文档数量: {len(original_docs)}")
    report.append(f"- 筛选后适合文档数量: {len(filtered_docs)}")
    report.append(f"- 筛选率: {len(filtered_docs)/len(original_docs)*100:.1f}%")
    report.append("")
    
    report.append("## 按类型分布")
    for category, count in category_stats.items():
        report.append(f"- {category}: {count}个")
    report.append("")
    
    report.append("## 适合生成流程图的文档清单")
    for i, doc in enumerate(filtered_docs, 1):
        category = doc['analysis']['task_book_category']
        confidence = doc['analysis']['confidence']
        report.append(f"{i}. **{doc['filename']}**")
        report.append(f"   - 分类: {category}")
        report.append(f"   - 置信度: {confidence}%")
        report.append("")
    
    # 显示被排除的文档
    excluded_docs = [doc for doc in original_docs if not doc['analysis']['task_book_suitable']]
    if excluded_docs:
        report.append("## 被排除的文档")
        for doc in excluded_docs:
            reason = doc['analysis']['exclusion_reason']
            report.append(f"- **{doc['filename']}**: {reason}")
        report.append("")
    
    return "\n".join(report)

def main():
    print("=== 第二阶段：流程图适用性筛选 ===")
    
    # 加载第一阶段结果
    documents = load_analysis_results()
    if not documents:
        return
    
    print(f"📄 加载了 {len(documents)} 个文档的分析结果")
    
    # 应用任务书筛选标准
    filtered_docs, category_stats = apply_task_book_criteria(documents)
    
    print(f"\n=== 筛选结果 ===")
    print(f"原始文档: {len(documents)} 个")
    print(f"适合生成流程图: {len(filtered_docs)} 个")
    print(f"筛选率: {len(filtered_docs)/len(documents)*100:.1f}%")
    
    print(f"\n=== 分类统计 ===")
    for category, count in category_stats.items():
        print(f"{category}: {count} 个")
    
    # 生成报告
    report_content = generate_filter_report(documents, filtered_docs, category_stats)
    
    # 保存筛选结果
    output_dir = Path("S:/PG-GMO/02-Output")
    output_dir.mkdir(exist_ok=True)
    
    # 保存筛选后的JSON数据
    filtered_json_file = output_dir / "流程图适用文档筛选结果.json"
    with open(filtered_json_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_docs, f, ensure_ascii=False, indent=2)
    
    # 保存筛选报告
    report_file = output_dir / "第二阶段筛选报告.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n📄 筛选结果已保存: {filtered_json_file}")
    print(f"📄 筛选报告已保存: {report_file}")
    
    print(f"\n=== 第二阶段：流程图适用性筛选 完成 ===")
    print(f"共筛选出 {len(filtered_docs)} 个适合生成流程图的文档")
    
    return filtered_docs

if __name__ == "__main__":
    main()