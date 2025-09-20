#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整批量生成剩余的所有ISO流程图
HQ-QP-05到HQ-QP-32（共28个流程图）
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from pathlib import Path
import os

class CompleteBatchFlowchartGenerator:
    def __init__(self):
        self.colors = {
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
            '相关部门': '#E8E8E8',
            '客户': '#F0F8FF',
            '供应商': '#FFE4E1',
            '使用部门': '#E6E6FA'
        }
        
        # 获取文档名称映射
        self.doc_names = self.get_document_names()
    
    def get_document_names(self):
        """获取所有文档的完整名称"""
        doc_names = {
            'HQ-QP-05': '设备、设施管理程序',
            'HQ-QP-06': '订单评审控制程序',
            'HQ-QP-07': '新产品设计开发控制程序',
            'HQ-QP-08': '外部提供过程、产品和服务控制程序',
            'HQ-QP-09': '生产计划和生产过程控制程序',
            'HQ-QP-10': '产品标识与可追溯性控制程序',
            'HQ-QP-11': '监视和测量资源控制程序',
            'HQ-QP-12': '顾客满意控制程序',
            'HQ-QP-13': '产品放行控制程序',
            'HQ-QP-14': '不合格品控制程序',
            'HQ-QP-15': '分析评价及过程监控控制程序',
            'HQ-QP-16': '纠正和纠正措施控制程序',
            'HQ-QP-17': '顾客投诉处理控制程序',
            'HQ-QP-18': '产品召回程序',
            'HQ-QP-19': '产品风险评估管理程序',
            'HQ-QP-20': '风险评估控制程序',
            'HQ-QP-21': '危险源辨识程序',
            'HQ-QP-22': '组织环境与风险机遇应对控制程序',
            'HQ-QP-23': '组织知识管理程序',
            'HQ-QP-24': '生产和服务变更管理程序',
            'HQ-QP-25': '产品认证变更控制程序',
            'HQ-QP-26': '尾单处理管理程序',
            'HQ-QP-27': '认证标志管理程序',
            'HQ-QP-28': '采购管理控制程序',
            'HQ-QP-29': '供应商管理程序',
            'HQ-QP-30': '物料来料异常处理程序',
            'HQ-QP-31': '生产品质异常处理程序',
            'HQ-QP-32': '紧急应变措施程序'
        }
        return doc_names
    
    def get_process_steps(self, doc_code):
        """根据文档编号获取专门的流程步骤"""
        
        processes = {
            'HQ-QP-05': [  # 设备、设施管理程序
                {'text': '设备需求申请', 'type': 'start', 'dept': '使用部门'},
                {'text': '制定设备采购计划', 'type': 'process', 'dept': '工程部'},
                {'text': '设备技术规格确定', 'type': 'process', 'dept': '工程部'},
                {'text': '供应商选择评估', 'type': 'process', 'dept': '采购部'},
                {'text': '设备采购执行', 'type': 'process', 'dept': '采购部'},
                {'text': '设备验收检查', 'type': 'process', 'dept': '工程部'},
                {'text': '设备是否合格？', 'type': 'decision', 'dept': '品质部'},
                {'text': '设备安装调试', 'type': 'process', 'dept': '工程部'},
                {'text': '操作培训实施', 'type': 'process', 'dept': '工程部'},
                {'text': '设备投入使用', 'type': 'process', 'dept': '使用部门'},
                {'text': '日常维护保养', 'type': 'process', 'dept': '工程部'},
                {'text': '定期检修保养', 'type': 'process', 'dept': '工程部'},
                {'text': '设备档案管理', 'type': 'process', 'dept': '工程部'},
                {'text': '设备报废处置', 'type': 'process', 'dept': '行政部'},
                {'text': '设备管理流程结束', 'type': 'end', 'dept': '工程部'}
            ],
            'HQ-QP-06': [  # 订单评审控制程序
                {'text': '客户订单接收', 'type': 'start', 'dept': '业务部'},
                {'text': '订单信息核对', 'type': 'process', 'dept': '业务部'},
                {'text': '产品技术要求评估', 'type': 'process', 'dept': '研发部'},
                {'text': '生产能力评估', 'type': 'process', 'dept': '生产部'},
                {'text': '交期可行性分析', 'type': 'process', 'dept': '生产部'},
                {'text': '成本核算分析', 'type': 'process', 'dept': '财务部'},
                {'text': '订单是否可接受？', 'type': 'decision', 'dept': '业务部'},
                {'text': '订单确认回复', 'type': 'process', 'dept': '业务部'},
                {'text': '合同条款谈判', 'type': 'process', 'dept': '业务部'},
                {'text': '正式合同签署', 'type': 'process', 'dept': '管理层'},
                {'text': '生产计划安排', 'type': 'process', 'dept': '生产部'},
                {'text': '订单跟踪监控', 'type': 'process', 'dept': '业务部'},
                {'text': '订单档案管理', 'type': 'process', 'dept': '业务部'},
                {'text': '订单评审流程结束', 'type': 'end', 'dept': '业务部'}
            ],
            'HQ-QP-07': [  # 新产品设计开发控制程序
                {'text': '设计开发项目启动', 'type': 'start', 'dept': '研发部'},
                {'text': '市场需求调研', 'type': 'process', 'dept': '业务部'},
                {'text': '设计输入确定', 'type': 'process', 'dept': '研发部'},
                {'text': '技术可行性分析', 'type': 'process', 'dept': '研发部'},
                {'text': '设计方案制定', 'type': 'process', 'dept': '研发部'},
                {'text': '方案评审确认', 'type': 'process', 'dept': '管理层'},
                {'text': '设计方案是否可行？', 'type': 'decision', 'dept': '研发部'},
                {'text': '详细设计开发', 'type': 'process', 'dept': '研发部'},
                {'text': '样品试制验证', 'type': 'process', 'dept': '研发部'},
                {'text': '设计验证测试', 'type': 'process', 'dept': '品质部'},
                {'text': '设计确认验收', 'type': 'process', 'dept': '业务部'},
                {'text': '工艺文件编制', 'type': 'process', 'dept': '工程部'},
                {'text': '小批量试产', 'type': 'process', 'dept': '生产部'},
                {'text': '设计输出确认', 'type': 'process', 'dept': '研发部'},
                {'text': '设计开发流程结束', 'type': 'end', 'dept': '研发部'}
            ],
            'HQ-QP-08': [  # 外部提供过程、产品和服务控制程序
                {'text': '外部需求确定', 'type': 'start', 'dept': '各部门'},
                {'text': '供应商资格评估', 'type': 'process', 'dept': '采购部'},
                {'text': '合格供应商选择', 'type': 'process', 'dept': '采购部'},
                {'text': '采购合同谈判', 'type': 'process', 'dept': '采购部'},
                {'text': '合同条款审核', 'type': 'process', 'dept': '品质部'},
                {'text': '供应商是否合格？', 'type': 'decision', 'dept': '品质部'},
                {'text': '采购合同签署', 'type': 'process', 'dept': '采购部'},
                {'text': '采购执行监控', 'type': 'process', 'dept': '采购部'},
                {'text': '产品服务验收', 'type': 'process', 'dept': '使用部门'},
                {'text': '供应商绩效评价', 'type': 'process', 'dept': '采购部'},
                {'text': '供应商关系维护', 'type': 'process', 'dept': '采购部'},
                {'text': '采购档案管理', 'type': 'process', 'dept': '采购部'},
                {'text': '外部提供流程结束', 'type': 'end', 'dept': '采购部'}
            ],
            'HQ-QP-09': [  # 生产计划和生产过程控制程序
                {'text': '生产计划制定', 'type': 'start', 'dept': '生产部'},
                {'text': '订单需求分析', 'type': 'process', 'dept': '生产部'},
                {'text': '生产能力评估', 'type': 'process', 'dept': '生产部'},
                {'text': '物料需求计划', 'type': 'process', 'dept': '生产部'},
                {'text': '生产调度安排', 'type': 'process', 'dept': '生产部'},
                {'text': '生产准备工作', 'type': 'process', 'dept': '生产部'},
                {'text': '生产准备是否就绪？', 'type': 'decision', 'dept': '生产部'},
                {'text': '生产过程执行', 'type': 'process', 'dept': '生产部'},
                {'text': '过程质量监控', 'type': 'process', 'dept': '品质部'},
                {'text': '生产进度跟踪', 'type': 'process', 'dept': '生产部'},
                {'text': '异常问题处理', 'type': 'process', 'dept': '生产部'},
                {'text': '产品质量检验', 'type': 'process', 'dept': '品质部'},
                {'text': '生产数据记录', 'type': 'process', 'dept': '生产部'},
                {'text': '生产计划完成', 'type': 'process', 'dept': '生产部'},
                {'text': '生产流程结束', 'type': 'end', 'dept': '生产部'}
            ],
            'HQ-QP-10': [  # 产品标识与可追溯性控制程序
                {'text': '标识需求确定', 'type': 'start', 'dept': '生产部'},
                {'text': '标识规则制定', 'type': 'process', 'dept': '品质部'},
                {'text': '标识材料准备', 'type': 'process', 'dept': '仓储部'},
                {'text': '产品标识实施', 'type': 'process', 'dept': '生产部'},
                {'text': '标识质量检查', 'type': 'process', 'dept': '品质部'},
                {'text': '标识是否清晰？', 'type': 'decision', 'dept': '品质部'},
                {'text': '标识信息记录', 'type': 'process', 'dept': '生产部'},
                {'text': '追溯信息维护', 'type': 'process', 'dept': '品质部'},
                {'text': '标识状态监控', 'type': 'process', 'dept': '品质部'},
                {'text': '追溯系统更新', 'type': 'process', 'dept': '品质部'},
                {'text': '追溯记录归档', 'type': 'process', 'dept': '品质部'},
                {'text': '标识控制流程结束', 'type': 'end', 'dept': '品质部'}
            ],
            'HQ-QP-11': [  # 监视和测量资源控制程序
                {'text': '测量需求确定', 'type': 'start', 'dept': '品质部'},
                {'text': '测量设备选择', 'type': 'process', 'dept': '品质部'},
                {'text': '设备采购安装', 'type': 'process', 'dept': '采购部'},
                {'text': '设备校准检定', 'type': 'process', 'dept': '品质部'},
                {'text': '校准结果评定', 'type': 'process', 'dept': '品质部'},
                {'text': '设备是否合格？', 'type': 'decision', 'dept': '品质部'},
                {'text': '设备投入使用', 'type': 'process', 'dept': '品质部'},
                {'text': '日常维护保养', 'type': 'process', 'dept': '品质部'},
                {'text': '定期校准检查', 'type': 'process', 'dept': '品质部'},
                {'text': '设备状态监控', 'type': 'process', 'dept': '品质部'},
                {'text': '校准记录管理', 'type': 'process', 'dept': '品质部'},
                {'text': '设备档案管理', 'type': 'process', 'dept': '品质部'},
                {'text': '测量资源流程结束', 'type': 'end', 'dept': '品质部'}
            ],
            'HQ-QP-12': [  # 顾客满意控制程序
                {'text': '满意度调查计划', 'type': 'start', 'dept': '业务部'},
                {'text': '调查方案设计', 'type': 'process', 'dept': '业务部'},
                {'text': '调查问卷制作', 'type': 'process', 'dept': '业务部'},
                {'text': '调查活动实施', 'type': 'process', 'dept': '业务部'},
                {'text': '数据收集整理', 'type': 'process', 'dept': '业务部'},
                {'text': '满意度数据分析', 'type': 'process', 'dept': '业务部'},
                {'text': '满意度是否达标？', 'type': 'decision', 'dept': '业务部'},
                {'text': '问题原因分析', 'type': 'process', 'dept': '业务部'},
                {'text': '改进措施制定', 'type': 'process', 'dept': '管理层'},
                {'text': '改进措施实施', 'type': 'process', 'dept': '各部门'},
                {'text': '改进效果跟踪', 'type': 'process', 'dept': '业务部'},
                {'text': '满意度记录归档', 'type': 'process', 'dept': '业务部'},
                {'text': '顾客满意流程结束', 'type': 'end', 'dept': '业务部'}
            ],
            'HQ-QP-13': [  # 产品放行控制程序
                {'text': '产品检验申请', 'type': 'start', 'dept': '生产部'},
                {'text': '检验计划制定', 'type': 'process', 'dept': '品质部'},
                {'text': '检验准备工作', 'type': 'process', 'dept': '品质部'},
                {'text': '产品检验实施', 'type': 'process', 'dept': '品质部'},
                {'text': '检验数据分析', 'type': 'process', 'dept': '品质部'},
                {'text': '检验结果判定', 'type': 'process', 'dept': '品质部'},
                {'text': '产品是否合格？', 'type': 'decision', 'dept': '品质部'},
                {'text': '放行决策确认', 'type': 'process', 'dept': '品质部'},
                {'text': '放行文件签署', 'type': 'process', 'dept': '品质部'},
                {'text': '产品发货准备', 'type': 'process', 'dept': '仓储部'},
                {'text': '发货执行监控', 'type': 'process', 'dept': '业务部'},
                {'text': '放行记录归档', 'type': 'process', 'dept': '品质部'},
                {'text': '产品放行流程结束', 'type': 'end', 'dept': '品质部'}
            ],
            'HQ-QP-14': [  # 不合格品控制程序
                {'text': '不合格品发现', 'type': 'start', 'dept': '各部门'},
                {'text': '不合格品标识', 'type': 'process', 'dept': '品质部'},
                {'text': '不合格品隔离', 'type': 'process', 'dept': '仓储部'},
                {'text': '不合格原因分析', 'type': 'process', 'dept': '品质部'},
                {'text': '处置方案确定', 'type': 'process', 'dept': '品质部'},
                {'text': '是否可以返工？', 'type': 'decision', 'dept': '品质部'},
                {'text': '返工处理执行', 'type': 'process', 'dept': '生产部'},
                {'text': '处置效果验证', 'type': 'process', 'dept': '品质部'},
                {'text': '预防措施制定', 'type': 'process', 'dept': '品质部'},
                {'text': '预防措施实施', 'type': 'process', 'dept': '相关部门'},
                {'text': '记录整理归档', 'type': 'process', 'dept': '品质部'},
                {'text': '不合格品流程结束', 'type': 'end', 'dept': '品质部'}
            ]
        }
        
        # 如果没有具体定义，使用通用流程
        if doc_code in processes:
            return processes[doc_code]
        else:
            return self.get_generic_process(doc_code)
    
    def get_generic_process(self, doc_code):
        """为未定义的文档生成通用流程"""
        doc_name = self.doc_names.get(doc_code, doc_code)
        
        # 基于文档名称的通用流程
        steps = [
            {'text': f'{doc_name}启动', 'type': 'start', 'dept': '相关部门'},
            {'text': '需求分析确认', 'type': 'process', 'dept': '相关部门'},
            {'text': '方案制定', 'type': 'process', 'dept': '执行部门'},
            {'text': '初步审核', 'type': 'process', 'dept': '品质部'},
            {'text': '是否符合要求？', 'type': 'decision', 'dept': '品质部'},
            {'text': '审批确认', 'type': 'process', 'dept': '管理层'},
            {'text': '执行实施', 'type': 'process', 'dept': '执行部门'},
            {'text': '过程监控', 'type': 'process', 'dept': '品质部'},
            {'text': '效果评估', 'type': 'process', 'dept': '品质部'},
            {'text': '记录归档', 'type': 'process', 'dept': '相关部门'},
            {'text': f'{doc_name}结束', 'type': 'end', 'dept': '相关部门'}
        ]
        
        return steps
    
    def generate_drawio_xml(self, doc_code, steps):
        """生成Draw.io XML格式的流程图"""
        doc_name = self.doc_names.get(doc_code, doc_code)
        
        # 创建XML结构
        mxfile = ET.Element('mxfile', host="app.diagrams.net", 
                          modified=datetime.now().isoformat(), 
                          agent="5.0", version="24.7.17")
        
        diagram = ET.SubElement(mxfile, 'diagram', name=f"{doc_code}流程图", id="flowchart")
        
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
                                 value=f"{doc_code} {doc_name}流程图",
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
            return_target_id = str(max(2, decision_index - 2))
            
            # 根据不同类型设置标签
            if "合格" in decision_step['text']:
                no_label = "不合格"
                yes_label = "合格"
            elif "可行" in decision_step['text']:
                no_label = "不可行"
                yes_label = "可行"
            elif "达标" in decision_step['text']:
                no_label = "未达标"
                yes_label = "达标"
            elif "返工" in decision_step['text']:
                no_label = "报废处理"
                yes_label = "返工"
            else:
                no_label = "否"
                yes_label = "是"
            
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
    
    def generate_all_remaining(self):
        """生成所有剩余的流程图"""
        # 需要生成的文档列表
        docs_to_generate = [
            'HQ-QP-05', 'HQ-QP-06', 'HQ-QP-07', 'HQ-QP-08', 'HQ-QP-09', 'HQ-QP-10',
            'HQ-QP-11', 'HQ-QP-12', 'HQ-QP-13', 'HQ-QP-14', 'HQ-QP-15', 'HQ-QP-16',
            'HQ-QP-17', 'HQ-QP-18', 'HQ-QP-19', 'HQ-QP-20', 'HQ-QP-21', 'HQ-QP-22',
            'HQ-QP-23', 'HQ-QP-24', 'HQ-QP-25', 'HQ-QP-26', 'HQ-QP-27', 'HQ-QP-28',
            'HQ-QP-29', 'HQ-QP-30', 'HQ-QP-31', 'HQ-QP-32'
        ]
        
        generated_files = []
        failed_files = []
        
        print(f"开始批量生成 {len(docs_to_generate)} 个剩余流程图...")
        
        for i, doc_code in enumerate(docs_to_generate, 1):
            try:
                doc_name = self.doc_names.get(doc_code, doc_code)
                print(f"[{i}/{len(docs_to_generate)}] 正在生成: {doc_code} {doc_name}")
                
                # 获取流程步骤
                steps = self.get_process_steps(doc_code)
                
                # 生成流程图
                xml_element = self.generate_drawio_xml(doc_code, steps)
                
                # 保存文件
                filename = f"{doc_code} {doc_name}.drawio"
                output_path = self.save_flowchart(xml_element, filename)
                generated_files.append(str(output_path))
                print(f"✅ 成功生成: {filename}")
                
            except Exception as e:
                print(f"❌ 生成失败: {doc_code} - {str(e)}")
                failed_files.append(doc_code)
        
        return generated_files, failed_files

def main():
    generator = CompleteBatchFlowchartGenerator()
    generated_files, failed_files = generator.generate_all_remaining()
    
    print(f"\n=== 批量生成完成 ===")
    print(f"✅ 成功生成: {len(generated_files)} 个流程图")
    print(f"❌ 生成失败: {len(failed_files)} 个文档")
    
    if generated_files:
        print(f"\n📁 生成的流程图文件:")
        for i, file_path in enumerate(generated_files[:10], 1):
            filename = Path(file_path).name
            print(f"{i:2d}. {filename}")
        if len(generated_files) > 10:
            print(f"    ... 还有 {len(generated_files) - 10} 个文件")
    
    if failed_files:
        print(f"\n❌ 生成失败的文档:")
        for doc_code in failed_files:
            print(f"   - {doc_code}")
    
    return generated_files, failed_files

if __name__ == "__main__":
    main()