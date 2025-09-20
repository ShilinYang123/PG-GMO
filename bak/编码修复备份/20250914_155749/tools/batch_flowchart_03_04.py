#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成HQ-QP-03和HQ-QP-04流程图
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from pathlib import Path

class BatchFlowchartGenerator:
    def __init__(self):
        self.colors = {
            '管理层': '#FF6B6B',
            '品质部': '#4ECDC4', 
            '各部门': '#E8E8E8',
            '内审员': '#FFEAA7',
            '被审核部门': '#DDA0DD',
            '人力资源部': '#98D8C8',
            '用人部门': '#96CEB4',
            '候选人': '#F7DC6F',
            '行政部': '#85C1E9'
        }
    
    def create_hq_qp_03_flowchart(self):
        """生成HQ-QP-03内部审核控制程序流程图"""
        
        # HQ-QP-03专门的内部审核流程步骤
        steps = [
            {'text': '制定年度内审计划', 'type': 'start', 'dept': '品质部'},
            {'text': '确定审核范围目标', 'type': 'process', 'dept': '品质部'},
            {'text': '组建内审小组', 'type': 'process', 'dept': '品质部'},
            {'text': '制定审核实施方案', 'type': 'process', 'dept': '内审员'},
            {'text': '编制审核检查表', 'type': 'process', 'dept': '内审员'},
            {'text': '发出审核通知书', 'type': 'process', 'dept': '品质部'},
            {'text': '召开首次会议', 'type': 'process', 'dept': '内审员'},
            {'text': '实施现场审核', 'type': 'process', 'dept': '内审员'},
            {'text': '收集审核证据', 'type': 'process', 'dept': '内审员'},
            {'text': '是否发现不符合项？', 'type': 'decision', 'dept': '内审员'},
            {'text': '开具不符合项报告', 'type': 'process', 'dept': '内审员'},
            {'text': '召开末次会议', 'type': 'process', 'dept': '内审员'},
            {'text': '编制内审报告', 'type': 'process', 'dept': '内审员'},
            {'text': '要求整改措施', 'type': 'process', 'dept': '被审核部门'},
            {'text': '验证整改效果', 'type': 'process', 'dept': '内审员'},
            {'text': '关闭不符合项', 'type': 'process', 'dept': '品质部'},
            {'text': '审核资料归档', 'type': 'process', 'dept': '品质部'},
            {'text': '内审流程结束', 'type': 'end', 'dept': '品质部'}
        ]
        
        return self.generate_drawio_xml("HQ-QP-03 内部审核控制程序", steps)
    
    def create_hq_qp_04_flowchart(self):
        """生成HQ-QP-04人力资源控制程序流程图"""
        
        # HQ-QP-04专门的人力资源流程步骤
        steps = [
            {'text': '确定人员需求', 'type': 'start', 'dept': '用人部门'},
            {'text': '制定招聘计划', 'type': 'process', 'dept': '人力资源部'},
            {'text': '发布招聘信息', 'type': 'process', 'dept': '人力资源部'},
            {'text': '收集简历筛选', 'type': 'process', 'dept': '人力资源部'},
            {'text': '初步面试评估', 'type': 'process', 'dept': '人力资源部'},
            {'text': '专业技能测试', 'type': 'process', 'dept': '用人部门'},
            {'text': '候选人是否合格？', 'type': 'decision', 'dept': '用人部门'},
            {'text': '背景调查验证', 'type': 'process', 'dept': '人力资源部'},
            {'text': '录用决定确认', 'type': 'process', 'dept': '管理层'},
            {'text': '签署劳动合同', 'type': 'process', 'dept': '人力资源部'},
            {'text': '安排入职培训', 'type': 'process', 'dept': '人力资源部'},
            {'text': '岗位技能培训', 'type': 'process', 'dept': '用人部门'},
            {'text': '试用期考核', 'type': 'process', 'dept': '用人部门'},
            {'text': '能力持续评估', 'type': 'process', 'dept': '用人部门'},
            {'text': '职业发展规划', 'type': 'process', 'dept': '人力资源部'},
            {'text': '绩效管理跟踪', 'type': 'process', 'dept': '人力资源部'},
            {'text': '人事档案管理', 'type': 'process', 'dept': '人力资源部'},
            {'text': '人力资源流程结束', 'type': 'end', 'dept': '人力资源部'}
        ]
        
        return self.generate_drawio_xml("HQ-QP-04 人力资源控制程序", steps)
    
    def generate_drawio_xml(self, title, steps):
        """生成Draw.io XML格式的流程图"""
        # 创建XML结构
        mxfile = ET.Element('mxfile', host="app.diagrams.net", 
                          modified=datetime.now().isoformat(), 
                          agent="5.0", version="24.7.17")
        
        diagram = ET.SubElement(mxfile, 'diagram', name=f"{title}流程图", id="flowchart")
        
        model = ET.SubElement(diagram, 'mxGraphModel', 
                            dx="1422", dy="794", grid="1", gridSize="10",
                            guides="1", tooltips="1", connect="1", arrows="1",
                            fold="1", page="1", pageScale="1", pageWidth="827", 
                            pageHeight="1169", math="0", shadow="0")
        
        root = ET.SubElement(model, 'root')
        ET.SubElement(root, 'mxCell', id="0")
        ET.SubElement(root, 'mxCell', id="1", parent="0")
        
        # 添加标题
        title_cell = ET.SubElement(root, 'mxCell', id="title", 
                                 value=f"{title}流程图",
                                 style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;",
                                 vertex="1", parent="1")
        ET.SubElement(title_cell, 'mxGeometry', x="250", y="20", width="350", height="30", **{"as": "geometry"})
        
        # 生成流程步骤
        start_x, start_y = 100, 80
        step_height = 70
        cell_id = 2
        
        for i, step in enumerate(steps):
            y_pos = start_y + i * step_height
            
            # 确定形状和颜色
            color = self.colors.get(step['dept'], '#E8E8E8')
            
            if step['type'] == 'start' or step['type'] == 'end':
                style = f"ellipse;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=11;fontStyle=1;"
                width, height = "140", "50"
            elif step['type'] == 'decision':
                style = f"rhombus;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=11;"
                width, height = "160", "70"
            else:
                style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=11;"
                width, height = "180", "50"
            
            # 添加步骤单元格
            step_text = f"{step['text']}\\n[{step['dept']}]"
            step_cell = ET.SubElement(root, 'mxCell', id=str(cell_id), value=step_text, 
                                    style=style, vertex="1", parent="1")
            ET.SubElement(step_cell, 'mxGeometry', x=str(start_x), y=str(y_pos), 
                        width=width, height=height, **{"as": "geometry"})
            
            # 添加连接线（除了最后一个步骤）
            if i < len(steps) - 1:
                edge_id = cell_id + 100
                edge_style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
                edge_cell = ET.SubElement(root, 'mxCell', id=str(edge_id), value="", 
                                        style=edge_style, edge="1", parent="1", 
                                        source=str(cell_id), target=str(cell_id + 1))
                ET.SubElement(edge_cell, 'mxGeometry', relative="1", **{"as": "geometry"})
            
            cell_id += 1
        
        # 添加决策分支
        decision_nodes = [(i, step) for i, step in enumerate(steps) if step['type'] == 'decision']
        if decision_nodes:
            decision_index, decision_step = decision_nodes[0]
            decision_node_id = str(decision_index + 2)
            
            # 根据不同的流程设置回退目标
            if "内部审核" in title:
                return_target_id = str(decision_index - 1)  # 回到收集审核证据
                no_label = "无不符合项"
                yes_label = "有不符合项"
            else:  # 人力资源
                return_target_id = str(max(2, decision_index - 2))  # 回到初步面试评估
                no_label = "不合格"
                yes_label = "合格"
            
            no_edge_cell = ET.SubElement(root, 'mxCell', id="200", value=no_label,
                                        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
                                        edge="1", parent="1", source=decision_node_id, target=return_target_id)
            ET.SubElement(no_edge_cell, 'mxGeometry', relative="1", **{"as": "geometry"})
            
            # 给"是"分支添加标签
            yes_edge_id = str(decision_index + 2 + 100)
            for edge in root.findall(f".//mxCell[@id='{yes_edge_id}'][@edge='1']"):
                edge.set('value', yes_label)
        
        return mxfile
    
    def save_flowchart(self, xml_element, filename):
        """保存流程图到文件"""
        rough_string = ET.tostring(xml_element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        formatted_xml = '\n'.join(lines)
        
        output_path = Path("S:/PG-GMO/02-Output/品高ISO流程图") / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_xml)
        
        return output_path
    
    def generate_batch(self):
        """批量生成HQ-QP-03和HQ-QP-04流程图"""
        generated_files = []
        
        print("批量生成HQ-QP-03和HQ-QP-04流程图...")
        
        # 生成HQ-QP-03
        print("[1/2] 正在生成HQ-QP-03内部审核控制程序流程图...")
        xml_03 = self.create_hq_qp_03_flowchart()
        path_03 = self.save_flowchart(xml_03, "HQ-QP-03 内部审核控制程序.drawio")
        generated_files.append(str(path_03))
        print(f"✅ HQ-QP-03流程图已生成: {path_03.name}")
        
        # 生成HQ-QP-04
        print("[2/2] 正在生成HQ-QP-04人力资源控制程序流程图...")
        xml_04 = self.create_hq_qp_04_flowchart()
        path_04 = self.save_flowchart(xml_04, "HQ-QP-04 人力资源控制程序.drawio")
        generated_files.append(str(path_04))
        print(f"✅ HQ-QP-04流程图已生成: {path_04.name}")
        
        return generated_files

def main():
    generator = BatchFlowchartGenerator()
    generated_files = generator.generate_batch()
    
    print(f"\n=== 批量生成完成 ===")
    print(f"✅ 成功生成: {len(generated_files)} 个流程图")
    print("\n📁 生成的流程图文件:")
    for i, file_path in enumerate(generated_files, 1):
        filename = Path(file_path).name
        print(f"{i}. {filename}")
    
    return generated_files

if __name__ == "__main__":
    main()