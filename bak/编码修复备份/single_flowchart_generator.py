#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单个流程图生成器
为指定的ISO文档生成流程图供检查
"""

import os
import json
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

class SingleFlowchartGenerator:
    def __init__(self):
        # 部门颜色配置
        self.department_colors = {
            '管理层': '#FF6B6B',
            '品质部': '#4ECDC4',
            '生产部': '#45B7D1',
            '研发部': '#96CEB4',
            '采购部': '#FFEAA7',
            '业务部': '#DDA0DD',
            '人力资源部': '#98D8C8',
            '财务部': '#F7DC6F',
            '仓储部': '#BB8FCE',
            '行政部': '#85C1E9',
            '工程部': '#82E0AA'
        }
        
    def create_drawio_flowchart(self, title, steps, output_path):
        """创建draw.io格式的流程图"""
        
        # 创建根元素
        mxfile = ET.Element('mxfile', host="app.diagrams.net", modified=datetime.now().isoformat())
        diagram = ET.SubElement(mxfile, 'diagram', id="flowchart", name=title)
        mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1422", dy="794", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="827", pageHeight="1169", math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, 'root')
        
        # 添加默认层
        ET.SubElement(root, 'mxCell', id="0")
        ET.SubElement(root, 'mxCell', id="1", parent="0")
        
        # 计算布局参数
        start_x = 100
        start_y = 100
        step_height = 80
        box_width = 200
        box_height = 60
        
        cell_id = 2
        
        # 创建标题
        title_cell = ET.SubElement(root, 'mxCell', 
                                 id=str(cell_id),
                                 value=title,
                                 style="rounded=1;whiteSpace=wrap;html=1;fontSize=16;fontStyle=1;fillColor=#e1d5e7;strokeColor=#9673a6;",
                                 vertex="1",
                                 parent="1")
        ET.SubElement(title_cell, 'mxGeometry', 
                     x=str(start_x), y="20", 
                     width=str(box_width + 100), height="40", 
                     **{"as": "geometry"})
        cell_id += 1
        
        # 创建流程步骤
        for i, step in enumerate(steps):
            y_pos = start_y + i * step_height
            
            # 确定步骤类型和颜色
            if i == 0:
                # 开始节点
                style = "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
            elif i == len(steps) - 1:
                # 结束节点
                style = "ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
            elif "审核" in step or "检查" in step or "验证" in step:
                # 决策节点
                style = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
            else:
                # 普通处理节点
                style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
            
            # 创建步骤节点
            step_cell = ET.SubElement(root, 'mxCell',
                                    id=str(cell_id),
                                    value=step,
                                    style=style,
                                    vertex="1",
                                    parent="1")
            ET.SubElement(step_cell, 'mxGeometry',
                         x=str(start_x), y=str(y_pos),
                         width=str(box_width), height=str(box_height),
                         **{"as": "geometry"})
            
            # 创建连接线（除了最后一个节点）
            if i < len(steps) - 1:
                arrow_cell = ET.SubElement(root, 'mxCell',
                                         id=str(cell_id + 1),
                                         value="",
                                         style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;",
                                         edge="1",
                                         parent="1",
                                         source=str(cell_id),
                                         target=str(cell_id + 2))
                ET.SubElement(arrow_cell, 'mxGeometry', relative="1", **{"as": "geometry"})
                cell_id += 1
            
            cell_id += 1
        
        # 保存文件
        tree = ET.ElementTree(mxfile)
        
        # 格式化XML
        rough_string = ET.tostring(mxfile, 'unicode')
        reparsed = minidom.parseString(rough_string)
        formatted_xml = reparsed.toprettyxml(indent="  ")
        
        # 移除空行
        formatted_xml = '\n'.join([line for line in formatted_xml.split('\n') if line.strip()])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_xml)
        
        return True
    
    def generate_sample_flowchart(self, doc_name="HQ-QP-01 形成文件的信息控制程序"):
        """生成示例流程图"""
        
        # 定义示例流程步骤
        sample_steps = [
            "开始：文件控制需求",
            "识别文件类型和控制要求",
            "制定文件编制计划",
            "文件起草和编写",
            "内部审核和技术审查",
            "是否通过审查？",
            "管理层批准",
            "文件发布和分发",
            "文件使用和维护",
            "定期评审和更新",
            "结束：文件控制完成"
        ]
        
        # 输出路径
        output_dir = Path("S:/PG-GMO/02-Output/品高ISO流程图")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{doc_name}.drawio"
        
        # 生成流程图
        success = self.create_drawio_flowchart(
            title=doc_name,
            steps=sample_steps,
            output_path=output_file
        )
        
        if success:
            print(f"✅ 示例流程图生成成功: {output_file}")
            print(f"📁 文件位置: {output_file.absolute()}")
            print(f"🎯 流程图标题: {doc_name}")
            print(f"📊 包含步骤数: {len(sample_steps)}")
            return str(output_file)
        else:
            print(f"❌ 流程图生成失败")
            return None

def main():
    print("=== 单个流程图生成器 ===")
    
    generator = SingleFlowchartGenerator()
    
    # 生成示例流程图
    result = generator.generate_sample_flowchart()
    
    if result:
        print(f"\n🎉 流程图生成完成！")
        print(f"📂 可以使用draw.io或diagrams.net打开查看")
        print(f"🔗 在线查看: https://app.diagrams.net/")
    else:
        print(f"\n❌ 流程图生成失败")

if __name__ == "__main__":
    main()