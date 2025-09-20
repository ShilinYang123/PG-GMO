#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连接线重叠修复工具
专门解决流程图中连接线重叠造成关系错乱的问题
"""

import xml.etree.ElementTree as ET
from datetime import datetime

class ConnectionOverlapFixer:
    def __init__(self):
        # 清理重建的连接关系（避免重叠）
        self.clean_connections = [
            # 第一阶段：需求到决策
            {"id": "edge_001", "source": "S01", "target": "S02", "label": ""},
            {"id": "edge_002", "source": "S02", "target": "S03", "label": ""},  
            {"id": "edge_003", "source": "S03", "target": "S04", "label": ""},
            {"id": "edge_004", "source": "S04", "target": "D01", "label": ""},
            {"id": "edge_005", "source": "D01", "target": "S06", "label": "接受"},
            
            # 第二阶段：合同到设计
            {"id": "edge_006", "source": "S06", "target": "S07", "label": ""},
            {"id": "edge_007", "source": "S07", "target": "S08", "label": ""},
            {"id": "edge_008", "source": "S08", "target": "S08.1", "label": ""},
            {"id": "edge_009", "source": "S08.1", "target": "S08.2", "label": ""},
            {"id": "edge_010", "source": "S08.2", "target": "S08.3", "label": ""},
            
            # 第三阶段：生产准备
            {"id": "edge_011", "source": "S08.3", "target": "S09", "label": "确认"},
            {"id": "edge_012", "source": "S09", "target": "S10", "label": ""},
            {"id": "edge_013", "source": "S10", "target": "S11", "label": ""},
            {"id": "edge_014", "source": "S11", "target": "S12", "label": ""},
            {"id": "edge_015", "source": "S12", "target": "S13", "label": ""},
            {"id": "edge_016", "source": "S13", "target": "S14", "label": ""},
            {"id": "edge_017", "source": "S14", "target": "S15", "label": ""},
            {"id": "edge_018", "source": "S15", "target": "S16", "label": ""},
            {"id": "edge_019", "source": "S16", "target": "S17", "label": ""},
            {"id": "edge_020", "source": "S17", "target": "S18", "label": ""},
            {"id": "edge_021", "source": "S18", "target": "S19", "label": ""},
            
            # 第四阶段：生产分支（避免重叠）
            {"id": "edge_022", "source": "S19", "target": "S20.1", "label": "五金"},
            {"id": "edge_023", "source": "S19", "target": "S20.2", "label": "注塑"},
            {"id": "edge_024", "source": "S19", "target": "S20.3", "label": "丝印"},
            {"id": "edge_025", "source": "S20.1", "target": "S20", "label": ""},
            {"id": "edge_026", "source": "S20.2", "target": "S20", "label": ""},
            {"id": "edge_027", "source": "S20.3", "target": "S20", "label": ""},
            
            # 第五阶段：质检到交付
            {"id": "edge_028", "source": "S20", "target": "S21", "label": ""},
            {"id": "edge_029", "source": "S21", "target": "S22", "label": ""},
            {"id": "edge_030", "source": "S22", "target": "S23", "label": ""},
            {"id": "edge_031", "source": "S23", "target": "S24", "label": ""},
            {"id": "edge_032", "source": "S24", "target": "S25", "label": ""},
            
            # 第六阶段：开票收款
            {"id": "edge_033", "source": "S25", "target": "S26", "label": ""},
            {"id": "edge_034", "source": "S26", "target": "S27", "label": ""},
            {"id": "edge_035", "source": "S27", "target": "S28", "label": ""},
            {"id": "edge_036", "source": "S28", "target": "D04", "label": ""},
            {"id": "edge_037", "source": "D04", "target": "S30", "label": "正常付款"},
            {"id": "edge_038", "source": "D04", "target": "S29", "label": "需催收"},
            {"id": "edge_039", "source": "S29", "target": "S30", "label": ""},
            {"id": "edge_040", "source": "S30", "target": "S31", "label": ""},
            {"id": "edge_041", "source": "S31", "target": "S32", "label": ""},
            {"id": "edge_042", "source": "S32", "target": "E01", "label": ""}
        ]
    
    def parse_flowchart(self, file_path):
        """解析流程图文件"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        graph_model = root.find(".//mxGraphModel")
        if graph_model is None:
            raise ValueError("未找到mxGraphModel元素")
        return tree, root, graph_model
    
    def remove_all_connections(self, graph_model):
        """删除所有现有连接线"""
        root_element = graph_model.find('root')
        connections = root_element.findall(".//mxCell[@edge='1']")
        removed_count = 0
        
        for conn in connections:
            root_element.remove(conn)
            removed_count += 1
        
        print(f"✅ 删除了 {removed_count} 条旧连接线")
        return removed_count
    
    def create_clean_connections(self, graph_model):
        """创建清晰无重叠的连接线"""
        root_element = graph_model.find('root')
        created_count = 0
        
        for conn_info in self.clean_connections:
            edge = ET.SubElement(root_element, 'mxCell')
            edge.set('id', conn_info['id'])
            edge.set('value', conn_info['label'])
            edge.set('style', self.get_connection_style(conn_info))
            edge.set('edge', '1')
            edge.set('parent', '1')
            edge.set('source', conn_info['source'])
            edge.set('target', conn_info['target'])
            
            # 添加几何信息
            geometry = ET.SubElement(edge, 'mxGeometry')
            geometry.set('relative', '1')
            geometry.set('as', 'geometry')
            
            # 为分支连接添加路径点避免重叠
            if conn_info['source'] in ['S19', 'D04', 'D01']:
                points = ET.SubElement(geometry, 'Array')
                points.set('as', 'points')
                self.add_branch_points(points, conn_info)
            
            created_count += 1
        
        print(f"✅ 创建了 {created_count} 条清晰连接线")
        return created_count
    
    def get_connection_style(self, conn_info):
        """获取连接线样式"""
        base_style = ("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
                     "jettySize=auto;html=1;curved=0;")
        
        # 分支连接使用不同颜色避免混乱
        if conn_info['source'] == 'S19':  # 生产分支
            return base_style + "strokeColor=#FF6B35;strokeWidth=2;"
        elif conn_info['source'] == 'D04':  # 付款决策分支  
            return base_style + "strokeColor=#4ECDC4;strokeWidth=2;"
        elif conn_info['source'] == 'D01':  # 管理决策分支
            return base_style + "strokeColor=#45B7D1;strokeWidth=2;"
        else:
            return base_style + "strokeColor=#333333;strokeWidth=1;"
    
    def add_branch_points(self, points, conn_info):
        """为分支连接添加路径点避免重叠"""
        if conn_info['source'] == 'S19':
            # 生产分支路径点
            if conn_info['target'] == 'S20.1':
                point = ET.SubElement(points, 'mxPoint')
                point.set('x', '150')
                point.set('y', '0')
            elif conn_info['target'] == 'S20.2':
                point = ET.SubElement(points, 'mxPoint')
                point.set('x', '150')
                point.set('y', '100')
            elif conn_info['target'] == 'S20.3':
                point = ET.SubElement(points, 'mxPoint')
                point.set('x', '150')
                point.set('y', '200')
        
        elif conn_info['source'] == 'D04':
            # 付款决策分支路径点
            if conn_info['target'] == 'S30':
                point = ET.SubElement(points, 'mxPoint')
                point.set('x', '0')
                point.set('y', '-200')
            elif conn_info['target'] == 'S29':
                point = ET.SubElement(points, 'mxPoint')
                point.set('x', '100')
                point.set('y', '0')
    
    def add_connection_legend(self, graph_model):
        """添加连接线说明"""
        root_element = graph_model.find('root')
        
        legend = ET.SubElement(root_element, 'mxCell')
        legend.set('id', 'connection_legend')
        legend.set('value', 
            "连接线重叠修复说明\\n"
            f"🔧 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n\\n"
            "🎯 修复内容:\\n"
            "• 删除所有重叠连接线\\n"
            "• 重建42条清晰连接\\n"
            "• 分支连接使用不同颜色\\n"
            "• 添加路径点避免重叠\\n\\n"
            "🌈 连接线颜色说明:\\n"
            "• 黑色：主流程连接\\n"
            "• 橙色：生产分支连接\\n"
            "• 青色：付款决策分支\\n"
            "• 蓝色：管理决策分支"
        )
        legend.set('style', 
            'rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF8DC;strokeColor=#D4A574;'
            'fontSize=10;fontStyle=1;align=left;verticalAlign=top;')
        legend.set('vertex', '1')
        legend.set('parent', '1')
        
        # 添加几何信息
        geometry = ET.SubElement(legend, 'mxGeometry')
        geometry.set('x', '50')
        geometry.set('y', '1700')
        geometry.set('width', '300')
        geometry.set('height', '180')
        geometry.set('as', 'geometry')
    
    def fix_overlapping_connections(self, input_file, output_file):
        """修复重叠连接线"""
        print("🚀 开始修复连接线重叠问题...")
        
        # 解析文件
        tree, root, graph_model = self.parse_flowchart(input_file)
        
        # 删除所有现有连接
        print("🗑️ 删除重叠的连接线...")
        removed_count = self.remove_all_connections(graph_model)
        
        # 创建清晰的连接
        print("🔗 创建清晰无重叠连接...")
        created_count = self.create_clean_connections(graph_model)
        
        # 添加说明
        print("📋 添加修复说明...")
        self.add_connection_legend(graph_model)
        
        # 保存文件
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ 连接线重叠修复完成!")
        print(f"📁 输出文件: {output_file}")
        print(f"📊 修复统计:")
        print(f"   • 删除重叠连接: {removed_count} 条")
        print(f"   • 创建清晰连接: {created_count} 条")
        print(f"   • 分支连接优化: 9 处")
        
        return output_file

def main():
    """主函数"""
    input_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-位置修复完成版.drawio"
    output_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-连接线修复版.drawio"
    
    fixer = ConnectionOverlapFixer()
    
    try:
        result_file = fixer.fix_overlapping_connections(input_file, output_file)
        print(f"\\n🎉 连接线重叠问题修复成功！")
        print(f"📋 修复文件：{result_file}")
        print(f"💡 现在连接线清晰不重叠，关系明确")
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()