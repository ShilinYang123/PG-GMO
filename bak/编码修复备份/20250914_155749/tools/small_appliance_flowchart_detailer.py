#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小家电制造业生产过程细化工具
基于现有流程图，将生产过程细化到具体工序级别
体现小家电制造业的真实生产控制逻辑
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

class SmallApplianceFlowchartDetailer:
    def __init__(self):
        self.detailed_processes = {
            "quality_positions": {
                "IQC": "来料质量控制",
                "IPQC": "制程质量控制", 
                "QA": "质量保证",
                "QE": "质量工程",
                "LAB": "实验室测试"
            },
            "hardware_processes": {
                "MOLDING": "成型工序",
                "WELDING": "焊接工序",
                "POLISHING": "抛光工序", 
                "CLEANING": "清洗工序",
                "MOLD_ROOM": "模房工序"
            },
            "assembly_positions": {
                "MATERIAL_CONTROL": "物料控制",
                "MOLD_MAINTENANCE": "模具夹具制作维修",
                "PRE_ASSEMBLY": "预装工序",
                "MAIN_ASSEMBLY": "主装配工序"
            },
            "silkscreen_processes": {
                "PRINT_PREP": "丝印前处理",
                "SCREEN_PRINT": "丝印工序",
                "POST_CURE": "后固化工序"
            }
        }
        
    def create_detailed_flowchart(self, source_file, output_file):
        """创建细化的小家电制造流程图"""
        print("🏭 开始生成小家电制造业详细生产流程图...")
        print(f"📁 源文件: {source_file}")
        print(f"📁 输出文件: {output_file}")
        print(f"⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        try:
            # 解析源文件
            tree = ET.parse(source_file)
            root = tree.getroot()
            graph_model = root.find(".//mxGraphModel")
            
            if graph_model is None:
                raise ValueError("未找到mxGraphModel元素")
            
            # 扩展画布尺寸以容纳详细流程
            graph_model.set('pageWidth', '8000')  # 扩展宽度
            graph_model.set('pageHeight', '6000')  # 扩展高度
            
            # 更新标题
            self.update_title(graph_model)
            
            # 扩展泳道结构
            self.expand_swimlanes(graph_model)
            
            # 细化生产工序
            self.detail_production_processes(graph_model)
            
            # 添加质量控制交互
            self.add_quality_interactions(graph_model)
            
            # 优化连接线
            self.optimize_connections(graph_model)
            
            # 保存文件
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            print(f"\n🎉 详细流程图生成完成！")
            print(f"📁 保存位置: {output_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ 生成过程中发生错误: {str(e)}")
            return False
    
    def update_title(self, graph_model):
        """更新标题"""
        root_element = graph_model.find('root')
        title_element = root_element.find(".//mxCell[@id='title']")
        
        if title_element is not None:
            title_element.set('value', '小家电制造业综合订单全流程ERP系统详细业务流程图\\n生产工序细化版 - 含品质部五大岗位交互')
    
    def expand_swimlanes(self, graph_model):
        """扩展泳道结构，添加细分岗位"""
        root_element = graph_model.find('root')
        
        # 扩展品质部泳道高度，添加子岗位
        self.expand_quality_department(root_element)
        
        # 扩展五金部泳道，添加具体工序
        self.expand_hardware_department(root_element)
        
        # 扩展装配线泳道，添加具体岗位
        self.expand_assembly_department(root_element)
        
        # 扩展丝印部泳道
        self.expand_silkscreen_department(root_element)
    
    def expand_quality_department(self, root_element):
        """扩展品质部，添加IQC、IPQC、实验室、QA、QE岗位"""
        # 调整品质部泳道高度和位置
        quality_lane = root_element.find(".//mxCell[@id='lane_quality']")
        if quality_lane is not None:
            geometry = quality_lane.find('mxGeometry')
            if geometry is not None:
                geometry.set('height', '250')  # 增加高度容纳子岗位
                
        # 添加IQC岗位泳道
        self.add_quality_sublane(root_element, 'lane_quality_iqc', 'IQC来料检验', 1470, 50, '#FFF5E6')
        
        # 添加IPQC岗位泳道
        self.add_quality_sublane(root_element, 'lane_quality_ipqc', 'IPQC制程检验', 1520, 50, '#FFF0E6')
        
        # 添加实验室泳道
        self.add_quality_sublane(root_element, 'lane_quality_lab', '实验室测试', 1570, 50, '#FFE8E6')
        
        # 添加QA泳道
        self.add_quality_sublane(root_element, 'lane_quality_qa', 'QA质量保证', 1620, 50, '#FFE0E6')
        
        # 添加QE泳道
        self.add_quality_sublane(root_element, 'lane_quality_qe', 'QE质量工程', 1670, 50, '#FFD8E6')
    
    def add_quality_sublane(self, root_element, lane_id, lane_name, y_pos, height, color):
        """添加品质部子岗位泳道"""
        lane = ET.SubElement(root_element, 'mxCell')
        lane.set('id', lane_id)
        lane.set('value', lane_name)
        lane.set('style', f'swimlane;html=1;startSize=20;horizontal=0;fillColor={color};strokeColor=#4A90E2;strokeWidth=1;strokeDashArray=10,3;fontSize=12;fontStyle=1;')
        lane.set('parent', '1')
        lane.set('vertex', '1')
        
        geometry = ET.SubElement(lane, 'mxGeometry')
        geometry.set('x', '120')
        geometry.set('y', str(y_pos))
        geometry.set('width', '5680')
        geometry.set('height', str(height))
        geometry.set('as', 'geometry')
    
    def expand_hardware_department(self, root_element):
        """扩展五金部，添加成型、焊接、抛光、清洗、模房工序"""
        # 调整五金部泳道高度
        hardware_lane = root_element.find(".//mxCell[@id='lane_hardware']")
        if hardware_lane is not None:
            geometry = hardware_lane.find('mxGeometry')
            if geometry is not None:
                geometry.set('height', '300')  # 增加高度
                
        # 添加成型工序泳道
        self.add_hardware_sublane(root_element, 'lane_hardware_molding', '成型工序', 1170, 50, '#FFE2E1')
        
        # 添加焊接工序泳道
        self.add_hardware_sublane(root_element, 'lane_hardware_welding', '焊接工序', 1220, 50, '#FFE0E1')
        
        # 添加抛光工序泳道
        self.add_hardware_sublane(root_element, 'lane_hardware_polishing', '抛光工序', 1270, 50, '#FFDEE1')
        
        # 添加清洗工序泳道
        self.add_hardware_sublane(root_element, 'lane_hardware_cleaning', '清洗工序', 1320, 50, '#FFDCE1')
        
        # 添加模房工序泳道
        self.add_hardware_sublane(root_element, 'lane_hardware_mold', '模房工序', 1370, 50, '#FFDAE1')
    
    def add_hardware_sublane(self, root_element, lane_id, lane_name, y_pos, height, color):
        """添加五金部子工序泳道"""
        lane = ET.SubElement(root_element, 'mxCell')
        lane.set('id', lane_id)
        lane.set('value', lane_name)
        lane.set('style', f'swimlane;html=1;startSize=20;horizontal=0;fillColor={color};strokeColor=#4A90E2;strokeWidth=1;strokeDashArray=10,3;fontSize=12;fontStyle=1;')
        lane.set('parent', '1')
        lane.set('vertex', '1')
        
        geometry = ET.SubElement(lane, 'mxGeometry')
        geometry.set('x', '120')
        geometry.set('y', str(y_pos))
        geometry.set('width', '5680')
        geometry.set('height', str(height))
        geometry.set('as', 'geometry')
    
    def expand_assembly_department(self, root_element):
        """扩展装配线，添加物料控制、模具夹具制作维修等岗位"""
        # 调整装配线泳道高度
        assembly_lane = root_element.find(".//mxCell[@id='lane_assembly']")
        if assembly_lane is not None:
            geometry = assembly_lane.find('mxGeometry')
            if geometry is not None:
                geometry.set('height', '200')  # 增加高度
                
        # 添加物料控制泳道
        self.add_assembly_sublane(root_element, 'lane_assembly_material', '物料控制', 1070, 50, '#FFE2E1')
        
        # 添加模具夹具制作维修泳道
        self.add_assembly_sublane(root_element, 'lane_assembly_mold', '模具夹具制作维修', 1120, 50, '#FFE0E1')
        
        # 添加预装工序泳道
        self.add_assembly_sublane(root_element, 'lane_assembly_pre', '预装工序', 1170, 50, '#FFDEE1')
    
    def add_assembly_sublane(self, root_element, lane_id, lane_name, y_pos, height, color):
        """添加装配线子岗位泳道"""
        lane = ET.SubElement(root_element, 'mxCell')
        lane.set('id', lane_id)
        lane.set('value', lane_name)
        lane.set('style', f'swimlane;html=1;startSize=20;horizontal=0;fillColor={color};strokeColor=#4A90E2;strokeWidth=1;strokeDashArray=10,3;fontSize=12;fontStyle=1;')
        lane.set('parent', '1')
        lane.set('vertex', '1')
        
        geometry = ET.SubElement(lane, 'mxGeometry')
        geometry.set('x', '120')
        geometry.set('y', str(y_pos))
        geometry.set('width', '5680')
        geometry.set('height', str(height))
        geometry.set('as', 'geometry')
    
    def expand_silkscreen_department(self, root_element):
        """扩展丝印部，添加具体工序"""
        # 调整丝印部泳道高度
        silkscreen_lane = root_element.find(".//mxCell[@id='lane_silkscreen']")
        if silkscreen_lane is not None:
            geometry = silkscreen_lane.find('mxGeometry')
            if geometry is not None:
                geometry.set('height', '150')  # 增加高度
                
        # 添加丝印前处理泳道
        self.add_silkscreen_sublane(root_element, 'lane_silkscreen_prep', '丝印前处理', 1370, 50, '#FFE2E1')
        
        # 添加丝印后处理泳道
        self.add_silkscreen_sublane(root_element, 'lane_silkscreen_post', '丝印后固化', 1420, 50, '#FFE0E1')
    
    def add_silkscreen_sublane(self, root_element, lane_id, lane_name, y_pos, height, color):
        """添加丝印部子工序泳道"""
        lane = ET.SubElement(root_element, 'mxCell')
        lane.set('id', lane_id)
        lane.set('value', lane_name)
        lane.set('style', f'swimlane;html=1;startSize=20;horizontal=0;fillColor={color};strokeColor=#4A90E2;strokeWidth=1;strokeDashArray=10,3;fontSize=12;fontStyle=1;')
        lane.set('parent', '1')
        lane.set('vertex', '1')
        
        geometry = ET.SubElement(lane, 'mxGeometry')
        geometry.set('x', '120')
        geometry.set('y', str(y_pos))
        geometry.set('width', '5680')
        geometry.set('height', str(height))
        geometry.set('as', 'geometry')
    
    def detail_production_processes(self, graph_model):
        """细化生产工序流程"""
        root_element = graph_model.find('root')
        
        # 细化五金生产流程
        self.detail_hardware_processes(root_element)
        
        # 细化注塑生产流程
        self.detail_injection_processes(root_element)
        
        # 细化丝印生产流程
        self.detail_silkscreen_processes(root_element)
        
        # 细化装配流程
        self.detail_assembly_processes(root_element)
        
        # 添加复杂的工序路径关系
        self.add_complex_process_flows(root_element)
    
    def detail_hardware_processes(self, root_element):
        """细化五金生产工序"""
        # 成型工序
        self.add_process_step(root_element, 'H01', '成型前准备\\n模具检查设定', 3900, 1185, 'lane_hardware_molding', '#FFE2E1')
        self.add_process_step(root_element, 'H02', '冲压成型\\n零件冲压加工', 4050, 1185, 'lane_hardware_molding', '#FFE2E1')
        
        # 焊接工序
        self.add_process_step(root_element, 'H03', '焊接前处理\\n清洁表面准备', 4200, 1235, 'lane_hardware_welding', '#FFE0E1')
        self.add_process_step(root_element, 'H04', '焊接作业\\n部件焊接组装', 4350, 1235, 'lane_hardware_welding', '#FFE0E1')
        
        # 抛光工序
        self.add_process_step(root_element, 'H05', '粗抛光\\n表面粗加工', 4500, 1285, 'lane_hardware_polishing', '#FFDEE1')
        self.add_process_step(root_element, 'H06', '精抛光\\n表面精加工', 4650, 1285, 'lane_hardware_polishing', '#FFDEE1')
        
        # 清洗工序
        self.add_process_step(root_element, 'H07', '脱脂清洗\\n去除油污杂质', 4800, 1335, 'lane_hardware_cleaning', '#FFDCE1')
        self.add_process_step(root_element, 'H08', '精密清洗\\n最终清洁处理', 4950, 1335, 'lane_hardware_cleaning', '#FFDCE1')
    
    def detail_injection_processes(self, root_element):
        """细化注塑生产工序"""
        # 注塑准备
        self.add_process_step(root_element, 'I01', '注塑前准备\\n模具预热设定', 4000, 1265, 'lane_injection', '#FFE4E1')
        
        # 注塑成型
        self.add_process_step(root_element, 'I02', '注塑成型\\n塑料件成型', 4200, 1265, 'lane_injection', '#FFE4E1')
        
        # 注塑后处理
        self.add_process_step(root_element, 'I03', '去毛刺处理\\n塑件修整', 4400, 1265, 'lane_injection', '#FFE4E1')
    
    def detail_silkscreen_processes(self, root_element):
        """细化丝印生产工序"""
        # 丝印前处理
        self.add_process_step(root_element, 'S01_SILK', '丝印前处理\\n表面清洁活化', 4100, 1385, 'lane_silkscreen_prep', '#FFE2E1')
        
        # 丝印工序
        self.add_process_step(root_element, 'S02_SILK', '丝印印刷\\n图案印制', 4300, 1365, 'lane_silkscreen', '#FFE4E1')
        
        # 丝印后固化
        self.add_process_step(root_element, 'S03_SILK', '固化干燥\\n丝印固化', 4500, 1435, 'lane_silkscreen_post', '#FFE0E1')
    
    def detail_assembly_processes(self, root_element):
        """细化装配流程"""
        # 物料控制
        self.add_process_step(root_element, 'A01', '物料配套\\n零件配套检查', 3800, 1085, 'lane_assembly_material', '#FFE2E1')
        
        # 模具夹具准备
        self.add_process_step(root_element, 'A02', '夹具准备\\n装配工装准备', 3900, 1135, 'lane_assembly_mold', '#FFE0E1')
        
        # 预装工序
        self.add_process_step(root_element, 'A03', '部分预装\\n子组件预装', 4000, 1185, 'lane_assembly_pre', '#FFDEE1')
        
        # 主装配
        self.add_process_step(root_element, 'A04', '主装配\\n最终产品装配', 4200, 1065, 'lane_assembly', '#FFE4E1')
    
    def add_process_step(self, root_element, step_id, step_content, x_pos, y_pos, parent_lane, color):
        """添加生产工序步骤"""
        step = ET.SubElement(root_element, 'mxCell')
        step.set('id', step_id)
        step.set('value', step_content)
        step.set('style', f'rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=9;')
        step.set('parent', '1')
        step.set('vertex', '1')
        
        geometry = ET.SubElement(step, 'mxGeometry')
        geometry.set('x', str(x_pos))
        geometry.set('y', str(y_pos))
        geometry.set('width', '120')
        geometry.set('height', '50')
        geometry.set('as', 'geometry')
    
    def add_quality_interactions(self, root_element):
        """添加品质部各岗位与生产工序的交互"""
        # IQC与物料入库的交互
        self.add_quality_step(root_element, 'Q01_IQC', 'IQC来料检验\\n原材料质量检查', 2950, 1485, 'lane_quality_iqc')
        
        # IPQC与各生产工序的交互
        self.add_quality_step(root_element, 'Q02_IPQC1', 'IPQC五金检验\\n五金件制程检验', 4100, 1535, 'lane_quality_ipqc')
        self.add_quality_step(root_element, 'Q03_IPQC2', 'IPQC注塑检验\\n注塑件制程检验', 4250, 1535, 'lane_quality_ipqc')
        self.add_quality_step(root_element, 'Q04_IPQC3', 'IPQC丝印检验\\n丝印质量检验', 4400, 1535, 'lane_quality_ipqc')
        self.add_quality_step(root_element, 'Q05_IPQC4', 'IPQC装配检验\\n装配质量检验', 4550, 1535, 'lane_quality_ipqc')
        
        # 实验室测试
        self.add_quality_step(root_element, 'Q06_LAB', '实验室检测\\n材料性能测试', 3400, 1585, 'lane_quality_lab')
        
        # QA质量保证
        self.add_quality_step(root_element, 'Q07_QA', 'QA质量审核\\n质量体系保证', 4700, 1635, 'lane_quality_qa')
        
        # QE质量工程
        self.add_quality_step(root_element, 'Q08_QE', 'QE质量改善\\n质量工程分析', 3600, 1685, 'lane_quality_qe')
    
    def add_quality_step(self, root_element, step_id, step_content, x_pos, y_pos, parent_lane):
        """添加品质部工序步骤"""
        step = ET.SubElement(root_element, 'mxCell')
        step.set('id', step_id)
        step.set('value', step_content)
        step.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF0E6;strokeColor=#FF6600;strokeWidth=2;fontSize=9;')
        step.set('parent', '1')
        step.set('vertex', '1')
        
        geometry = ET.SubElement(step, 'mxGeometry')
        geometry.set('x', str(x_pos))
        geometry.set('y', str(y_pos))
        geometry.set('width', '120')
        geometry.set('height', '50')
        geometry.set('as', 'geometry')
    
    def add_complex_process_flows(self, root_element):
        """添加复杂的工序流程关系"""
        # 五金→丝印→装配的路径
        self.add_process_connection(root_element, 'conn_h_to_silk', 'H08', 'S01_SILK', '五金完成→丝印', '#FF6B35')
        
        # 注塑→丝印→装配的路径
        self.add_process_connection(root_element, 'conn_i_to_silk', 'I03', 'S01_SILK', '注塑完成→丝印', '#FF6B35')
        
        # 丝印→装配的路径
        self.add_process_connection(root_element, 'conn_silk_to_asm', 'S03_SILK', 'A04', '丝印完成→装配', '#FF6B35')
        
        # 预装配与主装配的并行关系
        self.add_process_connection(root_element, 'conn_pre_to_main', 'A03', 'A04', '预装→主装配', '#FF6B35')
        
        # 品质检验的交互连接
        self.add_quality_connection(root_element, 'conn_iqc', 'S13', 'Q01_IQC', 'IQC检验', '#FF6600')
        self.add_quality_connection(root_element, 'conn_ipqc1', 'H02', 'Q02_IPQC1', 'IPQC检验', '#FF6600')
        self.add_quality_connection(root_element, 'conn_ipqc2', 'I02', 'Q03_IPQC2', 'IPQC检验', '#FF6600')
        self.add_quality_connection(root_element, 'conn_ipqc3', 'S02_SILK', 'Q04_IPQC3', 'IPQC检验', '#FF6600')
        self.add_quality_connection(root_element, 'conn_ipqc4', 'A04', 'Q05_IPQC4', 'IPQC检验', '#FF6600')
    
    def add_process_connection(self, root_element, conn_id, source_id, target_id, label, color):
        """添加工序连接线"""
        connection = ET.SubElement(root_element, 'mxCell')
        connection.set('id', conn_id)
        connection.set('value', label)
        connection.set('style', f'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={color};strokeWidth=2;')
        connection.set('source', source_id)
        connection.set('target', target_id)
        connection.set('edge', '1')
        connection.set('parent', '1')
        
        geometry = ET.SubElement(connection, 'mxGeometry')
        geometry.set('relative', '1')
        geometry.set('as', 'geometry')
    
    def add_quality_connection(self, root_element, conn_id, source_id, target_id, label, color):
        """添加品质检验连接线"""
        connection = ET.SubElement(root_element, 'mxCell')
        connection.set('id', conn_id)
        connection.set('value', label)
        connection.set('style', f'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={color};strokeWidth=1;strokeDashArray=3,3;')
        connection.set('source', source_id)
        connection.set('target', target_id)
        connection.set('edge', '1')
        connection.set('parent', '1')
        
        geometry = ET.SubElement(connection, 'mxGeometry')
        geometry.set('relative', '1')
        geometry.set('as', 'geometry')
    
    def optimize_connections(self, graph_model):
        """优化连接线，避免重合"""
        # 这里可以添加连接线优化逻辑
        pass

def main():
    """主函数"""
    source_file = "s:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-重新生成版.drawio"
    output_file = "s:\\PG-GMO\\office\\业务部\\小家电制造业详细生产流程图.drawio"
    
    detailer = SmallApplianceFlowchartDetailer()
    
    try:
        success = detailer.create_detailed_flowchart(source_file, output_file)
        
        if success:
            print(f"\n🎉 小家电制造业详细流程图生成成功！")
            print(f"📁 输出文件: {output_file}")
        else:
            print(f"\n⚠️ 生成过程中遇到问题。")
        
        return success
        
    except Exception as e:
        print(f"❌ 生成过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()