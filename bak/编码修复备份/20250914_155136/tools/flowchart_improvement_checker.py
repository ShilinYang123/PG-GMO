#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图改进验证工具
验证泳道虚线和连接线布局优化效果
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

class FlowchartImprovementChecker:
    def __init__(self):
        self.improvement_results = {
            "swimlane_dashed": {},
            "connection_optimization": {},
            "path_simplification": {},
            "overlap_reduction": {}
        }
        
    def check_improvements(self, file_path):
        """检查改进效果"""
        print("🔍 开始流程图改进验证...")
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
            
            # 执行各项改进检查
            self.check_swimlane_dash_lines(graph_model)
            self.check_connection_simplification(graph_model)
            self.check_path_optimization(graph_model)
            self.check_overlap_reduction(graph_model)
            
            # 生成改进验证报告
            self.generate_improvement_report()
            
            return True
            
        except Exception as e:
            print(f"❌ 检查过程中发生错误: {str(e)}")
            return False
    
    def check_swimlane_dash_lines(self, graph_model):
        """检查泳道虚线改进"""
        print("🏊 1. 泳道虚线样式检查")
        
        root_element = graph_model.find('root')
        # 改用更精确的查找方式
        swimlanes = []
        for cell in root_element.findall('.//mxCell'):
            style = cell.get('style', '')
            if 'swimlane' in style and cell.get('value'):
                swimlanes.append(cell)
        
        dash_results = {
            "total_lanes": 0,
            "dashed_lanes": 0,
            "lane_details": []
        }
        
        for lane in swimlanes:
            lane_name = lane.get('value', '')
            style = lane.get('style', '')
            
            dash_results["total_lanes"] += 1
            
            # 检查是否有strokeDashArray
            has_dash = 'strokeDashArray=' in style
            if has_dash:
                dash_results["dashed_lanes"] += 1
                
                # 提取虚线参数
                dash_start = style.find('strokeDashArray=') + 16
                dash_end = style.find(';', dash_start)
                if dash_end == -1:
                    dash_end = len(style)
                dash_pattern = style[dash_start:dash_end]
                
                dash_results["lane_details"].append({
                    "name": lane_name,
                    "has_dash": True,
                    "dash_pattern": dash_pattern,
                    "stroke_color": self._extract_stroke_color(style)
                })
            else:
                dash_results["lane_details"].append({
                    "name": lane_name,
                    "has_dash": False,
                    "dash_pattern": "无",
                    "stroke_color": self._extract_stroke_color(style)
                })
        
        self.improvement_results["swimlane_dashed"] = dash_results
        
        print(f"   ✅ 泳道总数: {dash_results['total_lanes']}")
        print(f"   ✅ 虚线泳道: {dash_results['dashed_lanes']}")
        if dash_results['total_lanes'] > 0:
            print(f"   ✅ 虚线率: {dash_results['dashed_lanes']/dash_results['total_lanes']*100:.1f}%")
        
        if dash_results['total_lanes'] > 0 and dash_results['dashed_lanes'] == dash_results['total_lanes']:
            print("   🎉 所有泳道都已应用虚线样式！")
        elif dash_results['total_lanes'] > 0:
            print(f"   ⚠️ 还有{dash_results['total_lanes']-dash_results['dashed_lanes']}个泳道未应用虚线")
        else:
            print("   ⚠️ 未找到泳道元素")
    
    def _extract_stroke_color(self, style):
        """提取strokeColor"""
        if 'strokeColor=' in style:
            start = style.find('strokeColor=') + 12
            end = style.find(';', start)
            if end == -1:
                end = len(style)
            return style[start:end]
        return "未设置"
    
    def check_connection_simplification(self, graph_model):
        """检查连接线简化"""
        print("\n🔗 2. 连接线简化检查")
        
        root_element = graph_model.find('root')
        connections = root_element.findall(".//mxCell[@edge='1']")
        
        simplification_results = {
            "total_connections": len(connections),
            "simplified_connections": 0,
            "complex_connections": 0,
            "direct_connections": 0,
            "connection_details": []
        }
        
        for conn in connections:
            conn_id = conn.get('id', '')
            source = conn.get('source', '')
            target = conn.get('target', '')
            
            # 检查几何路径
            geometry = conn.find('mxGeometry')
            has_points = False
            point_count = 0
            
            if geometry is not None:
                points_array = geometry.find('Array[@as="points"]')
                if points_array is not None:
                    has_points = True
                    point_count = len(points_array.findall('mxPoint'))
            
            # 分类连接线
            if not has_points:
                simplification_results["direct_connections"] += 1
                complexity = "直连"
            elif point_count <= 2:
                simplification_results["simplified_connections"] += 1
                complexity = f"简化({point_count}个路径点)"
            else:
                simplification_results["complex_connections"] += 1
                complexity = f"复杂({point_count}个路径点)"
            
            simplification_results["connection_details"].append({
                "id": conn_id,
                "source": source,
                "target": target,
                "complexity": complexity,
                "point_count": point_count
            })
        
        self.improvement_results["connection_optimization"] = simplification_results
        
        print(f"   ✅ 连接线总数: {simplification_results['total_connections']}")
        print(f"   ✅ 直连: {simplification_results['direct_connections']}")
        print(f"   ✅ 简化路径: {simplification_results['simplified_connections']}")
        print(f"   ✅ 复杂路径: {simplification_results['complex_connections']}")
        
        simple_rate = (simplification_results["direct_connections"] + 
                      simplification_results["simplified_connections"]) / simplification_results["total_connections"] * 100
        print(f"   🎯 简化率: {simple_rate:.1f}%")
    
    def check_path_optimization(self, graph_model):
        """检查路径优化"""
        print("\n📐 3. 路径优化检查")
        
        # 分析路径点使用情况
        root_element = graph_model.find('root')
        connections = root_element.findall(".//mxCell[@edge='1']")
        
        path_stats = defaultdict(int)
        total_path_points = 0
        
        for conn in connections:
            geometry = conn.find('mxGeometry')
            if geometry is not None:
                points_array = geometry.find('Array[@as="points"]')
                if points_array is not None:
                    point_count = len(points_array.findall('mxPoint'))
                    path_stats[f"{point_count}个路径点"] += 1
                    total_path_points += point_count
                else:
                    path_stats["直连"] += 1
        
        self.improvement_results["path_simplification"] = {
            "path_statistics": dict(path_stats),
            "total_path_points": total_path_points,
            "average_points_per_connection": total_path_points / len(connections)
        }
        
        print(f"   ✅ 路径点统计:")
        for path_type, count in path_stats.items():
            print(f"      {path_type}: {count}条连接线")
        
        print(f"   ✅ 平均路径点: {total_path_points / len(connections):.2f}个/连接线")
    
    def check_overlap_reduction(self, graph_model):
        """检查重叠减少"""
        print("\n🚫 4. 重叠减少检查")
        
        # 分析连接线颜色分布
        root_element = graph_model.find('root')
        connections = root_element.findall(".//mxCell[@edge='1']")
        
        color_distribution = defaultdict(int)
        
        for conn in connections:
            style = conn.get('style', '')
            
            if 'strokeColor=#FF6B35' in style:
                color_distribution["橙色(生产分支)"] += 1
            elif 'strokeColor=#4ECDC4' in style:
                color_distribution["青色(付款决策)"] += 1
            elif 'strokeColor=#45B7D1' in style:
                color_distribution["蓝色(管理决策)"] += 1
            elif 'strokeColor=#FF6B6B' in style:
                color_distribution["红色(拒绝分支)"] += 1
            else:
                color_distribution["黑色(主流程)"] += 1
        
        # 检查分支区域分离度
        branch_separation_score = len(color_distribution) * 20  # 每种颜色20分
        
        self.improvement_results["overlap_reduction"] = {
            "color_distribution": dict(color_distribution),
            "color_diversity": len(color_distribution),
            "separation_score": branch_separation_score
        }
        
        print(f"   ✅ 颜色分类数: {len(color_distribution)}")
        print(f"   ✅ 颜色分布:")
        for color, count in color_distribution.items():
            print(f"      {color}: {count}条")
        
        print(f"   ✅ 分离度评分: {branch_separation_score}/100")
    
    def generate_improvement_report(self):
        """生成改进验证报告"""
        print("\n" + "=" * 80)
        print("📊 流程图改进验证报告")
        print("=" * 80)
        
        # 泳道虚线改进评分
        dash_data = self.improvement_results["swimlane_dashed"]
        dash_score = (dash_data["dashed_lanes"] / dash_data["total_lanes"]) * 100 if dash_data["total_lanes"] > 0 else 0
        
        # 连接线简化评分
        conn_data = self.improvement_results["connection_optimization"]
        simple_connections = conn_data["direct_connections"] + conn_data["simplified_connections"]
        simplification_score = (simple_connections / conn_data["total_connections"]) * 100
        
        # 路径优化评分
        path_data = self.improvement_results["path_simplification"]
        avg_points = path_data["average_points_per_connection"]
        path_score = max(0, 100 - avg_points * 10)  # 路径点越少分数越高
        
        # 重叠减少评分
        overlap_data = self.improvement_results["overlap_reduction"]
        overlap_score = min(100, overlap_data["separation_score"])
        
        # 总体评分
        if dash_data["total_lanes"] > 0:
            overall_score = (dash_score + simplification_score + path_score + overlap_score) / 4
        else:
            overall_score = (simplification_score + path_score + overlap_score) / 3
        
        print(f"🎯 改进总评分: {overall_score:.1f}%")
        print(f"")
        print(f"📋 改进项目评分:")
        print(f"   🏊 泳道虚线改进: {dash_score:.1f}%")
        print(f"   🔗 连接线简化: {simplification_score:.1f}%")  
        print(f"   📐 路径优化: {path_score:.1f}%")
        print(f"   🚫 重叠减少: {overlap_score:.1f}%")
        
        # 改进效果评估
        if overall_score >= 90:
            grade = "🌟 优秀"
            status = "改进效果非常显著！"
        elif overall_score >= 80:
            grade = "👍 良好"
            status = "改进效果良好！"
        elif overall_score >= 70:
            grade = "⚠️ 一般"
            status = "改进效果一般，仍有优化空间。"
        else:
            grade = "❌ 需改进"
            status = "需要进一步优化。"
        
        print(f"\n🏆 改进等级: {grade}")
        print(f"💬 评估结论: {status}")
        
        # 详细改进成果
        print(f"\n🎉 具体改进成果:")
        print(f"   ✅ 泳道虚线: {dash_data['dashed_lanes']}/{dash_data['total_lanes']}个泳道已应用长虚线")
        print(f"   ✅ 连接线优化: {simple_connections}/{conn_data['total_connections']}条连接线已简化")
        print(f"   ✅ 颜色分类: {overlap_data['color_diversity']}种颜色避免重叠")
        print(f"   ✅ 平均路径点: {avg_points:.2f}个/连接线")
        
        return overall_score >= 80

def main():
    """主函数"""
    file_path = "s:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-重新生成版.drawio"
    
    checker = FlowchartImprovementChecker()
    
    try:
        success = checker.check_improvements(file_path)
        
        if success:
            print(f"\n🎉 改进验证完成！")
        else:
            print(f"\n⚠️ 验证过程中发现问题。")
        
        # 保存验证结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"s:\\PG-GMO\\office\\业务部\\流程图改进验证报告_{timestamp}.json"
        
        import json
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(checker.improvement_results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 详细验证结果已保存到: {report_file}")
        
        return success
        
    except Exception as e:
        print(f"❌ 验证过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()