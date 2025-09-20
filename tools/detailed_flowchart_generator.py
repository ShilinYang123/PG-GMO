#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细流程图生成器
专门用于生成HQ-QP-09生产计划和生产过程控制程序的详细流程图
"""

import os
import json
from datetime import datetime

class DetailedFlowchartGenerator:
    def __init__(self):
        self.output_dir = "S:\\PG-GMO\\02-Output\\品高ISO流程图"
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_hq_qp_09_flowchart(self):
        """生成HQ-QP-09生产计划和生产过程控制程序流程图"""
        
        # 基于ISO标准的生产计划和生产过程控制流程
        flowchart_data = {
            "title": "HQ-QP-09 生产计划和生产过程控制程序流程图",
            "version": "v1.0",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "departments": {
                "业务部": "#FFE6E6",  # 浅红色
                "PMC部": "#E6F3FF",   # 浅蓝色
                "生产部": "#E6FFE6",  # 浅绿色
                "品质部": "#FFF0E6",  # 浅橙色
                "仓库": "#F0E6FF",    # 浅紫色
                "工程部": "#FFFFE6"   # 浅黄色
            },
            "process_steps": [
                {
                    "id": "start",
                    "type": "start",
                    "text": "开始",
                    "department": "业务部",
                    "position": {"x": 100, "y": 50}
                },
                {
                    "id": "sales_order",
                    "type": "process",
                    "text": "接收客户订单\n填写销售订单",
                    "department": "业务部",
                    "forms": ["销售订单", "客户需求确认单"],
                    "position": {"x": 100, "y": 150}
                },
                {
                    "id": "order_review",
                    "type": "decision",
                    "text": "订单评审\n技术可行性评估",
                    "department": "PMC部",
                    "forms": ["订单评审表", "技术评估报告"],
                    "position": {"x": 100, "y": 250}
                },
                {
                    "id": "production_plan",
                    "type": "process",
                    "text": "制定生产计划\n编制生产任务单",
                    "department": "PMC部",
                    "forms": ["生产计划表", "生产任务单", "物料需求计划"],
                    "position": {"x": 300, "y": 250}
                },
                {
                    "id": "material_prepare",
                    "type": "process",
                    "text": "物料准备\n库存检查",
                    "department": "仓库",
                    "forms": ["物料清单", "库存报表", "领料单"],
                    "position": {"x": 500, "y": 250}
                },
                {
                    "id": "process_prepare",
                    "type": "process",
                    "text": "工艺准备\n设备检查",
                    "department": "工程部",
                    "forms": ["工艺流程图", "作业指导书", "设备点检表"],
                    "position": {"x": 300, "y": 350}
                },
                {
                    "id": "production_start",
                    "type": "process",
                    "text": "生产开始\n首件检验",
                    "department": "生产部",
                    "forms": ["生产日报表", "首件检验记录"],
                    "position": {"x": 300, "y": 450}
                },
                {
                    "id": "process_control",
                    "type": "process",
                    "text": "生产过程控制\n质量监控",
                    "department": "品质部",
                    "forms": ["QC巡查报告", "工艺参数记录", "异常报告"],
                    "position": {"x": 500, "y": 450}
                },
                {
                    "id": "quality_check",
                    "type": "decision",
                    "text": "质量检验",
                    "department": "品质部",
                    "forms": ["检验记录表", "不合格品处理单"],
                    "position": {"x": 300, "y": 550}
                },
                {
                    "id": "rework",
                    "type": "process",
                    "text": "返工/返修",
                    "department": "生产部",
                    "forms": ["返工单", "返修记录"],
                    "position": {"x": 100, "y": 550}
                },
                {
                    "id": "final_inspection",
                    "type": "process",
                    "text": "最终检验\n包装入库",
                    "department": "品质部",
                    "forms": ["最终检验报告", "包装清单"],
                    "position": {"x": 300, "y": 650}
                },
                {
                    "id": "delivery",
                    "type": "process",
                    "text": "发货交付\n客户确认",
                    "department": "仓库",
                    "forms": ["发货单", "客户签收单"],
                    "position": {"x": 300, "y": 750}
                },
                {
                    "id": "end",
                    "type": "end",
                    "text": "结束",
                    "department": "业务部",
                    "position": {"x": 300, "y": 850}
                }
            ],
            "connections": [
                {"from": "start", "to": "sales_order"},
                {"from": "sales_order", "to": "order_review"},
                {"from": "order_review", "to": "production_plan", "condition": "通过"},
                {"from": "order_review", "to": "sales_order", "condition": "不通过"},
                {"from": "production_plan", "to": "material_prepare"},
                {"from": "production_plan", "to": "process_prepare"},
                {"from": "material_prepare", "to": "production_start"},
                {"from": "process_prepare", "to": "production_start"},
                {"from": "production_start", "to": "process_control"},
                {"from": "process_control", "to": "quality_check"},
                {"from": "quality_check", "to": "final_inspection", "condition": "合格"},
                {"from": "quality_check", "to": "rework", "condition": "不合格"},
                {"from": "rework", "to": "quality_check"},
                {"from": "final_inspection", "to": "delivery"},
                {"from": "delivery", "to": "end"}
            ]
        }
        
        # 生成draw.io格式的XML
        drawio_xml = self.generate_drawio_xml(flowchart_data)
        
        # 保存文件
        filename = "HQ-QP-09_生产计划和生产过程控制程序流程图.drawio"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(drawio_xml)
        
        print(f"✅ 成功生成流程图: {filepath}")
        print(f"📊 包含 {len(flowchart_data['process_steps'])} 个流程步骤")
        print(f"🏢 涉及 {len(flowchart_data['departments'])} 个部门")
        print(f"📋 使用 {sum(len(step.get('forms', [])) for step in flowchart_data['process_steps'])} 个表单")
        
        return filepath
    
    def generate_drawio_xml(self, data):
        """生成draw.io格式的XML"""
        
        xml_header = '''<mxfile host="app.diagrams.net" modified="{date}" agent="DetailedFlowchartGenerator" version="1.0" etag="1" type="device">
  <diagram name="{title}" id="flowchart">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />'''.format(
            date=datetime.now().isoformat(),
            title=data['title']
        )
        
        xml_cells = []
        cell_id = 2
        
        # 生成流程步骤的XML
        for step in data['process_steps']:
            dept_color = data['departments'].get(step['department'], '#FFFFFF')
            
            if step['type'] == 'start' or step['type'] == 'end':
                shape = 'ellipse'
                style = f'ellipse;whiteSpace=wrap;html=1;fillColor={dept_color};strokeColor=#000000;'
            elif step['type'] == 'decision':
                shape = 'rhombus'
                style = f'rhombus;whiteSpace=wrap;html=1;fillColor={dept_color};strokeColor=#000000;'
            else:
                shape = 'rectangle'
                style = f'rounded=1;whiteSpace=wrap;html=1;fillColor={dept_color};strokeColor=#000000;'
            
            # 添加表单信息到文本中
            text = step['text']
            if 'forms' in step and step['forms']:
                text += '\n\n📋 相关表单:\n' + '\n'.join(f'• {form}' for form in step['forms'])
            
            text += f'\n\n🏢 {step["department"]}'
            
            xml_cells.append(f'''        <mxCell id="{cell_id}" value="{text}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{step['position']['x']}" y="{step['position']['y']}" width="120" height="80" as="geometry" />
        </mxCell>''')
            
            step['cell_id'] = cell_id
            cell_id += 1
        
        # 生成连接线的XML
        step_dict = {step['id']: step for step in data['process_steps']}
        
        for conn in data['connections']:
            from_step = step_dict[conn['from']]
            to_step = step_dict[conn['to']]
            
            label = conn.get('condition', '')
            label_style = 'edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];'
            
            xml_cells.append(f'''        <mxCell id="{cell_id}" value="{label}" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="{from_step['cell_id']}" target="{to_step['cell_id']}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>''')
            cell_id += 1
        
        xml_footer = '''      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        
        return xml_header + '\n' + '\n'.join(xml_cells) + '\n' + xml_footer

def main():
    """主函数"""
    print("🚀 启动详细流程图生成器...")
    
    generator = DetailedFlowchartGenerator()
    
    try:
        # 生成HQ-QP-09流程图
        filepath = generator.generate_hq_qp_09_flowchart()
        print(f"\n✅ 流程图生成完成！")
        print(f"📁 文件位置: {filepath}")
        print(f"\n💡 提示: 可以使用draw.io打开此文件进行查看和编辑")
        
    except Exception as e:
        print(f"❌ 生成流程图时发生错误: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()