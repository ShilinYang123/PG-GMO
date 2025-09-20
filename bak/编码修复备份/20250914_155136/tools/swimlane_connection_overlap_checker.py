#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
泳道与连接线重合检查工具
专门检查流程图中连接线与泳道边框线重合的问题
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

class SwimlaneConnectionOverlapChecker:
    def __init__(self):
        self.check_results = {
            "swimlane_positions": {},
            "connection_paths": {},
            "overlap_analysis": {},
            "recommendations": []
        }
        
    def check_overlap_issues(self, file_path):
        """检查连接线与泳道线重合问题"""
        print("🔍 开始检查连接线与泳道线重合问题...")
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
            
            # 执行检查
            self.analyze_swimlane_positions(graph_model)
            self.analyze_connection_paths(graph_model)
            self.detect_overlaps()
            self.generate_recommendations()
            
            # 生成报告
            self.generate_overlap_report()
            
            return True
            
        except Exception as e:
            print(f"❌ 检查过程中发生错误: {str(e)}")
            return False
    
    def analyze_swimlane_positions(self, graph_model):
        """分析泳道位置信息"""
        print("🏊 1. 分析泳道位置信息")
        
        root_element = graph_model.find('root')
        swimlanes = []
        for cell in root_element.findall('.//mxCell'):
            style = cell.get('style', '')
            if 'swimlane' in style and cell.get('value'):
                swimlanes.append(cell)
        
        swimlane_info = {}
        
        for lane in swimlanes:
            lane_name = lane.get('value', '')
            geometry = lane.find('mxGeometry')
            
            if geometry is not None:
                x = int(geometry.get('x', '0'))
                y = int(geometry.get('y', '0'))
                width = int(geometry.get('width', '0'))
                height = int(geometry.get('height', '0'))
                
                # 计算泳道边界线位置
                swimlane_info[lane_name] = {
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'top_line': y,
                    'bottom_line': y + height,
                    'left_line': x,
                    'right_line': x + width,
                    'horizontal_lines': [y, y + height],  # 上下边框线
                    'vertical_lines': [x, x + width]      # 左右边框线
                }
        
        self.check_results["swimlane_positions"] = swimlane_info
        
        print(f"   ✅ 找到泳道: {len(swimlane_info)}个")
        for name, info in swimlane_info.items():
            print(f"      {name}: ({info['x']}, {info['y']}) 尺寸:{info['width']}×{info['height']}")
    
    def analyze_connection_paths(self, graph_model):
        """分析连接线路径"""
        print("\n🔗 2. 分析连接线路径")
        
        root_element = graph_model.find('root')
        connections = root_element.findall(".//mxCell[@edge='1']")
        
        connection_paths = {}
        
        for conn in connections:
            conn_id = conn.get('id', '')
            source = conn.get('source', '')
            target = conn.get('target', '')
            
            # 分析连接线路径
            geometry = conn.find('mxGeometry')
            path_info = {
                'source': source,
                'target': target,
                'path_points': [],
                'crosses_horizontal': [],
                'crosses_vertical': []
            }
            
            if geometry is not None:
                # 获取路径点
                points_array = geometry.find('Array[@as="points"]')
                if points_array is not None:
                    for point in points_array.findall('mxPoint'):
                        x = int(point.get('x', '0'))
                        y = int(point.get('y', '0'))
                        path_info['path_points'].append((x, y))
                
                # 分析路径经过的坐标线
                if path_info['path_points']:
                    for i, (x, y) in enumerate(path_info['path_points']):
                        # 检查是否在水平线上（Y坐标固定）
                        if i > 0:
                            prev_x, prev_y = path_info['path_points'][i-1]
                            if y == prev_y:  # 水平线段
                                path_info['crosses_horizontal'].append(y)
                            if x == prev_x:  # 垂直线段
                                path_info['crosses_vertical'].append(x)
            
            connection_paths[conn_id] = path_info
        
        self.check_results["connection_paths"] = connection_paths
        
        print(f"   ✅ 分析连接线: {len(connection_paths)}条")
        
        # 统计路径类型
        with_points = sum(1 for p in connection_paths.values() if p['path_points'])
        direct_lines = len(connection_paths) - with_points
        
        print(f"      直连线: {direct_lines}条")
        print(f"      带路径点: {with_points}条")
    
    def detect_overlaps(self):
        """检测重叠问题"""
        print("\n⚠️ 3. 检测重叠问题")
        
        swimlanes = self.check_results["swimlane_positions"]
        connections = self.check_results["connection_paths"]
        
        overlap_issues = []
        tolerance = 5  # 容差范围（像素）
        
        for conn_id, conn_info in connections.items():
            for lane_name, lane_info in swimlanes.items():
                
                # 检查水平线段与泳道水平边界重合
                for y_coord in conn_info['crosses_horizontal']:
                    for lane_y in lane_info['horizontal_lines']:
                        if abs(y_coord - lane_y) <= tolerance:
                            overlap_issues.append({
                                'type': 'horizontal_overlap',
                                'connection': conn_id,
                                'swimlane': lane_name,
                                'connection_y': y_coord,
                                'swimlane_y': lane_y,
                                'severity': 'high' if abs(y_coord - lane_y) <= 2 else 'medium'
                            })
                
                # 检查垂直线段与泳道垂直边界重合
                for x_coord in conn_info['crosses_vertical']:
                    for lane_x in lane_info['vertical_lines']:
                        if abs(x_coord - lane_x) <= tolerance:
                            overlap_issues.append({
                                'type': 'vertical_overlap',
                                'connection': conn_id,
                                'swimlane': lane_name,
                                'connection_x': x_coord,
                                'swimlane_x': lane_x,
                                'severity': 'high' if abs(x_coord - lane_x) <= 2 else 'medium'
                            })
        
        self.check_results["overlap_analysis"] = {
            'total_overlaps': len(overlap_issues),
            'high_severity': sum(1 for issue in overlap_issues if issue['severity'] == 'high'),
            'medium_severity': sum(1 for issue in overlap_issues if issue['severity'] == 'medium'),
            'issues': overlap_issues
        }
        
        print(f"   ✅ 检测完成")
        print(f"      发现重叠问题: {len(overlap_issues)}个")
        print(f"      高严重度: {self.check_results['overlap_analysis']['high_severity']}个")
        print(f"      中等严重度: {self.check_results['overlap_analysis']['medium_severity']}个")
        
        # 详细列出重叠问题
        if overlap_issues:
            print(f"\n   ⚠️ 具体重叠问题:")
            for i, issue in enumerate(overlap_issues[:10]):  # 只显示前10个
                if issue['type'] == 'horizontal_overlap':
                    print(f"      {i+1}. 连接线{issue['connection']} 与 泳道{issue['swimlane']} 水平边界重合")
                    print(f"         连接线Y={issue['connection_y']}, 泳道Y={issue['swimlane_y']} (严重度:{issue['severity']})")
                else:
                    print(f"      {i+1}. 连接线{issue['connection']} 与 泳道{issue['swimlane']} 垂直边界重合")
                    print(f"         连接线X={issue['connection_x']}, 泳道X={issue['swimlane_x']} (严重度:{issue['severity']})")
            
            if len(overlap_issues) > 10:
                print(f"      ... 还有{len(overlap_issues) - 10}个问题未显示")
    
    def generate_recommendations(self):
        """生成修复建议"""
        print("\n💡 4. 生成修复建议")
        
        overlap_analysis = self.check_results["overlap_analysis"]
        recommendations = []
        
        if overlap_analysis['total_overlaps'] == 0:
            recommendations.append("🎉 未发现连接线与泳道线重合问题！")
        else:
            # 按问题类型分类建议
            horizontal_issues = [issue for issue in overlap_analysis['issues'] if issue['type'] == 'horizontal_overlap']
            vertical_issues = [issue for issue in overlap_analysis['issues'] if issue['type'] == 'vertical_overlap']
            
            if horizontal_issues:
                recommendations.append({
                    'type': 'horizontal_fix',
                    'count': len(horizontal_issues),
                    'suggestion': '建议将水平连接线路径上移或下移10-15像素，避开泳道上下边界线',
                    'affected_connections': list(set([issue['connection'] for issue in horizontal_issues]))
                })
            
            if vertical_issues:
                recommendations.append({
                    'type': 'vertical_fix',
                    'count': len(vertical_issues),
                    'suggestion': '建议将垂直连接线路径左移或右移10-15像素，避开泳道左右边界线',
                    'affected_connections': list(set([issue['connection'] for issue in vertical_issues]))
                })
            
            # 高优先级修复建议
            high_priority = [issue for issue in overlap_analysis['issues'] if issue['severity'] == 'high']
            if high_priority:
                recommendations.append({
                    'type': 'high_priority',
                    'count': len(high_priority),
                    'suggestion': '这些重合问题严重影响视觉效果，建议优先修复',
                    'affected_connections': list(set([issue['connection'] for issue in high_priority]))
                })
        
        self.check_results["recommendations"] = recommendations
        
        print(f"   ✅ 生成修复建议: {len(recommendations)}条")
        for i, rec in enumerate(recommendations):
            if isinstance(rec, str):
                print(f"      {i+1}. {rec}")
            else:
                print(f"      {i+1}. {rec['suggestion']} (影响{rec['count']}处)")
    
    def generate_overlap_report(self):
        """生成重叠检查报告"""
        print("\n" + "=" * 80)
        print("📊 连接线与泳道线重合检查报告")
        print("=" * 80)
        
        overlap_analysis = self.check_results["overlap_analysis"]
        swimlanes = self.check_results["swimlane_positions"]
        connections = self.check_results["connection_paths"]
        
        # 总体评估
        total_issues = overlap_analysis['total_overlaps']
        if total_issues == 0:
            quality_score = 100
            quality_level = "🌟 完美"
        elif total_issues <= 3:
            quality_score = 85
            quality_level = "👍 良好"
        elif total_issues <= 8:
            quality_score = 70
            quality_level = "⚠️ 一般"
        else:
            quality_score = 50
            quality_level = "❌ 需改进"
        
        print(f"🎯 重合检查评分: {quality_score}%")
        print(f"🏆 质量等级: {quality_level}")
        print(f"")
        print(f"📋 检查统计:")
        print(f"   🏊 泳道数量: {len(swimlanes)}个")
        print(f"   🔗 连接线数量: {len(connections)}条")
        print(f"   ⚠️ 重合问题: {total_issues}个")
        print(f"      高严重度: {overlap_analysis['high_severity']}个")
        print(f"      中等严重度: {overlap_analysis['medium_severity']}个")
        
        # 详细建议
        recommendations = self.check_results["recommendations"]
        if recommendations:
            print(f"\n💡 修复建议:")
            for i, rec in enumerate(recommendations):
                if isinstance(rec, str):
                    print(f"   {i+1}. {rec}")
                else:
                    print(f"   {i+1}. {rec['suggestion']}")
                    print(f"      影响连接线: {', '.join(rec['affected_connections'][:5])}")
                    if len(rec['affected_connections']) > 5:
                        print(f"      ...等共{len(rec['affected_connections'])}条连接线")
        
        return quality_score >= 80

def main():
    """主函数"""
    file_path = "s:\\PG-GMO\\office\\业务部\\综合订单全流程ERP系统业务流程图-重新生成版.drawio"
    
    checker = SwimlaneConnectionOverlapChecker()
    
    try:
        success = checker.check_overlap_issues(file_path)
        
        if success:
            print(f"\n🎉 重合检查完成！")
        else:
            print(f"\n⚠️ 检查过程中发现问题。")
        
        # 保存检查结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"s:\\PG-GMO\\office\\业务部\\泳道连接线重合检查报告_{timestamp}.json"
        
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