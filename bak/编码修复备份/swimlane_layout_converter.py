#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部门泳道布局重排工具
将综合订单全流程ERP系统业务流程图重新排列为部门泳道布局
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import re

class SwimlaneBPMNLayoutGenerator:
    def __init__(self):
        # 根据业务跟单流程图的部门泳道定义部门列
        self.department_columns = {
            "客户": {"x": 100, "color": "#F0F8FF"},
            "业务部": {"x": 250, "color": "#FFE6E6"},
            "研发部": {"x": 400, "color": "#E6FFF0"},
            "工程部": {"x": 550, "color": "#FFFFE6"},
            "采购部": {"x": 700, "color": "#F0F8FF"},
            "供应商": {"x": 850, "color": "#FFF0F5"},
            "仓储部": {"x": 1000, "color": "#F0E6FF"},
            "PMC部": {"x": 1150, "color": "#E6F3FF"},
            "生产部": {"x": 1300, "color": "#E6FFE6"},
            "品质部": {"x": 1450, "color": "#FFF0E6"},
            "财务部": {"x": 1600, "color": "#E0FFFF"},
            "管理层": {"x": 1750, "color": "#FFB6C1"}
        }
        
        # 定义列宽和行高
        self.column_width = 140
        self.row_height = 80
        self.start_y = 200
        self.step_spacing = 120  # 增加步骤间距从100到120
        
    def extract_department_from_text(self, text):
        """从步骤文本中提取部门信息"""
        # 解码HTML实体
        text = text.replace('\n', '\n').replace('\\n', '\n')
        
        # 查找🏢后面的部门名称
        match = re.search(r'🏢\s*([^\n💻]+)', text)
        if match:
            dept = match.group(1).strip()
            print(f"提取到部门: '{dept}' 从文本: {text[:50]}...")
            return dept
        
        # 备用方案：直接搜索已知部门名称
        known_depts = ["客户", "业务部", "研发部", "工程部", "采购部", "供应商", 
                      "仓储部", "PMC部", "生产部", "品质部", "财务部", "管理层"]
        for dept in known_depts:
            if dept in text:
                print(f"通过关键词匹配到部门: '{dept}'")
                return dept
        
        print(f"未能识别部门，文本: {text[:100]}...")
        return "其他部门"
    
    def parse_existing_flowchart(self, file_path):
        """解析现有的流程图文件"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 找到mxGraphModel
        graph_model = root.find(".//mxGraphModel")
        if graph_model is None:
            raise ValueError("未找到mxGraphModel元素")
        
        # 提取所有步骤单元格
        steps = []
        cells = graph_model.findall(".//mxCell[@value]")
        
        for cell in cells:
            value = cell.get('value', '')
            # 更宽松的步骤识别条件
            if value and ('S0' in value or 'S1' in value or 'S2' in value or 'S3' in value):
                # 提取步骤ID
                step_match = re.search(r'S(\d+)', value)
                if step_match:
                    step_id = int(step_match.group(1))
                    department = self.extract_department_from_text(value)
                    print(f"解析步骤 S{step_id:02d}: {department}")
                    
                    # 提取几何信息
                    geometry = cell.find('mxGeometry')
                    if geometry is not None:
                        width = float(geometry.get('width', '200'))
                        height = float(geometry.get('height', '100'))
                    else:
                        width, height = 200, 100
                    
                    # 确定形状类型
                    style = cell.get('style', '')
                    if 'ellipse' in style:
                        shape_type = 'ellipse'
                    elif 'rhombus' in style:
                        shape_type = 'rhombus'
                    else:
                        shape_type = 'rounded'
                    
                    steps.append({
                        'id': step_id,
                        'text': value,
                        'department': department,
                        'shape_type': shape_type,
                        'width': width,
                        'height': height
                    })
                    print(f"  -> 添加步骤: S{step_id:02d}, 部门: {department}, 形状: {shape_type}")
        
        # 按步骤ID排序
        steps.sort(key=lambda x: x['id'])
        return steps
    
    def generate_swimlane_layout_xml(self, steps):
        """生成部门泳道布局的XML"""
        
        # XML头部
        xml_header = f'''<mxfile host="Electron" agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/28.0.6 Chrome/138.0.7204.100 Electron/37.2.3 Safari/537.36" version="28.0.6">
  <diagram name="综合订单全流程ERP系统业务流程图-部门泳道布局" id="swimlane_erp_flowchart">
    <mxGraphModel dx="2200" dy="1400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2100" pageHeight="1400" background="#FFFFFF" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />'''
        
        xml_cells = []
        cell_id = 2
        
        # 添加标题
        xml_cells.append(f'''        <mxCell id="{cell_id}" value="品高集团综合订单全流程ERP系统业务流程图 - 部门泳道布局\\n从客户咨询到订单完结的端到端业务流程 (共{len(steps)}个关键步骤)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFD700;strokeColor=#000000;fontSize=16;fontStyle=1;strokeWidth=3;" vertex="1" parent="1">
          <mxGeometry x="50" y="20" width="1800" height="60" as="geometry" />
        </mxCell>''')
        cell_id += 1
        
        # 添加部门泳道标题
        for dept, config in self.department_columns.items():
            xml_cells.append(f'''        <mxCell id="{cell_id}" value="{dept}" style="rounded=0;whiteSpace=wrap;html=1;fillColor={config['color']};strokeColor=#000000;fontSize=14;fontStyle=1;verticalAlign=top;" vertex="1" parent="1">
          <mxGeometry x="{config['x']}" y="100" width="{self.column_width}" height="1200" as="geometry" />
        </mxCell>''')
            cell_id += 1
        
        # 按部门分组步骤
        dept_steps = {}
        for step in steps:
            dept = step['department']
            if dept not in dept_steps:
                dept_steps[dept] = []
            dept_steps[dept].append(step)
        
        # 生成步骤单元格
        step_positions = {}  # 记录步骤位置，用于连接线
        
        for dept, dept_step_list in dept_steps.items():
            if dept not in self.department_columns:
                continue
                
            dept_config = self.department_columns[dept]
            
            for i, step in enumerate(dept_step_list):
                # 计算位置
                x = dept_config['x'] + 10
                y = self.start_y + i * self.step_spacing
                
                # 记录步骤位置
                step_positions[step['id']] = {
                    'x': x + self.column_width // 2,
                    'y': y + step['height'] // 2,
                    'cell_id': cell_id
                }
                
                # 确定样式
                if step['shape_type'] == 'ellipse':
                    style = f"ellipse;whiteSpace=wrap;html=1;fillColor={dept_config['color']};strokeColor=#000000;fontSize=9;fontStyle=1;"
                elif step['shape_type'] == 'rhombus':
                    style = f"rhombus;whiteSpace=wrap;html=1;fillColor={dept_config['color']};strokeColor=#000000;fontSize=9;"
                else:
                    style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={dept_config['color']};strokeColor=#000000;fontSize=9;"
                
                xml_cells.append(f'''        <mxCell id="{cell_id}" value="{step['text']}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{self.column_width - 20}" height="{step['height']}" as="geometry" />
        </mxCell>''')
                cell_id += 1
        
        # 添加连接线（按步骤顺序连接）
        for i in range(len(steps) - 1):
            current_step = steps[i]
            next_step = steps[i + 1]
            
            if current_step['id'] in step_positions and next_step['id'] in step_positions:
                current_pos = step_positions[current_step['id']]
                next_pos = step_positions[next_step['id']]
                
                # 判断是否跨部门连接
                if current_step['department'] != next_step['department']:
                    # 跨部门连接，使用特殊样式
                    xml_cells.append(f'''        <mxCell id="{cell_id}" value="S{current_step['id']:02d}→S{next_step['id']:02d}" style="endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#FF6B6B;fontSize=10;fontColor=#FF6B6B;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{current_pos['x']}" y="{current_pos['y']}" as="sourcePoint" />
            <mxPoint x="{next_pos['x']}" y="{next_pos['y']}" as="targetPoint" />
          </mxGeometry>
        </mxCell>''')
                else:
                    # 同部门连接，使用普通样式
                    xml_cells.append(f'''        <mxCell id="{cell_id}" value="" style="endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#4CAF50;" edge="1" parent="1" source="{current_pos['cell_id']}" target="{next_pos['cell_id']}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>''')
                cell_id += 1
        
        xml_footer = '''      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        
        return xml_header + '\n' + '\n'.join(xml_cells) + '\n' + xml_footer
    
    def convert_to_swimlane_layout(self, input_file, output_file):
        """将现有流程图转换为部门泳道布局"""
        
        print(f"🚀 开始转换流程图布局...")
        print(f"📊 输入文件: {input_file}")
        print(f"📁 输出文件: {output_file}")
        
        # 解析现有流程图
        steps = self.parse_existing_flowchart(input_file)
        print(f"📋 解析到 {len(steps)} 个业务步骤")
        
        # 统计各部门步骤数
        dept_count = {}
        for step in steps:
            dept = step['department']
            dept_count[dept] = dept_count.get(dept, 0) + 1
        
        print(f"🏢 涉及部门分布:")
        for dept, count in dept_count.items():
            print(f"   • {dept}: {count} 个步骤")
        
        # 生成新的部门泳道布局XML
        xml_content = self.generate_swimlane_layout_xml(steps)
        
        # 保存文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ 部门泳道布局转换完成！")
        print(f"📐 新布局特点:")
        print(f"   • 采用部门泳道布局（各部门作为列）")
        print(f"   • 事件单元按部门垂直排列")
        print(f"   • 跨部门连接线用红色标识")
        print(f"   • 同部门连接线用绿色标识")
        
        return output_file

def main():
    """主函数"""
    
    input_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图（简）.drawio"
    output_file = "S:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-部门泳道布局.drawio"
    
    converter = SwimlaneBPMNLayoutGenerator()
    
    try:
        result_file = converter.convert_to_swimlane_layout(input_file, output_file)
        print(f"\n🎉 转换成功完成！")
        print(f"📋 新文件已保存：{result_file}")
        return True
        
    except Exception as e:
        print(f"❌ 转换过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()