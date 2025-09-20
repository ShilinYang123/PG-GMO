#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合订单全流程ERP系统设计流程图生成器
从业务接订单起到订单交货收款结束的完整业务流程
"""

import os
from datetime import datetime

class ComprehensiveERPFlowchartGenerator:
    def __init__(self):
        self.output_dir = "S:\\PG-GMO\\02-Output\\品高ISO流程图"
        self.ensure_output_dir()
        
        # ERP系统部门颜色配置
        self.department_colors = {
            "业务部": "#FFE6E6", "PMC部": "#E6F3FF", "研发部": "#E6FFF0",
            "采购部": "#F0F8FF", "生产部": "#E6FFE6", "品质部": "#FFF0E6",
            "仓储部": "#F0E6FF", "工程部": "#FFFFE6", "财务部": "#E0FFFF",
            "管理层": "#FFB6C1", "客户": "#F0F8FF", "供应商": "#FFF0F5"
        }
        
    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_comprehensive_erp_process(self):
        """获取综合订单全流程ERP系统流程定义"""
        return [
            # 订单获取阶段
            {'id': 'S01', 'text': '客户需求咨询\\n产品信息查询', 'type': 'start', 'department': '客户', 'systems': ['CRM系统', '产品数据库']},
            {'id': 'S02', 'text': '商务洽谈报价\\n技术方案讨论', 'type': 'process', 'department': '业务部', 'systems': ['报价系统', '技术文档系统']},
            {'id': 'S03', 'text': '技术可行性评估\\n工艺路线分析', 'type': 'process', 'department': '研发部', 'systems': ['技术管理系统', 'CAD系统']},
            {'id': 'S04', 'text': '成本核算分析\\n利润率评估', 'type': 'process', 'department': '财务部', 'systems': ['成本管理系统', 'ERP财务模块']},
            {'id': 'S05', 'text': '订单评审决策\\n接单风险评估', 'type': 'decision', 'department': '管理层', 'systems': ['决策支持系统', '风险管理系统']},
            
            # 合同签署阶段
            {'id': 'S06', 'text': '合同条款谈判\\n交期价格确认', 'type': 'process', 'department': '业务部', 'systems': ['合同管理系统', 'CRM系统']},
            {'id': 'S07', 'text': '正式合同签署\\n客户关系确立', 'type': 'process', 'department': '管理层', 'systems': ['合同管理系统', 'CRM系统']},
            {'id': 'S08', 'text': '订单信息录入\\nERP系统建档', 'type': 'process', 'department': '业务部', 'systems': ['ERP订单管理', '客户数据库']},
            
            # 生产准备阶段
            {'id': 'S09', 'text': '生产计划制定\\n产能负荷分析', 'type': 'process', 'department': 'PMC部', 'systems': ['MRP系统', '产能管理系统']},
            {'id': 'S10', 'text': '物料需求计算\\nBOM清单展开', 'type': 'process', 'department': 'PMC部', 'systems': ['MRP系统', 'BOM管理系统']},
            {'id': 'S11', 'text': '库存状态检查\\n缺料清单生成', 'type': 'process', 'department': '仓储部', 'systems': ['库存管理系统', 'WMS系统']},
            {'id': 'S12', 'text': '采购需求提交\\n供应商选择', 'type': 'process', 'department': '采购部', 'systems': ['采购管理系统', '供应商管理系统']},
            {'id': 'S13', 'text': '工艺路线设计\\n作业指导编制', 'type': 'process', 'department': '工程部', 'systems': ['工艺管理系统', '技术文档系统']},
            
            # 采购物流阶段
            {'id': 'S14', 'text': '供应商生产交付\\n物流运输安排', 'type': 'process', 'department': '供应商', 'systems': ['SRM系统', '物流跟踪系统']},
            {'id': 'S15', 'text': '来料检验验收\\n质量符合性确认', 'type': 'process', 'department': '品质部', 'systems': ['质量管理系统', '检验数据系统']},
            {'id': 'S16', 'text': '合格物料入库\\n库存信息更新', 'type': 'process', 'department': '仓储部', 'systems': ['WMS系统', '库存管理系统']},
            
            # 生产制造阶段
            {'id': 'S17', 'text': '生产任务下达\\n车间排程安排', 'type': 'process', 'department': 'PMC部', 'systems': ['MES系统', '排程系统']},
            {'id': 'S18', 'text': '物料领用出库\\n生产准备就绪', 'type': 'process', 'department': '仓储部', 'systems': ['WMS系统', 'MES系统']},
            {'id': 'S19', 'text': '生产过程执行\\n实时数据采集', 'type': 'process', 'department': '生产部', 'systems': ['MES系统', '数据采集系统']},
            {'id': 'S20', 'text': '过程质量监控\\nSPC统计分析', 'type': 'process', 'department': '品质部', 'systems': ['质量管理系统', 'SPC系统']},
            
            # 质量检验阶段
            {'id': 'S21', 'text': '首件检验确认\\n工艺稳定性验证', 'type': 'process', 'department': '品质部', 'systems': ['质量管理系统', 'MES系统']},
            {'id': 'S22', 'text': '最终产品检验\\n质量符合性判定', 'type': 'decision', 'department': '品质部', 'systems': ['质量管理系统', '检验设备系统']},
            {'id': 'S23', 'text': '产品质量放行\\n出货许可确认', 'type': 'process', 'department': '品质部', 'systems': ['质量管理系统', 'WMS系统']},
            
            # 库存包装阶段
            {'id': 'S24', 'text': '成品入库管理\\n库存信息更新', 'type': 'process', 'department': '仓储部', 'systems': ['WMS系统', '库存管理系统']},
            {'id': 'S25', 'text': '产品标识追溯\\n批次信息记录', 'type': 'process', 'department': '仓储部', 'systems': ['追溯系统', 'WMS系统']},
            {'id': 'S26', 'text': '包装规格确认\\n包装作业执行', 'type': 'process', 'department': '仓储部', 'systems': ['包装管理系统', 'WMS系统']},
            
            # 发货交付阶段
            {'id': 'S27', 'text': '客户发货通知\\n物流安排协调', 'type': 'process', 'department': '业务部', 'systems': ['CRM系统', '物流管理系统']},
            {'id': 'S28', 'text': '货物装车出库\\n运输过程跟踪', 'type': 'process', 'department': '仓储部', 'systems': ['WMS系统', '物流跟踪系统']},
            {'id': 'S29', 'text': '客户收货确认\\n验收签收完成', 'type': 'process', 'department': '客户', 'systems': ['客户门户系统', 'CRM系统']},
            
            # 财务结算阶段
            {'id': 'S30', 'text': '开具销售发票\\n应收账款确认', 'type': 'process', 'department': '财务部', 'systems': ['财务管理系统', '发票管理系统']},
            {'id': 'S31', 'text': '客户付款处理\\n收款确认入账', 'type': 'process', 'department': '财务部', 'systems': ['财务管理系统', '银行对接系统']},
            {'id': 'S32', 'text': '成本结算分析\\n项目盈亏核算', 'type': 'process', 'department': '财务部', 'systems': ['成本管理系统', 'ERP财务模块']},
            {'id': 'S33', 'text': '订单完结归档\\n数据分析总结', 'type': 'end', 'department': '业务部', 'systems': ['CRM系统', '数据分析系统']}
        ]
    
    def generate_comprehensive_erp_drawio_xml(self):
        """生成综合ERP系统流程图的Draw.io XML"""
        
        steps = self.get_comprehensive_erp_process()
        
        # A2横向画布配置
        canvas_width = 5940  # A2横向宽度
        canvas_height = 4200  # A2横向高度
        
        xml_header = f'''<mxfile host="app.diagrams.net" modified="{datetime.now().isoformat()}" agent="ComprehensiveERPFlowchartGenerator" version="2.0" etag="comprehensive_erp" type="device">
  <diagram name="综合订单全流程ERP系统业务流程图" id="comprehensive_erp_flowchart">
    <mxGraphModel dx="5940" dy="4200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{canvas_width}" pageHeight="{canvas_height}" math="0" shadow="0" background="#FFFFFF">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />'''
        
        xml_cells = []
        cell_id = 2
        
        # 添加标题
        xml_cells.append(f'''        <mxCell id="{cell_id}" value="品高集团综合订单全流程ERP系统业务流程图\\n从客户咨询到订单完结的端到端业务流程 (共{len(steps)}个关键步骤)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFD700;strokeColor=#000000;fontSize=18;fontStyle=1;strokeWidth=3;" vertex="1" parent="1">
          <mxGeometry x="100" y="30" width="1200" height="80" as="geometry" />
        </mxCell>''')
        cell_id += 1
        
        # 流程步骤布局参数
        steps_per_row = 8
        step_width = 200
        step_height = 100
        margin_x = 80
        margin_y = 150
        spacing_x = 50
        spacing_y = 30
        
        # 生成流程步骤
        for i, step in enumerate(steps):
            row = i // steps_per_row
            col = i % steps_per_row
            x = margin_x + col * (step_width + spacing_x)
            y = margin_y + row * (step_height + spacing_y)
            
            # 获取部门颜色
            color = self.department_colors.get(step['department'], '#F5F5F5')
            
            # 构建步骤文本内容
            text_content = f"{step['id']}. {step['text']}"
            text_content += f"\\n\\n🏢 {step['department']}"
            if 'systems' in step and step['systems']:
                text_content += f"\\n💻 {step['systems'][0]}"
            
            # 确定形状样式
            if step['type'] == 'start':
                style = f"ellipse;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=10;fontStyle=1;"
            elif step['type'] == 'end':
                style = f"ellipse;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=10;fontStyle=1;"
            elif step['type'] == 'decision':
                style = f"rhombus;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=10;"
            else:
                style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=10;"
            
            xml_cells.append(f'''        <mxCell id="{cell_id}" value="{text_content}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{step_width}" height="{step_height}" as="geometry" />
        </mxCell>''')
            
            # 添加连接线
            if i < len(steps) - 1:
                next_cell_id = cell_id + 1
                xml_cells.append(f'''        <mxCell id="{cell_id + 1000}" value="" style="endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#4CAF50;" edge="1" parent="1" source="{cell_id}" target="{next_cell_id}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>''')
            
            cell_id += 1
        
        # 添加部门图例
        legend_y = canvas_height - 300
        for idx, (dept, color) in enumerate(self.department_colors.items()):
            legend_x = 100 + (idx % 6) * 200
            legend_row_y = legend_y + (idx // 6) * 40
            
            xml_cells.append(f'''        <mxCell id="{cell_id}" value="{dept}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="{legend_x}" y="{legend_row_y}" width="180" height="30" as="geometry" />
        </mxCell>''')
            cell_id += 1
        
        xml_footer = '''      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        
        return xml_header + '\n' + '\n'.join(xml_cells) + '\n' + xml_footer
    
    def generate_comprehensive_erp_flowchart(self):
        """生成综合ERP系统业务流程图"""
        
        print("🚀 开始生成综合订单全流程ERP系统业务流程图...")
        print("📐 画布规格: A2横向 (59.4cm x 42cm)")
        
        steps = self.get_comprehensive_erp_process()
        departments = set(step['department'] for step in steps)
        
        print(f"📊 流程概览:")
        print(f"   • 业务步骤: {len(steps)} 个")
        print(f"   • 涉及部门: {len(departments)} 个")
        print(f"   • 相关系统: ERP核心模块 + 专业子系统")
        
        # 生成XML
        xml_content = self.generate_comprehensive_erp_drawio_xml()
        
        # 保存文件
        filename = "综合订单全流程ERP系统业务流程图.drawio"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ 成功生成: {filename}")
        print(f"📁 文件位置: {filepath}")
        print(f"📋 可使用Draw.io打开编辑")
        
        return filepath

def main():
    """主函数"""
    print("🚀 启动综合订单全流程ERP系统流程图生成器...")
    
    generator = ComprehensiveERPFlowchartGenerator()
    
    try:
        filepath = generator.generate_comprehensive_erp_flowchart()
        print(f"\n✅ 综合ERP系统流程图生成完成！")
        print(f"📋 文件可在Draw.io中打开查看和编辑")
        return True
        
    except Exception as e:
        print(f"❌ 生成过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()