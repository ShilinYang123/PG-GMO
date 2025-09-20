#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISO文档分析工具
用于分析品高ISO程序文档，判断流程图生成适用性
基于文件名和ISO标准程序特征进行智能判断
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict
import re

class ISODocumentAnalyzer:
    def __init__(self):
        self.base_path = Path(r'S:\PG-GMO\01-Input\原始文档\PG-ISO文件')
        self.output_path = Path(r'S:\PG-GMO\02-Output')
        
        # 基于ISO标准和文件名的适用性规则
        self.flowchart_suitable_patterns = {
            # 高适用性 - 明确的流程控制程序
            'high': [
                ('控制程序', '管理流程类'),
                ('管理程序', '管理流程类'),
                ('评审', '审批流程类'),
                ('审核', '审批流程类'),
                ('检验', '检验程序类'),
                ('检查', '检验程序类'),
                ('监控', '质量控制类'),
                ('测量', '检验程序类'),
                ('纠正', '质量控制类'),
                ('投诉处理', '客户服务类'),
                ('召回', '应急处理类'),
                ('风险评估', '风险管理类'),
                ('应对', '风险管理类'),
                ('变更', '变更管理类'),
                ('异常处理', '异常处理类'),
                ('应变措施', '应急处理类')
            ],
            # 中等适用性 - 可能包含流程的程序
            'medium': [
                ('资源', '资源管理类'),
                ('设备', '设备管理类'),
                ('设施', '设备管理类'),
                ('订单', '业务流程类'),
                ('设计开发', '产品开发类'),
                ('外部提供', '供应商管理类'),
                ('生产', '生产管理类'),
                ('标识', '标识管理类'),
                ('可追溯', '追溯管理类'),
                ('放行', '质量控制类'),
                ('满意', '客户服务类'),
                ('认证', '认证管理类'),
                ('采购', '采购管理类'),
                ('供应商', '供应商管理类')
            ],
            # 低适用性 - 主要是管理制度
            'low': [
                ('人力资源', '人事管理类'),
                ('知识管理', '知识管理类'),
                ('标志管理', '标识管理类'),
                ('尾单处理', '业务管理类')
            ]
        }
        
        self.analysis_results = []
    
    def analyze_document_by_filename(self, filename, file_path):
        """基于文件名分析文档适用性"""
        filename_lower = filename.lower()
        
        # 检查高适用性模式
        for pattern, category in self.flowchart_suitable_patterns['high']:
            if pattern in filename_lower:
                return {
                    'suitable': True,
                    'reason': f'包含高适用性关键词"{pattern}"，属于{category}，适合生成流程图',
                    'category': category,
                    'confidence': 90,
                    'pattern_matched': pattern,
                    'suitability_level': 'high'
                }
        
        # 检查中等适用性模式
        for pattern, category in self.flowchart_suitable_patterns['medium']:
            if pattern in filename_lower:
                return {
                    'suitable': True,
                    'reason': f'包含中等适用性关键词"{pattern}"，属于{category}，适合生成流程图',
                    'category': category,
                    'confidence': 70,
                    'pattern_matched': pattern,
                    'suitability_level': 'medium'
                }
        
        # 检查低适用性模式
        for pattern, category in self.flowchart_suitable_patterns['low']:
            if pattern in filename_lower:
                return {
                    'suitable': False,
                    'reason': f'包含低适用性关键词"{pattern}"，属于{category}，主要为管理制度，不适合生成流程图',
                    'category': category,
                    'confidence': 30,
                    'pattern_matched': pattern,
                    'suitability_level': 'low'
                }
        
        # 默认判断 - 所有HQ-QP程序都有一定流程性
        if filename.startswith('HQ-QP-'):
            return {
                'suitable': True,
                'reason': 'ISO质量程序文档，默认包含管理流程，适合生成流程图',
                'category': '标准程序类',
                'confidence': 60,
                'pattern_matched': 'HQ-QP-',
                'suitability_level': 'default'
            }
        
        return {
            'suitable': False,
            'reason': '未匹配到已知的流程模式',
            'category': '未知类型',
            'confidence': 0,
            'pattern_matched': None,
            'suitability_level': 'unknown'
        }
    
    def analyze_all_documents(self):
        """分析所有主要程序文档"""
        print("=== 开始分析ISO程序文档 ===")
        print(f"扫描路径: {self.base_path}")
        
        # 获取所有主要程序文档
        main_docs = []
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.startswith('HQ-QP-') and file.endswith('.doc'):
                    full_path = os.path.join(root, file)
                    main_docs.append((full_path, file))
        
        print(f"找到的文档路径示例:")
        for i, (path, name) in enumerate(main_docs[:3]):
            print(f"  {i+1}. {name}")
            print(f"     路径: {path}")
        
        print(f"\n找到 {len(main_docs)} 个主要程序文档")
        
        suitable_count = 0
        unsuitable_count = 0
        
        for file_path, filename in sorted(main_docs):
            print(f"\n分析文档: {filename}")
            
            # 基于文件名分析适用性
            analysis = self.analyze_document_by_filename(filename, file_path)
            
            # 保存分析结果
            result = {
                'filename': filename,
                'file_path': file_path,
                'relative_path': os.path.relpath(file_path, self.base_path),
                'analysis': analysis
            }
            
            self.analysis_results.append(result)
            
            # 统计结果
            if analysis['suitable']:
                suitable_count += 1
                print(f"  ✅ 适合生成流程图 - {analysis['reason']}")
            else:
                unsuitable_count += 1
                print(f"  ❌ 不适合生成流程图 - {analysis['reason']}")
            
            print(f"  📂 分类: {analysis['category']}")
            print(f"  🎯 匹配模式: {analysis.get('pattern_matched', '无')}")
            print(f"  📊 置信度: {analysis['confidence']}%")
            print(f"  🔍 适用性级别: {analysis['suitability_level']}")
        
        print(f"\n=== 分析完成 ===")
        print(f"适合生成流程图: {suitable_count} 个")
        print(f"不适合生成流程图: {unsuitable_count} 个")
        print(f"总计: {len(main_docs)} 个")
        print(f"适用率: {suitable_count/len(main_docs)*100:.1f}%")
        
        return self.analysis_results
    
    def generate_analysis_report(self):
        """生成分析报告"""
        if not self.analysis_results:
            print("没有分析结果，请先运行analyze_all_documents()")
            return
        
        # 生成详细报告
        report_content = []
        report_content.append("# ISO文档流程图适用性分析报告")
        report_content.append(f"\n**分析时间**: {self.get_current_time()}")
        report_content.append(f"**分析文档数量**: {len(self.analysis_results)}")
        report_content.append(f"**分析方法**: 基于文件名和ISO标准程序特征的智能判断")
        
        # 统计信息
        suitable_docs = [r for r in self.analysis_results if r['analysis']['suitable']]
        unsuitable_docs = [r for r in self.analysis_results if not r['analysis']['suitable']]
        
        report_content.append(f"\n## 📊 统计概览")
        report_content.append(f"- ✅ 适合生成流程图: **{len(suitable_docs)}** 个")
        report_content.append(f"- ❌ 不适合生成流程图: **{len(unsuitable_docs)}** 个")
        report_content.append(f"- 📈 适用率: **{len(suitable_docs)/len(self.analysis_results)*100:.1f}%**")
        
        # 适用性级别统计
        level_stats = defaultdict(int)
        for result in self.analysis_results:
            level_stats[result['analysis']['suitability_level']] += 1
        
        report_content.append(f"\n## 🎯 适用性级别统计")
        for level, count in sorted(level_stats.items()):
            report_content.append(f"- {level}: {count} 个")
        
        # 分类统计
        category_stats = defaultdict(int)
        for result in self.analysis_results:
            category_stats[result['analysis']['category']] += 1
        
        report_content.append(f"\n## 📂 文档分类统计")
        for category, count in sorted(category_stats.items()):
            report_content.append(f"- {category}: {count} 个")
        
        # 适合生成流程图的文档列表
        report_content.append(f"\n## ✅ 适合生成流程图的文档 ({len(suitable_docs)} 个)")
        
        # 按适用性级别分组
        high_docs = [r for r in suitable_docs if r['analysis']['suitability_level'] == 'high']
        medium_docs = [r for r in suitable_docs if r['analysis']['suitability_level'] == 'medium']
        default_docs = [r for r in suitable_docs if r['analysis']['suitability_level'] == 'default']
        
        if high_docs:
            report_content.append(f"\n### 🔥 高适用性文档 ({len(high_docs)} 个)")
            for result in high_docs:
                analysis = result['analysis']
                report_content.append(f"\n#### {result['filename']}")
                report_content.append(f"- **分类**: {analysis['category']}")
                report_content.append(f"- **置信度**: {analysis['confidence']}%")
                report_content.append(f"- **匹配模式**: {analysis['pattern_matched']}")
                report_content.append(f"- **理由**: {analysis['reason']}")
        
        if medium_docs:
            report_content.append(f"\n### 🎯 中等适用性文档 ({len(medium_docs)} 个)")
            for result in medium_docs:
                analysis = result['analysis']
                report_content.append(f"\n#### {result['filename']}")
                report_content.append(f"- **分类**: {analysis['category']}")
                report_content.append(f"- **置信度**: {analysis['confidence']}%")
                report_content.append(f"- **匹配模式**: {analysis['pattern_matched']}")
                report_content.append(f"- **理由**: {analysis['reason']}")
        
        if default_docs:
            report_content.append(f"\n### 📋 默认适用性文档 ({len(default_docs)} 个)")
            for result in default_docs:
                analysis = result['analysis']
                report_content.append(f"\n#### {result['filename']}")
                report_content.append(f"- **分类**: {analysis['category']}")
                report_content.append(f"- **置信度**: {analysis['confidence']}%")
                report_content.append(f"- **理由**: {analysis['reason']}")
        
        # 不适合生成流程图的文档列表
        if unsuitable_docs:
            report_content.append(f"\n## ❌ 不适合生成流程图的文档 ({len(unsuitable_docs)} 个)")
            for result in unsuitable_docs:
                analysis = result['analysis']
                report_content.append(f"\n### {result['filename']}")
                report_content.append(f"- **分类**: {analysis['category']}")
                report_content.append(f"- **置信度**: {analysis['confidence']}%")
                report_content.append(f"- **匹配模式**: {analysis.get('pattern_matched', '无')}")
                report_content.append(f"- **理由**: {analysis['reason']}")
        
        # 生成流程图建议清单
        report_content.append(f"\n## 🎨 流程图生成建议清单")
        report_content.append(f"\n基于分析结果，建议按以下优先级生成流程图：")
        
        if high_docs:
            report_content.append(f"\n### 优先级1：高适用性文档 ({len(high_docs)} 个)")
            for i, result in enumerate(high_docs, 1):
                report_content.append(f"{i}. {result['filename']} - {result['analysis']['category']}")
        
        if medium_docs:
            report_content.append(f"\n### 优先级2：中等适用性文档 ({len(medium_docs)} 个)")
            for i, result in enumerate(medium_docs, 1):
                report_content.append(f"{i}. {result['filename']} - {result['analysis']['category']}")
        
        if default_docs:
            report_content.append(f"\n### 优先级3：默认适用性文档 ({len(default_docs)} 个)")
            for i, result in enumerate(default_docs, 1):
                report_content.append(f"{i}. {result['filename']} - {result['analysis']['category']}")
        
        # 保存报告
        self.output_path.mkdir(parents=True, exist_ok=True)
        report_file = self.output_path / "ISO文档流程图适用性分析报告.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_content))
        
        print(f"\n📄 分析报告已保存: {report_file}")
        
        # 保存JSON格式的详细数据
        json_file = self.output_path / "ISO文档分析结果.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 详细数据已保存: {json_file}")
        
        return suitable_docs
    
    def get_current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

def main():
    """主函数"""
    analyzer = ISODocumentAnalyzer()
    
    # 分析所有文档
    results = analyzer.analyze_all_documents()
    
    # 生成报告
    suitable_docs = analyzer.generate_analysis_report()
    
    print(f"\n=== 第一阶段：文档扫描与分析 完成 ===")
    print(f"共分析 {len(results)} 个ISO程序文档")
    print(f"其中 {len(suitable_docs)} 个适合生成流程图")
    print(f"适用率: {len(suitable_docs)/len(results)*100:.1f}%")
    
    return suitable_docs

if __name__ == "__main__":
    main()