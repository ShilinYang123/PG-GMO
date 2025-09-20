#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图连接线交叉优化工具
实现连接线交叉点的弧形跨越处理
避免连接线交叉造成的视觉混乱
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import math
import re
from collections import defaultdict

class FlowchartCrossingOptimizer:
    def __init__(self):
        self.crossing_results = {
            "crossing_analysis": {},
            "arc_optimizations": {},
            "connection_hierarchy": {}
        }
        
    def optimize_crossings(self, source_file, output_file):
        """优化流程图中的连接线交叉问题"""
        print("🎯 开始流程图连接线交叉优化...")
        print(f"📁 源文件: {source_file}")
        print(f"📁 输出文件: {output_file}")
        print(f"⏰ 优化时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        try:
            # 解析源文件
            tree = ET.parse(source_file)
            root = tree.getroot()
            graph_model = root.find(".//mxGraphModel")
            
            if graph_model is None:
                raise ValueError("未找到mxGraphModel元素")
            
            # 分析连接线交叉情况
            self.analyze_crossings(graph_model)
            
            # 确定连接线层级
            self.determine_connection_hierarchy(graph_model)
            
            # 应用弧形跨越优化
            self.apply_arc_optimizations(graph_model)
            
            # 保存优化后的文件
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            print(f"\n🎉 连接线交叉优化完成！")
            print(f"📁 保存位置: {output_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ 优化过程中发生错误: {str(e)}")
            return False
    
    def analyze_crossings(self, graph_model):
        """分析连接线交叉情况"""
        print("🔍 1. 分析连接线交叉情况")
        
        root_element = graph_model.find('root')
        connections = root_element.findall(".//mxCell[@edge='1']")
        
        # 解析所有连接线的路径
        connection_paths = {}
        for conn in connections:
            conn_id = conn.get('id', '')
            path_segments = self.extract_path_segments(conn)
            connection_paths[conn_id] = {
                'segments': path_segments,
                'style': conn.get('style', ''),
                'element': conn
            }
        
        # 检测交叉点
        crossings = []
        conn_ids = list(connection_paths.keys())
        
        for i in range(len(conn_ids)):
            for j in range(i + 1, len(conn_ids)):
                conn1_id = conn_ids[i]
                conn2_id = conn_ids[j]
                
                conn1_segments = connection_paths[conn1_id]['segments']
                conn2_segments = connection_paths[conn2_id]['segments']
                
                # 检查每对线段是否相交
                for seg1 in conn1_segments:
                    for seg2 in conn2_segments:
                        intersection = self.find_line_intersection(seg1, seg2)
                        if intersection:
                            crossings.append({
                                'point': intersection,
                                'conn1': conn1_id,
                                'conn2': conn2_id,
                                'conn1_style': connection_paths[conn1_id]['style'],
                                'conn2_style': connection_paths[conn2_id]['style']
                            })
        
        self.crossing_results["crossing_analysis"] = {
            'total_connections': len(connections),
            'crossings_found': len(crossings),
            'crossings': crossings,
            'connection_paths': connection_paths
        }
        
        print(f"   ✅ 连接线总数: {len(connections)}")
        print(f"   ✅ 发现交叉点: {len(crossings)}个")
        
        if len(crossings) > 0:
            print(f"   📍 交叉点详情:")
            for i, crossing in enumerate(crossings[:5]):  # 只显示前5个
                print(f"      {i+1}. {crossing['conn1']} ⚡ {crossing['conn2']} 在 ({crossing['point'][0]:.1f}, {crossing['point'][1]:.1f})")
            if len(crossings) > 5:
                print(f"      ... 还有{len(crossings) - 5}个交叉点")
    
    def extract_path_segments(self, connection):
        """提取连接线的路径线段"""
        segments = []
        
        # 获取源点和目标点
        source_id = connection.get('source', '')
        target_id = connection.get('target', '')
        
        # 获取几何信息
        geometry = connection.find('mxGeometry')
        if geometry is None:
            return segments
            
        # 获取路径点
        points = []
        points_array = geometry.find('Array[@as="points"]')
        if points_array is not None:
            for point in points_array.findall('mxPoint'):
                x = float(point.get('x', '0'))
                y = float(point.get('y', '0'))
                points.append((x, y))
        
        # 如果没有路径点，这是一条直线
        if not points:
            # 这里应该获取源和目标的实际坐标，简化处理
            return segments
            
        # 构建线段
        if len(points) >= 2:
            for i in range(len(points) - 1):
                segments.append((points[i], points[i + 1]))
        
        return segments
    
    def find_line_intersection(self, line1, line2):
        """计算两条线段的交点"""
        (x1, y1), (x2, y2) = line1
        (x3, y3), (x4, y4) = line2
        
        # 计算方向向量
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        # 平行线
        if abs(denom) < 1e-10:
            return None
            
        # 计算交点参数
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        # 检查交点是否在两条线段上
        if 0 <= t <= 1 and 0 <= u <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
            
        return None
    
    def determine_connection_hierarchy(self, graph_model):
        """确定连接线的层级优先级"""
        print("\n📊 2. 确定连接线层级")
        
        crossings = self.crossing_results["crossing_analysis"]["crossings"]
        connection_paths = self.crossing_results["crossing_analysis"]["connection_paths"]
        
        # 连接线层级评分规则
        hierarchy_scores = {}
        
        for conn_id, conn_info in connection_paths.items():
            score = 0
            style = conn_info['style']
            
            # 根据样式确定优先级
            if 'strokeWidth=2' in style:
                score += 20  # 粗线优先级高
            elif 'strokeWidth=1' in style:
                score += 10
                
            # 根据颜色确定优先级
            if 'strokeColor=#FF6B35' in style:  # 橙色生产线
                score += 30
            elif 'strokeColor=#4ECDC4' in style:  # 青色决策线
                score += 25
            elif 'strokeColor=#45B7D1' in style:  # 蓝色管理线
                score += 20
            elif 'strokeColor=#FF6600' in style:  # 品质检验线
                score += 15
            else:  # 黑色主流程线
                score += 10
                
            # 根据虚线类型调整优先级
            if 'strokeDashArray' in style:
                score -= 5  # 虚线优先级稍低
                
            hierarchy_scores[conn_id] = score
        
        # 为每个交叉点确定哪条线应该使用弧形跨越
        arc_decisions = []
        for crossing in crossings:
            conn1_score = hierarchy_scores.get(crossing['conn1'], 0)
            conn2_score = hierarchy_scores.get(crossing['conn2'], 0)
            
            if conn1_score > conn2_score:
                # conn1优先级高，conn2使用弧形跨越
                arc_decisions.append({
                    'crossing_point': crossing['point'],
                    'arc_connection': crossing['conn2'],
                    'base_connection': crossing['conn1'],
                    'priority_diff': conn1_score - conn2_score
                })
            elif conn2_score > conn1_score:
                # conn2优先级高，conn1使用弧形跨越
                arc_decisions.append({
                    'crossing_point': crossing['point'],
                    'arc_connection': crossing['conn1'], 
                    'base_connection': crossing['conn2'],
                    'priority_diff': conn2_score - conn1_score
                })
            else:
                # 优先级相同，选择后绘制的使用弧形
                arc_decisions.append({
                    'crossing_point': crossing['point'],
                    'arc_connection': crossing['conn2'],  # 默认选择第二条
                    'base_connection': crossing['conn1'],
                    'priority_diff': 0
                })
        
        self.crossing_results["connection_hierarchy"] = {
            'hierarchy_scores': hierarchy_scores,
            'arc_decisions': arc_decisions
        }
        
        print(f"   ✅ 连接线层级评估完成")
        print(f"   ✅ 需要弧形处理: {len(arc_decisions)}个交叉点")
        
        # 显示层级最高的几条线
        sorted_scores = sorted(hierarchy_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"   🏆 优先级最高的连接线:")
        for conn_id, score in sorted_scores:
            print(f"      {conn_id}: {score}分")
    
    def apply_arc_optimizations(self, graph_model):
        """应用弧形跨越优化"""
        print("\n🌈 3. 应用弧形跨越优化")
        
        root_element = graph_model.find('root')
        arc_decisions = self.crossing_results["connection_hierarchy"]["arc_decisions"]
        connection_paths = self.crossing_results["crossing_analysis"]["connection_paths"]
        
        optimizations_applied = 0
        
        for decision in arc_decisions:
            arc_conn_id = decision['arc_connection']
            crossing_point = decision['crossing_point']
            
            # 找到需要修改的连接线元素
            arc_connection = None
            for conn_id, conn_info in connection_paths.items():
                if conn_id == arc_conn_id:
                    arc_connection = conn_info['element']
                    break
            
            if arc_connection is not None:
                success = self.add_arc_to_connection(arc_connection, crossing_point)
                if success:
                    optimizations_applied += 1
        
        self.crossing_results["arc_optimizations"] = {
            'total_crossings': len(arc_decisions),
            'optimizations_applied': optimizations_applied,
            'success_rate': optimizations_applied / len(arc_decisions) * 100 if arc_decisions else 100
        }
        
        print(f"   ✅ 弧形优化应用: {optimizations_applied}/{len(arc_decisions)}")
        print(f"   ✅ 成功率: {optimizations_applied / len(arc_decisions) * 100:.1f}%" if arc_decisions else "   ✅ 无需优化")
    
    def add_arc_to_connection(self, connection, crossing_point):
        """为连接线在交叉点添加弧形路径"""
        try:
            # 获取连接线的几何信息
            geometry = connection.find('mxGeometry')
            if geometry is None:
                return False
                
            # 获取现有路径点
            points_array = geometry.find('Array[@as="points"]')
            if points_array is None:
                # 创建新的路径点数组
                points_array = ET.SubElement(geometry, 'Array')
                points_array.set('as', 'points')
            
            existing_points = []
            for point in points_array.findall('mxPoint'):
                x = float(point.get('x', '0'))
                y = float(point.get('y', '0'))
                existing_points.append((x, y))
            
            # 在交叉点附近添加弧形路径点
            arc_points = self.calculate_enhanced_arc_points(crossing_point, existing_points)
            
            # 清除原有路径点
            points_array.clear()
            
            # 添加新的路径点（包括弧形点）
            all_points = self.merge_enhanced_arc_points(existing_points, arc_points, crossing_point)
            
            for point in all_points:
                point_element = ET.SubElement(points_array, 'mxPoint')
                point_element.set('x', str(int(point[0])))
                point_element.set('y', str(int(point[1])))
            
            # 修改连接线样式，使其支持曲线和增强的弧形效果
            style = connection.get('style', '')
            
            # 移除可能存在的直角样式
            style = re.sub(r'edgeStyle=orthogonalEdgeStyle;?', '', style)
            
            # 添加增强的曲线样式
            if 'curved=1' not in style:
                if style and not style.endswith(';'):
                    style += ';'
                style += 'curved=1;'
            
            # 添加平滑曲线和弧形跨越样式
            if 'noEdgeStyle=1' not in style:
                if style and not style.endswith(';'):
                    style += ';'
                style += 'noEdgeStyle=1;'
            
            # 增加弧形的曲率
            if 'curveFitting=1' not in style:
                if style and not style.endswith(';'):
                    style += ';'
                style += 'curveFitting=1;'
                
            connection.set('style', style)
            
            return True
            
        except Exception as e:
            print(f"   ⚠️ 处理连接线 {connection.get('id', '')} 时出错: {str(e)}")
            return False
    
    def calculate_enhanced_arc_points(self, crossing_point, existing_points):
        """计算增强的弧形路径点"""
        cx, cy = crossing_point
        arc_radius = 35  # 增大弧形半径，使弧形更明显
        
        # 根据交叉点周围的环境动态调整弧形方向
        # 默认向上弧形，如果上方空间不足则向下
        arc_direction = -1  # -1为向上，1为向下
        
        # 检查上方和下方的空间
        if cy < 300:  # 如果交叉点在图的上部，使用向下弧形
            arc_direction = 1
            
        # 生成更平滑的弧形控制点
        # 使用贝塞尔曲线控制点来创建更自然的弧形
        arc_points = [
            (cx - arc_radius * 1.2, cy),                                    # 弧形起始控制点
            (cx - arc_radius * 0.8, cy + arc_direction * arc_radius * 0.6), # 左侧控制点
            (cx - arc_radius * 0.3, cy + arc_direction * arc_radius),       # 左侧弧顶点
            (cx, cy + arc_direction * arc_radius * 1.1),                    # 弧形最高点
            (cx + arc_radius * 0.3, cy + arc_direction * arc_radius),       # 右侧弧顶点
            (cx + arc_radius * 0.8, cy + arc_direction * arc_radius * 0.6), # 右侧控制点
            (cx + arc_radius * 1.2, cy)                                     # 弧形结束控制点
        ]
        
        return arc_points
    
    def merge_enhanced_arc_points(self, existing_points, arc_points, crossing_point):
        """将增强弧形点智能合并到现有路径中"""
        if not existing_points:
            return arc_points
            
        cx, cy = crossing_point
        
        # 找到距离交叉点最近的路径段
        min_distance = float('inf')
        best_insert_index = len(existing_points) // 2
        
        for i in range(len(existing_points)):
            px, py = existing_points[i]
            distance = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
            if distance < min_distance:
                min_distance = distance
                best_insert_index = i
        
        # 智能插入弧形点
        result_points = []
        
        # 添加交叉点之前的路径点
        for i in range(best_insert_index):
            result_points.append(existing_points[i])
        
        # 添加弧形进入点
        if best_insert_index > 0:
            prev_point = existing_points[best_insert_index - 1]
            entry_point = (
                (prev_point[0] + cx) / 2,
                (prev_point[1] + cy) / 2
            )
            result_points.append(entry_point)
        
        # 添加弧形路径点
        result_points.extend(arc_points)
        
        # 添加弧形退出点
        if best_insert_index < len(existing_points):
            next_point = existing_points[best_insert_index]
            exit_point = (
                (next_point[0] + cx) / 2,
                (next_point[1] + cy) / 2
            )
            result_points.append(exit_point)
        
        # 添加交叉点之后的路径点
        for i in range(best_insert_index, len(existing_points)):
            result_points.append(existing_points[i])
        
        return result_points
    
    def generate_optimization_report(self):
        """生成优化报告"""
        print("\n" + "=" * 80)
        print("📊 流程图连接线交叉优化报告")
        print("=" * 80)
        
        crossing_analysis = self.crossing_results["crossing_analysis"]
        arc_optimizations = self.crossing_results["arc_optimizations"]
        
        print(f"🎯 优化总评分:")
        if crossing_analysis["crossings_found"] == 0:
            print(f"   🌟 完美: 无连接线交叉问题")
            overall_score = 100
        else:
            optimization_rate = arc_optimizations.get("success_rate", 0)
            overall_score = min(100, 50 + optimization_rate / 2)
            if overall_score >= 90:
                grade = "🌟 优秀"
            elif overall_score >= 80:
                grade = "👍 良好"
            elif overall_score >= 70:
                grade = "⚠️ 一般"
            else:
                grade = "❌ 需改进"
            print(f"   {grade}: {overall_score:.1f}%")
        
        print(f"\n📋 优化统计:")
        print(f"   🔗 连接线总数: {crossing_analysis['total_connections']}")
        print(f"   ⚡ 交叉点数量: {crossing_analysis['crossings_found']}")
        print(f"   🌈 弧形优化: {arc_optimizations.get('optimizations_applied', 0)}个")
        print(f"   ✅ 优化成功率: {arc_optimizations.get('success_rate', 0):.1f}%")
        
        # 连接线层级信息
        hierarchy = self.crossing_results.get("connection_hierarchy", {})
        if hierarchy:
            print(f"\n🏆 连接线层级分析:")
            scores = hierarchy.get("hierarchy_scores", {})
            if scores:
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
                for i, (conn_id, score) in enumerate(sorted_scores):
                    print(f"   {i+1}. {conn_id}: {score}分")
        
        return overall_score >= 80

def main():
    """主函数"""
    source_file = "s:\\PG-GMO\\office\\业务部\\小家电制造业详细生产流程图.drawio"
    output_file = "s:\\PG-GMO\\office\\业务部\\小家电制造业详细生产流程图-交叉优化版.drawio"
    
    optimizer = FlowchartCrossingOptimizer()
    
    try:
        success = optimizer.optimize_crossings(source_file, output_file)
        
        if success:
            # 生成优化报告
            optimizer.generate_optimization_report()
            print(f"\n🎉 连接线交叉优化完成！")
            print(f"📁 优化后文件: {output_file}")
        else:
            print(f"\n⚠️ 优化过程中遇到问题。")
        
        return success
        
    except Exception as e:
        print(f"❌ 优化过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    main()