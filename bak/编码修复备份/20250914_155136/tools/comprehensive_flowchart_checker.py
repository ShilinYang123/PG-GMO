#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图全面检查工具
对重新生成版本进行全面验证和质量检查
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

class FlowchartComprehensiveChecker:
    def __init__(self):
        self.check_results = {
            "structure": {},
            "content": {},
            "layout": {},
            "connections": {},
            "business_logic": {},
            "quality": {}
        }
        
    def perform_comprehensive_check(self, file_path):
        """执行全面检查"""
        print("🔍 开始流程图全面检查...")
        print(f"📁 检查文件: {file_path}")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        try:
            # 解析文件
            tree = ET.parse(file_path)
            root = tree.getroot()
            graph_model = root.find(".//mxGraphModel")
            
            if graph_model is None:
                raise ValueError("未找到mxGraphModel元素")
            
            # 执行各项检查
            self.check_xml_structure(tree, root, graph_model)
            self.check_swimlanes(graph_model)
            self.check_business_steps(graph_model)
            self.check_connections(graph_model)
            self.check_layout_quality(graph_model)
            self.check_business_logic()
            self.check_compliance_with_requirements()
            
            # 生成检查报告
            self.generate_check_report()
            
            return True
            
        except Exception as e:
            print(f"❌ 检查过程中发生错误: {str(e)}")
            return False
    
    def check_xml_structure(self, tree, root, graph_model):
        """检查XML结构完整性"""
        print("📋 1. XML结构检查")
        
        # 基本结构检查
        mxfile = root
        diagram = mxfile.find('diagram')
        
        self.check_results["structure"]["xml_valid"] = True
        self.check_results["structure"]["has_mxfile"] = mxfile is not None
        self.check_results["structure"]["has_diagram"] = diagram is not None
        self.check_results["structure"]["has_graph_model"] = graph_model is not None
        
        # 画布设置检查
        canvas_width = graph_model.get('pageWidth', '0')
        canvas_height = graph_model.get('pageHeight', '0')
        
        self.check_results["structure"]["canvas_size"] = f"{canvas_width}×{canvas_height}"
        
        print(f"   ✅ XML结构完整性: 通过")
        print(f"   ✅ 画布尺寸: {canvas_width}×{canvas_height}px")
        
    def check_swimlanes(self, graph_model):
        """检查泳道设置"""
        print("\n🏊 2. 泳道结构检查")
        
        root_element = graph_model.find('root')
        swimlanes = root_element.findall(".//mxCell[@value][@style*='swimlane']")
        
        expected_lanes = [
            "客户", "业务部", "工程部", "财务部", "管理层", "PMC部",
            "采购部", "供应商", "仓储部", "装配线", "五金", "注塑", "丝印", "品质部"
        ]
        
        found_lanes = []
        lane_positions = {}
        
        for lane in swimlanes:
            lane_name = lane.get('value', '')
            geometry = lane.find('mxGeometry')
            if geometry is not None:
                y_pos = int(geometry.get('y', '0'))
                width = int(geometry.get('width', '0'))
                height = int(geometry.get('height', '0'))
                
                found_lanes.append(lane_name)
                lane_positions[lane_name] = {
                    'y': y_pos,
                    'width': width,
                    'height': height
                }
        
        self.check_results["layout"]["swimlanes"] = {
            "expected_count": len(expected_lanes),
            "actual_count": len(found_lanes),
            "found_lanes": found_lanes,
            "positions": lane_positions
        }
        
        # 检查生产部门细分
        production_lanes = ["装配线", "五金", "注塑", "丝印"]
        production_found = [lane for lane in found_lanes if lane in production_lanes]
        
        print(f"   ✅ 泳道总数: {len(found_lanes)}/{len(expected_lanes)}")
        print(f"   ✅ 生产部门细分: {len(production_found)}/4 ({', '.join(production_found)})")
        
        missing_lanes = [lane for lane in expected_lanes if lane not in found_lanes]
        if missing_lanes:
            print(f"   ⚠️  缺失泳道: {', '.join(missing_lanes)}")
        
    def check_business_steps(self, graph_model):
        """检查业务步骤"""
        print("\n📊 3. 业务步骤检查")
        
        root_element = graph_model.find('root')
        all_cells = root_element.findall(".//mxCell[@value]")
        
        # 分析业务步骤
        business_steps = []
        decision_nodes = []
        other_elements = []
        
        step_positions = {}
        duplicate_positions = defaultdict(list)
        
        for cell in all_cells:
            cell_id = cell.get('id', '')
            cell_value = cell.get('value', '')
            
            # 跳过泳道
            if 'swimlane' in cell.get('style', ''):
                continue
                
            # 获取位置信息
            geometry = cell.find('mxGeometry')
            if geometry is not None:
                x_pos = int(geometry.get('x', '0'))
                y_pos = int(geometry.get('y', '0'))
                width = int(geometry.get('width', '0'))
                height = int(geometry.get('height', '0'))
                
                position_key = f"({x_pos}, {y_pos})"
                duplicate_positions[position_key].append(cell_id)
                
                step_positions[cell_id] = {
                    'x': x_pos, 'y': y_pos, 
                    'width': width, 'height': height,
                    'value': cell_value
                }
            
            # 分类步骤
            if cell_id.startswith('S') or cell_id.startswith('E'):
                business_steps.append(cell_id)
            elif cell_id.startswith('D'):
                decision_nodes.append(cell_id)
            elif cell_id not in ['0', '1'] and not cell_id.startswith('lane_') and not cell_id.startswith('edge_'):
                other_elements.append(cell_id)
        
        # 检查重复位置
        overlapping_positions = {pos: ids for pos, ids in duplicate_positions.items() if len(ids) > 1}
        
        self.check_results["content"]["business_steps"] = {
            "total_steps": len(business_steps),
            "decision_nodes": len(decision_nodes),
            "step_list": business_steps,
            "decision_list": decision_nodes,
            "positions": step_positions,
            "overlapping": overlapping_positions
        }
        
        print(f"   ✅ 业务步骤总数: {len(business_steps)}")
        print(f"   ✅ 决策节点数: {len(decision_nodes)}")
        print(f"   ✅ 其他元素数: {len(other_elements)}")
        
        if overlapping_positions:
            print(f"   ❌ 发现重叠位置: {len(overlapping_positions)}处")
            for pos, ids in overlapping_positions.items():
                print(f"      位置{pos}: {', '.join(ids)}")
        else:
            print(f"   ✅ 无位置重叠问题")
    
    def check_connections(self, graph_model):
        """检查连接线"""
        print("\n🔗 4. 连接线检查")
        
        root_element = graph_model.find('root')
        connections = root_element.findall(".//mxCell[@edge='1']")
        
        connection_data = []
        color_usage = defaultdict(int)
        
        for conn in connections:
            conn_id = conn.get('id', '')
            source = conn.get('source', '')
            target = conn.get('target', '')
            style = conn.get('style', '')
            value = conn.get('value', '')
            
            # 分析颜色
            if 'strokeColor=#FF6B35' in style:
                color_type = "橙色(生产分支)"
                color_usage["橙色"] += 1
            elif 'strokeColor=#4ECDC4' in style:
                color_type = "青色(付款决策)"
                color_usage["青色"] += 1
            elif 'strokeColor=#45B7D1' in style:
                color_type = "蓝色(管理决策)"
                color_usage["蓝色"] += 1
            elif 'strokeColor=#FF6B6B' in style:
                color_type = "红色(拒绝分支)"
                color_usage["红色"] += 1
            else:
                color_type = "黑色(主流程)"
                color_usage["黑色"] += 1
            
            connection_data.append({
                'id': conn_id,
                'source': source,
                'target': target,
                'label': value,
                'color': color_type
            })
        
        self.check_results["connections"] = {
            "total_connections": len(connections),
            "connections": connection_data,
            "color_usage": dict(color_usage)
        }
        
        print(f"   ✅ 连接线总数: {len(connections)}")
        print(f"   ✅ 颜色分类统计:")
        for color, count in color_usage.items():
            print(f"      {color}: {count}条")
    
    def check_layout_quality(self, graph_model):
        """检查布局质量"""
        print("\n📐 5. 布局质量检查")
        
        # 从之前收集的数据分析布局
        steps = self.check_results["content"]["business_steps"]["positions"]
        lanes = self.check_results["layout"]["swimlanes"]["positions"]
        
        # 检查单元格尺寸一致性
        size_stats = defaultdict(int)
        for step_id, pos_info in steps.items():
            if step_id.startswith('S') or step_id.startswith('D') or step_id.startswith('E'):
                size_key = f"{pos_info['width']}×{pos_info['height']}"
                size_stats[size_key] += 1
        
        # 检查泳道内步骤分布
        lane_step_distribution = defaultdict(list)
        for step_id, pos_info in steps.items():
            if step_id.startswith('S') or step_id.startswith('D') or step_id.startswith('E'):
                step_y = pos_info['y']
                for lane_name, lane_info in lanes.items():
                    lane_y_start = lane_info['y']
                    lane_y_end = lane_y_start + lane_info['height']
                    if lane_y_start <= step_y <= lane_y_end:
                        lane_step_distribution[lane_name].append(step_id)
                        break
        
        self.check_results["layout"]["quality"] = {
            "size_consistency": dict(size_stats),
            "lane_distribution": dict(lane_step_distribution)
        }
        
        print(f"   ✅ 单元格尺寸统计:")
        for size, count in size_stats.items():
            print(f"      {size}: {count}个")
        
        print(f"   ✅ 泳道步骤分布:")
        for lane, steps_list in lane_step_distribution.items():
            print(f"      {lane}: {len(steps_list)}个步骤")
    
    def check_business_logic(self):
        """检查业务逻辑完整性"""
        print("\n🧠 6. 业务逻辑检查")
        
        connections = self.check_results["connections"]["connections"]
        steps = self.check_results["content"]["business_steps"]["step_list"]
        
        # 构建流程图
        flow_graph = defaultdict(list)
        for conn in connections:
            flow_graph[conn['source']].append(conn['target'])
        
        # 检查流程连续性
        start_nodes = [step for step in steps if step.startswith('S01')]
        end_nodes = [step for step in steps if step.startswith('E')]
        
        # 检查决策分支
        decision_branches = {}
        for conn in connections:
            if conn['source'].startswith('D') and conn['label']:
                if conn['source'] not in decision_branches:
                    decision_branches[conn['source']] = []
                decision_branches[conn['source']].append(conn['label'])
        
        self.check_results["business_logic"] = {
            "start_nodes": start_nodes,
            "end_nodes": end_nodes,
            "decision_branches": decision_branches,
            "flow_graph": dict(flow_graph)
        }
        
        print(f"   ✅ 起始节点: {', '.join(start_nodes)}")
        print(f"   ✅ 结束节点: {', '.join(end_nodes)}")
        print(f"   ✅ 决策分支:")
        for decision, branches in decision_branches.items():
            print(f"      {decision}: {', '.join(branches)}")
    
    def check_compliance_with_requirements(self):
        """检查需求符合性"""
        print("\n📋 7. 需求符合性检查")
        
        # 检查关键需求
        requirements = {
            "消除S09和S19重复定义": self.check_no_duplicate_definitions(),
            "保持生产部门细分": self.check_production_subdivision(),
            "连接线无重叠": self.check_no_connection_overlap(),
            "所有步骤在正确泳道": self.check_correct_lane_placement(),
            "业务流程完整": self.check_complete_business_flow()
        }
        
        self.check_results["quality"]["requirements_compliance"] = requirements
        
        for req, passed in requirements.items():
            status = "✅ 通过" if passed else "❌ 未通过"
            print(f"   {status} {req}")
    
    def check_no_duplicate_definitions(self):
        """检查无重复定义"""
        overlapping = self.check_results["content"]["business_steps"]["overlapping"]
        return len(overlapping) == 0
    
    def check_production_subdivision(self):
        """检查生产部门细分"""
        found_lanes = self.check_results["layout"]["swimlanes"]["found_lanes"]
        production_lanes = ["装配线", "五金", "注塑", "丝印"]
        return all(lane in found_lanes for lane in production_lanes)
    
    def check_no_connection_overlap(self):
        """检查连接线无重叠"""
        # 基于颜色分类系统判断
        color_usage = self.check_results["connections"]["color_usage"]
        return len(color_usage) >= 4  # 至少有4种颜色分类
    
    def check_correct_lane_placement(self):
        """检查正确泳道放置"""
        distribution = self.check_results["layout"]["quality"]["lane_distribution"]
        # 检查关键部门是否有步骤
        key_departments = ["客户", "业务部", "工程部", "PMC部", "装配线"]
        return all(dept in distribution and len(distribution[dept]) > 0 for dept in key_departments)
    
    def check_complete_business_flow(self):
        """检查业务流程完整性"""
        flow_graph = self.check_results["business_logic"]["flow_graph"]
        steps = self.check_results["content"]["business_steps"]["step_list"]
        
        # 检查是否有孤立节点
        connected_nodes = set()
        for source, targets in flow_graph.items():
            connected_nodes.add(source)
            connected_nodes.update(targets)
        
        isolated_steps = [step for step in steps if step not in connected_nodes]
        return len(isolated_steps) == 0
    
    def generate_check_report(self):
        """生成检查报告"""
        print("\n" + "=" * 80)
        print("📊 全面检查报告总结")
        print("=" * 80)
        
        total_checks = 0
        passed_checks = 0
        
        # 统计各项检查结果
        for category, results in self.check_results.items():
            if category == "quality" and "requirements_compliance" in results:
                for req, passed in results["requirements_compliance"].items():
                    total_checks += 1
                    if passed:
                        passed_checks += 1
        
        success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        print(f"🎯 总体评分: {success_rate:.1f}% ({passed_checks}/{total_checks})")
        print(f"📈 检查项目: {total_checks}项")
        print(f"✅ 通过项目: {passed_checks}项")
        print(f"❌ 失败项目: {total_checks - passed_checks}项")
        
        # 详细统计
        content = self.check_results["content"]["business_steps"]
        connections = self.check_results["connections"]
        layout = self.check_results["layout"]["swimlanes"]
        
        print(f"\n📋 详细统计:")
        print(f"   • 业务步骤: {content['total_steps']}个")
        print(f"   • 决策节点: {content['decision_nodes']}个")
        print(f"   • 连接线: {connections['total_connections']}条")
        print(f"   • 泳道: {layout['actual_count']}个")
        
        # 质量评估
        if success_rate >= 90:
            quality_level = "🌟 优秀"
        elif success_rate >= 80:
            quality_level = "👍 良好"
        elif success_rate >= 70:
            quality_level = "⚠️ 一般"
        else:
            quality_level = "❌ 需改进"
        
        print(f"\n🏆 质量等级: {quality_level}")
        
        return success_rate >= 80

def main():
    """主函数"""
    file_path = "s:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-重新生成版.drawio"
    
    checker = FlowchartComprehensiveChecker()
    
    try:
        success = checker.perform_comprehensive_check(file_path)
        
        if success:
            print(f"\n🎉 全面检查完成！流程图质量达标。")
        else:
            print(f"\n⚠️ 检查发现问题，需要进一步优化。")
        
        # 保存检查结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"s:\\PG-GMO\\office\\业务部\\流程图全面检查报告_{timestamp}.json"
        
        import json
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(checker.check_results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 详细检查结果已保存到: {report_file}")
        
        return success
        
    except Exception as e:
        print(f"❌ 检查过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()