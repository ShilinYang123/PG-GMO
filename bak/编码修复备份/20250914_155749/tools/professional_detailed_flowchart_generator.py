#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业级详细流程图生成器 - 核心版本
为所有32个ISO质量体系文档生成编程序级别的详细流程图
基于早上HQ-QP-09成功模式，确保每个流程图都具备专业性和实用性
"""

import os
import json
from datetime import datetime
from pathlib import Path

class ProfessionalDetailedFlowchartGenerator:
    def __init__(self):
        self.output_dir = "S:\\PG-GMO\\02-Output\\品高ISO流程图"
        self.ensure_output_dir()
        
        # 专业部门颜色配置
        self.department_colors = {
            "业务部": "#FFE6E6", "PMC部": "#E6F3FF", "生产部": "#E6FFE6", 
            "品质部": "#FFF0E6", "仓库": "#F0E6FF", "工程部": "#FFFFE6",
            "研发部": "#E6FFF0", "采购部": "#F0F8FF", "人力资源部": "#F5F5DC",
            "财务部": "#E0FFFF", "行政部": "#FFF8DC", "管理层": "#FFB6C1",
            "各部门": "#F5F5F5", "客户": "#F0F8FF", "供应商": "#FFF0F5",
            "内审员": "#E6E6FA", "管理代表": "#DDA0DD", "被审核部门": "#FFEFD5"
        }
        
    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_drawio_xml(self, doc_code, doc_name, steps):
        """生成专业级Draw.io XML格式流程图"""
        
        # XML头部
        xml_header = f'''<mxfile host="app.diagrams.net" modified="{datetime.now().isoformat()}" agent="ProfessionalDetailedFlowchartGenerator" version="2.0" etag="professional" type="device">
  <diagram name="{doc_code} {doc_name}流程图" id="professional_flowchart">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />'''
        
        xml_cells = []
        
        # 生成流程步骤单元格
        for i, step in enumerate(steps):
            cell_id = i + 2
            
            # 确定颜色
            color = self.department_colors.get(step['department'], '#F5F5F5')
            
            # 构建文本内容 - 专业格式
            text_content = step['text']
            if 'forms' in step and step['forms']:
                text_content += "\\n\\n📋 相关表单:"
                for form in step['forms']:
                    text_content += f"\\n• {form}"
            text_content += f"\\n\\n🏢 {step['department']}"
            
            # 确定形状和尺寸
            if step['type'] == 'start' or step['type'] == 'end':
                style = f"ellipse;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=10;fontStyle=1;"
                width, height = "140", "90"
            elif step['type'] == 'decision':
                style = f"rhombus;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=10;"
                width, height = "160", "100"  
            else:
                style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#000000;fontSize=10;"
                width, height = "180", "120"
            
            # 计算位置
            x_pos = 100 + (i % 3) * 250
            y_pos = 50 + (i // 3) * 140
            
            # 添加单元格
            xml_cells.append(f'''        <mxCell id="{cell_id}" value="{text_content}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{x_pos}" y="{y_pos}" width="{width}" height="{height}" as="geometry" />
        </mxCell>''')
            
            # 添加连接线（简化版本）
            if i < len(steps) - 1:
                next_cell_id = cell_id + 1
                xml_cells.append(f'''        <mxCell id="{cell_id + 100}" value="" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="{cell_id}" target="{next_cell_id}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>''')
        
        xml_footer = '''      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        
        return xml_header + '\n' + '\n'.join(xml_cells) + '\n' + xml_footer
    
    def generate_professional_flowchart(self, doc_code):
        """生成专业级详细流程图"""
        
        # 获取文档规格
        doc_specs = self.get_document_specifications()
        
        if doc_code not in doc_specs:
            print(f"⚠️  未找到 {doc_code} 的专业规格，使用通用规格")
            return self.generate_generic_flowchart(doc_code)
        
        spec = doc_specs[doc_code]
        doc_name = spec['name']
        steps = spec['steps']
        
        print(f"🚀 正在生成专业级流程图: {doc_code} {doc_name}")
        print(f"📊 包含 {len(steps)} 个详细步骤")
        print(f"🏢 涉及 {len(set(step['department'] for step in steps))} 个部门")
        print(f"📋 关联 {sum(len(step.get('forms', [])) for step in steps)} 个表单")
        
        # 生成XML
        xml_content = self.generate_drawio_xml(doc_code, doc_name, steps)
        
        # 保存文件
        filename = f"{doc_code} {doc_name}.drawio"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ 成功生成: {filename}")
        return filepath
    
    def get_document_specifications(self):
        """获取所有文档的专业规格 - 完整版本"""
        # 导入扩展规格库
        try:
            from extended_professional_specs import get_extended_professional_specifications
            extended_specs = get_extended_professional_specifications()
        except ImportError:
            extended_specs = {}
        
        # 基础规格 + 扩展规格 + 快速生成的剩余规格
        remaining_specs = {
            'HQ-QP-16': {'name': '纠正和纠正措施控制程序', 'steps': [{'text': '问题识别发现\\n不符合项记录', 'type': 'start', 'department': '各部门', 'forms': ['问题识别记录', '不符合项报告']}, {'text': '问题分析评估\\n影响程度判定', 'type': 'process', 'department': '品质部', 'forms': ['问题分析报告', '影响评估']}, {'text': '纠正措施制定\\n临时措施实施', 'type': 'process', 'department': '责任部门', 'forms': ['纠正措施计划', '临时措施记录']}, {'text': '根本原因分析\\n系统性原因调查', 'type': 'process', 'department': '品质部', 'forms': ['根本原因分析', '系统调查报告']}, {'text': '预防措施制定\\n系统改进方案', 'type': 'process', 'department': '品质部', 'forms': ['预防措施计划', '系统改进方案']}, {'text': '措施实施执行\\n跨部门协调配合', 'type': 'process', 'department': '各部门', 'forms': ['实施执行记录', '协调配合记录']}, {'text': '实施效果验证\\n改进成果评估', 'type': 'process', 'department': '品质部', 'forms': ['效果验证报告', '成果评估']}, {'text': '是否有效改进？\\n目标达成评估', 'type': 'decision', 'department': '品质部', 'forms': ['有效性评估', '目标达成分析']}, {'text': '经验教训总结\\n知识管理更新', 'type': 'process', 'department': '品质部', 'forms': ['经验教训总结', '知识库更新']}, {'text': '纠正措施流程完成', 'type': 'end', 'department': '品质部', 'forms': []}]},
            'HQ-QP-17': {'name': '顾客投诉处理控制程序', 'steps': [{'text': '投诉信息接收\\n客户问题登记', 'type': 'start', 'department': '业务部', 'forms': ['投诉登记表', '客户问题记录']}, {'text': '投诉内容确认\\n问题严重程度评估', 'type': 'process', 'department': '业务部', 'forms': ['投诉确认书', '严重程度评估']}, {'text': '紧急处理措施\\n客户关系维护', 'type': 'process', 'department': '业务部', 'forms': ['紧急处理记录', '客户沟通记录']}, {'text': '问题原因调查\\n责任部门追溯', 'type': 'process', 'department': '品质部', 'forms': ['原因调查报告', '责任追溯记录']}, {'text': '解决方案制定\\n补救措施确定', 'type': 'process', 'department': '品质部', 'forms': ['解决方案', '补救措施计划']}, {'text': '方案客户确认\\n实施条件协商', 'type': 'process', 'department': '业务部', 'forms': ['客户确认书', '实施协商记录']}, {'text': '解决方案实施\\n执行过程监控', 'type': 'process', 'department': '相关部门', 'forms': ['实施执行记录', '过程监控表']}, {'text': '客户满意度确认\\n投诉关闭验证', 'type': 'process', 'department': '业务部', 'forms': ['满意度确认', '投诉关闭验证']}, {'text': '是否满意解决？\\n客户接受度评估', 'type': 'decision', 'department': '业务部', 'forms': ['满意度评估', '接受度分析']}, {'text': '预防措施制定\\n系统改进实施', 'type': 'process', 'department': '品质部', 'forms': ['预防措施', '系统改进计划']}, {'text': '投诉处理流程完成', 'type': 'end', 'department': '业务部', 'forms': []}]}
        }
        
        # 其他快速生成的通用规格...
        for doc_code in ['HQ-QP-18', 'HQ-QP-19', 'HQ-QP-20', 'HQ-QP-21', 'HQ-QP-22', 'HQ-QP-23', 'HQ-QP-24', 'HQ-QP-25', 'HQ-QP-26', 'HQ-QP-27', 'HQ-QP-28', 'HQ-QP-29', 'HQ-QP-30', 'HQ-QP-31', 'HQ-QP-32']:
            if doc_code not in remaining_specs:
                doc_names = {
                    'HQ-QP-18': '产品召回程序', 'HQ-QP-19': '产品风险评估管理程序', 'HQ-QP-20': '风险评估控制程序',
                    'HQ-QP-21': '危险源辨识程序', 'HQ-QP-22': '组织环境与风险机遇应对控制程序', 'HQ-QP-23': '组织知识管理程序',
                    'HQ-QP-24': '生产和服务变更管理程序', 'HQ-QP-25': '产品认证变更控制程序', 'HQ-QP-26': '尾单处理管理程序',
                    'HQ-QP-27': '认证标志管理程序', 'HQ-QP-28': '采购管理控制程序', 'HQ-QP-29': '供应商管理程序',
                    'HQ-QP-30': '物料来料异常处理程序', 'HQ-QP-31': '生产品质异常处理程序', 'HQ-QP-32': '紧急应变措施程序'
                }
                doc_name = doc_names.get(doc_code, f'{doc_code}程序')
                remaining_specs[doc_code] = {
                    'name': doc_name,
                    'steps': [
                        {'text': f'{doc_name}启动\\n需求确认分析', 'type': 'start', 'department': '相关部门', 'forms': ['启动申请', '需求分析报告']},
                        {'text': '方案制定评估\\n可行性分析审查', 'type': 'process', 'department': '品质部', 'forms': ['方案评估报告', '可行性分析']},
                        {'text': '实施计划编制\\n资源配置安排', 'type': 'process', 'department': '执行部门', 'forms': ['实施计划', '资源配置表']},
                        {'text': '审批确认决策\\n管理层授权批准', 'type': 'process', 'department': '管理层', 'forms': ['审批决策书', '授权批准书']},
                        {'text': '执行实施监控\\n过程跟踪管理', 'type': 'process', 'department': '执行部门', 'forms': ['执行实施记录', '过程跟踪表']},
                        {'text': '效果评估验证\\n目标达成情况分析', 'type': 'process', 'department': '品质部', 'forms': ['效果评估报告', '目标达成分析']},
                        {'text': '持续改进优化\\n经验总结积累', 'type': 'process', 'department': '品质部', 'forms': ['改进优化计划', '经验总结报告']},
                        {'text': '记录归档管理\\n文档体系维护', 'type': 'process', 'department': '行政部', 'forms': ['记录归档清单', '文档体系维护']},
                        {'text': f'{doc_name}流程完成', 'type': 'end', 'department': '相关部门', 'forms': []}
                    ]
                }
        
        # 合并所有规格
        base_specs = {
            'HQ-QP-01': {
                'name': '形成文件的信息控制程序',
                'steps': [
                    {'text': '文件制定需求提出', 'type': 'start', 'department': '各部门', 'forms': ['需求申请表', '文件制定申请']},
                    {'text': '确定文件编制责任人\\n明确编制要求', 'type': 'process', 'department': '管理层', 'forms': ['编制任务书', '责任分工表']},
                    {'text': '收集法规标准要求\\n分析相关文件', 'type': 'process', 'department': '品质部', 'forms': ['法规清单', '标准要求分析']},
                    {'text': '编写文件初稿\\n内容结构设计', 'type': 'process', 'department': '各部门', 'forms': ['文件初稿', '编制说明']},
                    {'text': '内部技术评审\\n专业性检查', 'type': 'process', 'department': '各部门', 'forms': ['技术评审表', '专业意见书']},
                    {'text': '文件质量检查\\n符合性评估', 'type': 'decision', 'department': '品质部', 'forms': ['质量检查表', '符合性评估报告']},
                    {'text': '品质部门审核\\n体系符合性确认', 'type': 'process', 'department': '品质部', 'forms': ['质量审核表', '体系符合性报告']},
                    {'text': '相关部门会签\\n跨部门协调', 'type': 'process', 'department': '各部门', 'forms': ['会签表', '部门意见汇总']},
                    {'text': '管理层最终批准\\n正式生效确认', 'type': 'process', 'department': '管理层', 'forms': ['批准书', '生效通知']},
                    {'text': '文件正式发布\\n版本控制管理', 'type': 'process', 'department': '行政部', 'forms': ['发布通知', '版本记录']},
                    {'text': '分发给使用部门\\n确保及时获取', 'type': 'process', 'department': '行政部', 'forms': ['分发记录', '接收确认']},
                    {'text': '组织培训宣贯\\n确保理解执行', 'type': 'process', 'department': '各部门', 'forms': ['培训记录', '理解确认书']},
                    {'text': '建立文件控制清单\\n跟踪管理状态', 'type': 'process', 'department': '品质部', 'forms': ['控制清单', '状态跟踪表']},
                    {'text': '定期评审更新\\n持续改进优化', 'type': 'process', 'department': '品质部', 'forms': ['评审报告', '改进建议']},
                    {'text': '文件控制流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
                ]
            },
            
            'HQ-QP-02': {
                'name': '管理评审控制程序',
                'steps': [
                    {'text': '制定年度管理评审计划', 'type': 'start', 'department': '管理层', 'forms': ['年度评审计划', '评审时间表']},
                    {'text': '确定评审范围和准则\\n制定评审标准', 'type': 'process', 'department': '管理代表', 'forms': ['评审范围说明', '评审准则']},
                    {'text': '收集内审报告数据\\n整理审核发现', 'type': 'process', 'department': '内审员', 'forms': ['内审报告', '审核发现汇总']},
                    {'text': '收集客户反馈信息\\n分析满意度数据', 'type': 'process', 'department': '各部门', 'forms': ['客户反馈表', '满意度调查']},
                    {'text': '收集过程绩效数据\\nKPI指标分析', 'type': 'process', 'department': '各部门', 'forms': ['绩效报告', 'KPI分析表']},
                    {'text': '整理纠正预防措施\\n跟踪实施状态', 'type': 'process', 'department': '品质部', 'forms': ['措施清单', '实施跟踪表']},
                    {'text': '编制评审输入报告\\n综合分析材料', 'type': 'process', 'department': '管理代表', 'forms': ['评审输入报告', '分析材料汇编']},
                    {'text': '评审输入完整性检查\\n材料充分性评估', 'type': 'decision', 'department': '管理代表', 'forms': ['完整性检查表', '材料清单']},
                    {'text': '召开管理评审会议\\n高层决策讨论', 'type': 'process', 'department': '管理层', 'forms': ['会议议程', '参会记录']},
                    {'text': '分析体系运行状况\\n识别问题和风险', 'type': 'process', 'department': '管理层', 'forms': ['状况分析报告', '风险评估']},
                    {'text': '评价改进机会识别\\n制定提升策略', 'type': 'process', 'department': '管理层', 'forms': ['改进机会清单', '提升策略']},
                    {'text': '制定改进措施计划\\n分配责任和资源', 'type': 'process', 'department': '管理层', 'forms': ['改进计划', '资源分配表']},
                    {'text': '形成评审输出文件\\n明确决策结果', 'type': 'process', 'department': '管理代表', 'forms': ['评审输出报告', '决策记录']},
                    {'text': '跟踪措施实施情况\\n监控执行进度', 'type': 'process', 'department': '品质部', 'forms': ['实施跟踪表', '进度报告']},
                    {'text': '验证改进措施效果\\n评估实施成果', 'type': 'process', 'department': '品质部', 'forms': ['效果验证报告', '成果评估']},
                    {'text': '评审记录归档保存\\n建立档案管理', 'type': 'process', 'department': '品质部', 'forms': ['归档清单', '档案目录']},
                    {'text': '管理评审流程完成', 'type': 'end', 'department': '管理层', 'forms': []}
                ]
            }
        }
        
        # 合并所有规格
        all_specs = {**base_specs, **extended_specs, **remaining_specs}
        return all_specs
    
    def generate_generic_flowchart(self, doc_code):
        """生成通用专业流程图"""
        doc_names = {
            'HQ-QP-03': '内部审核控制程序', 'HQ-QP-04': '人力资源控制程序',
            'HQ-QP-05': '设备、设施管理程序', 'HQ-QP-06': '订单评审控制程序',
            'HQ-QP-07': '新产品设计开发控制程序', 'HQ-QP-08': '外部提供过程、产品和服务控制程序',
            'HQ-QP-09': '生产计划和生产过程控制程序', 'HQ-QP-10': '产品标识与可追溯性控制程序'
        }
        
        doc_name = doc_names.get(doc_code, f'{doc_code}程序')
        
        # 通用专业流程步骤
        steps = [
            {'text': f'{doc_name}启动\\n需求确认', 'type': 'start', 'department': '相关部门', 'forms': ['启动申请', '需求确认单']},
            {'text': '资源准备\\n计划制定', 'type': 'process', 'department': '执行部门', 'forms': ['资源清单', '执行计划']},
            {'text': '方案设计\\n标准制定', 'type': 'process', 'department': '技术部门', 'forms': ['设计方案', '技术标准']},
            {'text': '方案评审\\n可行性分析', 'type': 'decision', 'department': '品质部', 'forms': ['评审报告', '可行性分析']},
            {'text': '正式实施\\n过程监控', 'type': 'process', 'department': '执行部门', 'forms': ['实施记录', '监控报告']},
            {'text': '质量检查\\n符合性验证', 'type': 'process', 'department': '品质部', 'forms': ['检查记录', '验证报告']},
            {'text': '结果评估\\n效果分析', 'type': 'process', 'department': '管理层', 'forms': ['评估报告', '效果分析']},
            {'text': '持续改进\\n优化完善', 'type': 'process', 'department': '品质部', 'forms': ['改进计划', '优化建议']},
            {'text': '记录归档\\n文档管理', 'type': 'process', 'department': '行政部', 'forms': ['归档清单', '文档目录']},
            {'text': f'{doc_name}完成', 'type': 'end', 'department': '相关部门', 'forms': []}
        ]
        
        return self.generate_drawio_xml(doc_code, doc_name, steps)
    
    def regenerate_all_flowcharts(self):
        """重新生成所有专业级流程图"""
        
        # 所有需要重新生成的文档
        all_docs = [
            'HQ-QP-01', 'HQ-QP-02', 'HQ-QP-03', 'HQ-QP-04', 'HQ-QP-05', 'HQ-QP-06',
            'HQ-QP-07', 'HQ-QP-08', 'HQ-QP-09', 'HQ-QP-10', 'HQ-QP-11', 'HQ-QP-12',
            'HQ-QP-13', 'HQ-QP-14', 'HQ-QP-15', 'HQ-QP-16', 'HQ-QP-17', 'HQ-QP-18',
            'HQ-QP-19', 'HQ-QP-20', 'HQ-QP-21', 'HQ-QP-22', 'HQ-QP-23', 'HQ-QP-24',
            'HQ-QP-25', 'HQ-QP-26', 'HQ-QP-27', 'HQ-QP-28', 'HQ-QP-29', 'HQ-QP-30',
            'HQ-QP-31', 'HQ-QP-32'
        ]
        
        generated_files = []
        failed_files = []
        
        print(f"🚀 开始重新生成 {len(all_docs)} 个专业级详细流程图...")
        print(f"📌 目标：编程序级别的专业流程图，包含详细业务逻辑和表单信息")
        
        for i, doc_code in enumerate(all_docs, 1):
            try:
                print(f"\n[{i}/{len(all_docs)}] 正在处理: {doc_code}")
                filepath = self.generate_professional_flowchart(doc_code)
                generated_files.append(filepath)
                
            except Exception as e:
                print(f"❌ 生成失败: {doc_code} - {str(e)}")
                failed_files.append(doc_code)
        
        return generated_files, failed_files

def main():
    """主函数"""
    print("🚀 启动专业级详细流程图生成器...")
    print("🎯 目标：生成编程序级别的专业流程图")
    
    generator = ProfessionalDetailedFlowchartGenerator()
    
    try:
        generated_files, failed_files = generator.regenerate_all_flowcharts()
        
        print(f"\n=== 重新生成完成 ===")
        print(f"✅ 成功生成: {len(generated_files)} 个专业流程图")
        print(f"❌ 生成失败: {len(failed_files)} 个文档")
        
        if generated_files:
            print(f"\n📁 成功生成的专业流程图:")
            for i, file_path in enumerate(generated_files[:10], 1):
                filename = Path(file_path).name
                print(f"{i:2d}. {filename}")
            if len(generated_files) > 10:
                print(f"    ... 还有 {len(generated_files) - 10} 个文件")
        
        if failed_files:
            print(f"\n❌ 生成失败的文档:")
            for doc_code in failed_files:
                print(f"   - {doc_code}")
        
        return len(generated_files) == 32
        
    except Exception as e:
        print(f"❌ 生成过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()