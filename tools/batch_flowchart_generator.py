#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量ISO流程图生成器
基于详细流程图生成器，为所有ISO文档批量生成流程图
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

class BatchFlowchartGenerator:
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
            '工程部': '#82E0AA'
        }
        
        # 动态检查已生成的文档列表
        self.generated_docs = self.get_already_generated_docs()
        
    def get_already_generated_docs(self):
        """获取已生成的文档列表"""
        generated_docs = []
        if self.output_dir.exists():
            for flowchart_file in self.output_dir.glob('*.drawio'):
                # 从流程图文件名提取原始文档名
                filename = flowchart_file.stem
                # 如果文件名包含'流程图'，则移除它
                if '流程图' in filename:
                    doc_name = filename.replace('流程图', '') + '.doc'
                else:
                    # 对于没有'流程图'后缀的文件，直接添加.doc
                    doc_name = filename + '.doc'
                
                if 'HQ-QP-' in doc_name:
                    generated_docs.append(doc_name)
                    print(f"已生成的文档: {doc_name}")
        return generated_docs
        
    def get_suitable_documents(self):
        """直接从输入目录扫描所有适合生成流程图的文档"""
        suitable_docs = []
        
        # 直接扫描输入目录
        if self.input_dir.exists():
            # 扫描所有子目录中的.doc文件
            for item in self.input_dir.iterdir():
                if item.is_dir():
                    # 在子目录中查找.doc文件
                    for doc_file in item.glob('*.doc'):
                        if 'HQ-QP-' in doc_file.name:
                            suitable_docs.append(doc_file.name)
                elif item.is_file() and item.suffix == '.doc' and 'HQ-QP-' in item.name:
                    suitable_docs.append(item.name)
        
        # 排除已生成的文档
        remaining_docs = [doc for doc in suitable_docs if doc not in self.generated_docs]
        return remaining_docs
    
    def create_document_based_flowchart(self, doc_name):
        """基于文档内容创建流程图"""
        try:
            # 对于HQ-QP-09，使用详细流程图生成器
            if 'HQ-QP-09' in doc_name:
                print(f"正在为 {doc_name} 使用详细流程图生成器...")
                from detailed_flowchart_generator import DetailedFlowchartGenerator
                detailed_generator = DetailedFlowchartGenerator()
                result = detailed_generator.generate_hq_qp_09_flowchart()
                print(f"详细流程图生成器返回结果: {result}")
                return result
            else:
                # 对于其他文档，基于内容生成
                return self.analyze_and_generate_flowchart(doc_name)
                
        except Exception as e:
            import traceback
            print(f"基于文档内容生成失败: {e}")
            print(f"错误详情: {traceback.format_exc()}")
            print("使用通用模板")
            return self.create_generic_flowchart(doc_name)
    
    def analyze_and_generate_flowchart(self, doc_name):
        """分析文档内容并生成对应流程图"""
        try:
            # 导入文档读取器
            from office_document_reader import OfficeDocumentReader
            
            # 查找对应的文档文件
            doc_path = self.find_document_path(doc_name)
            if not doc_path:
                print(f"找不到文档: {doc_name}，使用通用模板")
                return self.create_generic_flowchart(doc_name)
            
            # 读取文档内容
            reader = OfficeDocumentReader()
            content = reader.read_document(doc_path)
            
            if not content:
                print(f"无法读取文档内容: {doc_name}，使用通用模板")
                return self.create_generic_flowchart(doc_name)
            
            # 分析文档内容，提取流程步骤
            steps = self.extract_process_steps_from_content(content, doc_name)
            
            # 基于提取的步骤生成流程图
            return self.generate_drawio_xml(doc_name, steps)
            
        except Exception as e:
            print(f"文档分析失败: {str(e)}，使用通用模板")
            return self.create_generic_flowchart(doc_name)
    
    def find_document_path(self, doc_name):
        """查找文档路径"""
        base_dir = "S:\\PG-GMO\\01-Input\\原始文档\\PG-ISO文件"
        
        # 提取文档编号
        doc_code = doc_name.split(' ')[0] if ' ' in doc_name else doc_name
        
        # 搜索对应的文档目录
        for root, dirs, files in os.walk(base_dir):
            if doc_code in root:
                for file in files:
                    if file.endswith(('.doc', '.docx')) and doc_code in file:
                        return os.path.join(root, file)
        return None
    
    def extract_process_steps_from_content(self, content, doc_name):
        """从文档内容中提取流程步骤"""
        # 基础流程步骤模板
        steps = [
            {'id': 'start', 'text': '流程开始', 'type': 'start', 'dept': '相关部门'},
            {'id': 'input', 'text': '输入准备', 'type': 'process', 'dept': '相关部门'},
            {'id': 'review', 'text': '初步审核', 'type': 'process', 'dept': '品质部'},
            {'id': 'decision', 'text': '是否符合要求？', 'type': 'decision', 'dept': '品质部'},
            {'id': 'approve', 'text': '审批确认', 'type': 'process', 'dept': '管理层'},
            {'id': 'execute', 'text': '执行操作', 'type': 'process', 'dept': '执行部门'},
            {'id': 'monitor', 'text': '过程监控', 'type': 'process', 'dept': '品质部'},
            {'id': 'record', 'text': '记录归档', 'type': 'process', 'dept': '相关部门'},
            {'id': 'end', 'text': '流程结束', 'type': 'end', 'dept': '相关部门'}
        ]
        
        # 根据文档内容和名称调整流程步骤
        if content and 'paragraphs' in content:
            paragraphs = content['paragraphs']
            
            # 分析文档内容，寻找关键词和流程描述
            content_text = ' '.join(paragraphs).lower()
            
            # 尝试从文档中提取实际的流程步骤
            extracted_steps = self.parse_process_steps_from_text(paragraphs, doc_name)
            if extracted_steps:
                return extracted_steps
            
            # 如果无法提取具体步骤，根据文档类型调整模板
            self.customize_steps_by_document_type(steps, doc_name, content_text)
        else:
            # 如果没有内容，根据文档名称调整
            process_name = doc_name.replace('.doc', '')
            if '采购' in process_name:
                steps[1]['text'] = '采购需求确认'
                steps[1]['dept'] = '采购部'
                steps[5]['text'] = '供应商选择与采购'
                steps[5]['dept'] = '采购部'
            elif '设计' in process_name or '开发' in process_name:
                steps[1]['text'] = '设计开发输入'
                steps[1]['dept'] = '研发部'
                steps[5]['text'] = '设计开发实施'
                steps[5]['dept'] = '研发部'
            elif '生产' in process_name:
                steps[1]['text'] = '生产计划制定'
                steps[1]['dept'] = '生产部'
                steps[5]['text'] = '生产执行'
                steps[5]['dept'] = '生产部'
            elif '检验' in process_name or '测量' in process_name:
                steps[1]['text'] = '检验测量准备'
                steps[1]['dept'] = '品质部'
                steps[5]['text'] = '检验测量执行'
                steps[5]['dept'] = '品质部'
            elif '客户' in process_name or '顾客' in process_name:
                steps[1]['text'] = '客户需求接收'
                steps[1]['dept'] = '业务部'
                steps[5]['text'] = '客户服务执行'
                steps[5]['dept'] = '业务部'
        
        return steps
    
    def parse_process_steps_from_text(self, paragraphs, doc_name):
        """从文档文本中解析实际的流程步骤"""
        steps = []
        step_keywords = ['步骤', '流程', '程序', '过程', '阶段', '环节']
        
        # 确保paragraphs是列表
        if isinstance(paragraphs, str):
            paragraphs = [paragraphs]
        elif not isinstance(paragraphs, list):
            return None
        
        # 查找包含流程步骤的段落
        for i, paragraph in enumerate(paragraphs):
            if not isinstance(paragraph, str):
                continue
                
            text = paragraph.strip()
            if not text:
                continue
                
            # 检查是否包含步骤关键词
            if any(keyword in text for keyword in step_keywords):
                # 尝试提取步骤信息
                if '：' in text or ':' in text:
                    parts = text.split('：') if '：' in text else text.split(':')
                    if len(parts) >= 2:
                        step_text = parts[1].strip()
                        if step_text and len(step_text) > 3:
                            step_id = f'step_{len(steps) + 1}'
                            dept = self.identify_department_from_text(step_text)
                            step_type = self.identify_step_type(step_text)
                            
                            steps.append({
                                'id': step_id,
                                'text': step_text[:30] + ('...' if len(step_text) > 30 else ''),
                                'type': step_type,
                                'dept': dept
                            })
        
        # 如果找到了步骤，添加开始和结束节点
        if steps:
            steps.insert(0, {'id': 'start', 'text': '流程开始', 'type': 'start', 'dept': '相关部门'})
            steps.append({'id': 'end', 'text': '流程结束', 'type': 'end', 'dept': '相关部门'})
            return steps
        
        return None
    
    def identify_department_from_text(self, text):
        """从文本中识别部门"""
        dept_keywords = {
            '研发部': ['设计', '开发', '研发', '技术'],
            '品质部': ['质量', '检验', '审核', '品质', '测试'],
            '生产部': ['生产', '制造', '加工'],
            '采购部': ['采购', '供应商', '物料'],
            '业务部': ['销售', '客户', '订单', '市场'],
            '管理层': ['审批', '决策', '管理', '领导']
        }
        
        text_lower = text.lower()
        for dept, keywords in dept_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return dept
        
        return '相关部门'
    
    def identify_step_type(self, text):
        """识别步骤类型"""
        if '？' in text or '?' in text or '是否' in text:
            return 'decision'
        elif '开始' in text:
            return 'start'
        elif '结束' in text or '完成' in text:
            return 'end'
        else:
            return 'process'
    
    def customize_steps_by_document_type(self, steps, doc_name, content_text):
        """根据文档类型定制步骤"""
        if '设计开发' in doc_name:
            steps[1]['text'] = '设计开发输入'
            steps[1]['dept'] = '研发部'
            steps[5]['text'] = '设计开发实施'
            steps[5]['dept'] = '研发部'
        elif '采购' in doc_name:
            steps[1]['text'] = '采购申请'
            steps[1]['dept'] = '采购部'
            steps[5]['text'] = '采购执行'
            steps[5]['dept'] = '采购部'
        elif '生产' in doc_name:
            steps[1]['text'] = '生产计划'
            steps[1]['dept'] = '生产部'
            steps[5]['text'] = '生产执行'
            steps[5]['dept'] = '生产部'
        elif '审核' in doc_name:
            steps[1]['text'] = '审核准备'
            steps[1]['dept'] = '品质部'
            steps[5]['text'] = '审核实施'
            steps[5]['dept'] = '品质部'
        elif '管理评审' in doc_name:
            steps[1]['text'] = '评审准备'
            steps[1]['dept'] = '管理层'
            steps[5]['text'] = '评审实施'
            steps[5]['dept'] = '管理层'
    
    def create_generic_flowchart(self, doc_name):
        """为指定文档创建通用流程图（备用方法）"""
        # 根据文档名称推断流程类型和步骤
        process_name = doc_name.replace('.doc', '')
        
        # 通用ISO流程步骤
        steps = [
            {'id': 'start', 'text': '流程开始', 'type': 'start', 'dept': '相关部门'},
            {'id': 'input', 'text': '接收输入/申请', 'type': 'process', 'dept': '执行部门'},
            {'id': 'review', 'text': '初步审核', 'type': 'process', 'dept': '品质部'},
            {'id': 'decision1', 'text': '是否符合要求？', 'type': 'decision', 'dept': '品质部'},
            {'id': 'approve', 'text': '审批确认', 'type': 'process', 'dept': '管理层'},
            {'id': 'execute', 'text': '执行操作', 'type': 'process', 'dept': '执行部门'},
            {'id': 'monitor', 'text': '过程监控', 'type': 'process', 'dept': '品质部'},
            {'id': 'record', 'text': '记录归档', 'type': 'process', 'dept': '相关部门'},
            {'id': 'end', 'text': '流程结束', 'type': 'end', 'dept': '相关部门'}
        ]
        
        # 根据文档类型调整流程步骤
        if '采购' in process_name:
            steps[1]['text'] = '采购需求确认'
            steps[1]['dept'] = '采购部'
            steps[5]['text'] = '供应商选择与采购'
            steps[5]['dept'] = '采购部'
        elif '设计' in process_name or '开发' in process_name:
            steps[1]['text'] = '设计开发输入'
            steps[1]['dept'] = '研发部'
            steps[5]['text'] = '设计开发实施'
            steps[5]['dept'] = '研发部'
        elif '生产' in process_name:
            steps[1]['text'] = '生产计划制定'
            steps[1]['dept'] = '生产部'
            steps[5]['text'] = '生产执行'
            steps[5]['dept'] = '生产部'
        elif '检验' in process_name or '测量' in process_name:
            steps[1]['text'] = '检验测量准备'
            steps[1]['dept'] = '品质部'
            steps[5]['text'] = '检验测量执行'
            steps[5]['dept'] = '品质部'
        elif '客户' in process_name or '顾客' in process_name:
            steps[1]['text'] = '客户需求接收'
            steps[1]['dept'] = '业务部'
            steps[5]['text'] = '客户服务执行'
            steps[5]['dept'] = '业务部'
        
        return self.generate_drawio_xml(process_name, steps)
    
    def generate_drawio_xml(self, process_name, steps):
        """生成Draw.io格式的XML"""
        # 创建根元素
        mxfile = ET.Element('mxfile', host="app.diagrams.net", modified=datetime.now().isoformat(), agent="5.0", version="24.7.17")
        diagram = ET.SubElement(mxfile, 'diagram', name="流程图", id="flowchart")
        mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1422", dy="794", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="827", pageHeight="1169", math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, 'root')
        
        # 添加默认层
        ET.SubElement(root, 'mxCell', id="0")
        ET.SubElement(root, 'mxCell', id="1", parent="0")
        
        # 添加标题
        title_cell = ET.SubElement(root, 'mxCell', id="title", value=f"{process_name}流程图", style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;", vertex="1", parent="1")
        title_geom = ET.SubElement(title_cell, 'mxGeometry', x="300", y="20", width="200", height="30", **{"as": "geometry"})
        
        # 计算位置
        start_x = 100
        start_y = 80
        step_height = 80
        
        cell_id = 2
        
        for i, step in enumerate(steps):
            y_pos = start_y + i * step_height
            
            # 确定形状和颜色
            if step['type'] == 'start' or step['type'] == 'end':
                style = f"ellipse;whiteSpace=wrap;html=1;fillColor={self.department_colors.get(step['dept'], '#E8E8E8')};strokeColor=#000000;fontSize=12;"
                width, height = "120", "60"
            elif step['type'] == 'decision':
                style = f"rhombus;whiteSpace=wrap;html=1;fillColor={self.department_colors.get(step['dept'], '#E8E8E8')};strokeColor=#000000;fontSize=12;"
                width, height = "140", "80"
            else:
                style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={self.department_colors.get(step['dept'], '#E8E8E8')};strokeColor=#000000;fontSize=12;"
                width, height = "160", "60"
            
            # 添加步骤单元格
            step_text = f"{step['text']}\n({step['dept']})"
            step_cell = ET.SubElement(root, 'mxCell', id=str(cell_id), value=step_text, style=style, vertex="1", parent="1")
            step_geom = ET.SubElement(step_cell, 'mxGeometry', x=str(start_x), y=str(y_pos), width=width, height=height, **{"as": "geometry"})
            
            # 添加连接线（除了最后一个步骤）
            if i < len(steps) - 1:
                edge_id = cell_id + 100
                edge_cell = ET.SubElement(root, 'mxCell', id=str(edge_id), value="", style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;", edge="1", parent="1", source=str(cell_id), target=str(cell_id + 1))
                edge_geom = ET.SubElement(edge_cell, 'mxGeometry', relative="1", **{"as": "geometry"})
            
            cell_id += 1
        
        # 添加决策分支（如果有决策节点）
        for i, step in enumerate(steps):
            if step['type'] == 'decision':
                # 添加"否"分支回到前面的步骤
                no_edge_id = cell_id + 200
                source_id = str(i + 2)  # 决策节点的ID
                target_id = str(max(1, i))  # 回到前一个步骤
                
                no_edge_cell = ET.SubElement(root, 'mxCell', id=str(no_edge_id), value="否", style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;", edge="1", parent="1", source=source_id, target=target_id)
                no_edge_geom = ET.SubElement(no_edge_cell, 'mxGeometry', relative="1", **{"as": "geometry"})
                
                # 添加"是"标签到下一个步骤的连接线
                if i < len(steps) - 1:
                    yes_edge_id = i + 2 + 100  # 对应的连接线ID
                    # 找到对应的边并添加"是"标签
                    for edge in root.findall(".//mxCell[@id='{}'][@edge='1']".format(yes_edge_id)):
                        edge.set('value', '是')
                break
        
        return mxfile
    
    def save_flowchart(self, xml_element, filename):
        """保存流程图到文件"""
        # 格式化XML
        rough_string = ET.tostring(xml_element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # 移除空行
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        formatted_xml = '\n'.join(lines)
        
        # 保存文件
        output_path = self.output_dir / f"{filename.replace('.doc', '')}.drawio"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_xml)
        
        return output_path
    
    def generate_all_remaining_flowcharts(self):
        """生成所有剩余的流程图"""
        remaining_docs = self.get_suitable_documents()
        
        print(f"杨老师，找到 {len(remaining_docs)} 个需要生成流程图的文档")
        print("开始批量生成流程图...\n")
        
        generated_files = []
        failed_files = []
        
        for i, doc_name in enumerate(remaining_docs, 1):
            try:
                print(f"[{i}/{len(remaining_docs)}] 正在生成: {doc_name}")
                
                # 创建流程图
                result = self.create_document_based_flowchart(doc_name)
                
                # 检查返回结果类型
                if isinstance(result, str):
                    # 如果返回的是文件路径（如detailed_flowchart_generator的情况）
                    output_path = Path(result)
                    generated_files.append(str(output_path))
                    print(f"✅ 成功生成: {output_path.name}")
                else:
                    # 如果返回的是XML元素，使用原有的保存方法
                    output_path = self.save_flowchart(result, doc_name)
                    generated_files.append(str(output_path))
                    print(f"✅ 成功生成: {output_path.name}")
                
            except Exception as e:
                import traceback
                print(f"❌ 生成失败: {doc_name} - {str(e)}")
                print(f"错误详情: {traceback.format_exc()}")
                failed_files.append(doc_name)
        
        return generated_files, failed_files
    
    def generate_summary_report(self, generated_files, failed_files):
        """生成批量生成汇总报告"""
        total_docs = 32  # 总共32个适合的文档
        already_generated = len(self.generated_docs)  # 已生成的数量
        newly_generated = len(generated_files)  # 新生成的数量
        
        report_content = f"""# 品高ISO流程图批量生成汇总报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 生成统计

- **总文档数**: {total_docs} 个
- **已生成**: {already_generated} 个（之前生成）
- **本次新生成**: {newly_generated} 个
- **生成失败**: {len(failed_files)} 个
- **完成进度**: {already_generated + newly_generated}/{total_docs} ({((already_generated + newly_generated) / total_docs * 100):.1f}%)

## 本次新生成的流程图

"""
        
        for i, file_path in enumerate(generated_files, 1):
            filename = Path(file_path).name
            report_content += f"{i}. {filename}\n"
        
        if failed_files:
            report_content += "\n## 生成失败的文档\n\n"
            for i, doc_name in enumerate(failed_files, 1):
                report_content += f"{i}. {doc_name}\n"
        
        report_content += f"""\n## 使用说明

所有流程图文件均为Draw.io格式(.drawio)，可以：

1. 直接在 https://app.diagrams.net 中打开编辑
2. 使用Draw.io桌面版打开
3. 在VS Code中安装Draw.io插件后打开

## 流程图特色

- **部门颜色区分**: 不同部门使用不同颜色标识
- **标准化流程**: 基于ISO质量管理体系标准
- **完整流转**: 包含审核、批准、执行、监控等关键环节
- **可编辑格式**: 支持后续修改和完善

## 输出目录

所有流程图保存在: `{self.output_dir}`

---

**注意**: 本批次生成的流程图为通用模板，建议根据具体文档内容进行细化调整。
"""
        
        report_path = self.output_dir / "批量流程图生成汇总报告.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n📊 汇总报告已生成: {report_path}")
        return report_path

def main():
    input_dir = "S:/PG-GMO/01-Input/原始文档/PG-ISO文件"
    output_dir = "S:/PG-GMO/02-Output/品高ISO流程图"
    
    print("=== 品高ISO流程图批量生成器 ===")
    print(f"输出目录: {output_dir}\n")
    
    generator = BatchFlowchartGenerator(input_dir, output_dir)
    generated_files, failed_files = generator.generate_all_remaining_flowcharts()
    
    print(f"\n=== 批量生成完成 ===")
    print(f"✅ 成功生成: {len(generated_files)} 个流程图")
    print(f"❌ 生成失败: {len(failed_files)} 个文档")
    
    # 生成汇总报告
    report_path = generator.generate_summary_report(generated_files, failed_files)
    
    if generated_files:
        print(f"\n📁 新生成的流程图文件:")
        for i, file_path in enumerate(generated_files[:10], 1):  # 只显示前10个
            filename = Path(file_path).name
            print(f"{i:2d}. {filename}")
        if len(generated_files) > 10:
            print(f"    ... 还有 {len(generated_files) - 10} 个文件")
    
    print(f"\n📊 详细报告: {report_path}")
    print(f"📁 所有文件保存在: {output_dir}")
    
    return generated_files, failed_files

if __name__ == "__main__":
    main()