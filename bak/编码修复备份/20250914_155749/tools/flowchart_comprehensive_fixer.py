#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图全面优化修复工具 v2.0
解决布局不合理、连线混乱、业务逻辑错误等问题
"""

import xml.etree.ElementTree as ET
import re
from datetime import datetime

class FlowchartComprehensiveFixer:
    def __init__(self):
        # 重新设计的标准泳道布局 (调整为100px高度)
        self.swimlanes = {
            "客户": {"y_start": 150, "y_end": 250, "color": "#E6F3FF"},
            "业务部": {"y_start": 250, "y_end": 350, "color": "#FFE6E6"},
            "研发部": {"y_start": 350, "y_end": 450, "color": "#E6FFF0"},
            "工程部": {"y_start": 450, "y_end": 550, "color": "#FFFFE6"},
            "财务部": {"y_start": 550, "y_end": 650, "color": "#E0FFFF"},
            "管理层": {"y_start": 650, "y_end": 750, "color": "#FFB6C1"},
            "PMC部": {"y_start": 750, "y_end": 850, "color": "#E6F3FF"},
            "采购部": {"y_start": 850, "y_end": 950, "color": "#F0F8FF"},
            "供应商": {"y_start": 950, "y_end": 1050, "color": "#FFF0F5"},
            "仓储部": {"y_start": 1050, "y_end": 1150, "color": "#F0E6FF"},
            "装配线": {"y_start": 1150, "y_end": 1250, "color": "#FFE4E1"},
            "五金": {"y_start": 1250, "y_end": 1350, "color": "#FFE4E1"},
            "注塑": {"y_start": 1350, "y_end": 1450, "color": "#FFE4E1"},
            "丝印": {"y_start": 1450, "y_end": 1550, "color": "#FFE4E1"},
            "品质部": {"y_start": 1550, "y_end": 1650, "color": "#FFF0E6"}
        }
        
        # 重新规划的步骤部门分配
        self.step_departments = {
            "S01": "客户",
            "S02": "业务部", 
            "S03": "工程部",      # 从研发部改为工程部
            "S04": "财务部",
            "D01": "管理层",
            "S06": "业务部",
            "S07": "业务部",
            "S08": "工程部",
            "S08.1": "工程部",
            "S08.2": "工程部",
            "S08.3": "客户",
            "S09": "PMC部",       # 生产准备统筹
            "S10": "PMC部",       # BOM制定
            "S11": "PMC部",       # 生产计划
            "S12": "采购部",      # 采购执行
            "S13": "仓储部",      # 物料入库
            "S14": "供应商",      # 供应商交付
            "S15": "PMC部",       # 生产调度
            "S16": "品质部",      # 首件检验
            "S17": "PMC部",       # 生产任务下达
            "S18": "仓储部",      # 物料领用
            "S19": "装配线",      # 重新定义为装配准备
            "S20.1": "五金",      # 五金生产
            "S20.2": "注塑",      # 注塑生产  
            "S20.3": "丝印",      # 丝印生产
            "S20": "装配线",      # 装配生产
            "S21": "品质部",      # 过程检验
            "S22": "品质部",      # 成品检验
            "S23": "仓储部",      # 包装入库
            "S24": "仓储部",      # 出货安排
            "S25": "客户",        # 收货确认
            "S26": "业务部",      # 开票申请
            "S27": "财务部",      # 发票开具
            "S28": "客户",        # 发票寄送
            "D04": "财务部",      # 付款决策
            "S29": "业务部",      # 付款催收
            "S30": "客户",        # 客户付款
            "S31": "财务部",      # 收款确认
            "S32": "业务部",      # 订单结案
            "E01": "客户"         # 流程结束
        }
        
        # 重新设计的水平位置布局 (X坐标)
        self.step_positions = {
            "S01": {"x": 200, "y": None},   # 客户询价
            "S02": {"x": 500, "y": None},   # 商务洽谈
            "S03": {"x": 800, "y": None},   # 技术评估  
            "S04": {"x": 1100, "y": None},  # 成本核算
            "D01": {"x": 1400, "y": None},  # 管理决策
            "S06": {"x": 1700, "y": None},  # 合同签订
            "S07": {"x": 2000, "y": None},  # 订单录入
            "S08": {"x": 2300, "y": None},  # 工程设计
            "S08.1": {"x": 2600, "y": None}, # 图纸会审
            "S08.2": {"x": 2900, "y": None}, # 图纸修正
            "S08.3": {"x": 3200, "y": None}, # 客户确认
            "S09": {"x": 200, "y": None},   # 生产准备(PMC)
            "S10": {"x": 500, "y": None},   # BOM制定
            "S11": {"x": 800, "y": None},   # 生产计划
            "S12": {"x": 1100, "y": None},  # 采购订单
            "S13": {"x": 1400, "y": None},  # 物料入库
            "S14": {"x": 1700, "y": None},  # 供应商交付
            "S15": {"x": 2000, "y": None},  # 生产调度
            "S16": {"x": 2300, "y": None},  # 首件检验
            "S17": {"x": 2600, "y": None},  # 任务下达
            "S18": {"x": 2900, "y": None},  # 物料领用
            "S19": {"x": 3200, "y": None},  # 装配准备
            "S20.1": {"x": 200, "y": None}, # 五金生产
            "S20.2": {"x": 500, "y": None}, # 注塑生产
            "S20.3": {"x": 800, "y": None}, # 丝印生产
            "S20": {"x": 1100, "y": None},  # 装配生产
            "S21": {"x": 1400, "y": None},  # 过程检验
            "S22": {"x": 1700, "y": None},  # 成品检验
            "S23": {"x": 2000, "y": None},  # 包装入库
            "S24": {"x": 2300, "y": None},  # 出货安排
            "S25": {"x": 2600, "y": None},  # 客户收货
            "S26": {"x": 2900, "y": None},  # 开票申请
            "S27": {"x": 3200, "y": None},  # 发票开具
            "S28": {"x": 3500, "y": None},  # 发票寄送
            "D04": {"x": 3800, "y": None},  # 付款决策
            "S29": {"x": 4100, "y": None},  # 付款催收
            "S30": {"x": 4400, "y": None},  # 客户付款
            "S31": {"x": 4700, "y": None},  # 收款确认
            "S32": {"x": 5000, "y": None},  # 订单结案
            "E01": {"x": 5300, "y": None}   # 流程结束
        }
        
        # 步骤内容优化
        self.step_content_updates = {
            "S09": {
                "title": "生产准备启动\n资源统筹配置",
                "department": "PMC部",
                "content": "📌 业务跟单要点:\n• 生产资源评估\n• 工艺流程确认\n• 生产计划制定"
            },
            "S19": {
                "title": "装配准备工作\n工艺设备调试", 
                "department": "装配线",
                "content": "📌 业务跟单要点:\n• 装配工艺确认\n• 设备状态检查\n• 人员技能培训"
            }
        }
        
        # 重新设计连接关系(解决连接逻辑问题)
        self.connection_map = {
            "S01": ["S02"],
            "S02": ["S03"], 
            "S03": ["S04"],
            "S04": ["D01"],
            "D01": ["S06"],  # 接受分支
            "S06": ["S07"],
            "S07": ["S08"],
            "S08": ["S08.1"],
            "S08.1": ["S08.2"],
            "S08.2": ["S08.3"],
            "S08.3": ["S09"],  # 客户确认后启动生产准备
            "S09": ["S10"],   # 生产准备→BOM制定
            "S10": ["S11"],   # BOM→生产计划
            "S11": ["S12"],   # 生产计划→采购订单
            "S12": ["S13"],   # 采购→物料入库
            "S13": ["S14"],   # 入库检验→供应商确认
            "S14": ["S15"],   # 供应商交付→生产调度
            "S15": ["S16"],   # 生产调度→首件检验
            "S16": ["S17"],   # 首件检验→任务下达
            "S17": ["S18"],   # 任务下达→物料领用
            "S18": ["S19"],   # 物料准备→装配准备
            "S19": ["S20.1", "S20.2", "S20.3"],  # 分支到各生产线
            "S20.1": ["S20"], # 五金→装配
            "S20.2": ["S20"], # 注塑→装配
            "S20.3": ["S20"], # 丝印→装配
            "S20": ["S21"],   # 装配→过程检验
            "S21": ["S22"],   # 过程检验→成品检验
            "S22": ["S23"],   # 成品检验→包装入库
            "S23": ["S24"],   # 包装→出货安排
            "S24": ["S25"],   # 出货→客户收货
            "S25": ["S26"],   # 收货→开票申请
            "S26": ["S27"],   # 开票→发票开具
            "S27": ["S28"],   # 开具→发票寄送
            "S28": ["D04"],   # 发票→付款决策
            "D04": ["S30", "S29"],  # 决策分支
            "S29": ["S30"],   # 催收→付款
            "S30": ["S31"],   # 付款→收款确认
            "S31": ["S32"],   # 收款→订单结案
            "S32": ["E01"]    # 结案→流程结束
        }
    
    def parse_flowchart(self, file_path):
        """解析流程图XML文件"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        graph_model = root.find(".//mxGraphModel")
        if graph_model is None:
            raise ValueError("未找到mxGraphModel元素")
        return tree, root, graph_model
    
    def fix_swimlanes(self, graph_model):
        """修正泳道Y坐标范围"""
        fixed_count = 0
        lanes = graph_model.findall(".//mxCell[@id]")
        
        for lane in lanes:
            lane_id = lane.get('id', '')
            if lane_id.startswith('lane_'):
                # 提取部门名称
                dept_name = None
                value = lane.get('value', '')
                for dept in self.swimlanes.keys():
                    if dept in value:
                        dept_name = dept
                        break
                
                if dept_name:
                    geometry = lane.find('mxGeometry')
                    if geometry is not None:
                        target_y = self.swimlanes[dept_name]['y_start']
                        geometry.set('y', str(target_y))
                        geometry.set('height', '100')  # 标准100px高度
                        fixed_count += 1
        
        print(f"✅ 修正了 {fixed_count} 个泳道位置")
        return fixed_count
    
    def fix_step_positions_comprehensive(self, graph_model):
        """全面修正步骤位置"""
        fixed_count = 0
        cells = graph_model.findall(".//mxCell[@value]")
        
        for cell in cells:
            cell_id = cell.get('id', '')
            
            if cell_id in self.step_departments:
                dept_name = self.step_departments[cell_id]
                target_lane = self.swimlanes[dept_name]
                target_position = self.step_positions.get(cell_id, {})
                
                geometry = cell.find('mxGeometry')
                if geometry is not None:
                    # 设置X坐标
                    if 'x' in target_position:
                        geometry.set('x', str(target_position['x']))
                    
                    # 设置Y坐标(泳道中心)
                    lane_center_y = target_lane['y_start'] + (target_lane['y_end'] - target_lane['y_start'] - 85) // 2
                    geometry.set('y', str(lane_center_y))
                    
                    # 标准化尺寸
                    geometry.set('width', '180')   # 增大宽度适应内容
                    geometry.set('height', '85')
                    
                    # 更新颜色
                    current_style = cell.get('style', '')
                    if 'fillColor=' in current_style:
                        new_style = re.sub(r'fillColor=#[A-Fa-f0-9]{6}', 
                                          f'fillColor={target_lane["color"]}', current_style)
                        cell.set('style', new_style)
                    
                    # 更新内容(如果有优化)
                    if cell_id in self.step_content_updates:
                        update_info = self.step_content_updates[cell_id]
                        new_value = (f"{cell_id}. {update_info['title']}\\n\\n"
                                   f"🏢 {update_info['department']}\\n"
                                   f"💻 系统\\n\\n{update_info['content']}")
                        cell.set('value', new_value)
                    
                    fixed_count += 1
        
        print(f"✅ 全面修正了 {fixed_count} 个步骤位置")
        return fixed_count
    
    def remove_duplicate_steps(self, graph_model):
        """删除重复的步骤定义"""
        root_element = graph_model.find('root')
        cells_to_remove = []
        
        # 查找重复的S09和S19
        s09_cells = []
        cells = root_element.findall('mxCell')
        
        for cell in cells:
            cell_id = cell.get('id', '')
            if cell_id == 'S09' or (cell.get('value', '').startswith('S09') and cell_id != 'S09'):
                s09_cells.append(cell)
        
        # 如果找到多个S09，保留第一个，删除其他
        if len(s09_cells) > 1:
            for cell in s09_cells[1:]:
                cells_to_remove.append(cell)
                print(f"🗑️ 标记删除重复步骤: {cell.get('id', 'unknown')}")
        
        # 删除标记的重复步骤
        for cell in cells_to_remove:
            root_element.remove(cell)
        
        return len(cells_to_remove)
    
    def optimize_connections_comprehensive(self, graph_model):
        """全面优化连接线"""
        root_element = graph_model.find('root')
        
        # 删除所有现有连接
        existing_connections = root_element.findall(".//mxCell[@edge='1']")
        for conn in existing_connections:
            root_element.remove(conn)
        
        # 重新创建连接
        connection_id = 3000
        created_count = 0
        
        for source_id, target_list in self.connection_map.items():
            for target_id in target_list:
                # 创建新的连接
                edge = ET.SubElement(root_element, 'mxCell')
                edge.set('id', f'edge_{connection_id}')
                edge.set('style', 
                        'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;'
                        'jettySize=auto;html=1;curved=0;entryX=0;entryY=0.5;'
                        'exitX=1;exitY=0.5;entryDx=0;entryDy=0;exitDx=0;exitDy=0;')
                edge.set('edge', '1')
                edge.set('parent', '1')
                edge.set('source', source_id)
                edge.set('target', target_id)
                
                # 添加几何信息
                geometry = ET.SubElement(edge, 'mxGeometry')
                geometry.set('relative', '1')
                geometry.set('as', 'geometry')
                
                connection_id += 1
                created_count += 1
        
        print(f"✅ 重新创建了 {created_count} 条连接线")
        return created_count
    
    def add_decision_branches(self, graph_model):
        """添加决策分支处理"""
        root_element = graph_model.find('root')
        
        # 为D01添加拒绝分支
        reject_step = ET.SubElement(root_element, 'mxCell')
        reject_step.set('id', 'S05_REJECT')
        reject_step.set('value', 
            "S05. 订单拒绝\\n风险评估不通过\\n\\n🏢 业务部\\n💻 CRM系统\\n\\n"
            "📌 业务跟单要点:\\n• 拒绝原因说明\\n• 客户关系维护")
        reject_step.set('style', 
            'rounded=1;whiteSpace=wrap;html=1;fillColor=#FFE6E6;strokeColor=#FF0000;fontSize=12;')
        reject_step.set('vertex', '1')
        reject_step.set('parent', '1')
        
        # 添加几何信息
        geometry = ET.SubElement(reject_step, 'mxGeometry')
        geometry.set('x', '1000')
        geometry.set('y', '275')  # 业务部泳道
        geometry.set('width', '180')
        geometry.set('height', '85')
        geometry.set('as', 'geometry')
        
        print("✅ 添加了决策分支处理")
    
    def add_comprehensive_legend(self, graph_model):
        """添加全面的图例说明"""
        root_element = graph_model.find('root')
        
        legend = ET.SubElement(root_element, 'mxCell')
        legend.set('id', 'comprehensive_legend')
        legend.set('value', 
            "综合订单全流程ERP系统业务流程图\\n"
            "🔧 全面优化版本 v2.0\\n"
            f"✅ 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n\\n"
            "🎯 主要改进:\\n"
            "• 重新设计泳道布局(100px标准高度)\\n"
            "• 优化步骤位置分配(避免重叠)\\n" 
            "• 重构连接线逻辑(符合业务流程)\\n"
            "• 消除重复步骤定义\\n"
            "• 标准化单元格尺寸(180×85px)\\n\\n"
            "📋 使用说明:\\n"
            "• 蓝色系：客户相关步骤\\n"
            "• 红色系：业务部门步骤\\n"
            "• 绿色系：技术部门步骤\\n"
            "• 橙色系：生产部门步骤\\n"
            "• 紫色系：支持部门步骤"
        )
        legend.set('style', 
            'rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F8FF;strokeColor=#4169E1;'
            'fontSize=11;fontStyle=1;align=left;verticalAlign=top;')
        legend.set('vertex', '1')
        legend.set('parent', '1')
        
        # 添加几何信息
        geometry = ET.SubElement(legend, 'mxGeometry')
        geometry.set('x', '50')
        geometry.set('y', '50')
        geometry.set('width', '400')
        geometry.set('height', '250')
        geometry.set('as', 'geometry')
        
        print("✅ 添加了全面的图例说明")
    
    def comprehensive_fix(self, input_file, output_file):
        """执行全面修复"""
        print("🚀 开始流程图全面优化修复...")
        
        # 解析文件
        tree, root, graph_model = self.parse_flowchart(input_file)
        
        # 1. 修正泳道布局
        print("📐 修正泳道布局...")
        swimlane_count = self.fix_swimlanes(graph_model)
        
        # 2. 删除重复步骤
        print("🗑️ 删除重复步骤...")
        duplicate_count = self.remove_duplicate_steps(graph_model)
        
        # 3. 全面修正步骤位置
        print("📍 全面修正步骤位置...")
        position_count = self.fix_step_positions_comprehensive(graph_model)
        
        # 4. 重新设计连接线
        print("🔗 重新设计连接线...")
        connection_count = self.optimize_connections_comprehensive(graph_model)
        
        # 5. 添加决策分支
        print("🔀 添加决策分支...")
        self.add_decision_branches(graph_model)
        
        # 6. 添加全面图例
        print("📋 添加图例说明...")
        self.add_comprehensive_legend(graph_model)
        
        # 保存文件
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ 全面修复完成!")
        print(f"📁 输出文件: {output_file}")
        print(f"📊 修复统计:")
        print(f"   • 修正泳道布局: {swimlane_count} 个")
        print(f"   • 删除重复步骤: {duplicate_count} 个")
        print(f"   • 修正步骤位置: {position_count} 个")
        print(f"   • 重建连接线: {connection_count} 条")
        print(f"   • 泳道总数: {len(self.swimlanes)} 个")
        print(f"   • 业务步骤总数: {len(self.step_departments)} 个")
        
        return output_file

def main():
    """主函数"""
    input_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-位置修复完成版.drawio"
    output_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-全面优化版.drawio"
    
    fixer = FlowchartComprehensiveFixer()
    
    try:
        result_file = fixer.comprehensive_fix(input_file, output_file)
        print(f"\\n🎉 流程图全面优化成功完成！")
        print(f"📋 新文件：{result_file}")
        print(f"💡 建议用Draw.io打开查看优化效果")
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()