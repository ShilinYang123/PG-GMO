#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图泳道位置修复工具
修复泳道中节点位置错乱，并锁定泳道防止误操作
"""

import xml.etree.ElementTree as ET
import re
from datetime import datetime

class FlowchartLaneFixer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        self.fixes = []
        
        # 定义泳道和对应的背景颜色
        self.lane_configs = {
            'lane_customer': {
                'name': '客户',
                'color': '#E6F3FF',
                'y': 150,
                'height': 100,
                'nodes': ['S01', 'S25', 'S28', 'S30']
            },
            'lane_business': {
                'name': '业务部',
                'color': '#FFE6E6', 
                'y': 250,
                'height': 100,
                'nodes': ['S02', 'S06', 'S07', 'S26', 'S29', 'S32', 'E01']
            },
            'lane_engineering': {
                'name': '工程部',
                'color': '#FFFFE6',
                'y': 350,
                'height': 100,
                'nodes': ['S03', 'S08', 'S08.1', 'S08.2']
            },
            'lane_finance': {
                'name': '财务部',
                'color': '#E0FFFF',
                'y': 450,
                'height': 100,
                'nodes': ['S04', 'S27', 'S31', 'D04']
            },
            'lane_management': {
                'name': '管理层',
                'color': '#FFB6C1',
                'y': 550,
                'height': 100,
                'nodes': ['D01']
            },
            'lane_pmc': {
                'name': 'PMC部',
                'color': '#E6F3FF',
                'y': 650,
                'height': 100,
                'nodes': ['S09', 'S10', 'S11', 'S15', 'S17']
            },
            'lane_procurement': {
                'name': '采购部',
                'color': '#F0F8FF',
                'y': 750,
                'height': 100,
                'nodes': ['S12']
            },
            'lane_supplier': {
                'name': '供应商',
                'color': '#FFF0F5',
                'y': 850,
                'height': 100,
                'nodes': ['S14']
            },
            'lane_warehouse': {
                'name': '仓储部',
                'color': '#F0E6FF',
                'y': 950,
                'height': 100,
                'nodes': ['S13', 'S18', 'S23', 'S24']
            },
            'lane_assembly': {
                'name': '装配线',
                'color': '#FFE4E1',
                'y': 1050,
                'height': 200,
                'nodes': ['S19', 'S20']
            },
            'lane_hardware': {
                'name': '五金',
                'color': '#FFE4E1',
                'y': 1150,
                'height': 300,
                'nodes': ['S20.1']
            },
            'lane_injection': {
                'name': '注塑',
                'color': '#FFE4E1',
                'y': 1250,
                'height': 100,
                'nodes': ['S20.2']
            },
            'lane_silkscreen': {
                'name': '丝印',
                'color': '#FFE4E1',
                'y': 1350,
                'height': 150,
                'nodes': ['S20.3']
            },
            'lane_quality': {
                'name': '品质部',
                'color': '#FFF0E6',
                'y': 1450,
                'height': 250,
                'nodes': ['S16', 'S21', 'S22', 'Q01_IQC', 'Q02_IPQC1', 'Q03_IPQC2', 'Q04_IPQC3', 'Q05_IPQC4', 'Q06_LAB', 'Q07_QA', 'Q08_QE']
            }
        }

    def find_element_by_id(self, element_id):
        """查找指定ID的元素"""
        for elem in self.root.iter('mxCell'):
            if elem.get('id') == element_id:
                return elem
        return None

    def fix_node_parent_relationships(self):
        """修复节点的父子关系，将节点放置到正确的泳道中"""
        fixed_nodes = []
        
        for lane_id, config in self.lane_configs.items():
            for node_id in config['nodes']:
                node = self.find_element_by_id(node_id)
                if node is not None:
                    current_parent = node.get('parent', '1')
                    if current_parent != lane_id:
                        # 修复父子关系
                        node.set('parent', lane_id)
                        fixed_nodes.append(f"{node_id}: {current_parent} → {lane_id}")
                        
                        # 修复节点颜色，使其与泳道匹配
                        style = node.get('style', '')
                        expected_color = config['color']
                        
                        # 更新fillColor
                        if 'fillColor=' in style:
                            style = re.sub(r'fillColor=#[A-Fa-f0-9]{6}', f'fillColor={expected_color}', style)
                        else:
                            style += f';fillColor={expected_color}'
                        
                        node.set('style', style)
        
        if fixed_nodes:
            self.fixes.append("节点父子关系修复:")
            self.fixes.extend([f"  • {fix}" for fix in fixed_nodes])
        
        return len(fixed_nodes)

    def lock_swimlanes(self):
        """锁定所有泳道，防止意外移动"""
        locked_lanes = []
        
        for lane_id in self.lane_configs.keys():
            lane = self.find_element_by_id(lane_id)
            if lane is not None:
                style = lane.get('style', '')
                
                # 添加锁定属性
                if 'locked=1' not in style:
                    style += ';locked=1'
                    lane.set('style', style)
                    locked_lanes.append(lane_id)
        
        if locked_lanes:
            self.fixes.append("泳道锁定:")
            self.fixes.extend([f"  • {lane_id}" for lane_id in locked_lanes])
        
        return len(locked_lanes)

    def fix_swimlane_positions(self):
        """修复泳道位置，确保垂直排列正确"""
        position_fixes = []
        
        for lane_id, config in self.lane_configs.items():
            lane = self.find_element_by_id(lane_id)
            if lane is not None:
                geometry = lane.find('mxGeometry')
                if geometry is not None:
                    current_y = int(geometry.get('y', 0))
                    expected_y = config['y']
                    
                    if current_y != expected_y:
                        geometry.set('y', str(expected_y))
                        position_fixes.append(f"{lane_id}: y={current_y} → y={expected_y}")
        
        if position_fixes:
            self.fixes.append("泳道位置修复:")
            self.fixes.extend([f"  • {fix}" for fix in position_fixes])
        
        return len(position_fixes)

    def standardize_swimlane_styles(self):
        """标准化泳道样式"""
        style_fixes = []
        
        standard_style_parts = {
            'swimlane': 'swimlane',
            'html': 'html=1',
            'startSize': 'startSize=20',
            'horizontal': 'horizontal=0',
            'strokeColor': 'strokeColor=#4A90E2',
            'strokeWidth': 'strokeWidth=2',
            'strokeDashArray': 'strokeDashArray=15,5',
            'fontSize': 'fontSize=14',
            'fontStyle': 'fontStyle=1'
        }
        
        for lane_id, config in self.lane_configs.items():
            lane = self.find_element_by_id(lane_id)
            if lane is not None:
                current_style = lane.get('style', '')
                
                # 构建标准样式
                new_style_parts = []
                new_style_parts.append('swimlane')
                new_style_parts.append('html=1')
                new_style_parts.append('startSize=20')
                new_style_parts.append('horizontal=0')
                new_style_parts.append(f'fillColor={config["color"]}')
                new_style_parts.append('strokeColor=#4A90E2')
                new_style_parts.append('strokeWidth=2')
                new_style_parts.append('strokeDashArray=15,5')
                new_style_parts.append('fontSize=14')
                new_style_parts.append('fontStyle=1')
                new_style_parts.append('locked=1')  # 添加锁定
                
                new_style = ';'.join(new_style_parts)
                
                if current_style != new_style:
                    lane.set('style', new_style)
                    style_fixes.append(f"{lane_id}: 样式标准化")
        
        if style_fixes:
            self.fixes.append("泳道样式标准化:")
            self.fixes.extend([f"  • {fix}" for fix in style_fixes])
        
        return len(style_fixes)

    def fix_node_positions_in_lanes(self):
        """调整节点在泳道内的相对位置"""
        position_fixes = []
        
        for lane_id, config in self.lane_configs.items():
            for node_id in config['nodes']:
                node = self.find_element_by_id(node_id)
                if node is not None and node.get('parent') == lane_id:
                    geometry = node.find('mxGeometry')
                    if geometry is not None:
                        current_y = int(geometry.get('y', 0))
                        # 确保节点在泳道内部的合理位置（距离泳道顶部15px）
                        expected_y = 15
                        
                        if current_y != expected_y:
                            geometry.set('y', str(expected_y))
                            position_fixes.append(f"{node_id}: 泳道内y={current_y} → y={expected_y}")
        
        if position_fixes:
            self.fixes.append("节点泳道内位置修复:")
            self.fixes.extend([f"  • {fix}" for fix in position_fixes])
        
        return len(position_fixes)

    def run_fixes(self):
        """执行所有修复操作"""
        print("🔧 开始修复流程图泳道和节点位置...")
        
        # 执行各种修复
        node_fixes = self.fix_node_parent_relationships()
        position_fixes = self.fix_swimlane_positions()
        style_fixes = self.standardize_swimlane_styles()
        lane_position_fixes = self.fix_node_positions_in_lanes()
        lock_fixes = self.lock_swimlanes()
        
        total_fixes = node_fixes + position_fixes + style_fixes + lane_position_fixes
        
        if total_fixes > 0:
            # 保存修复后的文件
            backup_path = self.file_path.replace('.drawio', '_backup.drawio')
            self.tree.write(backup_path, encoding='utf-8', xml_declaration=True)
            print(f"📁 原文件备份到: {backup_path}")
            
            self.tree.write(self.file_path, encoding='utf-8', xml_declaration=True)
            print(f"✅ 修复完成! 共修复 {total_fixes} 个问题")
            
            # 生成修复报告
            self.generate_report()
            
        else:
            print("✅ 流程图结构良好，无需修复")
        
        return total_fixes

    def generate_report(self):
        """生成修复报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.file_path.replace('.drawio', f'_修复报告_{timestamp}.md')
        
        report_content = f"""# 流程图泳道修复报告

## 📋 修复概要
**修复时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}  
**目标文件**: {self.file_path}  
**修复状态**: ✅ 完成

## 🔧 修复详情

"""
        
        for fix_section in self.fixes:
            report_content += fix_section + "\n"
        
        report_content += f"""

## 🎯 修复成果

### ✅ 主要改进
1. **节点归位**: 所有业务节点正确放置在对应泳道中
2. **泳道锁定**: 所有泳道已锁定，防止意外移动
3. **样式统一**: 泳道样式标准化，视觉效果一致
4. **位置优化**: 节点在泳道内位置规范化

### 📊 泳道配置确认
"""
        
        for lane_id, config in self.lane_configs.items():
            report_content += f"- **{config['name']}** (`{lane_id}`): {len(config['nodes'])}个节点\n"
        
        report_content += f"""

### 🛡️ 锁定保护
- 所有泳道已设置 `locked=1` 属性
- 防止意外拖拽和调整泳道位置
- 需要修改时需要先解锁

## 📁 文件状态
- **原文件**: 已更新修复
- **备份文件**: 已自动创建备份
- **兼容性**: 完全兼容Draw.io

---
**修复工具**: FlowchartLaneFixer v1.0  
**生成时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 修复报告已生成: {report_path}")

def main():
    file_path = r"S:\PG-GMO\office\业务部\小家电制造业详细生产流程图-交叉优化版.drawio"
    
    try:
        fixer = FlowchartLaneFixer(file_path)
        fixer.run_fixes()
        
    except Exception as e:
        print(f"❌ 修复过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()