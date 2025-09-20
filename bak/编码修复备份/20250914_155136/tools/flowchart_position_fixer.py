#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图位置修复工具
批量修正流程步骤位置，确保每个步骤都在正确的泳道中
"""

import xml.etree.ElementTree as ET
import re
from datetime import datetime

class FlowchartPositionFixer:
    def __init__(self):
        # 定义泳道Y坐标范围
        self.swimlanes = {
            "客户": {"y_start": 160, "y_end": 260, "color": "#E6F3FF"},
            "业务部": {"y_start": 260, "y_end": 360, "color": "#FFE6E6"},
            "研发部": {"y_start": 360, "y_end": 460, "color": "#E6FFF0"},
            "工程部": {"y_start": 460, "y_end": 560, "color": "#FFFFE6"},
            "财务部": {"y_start": 560, "y_end": 660, "color": "#E0FFFF"},
            "管理层": {"y_start": 660, "y_end": 760, "color": "#FFB6C1"},
            "PMC部": {"y_start": 760, "y_end": 860, "color": "#E6F3FF"},
            "采购部": {"y_start": 860, "y_end": 960, "color": "#F0F8FF"},
            "供应商": {"y_start": 960, "y_end": 1060, "color": "#FFF0F5"},
            "仓储部": {"y_start": 1060, "y_end": 1160, "color": "#F0E6FF"},
            "装配线": {"y_start": 1160, "y_end": 1260, "color": "#FFE4E1"},
            "五金": {"y_start": 1260, "y_end": 1360, "color": "#FFE4E1"},
            "注塑": {"y_start": 1360, "y_end": 1460, "color": "#FFE4E1"},
            "丝印": {"y_start": 1460, "y_end": 1560, "color": "#FFE4E1"},
            "品质部": {"y_start": 1560, "y_end": 1660, "color": "#FFF0E6"}
        }
        
        # 定义每个步骤应该在哪个泳道
        self.step_departments = {
            "S01": "客户",
            "S02": "业务部",
            "S03": "研发部", 
            "S04": "财务部",
            "D01": "管理层",
            "S06": "业务部",
            "S07": "业务部",
            "S08": "工程部",
            "S08.1": "工程部",
            "S08.2": "工程部", 
            "S08.3": "客户",
            "S09": "装配线",
            "S10": "PMC部",
            "S11": "PMC部",
            "S12": "采购部",
            "S13": "仓储部",
            "S14": "供应商",
            "S15": "PMC部",
            "S16": "品质部",
            "S17": "PMC部",
            "S18": "仓储部",
            "S19": "装配线",
            "S20.1": "五金",
            "S20.2": "注塑",
            "S20.3": "丝印",
            "S20": "装配线",
            "S21": "品质部",
            "S22": "品质部",
            "S23": "仓储部",
            "S24": "仓储部",
            "S25": "客户",
            "S26": "业务部",
            "S27": "财务部",
            "S28": "客户",
            "D04": "财务部",
            "S29": "业务部",
            "S30": "客户", 
            "S31": "财务部",
            "S32": "业务部",
            "E01": "客户"
        }
        
        # 步骤内容修正（更正部门信息）
        self.step_corrections = {
            "S09": {
                "title": "样板制作\n首件试制确认",
                "department": "装配线",
                "content": "📌 业务跟单要点:\n• 样板制作跟进\n• 质量标准确认"
            },
            "S10": {
                "title": "BOM清单制定\n物料需求分析", 
                "department": "PMC部",
                "content": "📌 业务跟单要点:\n• BOM准确性确认\n• 物料需求计算"
            },
            "S11": {
                "title": "生产计划制定\n物料采购协调",
                "department": "PMC部", 
                "content": "📌 业务跟单要点:\n• 生产计划确认\n• 采购需求协调"
            },
            "S12": {
                "title": "采购订单下达\n供应商合作确认",
                "department": "采购部",
                "content": "📌 业务跟单要点:\n• 采购进度跟踪\n• 交期协调管理"
            },
            "S13": {
                "title": "物料入库检验\n库存管理确认",
                "department": "仓储部",
                "content": "📌 业务跟单要点:\n• 入库进度跟踪\n• 质量问题处理"
            },
            "S14": {
                "title": "供应商交付\n物料供应保障", 
                "department": "供应商",
                "content": "📌 业务跟单要点:\n• 交付进度监控\n• 质量标准确保"
            },
            "S15": {
                "title": "生产任务调度\n资源配置管理",
                "department": "PMC部",
                "content": "📌 业务跟单要点:\n• 生产排程确认\n• 资源调配优化"
            },
            "S16": {
                "title": "首件检验\n生产质量确认",
                "department": "品质部", 
                "content": "📌 业务跟单要点:\n• 首件质量确认\n• 生产标准建立"
            },
            "S17": {
                "title": "生产任务下达\n车间作业安排",
                "department": "PMC部",
                "content": "📌 业务跟单要点:\n• 生产任务跟踪\n• 进度实时监控"
            },
            "S18": {
                "title": "物料领用\n生产保障支持",
                "department": "仓储部",
                "content": "📌 业务跟单要点:\n• 物料配送跟踪\n• 生产保障确认"
            }
        }
    
    def parse_flowchart(self, file_path):
        """解析流程图XML文件"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        graph_model = root.find(".//mxGraphModel")
        if graph_model is None:
            raise ValueError("未找到mxGraphModel元素")
        
        return tree, root, graph_model
    
    def fix_step_positions(self, graph_model):
        """修正步骤位置"""
        cells = graph_model.findall(".//mxCell[@value]")
        fixed_count = 0
        
        for cell in cells:
            cell_id = cell.get('id', '')
            value = cell.get('value', '')
            
            # 检查是否是需要修正的步骤
            if cell_id in self.step_departments:
                target_dept = self.step_departments[cell_id]
                target_lane = self.swimlanes[target_dept]
                
                # 获取几何信息
                geometry = cell.find('mxGeometry')
                if geometry is not None:
                    current_x = int(geometry.get('x', '0'))
                    current_width = int(geometry.get('width', '150'))
                    current_height = int(geometry.get('height', '85'))
                    
                    # 计算新的Y坐标（居中在泳道中）
                    lane_center_y = target_lane['y_start'] + (target_lane['y_end'] - target_lane['y_start'] - current_height) // 2
                    
                    # 更新位置
                    geometry.set('y', str(lane_center_y))
                    geometry.set('width', '150')  # 标准化宽度
                    geometry.set('height', '85')  # 标准化高度
                    
                    # 更新颜色
                    current_style = cell.get('style', '')
                    if 'fillColor=' in current_style:
                        new_style = re.sub(r'fillColor=#[A-Fa-f0-9]{6}', f'fillColor={target_lane["color"]}', current_style)
                        cell.set('style', new_style)
                    
                    # 更新步骤内容（如果有修正信息）
                    if cell_id in self.step_corrections:
                        correction = self.step_corrections[cell_id]
                        new_value = f"{cell_id}. {correction['title']}\\n\\n🏢 {correction['department']}\\n💻 系统\\n\\n{correction['content']}"
                        cell.set('value', new_value)
                    
                    fixed_count += 1
        
        print(f"✅ 修正了 {fixed_count} 个步骤的位置")
        return fixed_count
    
    def optimize_connections(self, graph_model):
        """优化连接线为折线"""
        connections = graph_model.findall(".//mxCell[@edge='1']")
        optimized_count = 0
        
        for conn in connections:
            current_style = conn.get('style', '')
            if 'edgeStyle=orthogonalEdgeStyle' not in current_style:
                new_style = current_style + ';edgeStyle=orthogonalEdgeStyle;curved=0;orthogonalLoop=1;jettySize=auto;'
                conn.set('style', new_style)
                optimized_count += 1
        
        print(f"✅ 优化了 {optimized_count} 条连接线")
        return optimized_count
    
    def add_completion_note(self, graph_model):
        """添加修复完成说明"""
        # 找到最大cell_id
        cells = graph_model.findall(".//mxCell")
        max_id = 0
        for cell in cells:
            try:
                cell_id = int(cell.get('id', '0'))
                max_id = max(max_id, cell_id)
            except:
                pass
        
        # 添加修复说明
        note_id = max_id + 2000
        note_cell = ET.SubElement(graph_model.find('root'), 'mxCell')
        note_cell.set('id', str(note_id))
        note_cell.set('value', 
            "流程图位置修复完成说明\\n"
            f"🔧 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n"
            "✅ 所有步骤已放置在正确泳道中\\n"
            "🎯 保持生产部门细分结构\\n"
            "📐 统一单元格尺寸为150×85px\\n"
            "🔗 连接线已优化为折线格式"
        )
        note_cell.set('style', 
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6FA;strokeColor=#000000;fontSize=11;fontStyle=1;"
        )
        note_cell.set('vertex', '1')
        note_cell.set('parent', '1')
        
        # 添加几何信息
        geometry = ET.SubElement(note_cell, 'mxGeometry')
        geometry.set('x', '50')
        geometry.set('y', '50')
        geometry.set('width', '350')
        geometry.set('height', '100')
        geometry.set('as', 'geometry')
    
    def fix_flowchart(self, input_file, output_file):
        """修复流程图"""
        print("🚀 开始修复流程图位置...")
        
        # 解析文件
        tree, root, graph_model = self.parse_flowchart(input_file)
        
        # 修正步骤位置
        print("📐 修正步骤位置到正确泳道...")
        position_count = self.fix_step_positions(graph_model)
        
        # 优化连接线
        print("🔗 优化连接线为折线...")
        connection_count = self.optimize_connections(graph_model)
        
        # 添加修复说明
        print("📋 添加修复完成说明...")
        self.add_completion_note(graph_model)
        
        # 保存文件
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ 修复完成!")
        print(f"📁 输出文件: {output_file}")
        print(f"📊 修复统计:")
        print(f"   • 修正步骤位置: {position_count} 个")
        print(f"   • 优化连接线: {connection_count} 条")
        print(f"   • 泳道总数: {len(self.swimlanes)} 个")
        
        return output_file

def main():
    """主函数"""
    input_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-融合业务跟单-新版.drawio"
    output_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-位置修复完成版.drawio"
    
    fixer = FlowchartPositionFixer()
    
    try:
        result_file = fixer.fix_flowchart(input_file, output_file)
        print(f"\\n🎉 流程图修复成功完成！")
        print(f"📋 新文件已保存：{result_file}")
        print(f"💡 建议用Draw.io打开查看修复效果")
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()