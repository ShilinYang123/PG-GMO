#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的批量ISO流程图生成器
基于ISO文档名称和业务逻辑，生成精准的流程图
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

class ImprovedBatchFlowchartGenerator:
    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
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
            '工程部': '#82E0AA',
            '各部门': '#E8E8E8',
            '相关部门': '#E8E8E8'
        }
        
    def get_process_steps_by_document(self, doc_code):
        """根据文档编号获取具体的流程步骤"""
        
        # 简化版本，包含主要的ISO文档流程
        iso_processes = {
            'HQ-QP-01': [  # 形成文件的信息控制程序
                {'text': '文件制定需求', 'type': 'start', 'dept': '各部门'},
                {'text': '文件起草编制', 'type': 'process', 'dept': '起草部门'},
                {'text': '内容审查校对', 'type': 'process', 'dept': '品质部'},
                {'text': '部门领导审核', 'type': 'process', 'dept': '管理层'},
                {'text': '文件是否符合要求？', 'type': 'decision', 'dept': '品质部'},
                {'text': '管理层批准', 'type': 'process', 'dept': '管理层'},
                {'text': '文件发布实施', 'type': 'process', 'dept': '品质部'},
                {'text': '文件分发控制', 'type': 'process', 'dept': '行政部'},
                {'text': '执行监督检查', 'type': 'process', 'dept': '品质部'},
                {'text': '文件归档管理', 'type': 'process', 'dept': '行政部'},
                {'text': '流程结束', 'type': 'end', 'dept': '各部门'}
            ],
            'HQ-QP-02': [  # 管理评审控制程序
                {'text': '管理评审计划', 'type': 'start', 'dept': '管理层'},
                {'text': '评审输入准备', 'type': 'process', 'dept': '品质部'},
                {'text': '收集相关数据', 'type': 'process', 'dept': '各部门'},
                {'text': '编制评审报告', 'type': 'process', 'dept': '品质部'},
                {'text': '数据是否完整？', 'type': 'decision', 'dept': '品质部'},
                {'text': '召开评审会议', 'type': 'process', 'dept': '管理层'},
                {'text': '评审结果分析', 'type': 'process', 'dept': '管理层'},
                {'text': '制定改进措施', 'type': 'process', 'dept': '管理层'},
                {'text': '跟踪措施执行', 'type': 'process', 'dept': '品质部'},
                {'text': '评审记录归档', 'type': 'process', 'dept': '行政部'},
                {'text': '流程结束', 'type': 'end', 'dept': '管理层'}
            ],
            'HQ-QP-28': [  # 采购管理控制程序
                {'text': '采购需求确定', 'type': 'start', 'dept': '各部门'},
                {'text': '采购计划制定', 'type': 'process', 'dept': '采购部'},
                {'text': '供应商评估选择', 'type': 'process', 'dept': '采购部'},
                {'text': '采购合同谈判', 'type': 'process', 'dept': '采购部'},
                {'text': '供应商是否合格？', 'type': 'decision', 'dept': '品质部'},
                {'text': '采购订单下达', 'type': 'process', 'dept': '采购部'},
                {'text': '采购执行跟踪', 'type': 'process', 'dept': '采购部'},
                {'text': '到货验收检查', 'type': 'process', 'dept': '品质部'},
                {'text': '供应商绩效评价', 'type': 'process', 'dept': '采购部'},
                {'text': '采购记录归档', 'type': 'process', 'dept': '采购部'},
                {'text': '流程结束', 'type': 'end', 'dept': '采购部'}
            ]
        }
        
        # 如果有具体定义，返回具体流程
        if doc_code in iso_processes:
            return iso_processes[doc_code]
        
        # 否则基于文档名称生成通用流程
        return self.generate_generic_process_by_name(doc_code)
    
    def generate_generic_process_by_name(self, doc_code):
        """基于文档名称生成通用流程"""
        base_steps = [
            {'text': '流程启动', 'type': 'start', 'dept': '相关部门'},
            {'text': '需求确认', 'type': 'process', 'dept': '申请部门'},
            {'text': '方案制定', 'type': 'process', 'dept': '执行部门'},
            {'text': '初步审核', 'type': 'process', 'dept': '品质部'},
            {'text': '是否符合要求？', 'type': 'decision', 'dept': '品质部'},
            {'text': '审批确认', 'type': 'process', 'dept': '管理层'},
            {'text': '执行实施', 'type': 'process', 'dept': '执行部门'},
            {'text': '过程监控', 'type': 'process', 'dept': '品质部'},
            {'text': '效果评估', 'type': 'process', 'dept': '品质部'},
            {'text': '记录归档', 'type': 'process', 'dept': '相关部门'},
            {'text': '流程结束', 'type': 'end', 'dept': '相关部门'}
        ]
        
        # 根据文档类型调整
        if '采购' in doc_code:
            base_steps[1]['text'] = '采购需求确认'
            base_steps[1]['dept'] = '采购部'
            base_steps[6]['text'] = '采购执行'
            base_steps[6]['dept'] = '采购部'
        elif '生产' in doc_code:
            base_steps[1]['text'] = '生产计划制定'
            base_steps[1]['dept'] = '生产部'
            base_steps[6]['text'] = '生产执行'
            base_steps[6]['dept'] = '生产部'
        elif '检验' in doc_code or '测量' in doc_code:
            base_steps[1]['text'] = '检验计划制定'
            base_steps[1]['dept'] = '品质部'
            base_steps[6]['text'] = '检验执行'
            base_steps[6]['dept'] = '品质部'
        
        return base_steps
    
    def generate_drawio_xml(self, doc_name, steps):
        """生成Draw.io XML格式的流程图"""
        # 创建基本XML结构
        mxfile = ET.Element('mxfile', host="app.diagrams.net", 
                          modified=datetime.now().isoformat(), 
                          agent="5.0", version="24.7.17")
        
        diagram = ET.SubElement(mxfile, 'diagram', name="流程图", id="flowchart")
        
        model = ET.SubElement(diagram, 'mxGraphModel', 
                            dx="1422", dy="794", grid="1", gridSize="10",
                            guides="1", tooltips="1", connect="1", arrows="1",
                            fold="1", page="1", pageScale="1", pageWidth="827", 
                            pageHeight="1169", math="0", shadow="0")
        
        root = ET.SubElement(model, 'root')
        ET.SubElement(root, 'mxCell', id="0")
        ET.SubElement(root, 'mxCell', id="1", parent="0")
        
        # 添加标题
        title_text = doc_name.replace('.doc', '') + '流程图'
        title_cell = ET.SubElement(root, 'mxCell', id="title", value=title_text,
                                 style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;",
                                 vertex="1", parent="1")
        ET.SubElement(title_cell, 'mxGeometry', x="300", y="20", width="200", height="30", **{"as": "geometry"})
        
        # 生成流程步骤
        start_x, start_y = 100, 80
        step_height = 80
        cell_id = 2
        
        for i, step in enumerate(steps):
            y_pos = start_y + i * step_height
            
            # 确定形状和颜色
            color = self.department_colors.get(step['dept'], '#E8E8E8')
            
            if step['type'] == 'start' or step['type'] == 'end':
                style = f"ellipse;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=12;"
                width, height = "120", "60"
            elif step['type'] == 'decision':
                style = f"rhombus;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=12;"
                width, height = "140", "80"
            else:
                style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=12;"
                width, height = "160", "60"
            
            # 添加步骤单元格
            step_text = f"{step['text']}\n({step['dept']})"
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
        for i, step in enumerate(steps):
            if step['type'] == 'decision':
                no_edge_id = cell_id + 200
                source_id = str(i + 2)
                target_id = str(max(2, i))
                
                no_edge_cell = ET.SubElement(root, 'mxCell', id=str(no_edge_id), value="否",
                                           style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
                                           edge="1", parent="1", source=source_id, target=target_id)
                ET.SubElement(no_edge_cell, 'mxGeometry', relative="1", **{"as": "geometry"})
                
                # 给下一条连接线添加"是"标签
                if i < len(steps) - 1:
                    yes_edge_id = i + 2 + 100
                    for edge in root.findall(f".//mxCell[@id='{yes_edge_id}'][@edge='1']"):
                        edge.set('value', '是')
                break
        
        return mxfile
    
    def save_flowchart(self, xml_element, filename):
        """保存流程图到文件"""
        rough_string = ET.tostring(xml_element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        formatted_xml = '\n'.join(lines)
        
        output_path = self.output_dir / f"{filename.replace('.doc', '')}.drawio"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_xml)
        
        return output_path
    
    def get_iso_documents(self):
        """获取所有ISO文档列表"""
        docs = []
        for i in range(1, 33):
            if i == 9:  # HQ-QP-09已经有专门的处理
                continue
            doc_name = f"HQ-QP-{i:02d}"
            docs.append(doc_name)
        return docs
    
    def regenerate_all_flowcharts(self):
        """重新生成所有流程图"""
        docs = self.get_iso_documents()
        
        print(f"开始重新生成 {len(docs)} 个改进的流程图...")
        
        generated_files = []
        failed_files = []
        
        for i, doc_code in enumerate(docs, 1):
            try:
                print(f"[{i}/{len(docs)}] 正在生成改进版本: {doc_code}")
                
                # 获取流程步骤
                steps = self.get_process_steps_by_document(doc_code)
                
                # 生成流程图
                xml_element = self.generate_drawio_xml(f"{doc_code}.doc", steps)
                
                # 保存文件
                output_path = self.save_flowchart(xml_element, f"{doc_code}.doc")
                generated_files.append(str(output_path))
                print(f"✅ 成功生成: {output_path.name}")
                
            except Exception as e:
                print(f"❌ 生成失败: {doc_code} - {str(e)}")
                failed_files.append(doc_code)
        
        return generated_files, failed_files

def main():
    input_dir = "S:/PG-GMO/01-Input/原始文档/PG-ISO文件"
    output_dir = "S:/PG-GMO/02-Output/品高ISO流程图"
    
    print("=== 改进的品高ISO流程图生成器 ===")
    print("正在重新生成精准的流程图...\n")
    
    generator = ImprovedBatchFlowchartGenerator(input_dir, output_dir)
    generated_files, failed_files = generator.regenerate_all_flowcharts()
    
    print(f"\n=== 重新生成完成 ===")
    print(f"✅ 成功生成: {len(generated_files)} 个改进流程图")
    print(f"❌ 生成失败: {len(failed_files)} 个文档")
    
    if generated_files:
        print(f"\n📁 重新生成的改进流程图:")
        for i, file_path in enumerate(generated_files[:10], 1):
            filename = Path(file_path).name
            print(f"{i:2d}. {filename}")
        if len(generated_files) > 10:
            print(f"    ... 还有 {len(generated_files) - 10} 个文件")
    
    return generated_files, failed_files

if __name__ == "__main__":
    main()