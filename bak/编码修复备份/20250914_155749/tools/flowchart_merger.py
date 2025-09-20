#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图融合工具
将业务跟单流程图的内容融合到综合订单全流程ERP系统业务流程图-部门泳道布局中
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import re

class FlowchartMerger:
    def __init__(self):
        # 业务跟单流程步骤映射到ERP流程
        self.business_follow_steps = {
            "开始": {"erp_step": "S01", "description": "客户需求咨询", "department": "客户"},
            "1.收集资料": {"erp_step": "S02", "description": "商务洽谈报价", "department": "业务部"},
            "2.制作报价": {"erp_step": "S02", "description": "商务洽谈报价", "department": "业务部"},
            "3.准备样板": {"erp_step": "S03", "description": "技术可行性评估", "department": "研发部"},
            "按样板单2天内落实物料情况": {"erp_step": "S10", "description": "物料需求计算", "department": "PMC部"},
            "2天内下采购单给采购": {"erp_step": "S12", "description": "采购需求提交", "department": "采购部"},
            "采购流程": {"erp_step": "S14", "description": "供应商生产交付", "department": "供应商"},
            "样板制作": {"erp_step": "S13", "description": "工艺路线设计", "department": "工程部"},
            "纸质样板单给品质送检": {"erp_step": "S15", "description": "来料检验验收", "department": "品质部"},
            "品质检验": {"erp_step": "S22", "description": "最终产品检验", "department": "品质部"},
            "通知整改": {"erp_step": "S30", "description": "不合格品处理", "department": "品质部"},
            "检测合格报告": {"erp_step": "S23", "description": "产品质量放行", "department": "品质部"},
            "接收报告样板拍照": {"erp_step": "S02", "description": "商务洽谈报价-样板确认", "department": "业务部"},
            "样板工打包": {"erp_step": "S26", "description": "包装规格确认", "department": "仓储部"},
            "寄样板沟通客户": {"erp_step": "S27", "description": "客户发货通知", "department": "业务部"},
            "落实订单交期数量": {"erp_step": "S05", "description": "订单评审决策", "department": "管理层"},
            "合同评审": {"erp_step": "S06", "description": "合同条款谈判", "department": "业务部"},
            "订单基本资料表": {"erp_step": "S08", "description": "订单信息录入", "department": "业务部"},
            "BOM表": {"erp_step": "S10", "description": "物料需求计算-BOM展开", "department": "PMC部"},
            "PMC确定货期是否满足": {"erp_step": "S09", "description": "生产计划制定", "department": "PMC部"},
            "5.落实订单交期数量": {"erp_step": "S17", "description": "生产任务下达", "department": "PMC部"},
            "6.跟进内部生产/包材确认": {"erp_step": "S19", "description": "生产过程执行", "department": "生产部"},
            "7.按客人要求订验货": {"erp_step": "S22", "description": "最终产品检验", "department": "品质部"},
            "9.跟进收款": {"erp_step": "S31", "description": "客户付款处理", "department": "财务部"},
            "10.反馈客人售后问题/意见": {"erp_step": "S29", "description": "客户收货确认", "department": "客户"},
            "11.处理沟通各种订单问题": {"erp_step": "S33", "description": "订单完结归档", "department": "业务部"}
        }
        
        # 部门扩展映射
        self.dept_mapping = {
            "业务": "业务部",
            "工程/样板员": "工程部", 
            "采购": "采购部",
            "品质部": "品质部",
            "注塑": "生产部",
            "丝印": "生产部", 
            "仓储": "仓储部",
            "计划": "PMC部",
            "装配": "生产部",
            "五金": "生产部"
        }
        
    def parse_business_follow_flowchart(self, file_path):
        """解析业务跟单流程图"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 找到mxGraphModel
        graph_model = root.find(".//mxGraphModel")
        if graph_model is None:
            raise ValueError("未找到mxGraphModel元素")
        
        # 提取业务跟单步骤
        business_steps = []
        cells = graph_model.findall(".//mxCell[@value]")
        
        for cell in cells:
            value = cell.get('value', '').strip()
            if value and not value.startswith('shape='):
                # 清理HTML标签
                clean_value = re.sub(r'<[^>]+>', '', value).strip()
                if clean_value and len(clean_value) > 1:
                    business_steps.append({
                        'text': clean_value,
                        'original_value': value,
                        'cell_id': cell.get('id', ''),
                        'style': cell.get('style', '')
                    })
        
        return business_steps
    
    def parse_erp_swimlane_flowchart(self, file_path):
        """解析ERP部门泳道流程图"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 找到mxGraphModel
        graph_model = root.find(".//mxGraphModel")
        if graph_model is None:
            raise ValueError("未找到mxGraphModel元素")
        
        return tree, root, graph_model
    
    def extract_business_details(self, business_steps):
        """从业务跟单流程中提取业务细节"""
        business_details = {}
        
        for step in business_steps:
            text = step['text']
            
            # 匹配业务跟单步骤
            for pattern, mapping in self.business_follow_steps.items():
                if pattern in text or self.text_similarity(pattern, text) > 0.6:
                    erp_step = mapping['erp_step']
                    
                    if erp_step not in business_details:
                        business_details[erp_step] = {
                            'business_notes': [],
                            'additional_info': [],
                            'quality_checks': []
                        }
                    
                    # 添加业务跟单的具体细节
                    business_details[erp_step]['business_notes'].append({
                        'original_text': text,
                        'business_context': mapping['description'],
                        'department_focus': mapping['department']
                    })
        
        return business_details
    
    def text_similarity(self, text1, text2):
        """简单的文本相似度计算"""
        text1_chars = set(text1)
        text2_chars = set(text2)
        intersection = text1_chars.intersection(text2_chars)
        union = text1_chars.union(text2_chars)
        return len(intersection) / len(union) if union else 0
    
    def enhance_erp_steps_with_business_details(self, tree, graph_model, business_details):
        """用业务跟单细节增强ERP流程步骤"""
        
        cells = graph_model.findall(".//mxCell[@value]")
        enhanced_count = 0
        
        for cell in cells:
            value = cell.get('value', '')
            
            # 识别ERP步骤
            step_match = re.search(r'S(\d+)', value)
            if step_match:
                step_id = f"S{int(step_match.group(1)):02d}"
                
                if step_id in business_details:
                    details = business_details[step_id]
                    
                    # 增强步骤内容
                    enhanced_content = value
                    
                    # 添加业务跟单备注
                    if details['business_notes']:
                        enhanced_content += "\\n\\n📌 业务跟单要点:"
                        for note in details['business_notes'][:2]:  # 限制添加数量
                            enhanced_content += f"\\n• {note['original_text'][:30]}..."
                    
                    # 更新单元格内容
                    cell.set('value', enhanced_content)
                    enhanced_count += 1
        
        print(f"✅ 增强了 {enhanced_count} 个ERP流程步骤")
        return enhanced_count
    
    def convert_connections_to_polylines(self, graph_model):
        """将直线连接转换为折线连接，避免遮挡图元"""
        
        # 找到所有连接线
        connections = graph_model.findall(".//mxCell[@edge='1']")
        converted_count = 0
        
        for conn in connections:
            # 获取连接线的几何信息
            geometry = conn.find('mxGeometry')
            if geometry is not None:
                # 添加折线点，使连接线避开图元
                points = ET.SubElement(geometry, 'Array')
                points.set('as', 'points')
                
                # 添加中间折点，创建L形或Z形连接
                point1 = ET.SubElement(points, 'mxPoint')
                point1.set('x', '50')  # 向右偏移50px
                point1.set('y', '0')   # 保持同一水平线
                
                point2 = ET.SubElement(points, 'mxPoint')
                point2.set('x', '50')  # 保持垂直线
                point2.set('y', '60')  # 向下偏移60px
                
                # 更新连接线样式，使用折线
                current_style = conn.get('style', '')
                if 'edgeStyle=' not in current_style:
                    new_style = current_style + ';edgeStyle=orthogonalEdgeStyle;curved=0;orthogonalLoop=1;jettySize=auto;'
                    conn.set('style', new_style)
                
                converted_count += 1
        
        print(f"✅ 转换了 {converted_count} 条连接线为折线")
        return converted_count
    
    def add_business_follow_legend(self, graph_model):
        """添加业务跟单流程说明"""
        
        # 找到最大的cell_id
        cells = graph_model.findall(".//mxCell")
        max_id = 0
        for cell in cells:
            try:
                cell_id = int(cell.get('id', '0'))
                max_id = max(max_id, cell_id)
            except:
                pass
        
        # 添加业务跟单说明框
        legend_id = max_id + 1000
        legend_cell = ET.SubElement(graph_model.find('root'), 'mxCell')
        legend_cell.set('id', str(legend_id))
        legend_cell.set('value', 
            "业务跟单流程融合说明\\n"
            "📌 本流程图融合了业务跟单的关键节点\\n"
            "🔄 ERP系统步骤已增强业务跟单细节\\n"
            "📋 包含样板确认、质量检验、收款跟进等\\n"
            "🎯 实现从样板到交付的完整业务管控"
        )
        legend_cell.set('style', 
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6FA;strokeColor=#000000;fontSize=11;fontStyle=1;"
        )
        legend_cell.set('vertex', '1')
        legend_cell.set('parent', '1')
        
        # 添加几何信息
        geometry = ET.SubElement(legend_cell, 'mxGeometry')
        geometry.set('x', '50')
        geometry.set('y', '1350')
        geometry.set('width', '300')
        geometry.set('height', '120')
        geometry.set('as', 'geometry')
    
    def merge_flowcharts(self, business_file, erp_file, output_file):
        """融合两个流程图"""
        
        print("🚀 开始融合业务跟单流程图和ERP系统流程图...")
        
        # 解析业务跟单流程图
        print("📊 解析业务跟单流程图...")
        business_steps = self.parse_business_follow_flowchart(business_file)
        print(f"   • 提取到 {len(business_steps)} 个业务步骤")
        
        # 解析ERP泳道流程图
        print("📊 解析ERP部门泳道流程图...")
        tree, root, graph_model = self.parse_erp_swimlane_flowchart(erp_file)
        
        # 提取业务细节
        print("🔍 分析业务跟单细节...")
        business_details = self.extract_business_details(business_steps)
        print(f"   • 识别到 {len(business_details)} 个关键映射")
        
        # 增强ERP流程步骤
        print("🔧 增强ERP流程步骤...")
        enhanced_count = self.enhance_erp_steps_with_business_details(tree, graph_model, business_details)
        
        # 转换连接线为折线
        print("🔄 优化连接线为折线，避免遮挡...")
        connection_count = self.convert_connections_to_polylines(graph_model)
        
        # 添加业务跟单说明
        print("📋 添加业务跟单流程说明...")
        self.add_business_follow_legend(graph_model)
        
        # 更新标题
        title_cells = graph_model.findall(".//mxCell[@value]")
        for cell in title_cells:
            value = cell.get('value', '')
            if '综合订单全流程ERP系统业务流程图' in value and '部门泳道布局' in value:
                new_title = value.replace(
                    '部门泳道布局',
                    '部门泳道布局(融合业务跟单流程)'
                )
                cell.set('value', new_title)
                break
        
        # 保存融合后的文件
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ 融合完成!")
        print(f"📁 输出文件: {output_file}")
        print(f"📊 融合统计:")
        print(f"   • 业务跟单步骤: {len(business_steps)} 个")
        print(f"   • 增强ERP步骤: {enhanced_count} 个")
        print(f"   • 优化连接线: {connection_count} 条")
        print(f"   • 映射关系: {len(business_details)} 个")
        
        return output_file

def main():
    """主函数"""
    
    business_file = "S:\\PG-GMO\\office\\业务部\\业务跟单流程图.drawio"
    erp_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-部门泳道布局.drawio"
    output_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-深度融合业务跟单.drawio"
    
    merger = FlowchartMerger()
    
    try:
        result_file = merger.merge_flowcharts(business_file, erp_file, output_file)
        print(f"🎉 深度融合成功完成！")
        print(f"📋 新文件已保存：{result_file}")
        print(f"💡 建议用Draw.io打开查看深度融合效果，单元格内容已完全重写")
        return True
        
    except Exception as e:
        print(f"❌ 融合过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()