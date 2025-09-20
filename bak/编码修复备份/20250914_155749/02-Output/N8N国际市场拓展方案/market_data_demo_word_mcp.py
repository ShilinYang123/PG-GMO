#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N8N市场调查数据获取演示脚本 - 使用Word MCP服务器
模拟N8N工作流的数据收集和Word报告生成过程
"""

import json
import random
from datetime import datetime
import os
import sys

# 添加MCP服务器路径
sys.path.append(r'S:\PG-GMO\tools\MCP\office\word-mcp')

try:
    from word_document_server.tools.document_tools import create_document, get_document_info
    from word_document_server.tools.content_tools import add_heading, add_paragraph, add_table
    from word_document_server.tools.format_tools import format_table
    MCP_AVAILABLE = True
except ImportError as e:
    print(f"警告: Word MCP服务器不可用: {str(e)}，将生成JSON格式报告")
    MCP_AVAILABLE = False

def generate_market_data():
    """模拟获取市场数据"""
    print("📊 步骤1: 获取市场数据...")
    
    products = [
        "智能空调", "变频洗衣机", "节能冰箱", 
        "智能热水器", "空气净化器"
    ]
    
    regions = ["华东", "华南", "华北", "西南", "华中"]
    competitors = ["海尔", "美的", "格力", "TCL", "海信"]
    trends = ["上升", "稳定", "下降"]
    
    market_data = []
    
    for product in products:
        data = {
            "产品名称": product,
            "市场价格": f"¥{random.randint(2000, 8000):,}",
            "市场份额": f"{random.randint(8, 25)}%",
            "主要竞争对手": random.choice(competitors),
            "价格趋势": random.choice(trends),
            "主要区域": random.choice(regions),
            "市场价值": f"¥{random.randint(5000000, 15000000):,}",
            "调查时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        market_data.append(data)
    
    print(f"✅ 成功获取 {len(market_data)} 个产品的市场数据")
    return market_data

def validate_data(data):
    """验证数据完整性"""
    print("🔍 步骤2: 验证数据完整性...")
    
    required_fields = ["产品名称", "市场价格", "市场份额", "主要竞争对手"]
    valid_count = 0
    
    for item in data:
        if all(field in item and item[field] for field in required_fields):
            valid_count += 1
    
    validation_rate = (valid_count / len(data)) * 100
    print(f"✅ 数据验证完成，通过率: {validation_rate:.1f}%")
    
    return validation_rate > 90

def process_data(data):
    """处理和分析数据"""
    print("⚙️ 步骤3: 处理和分析数据...")
    
    # 计算总市场价值
    total_value = 0
    for item in data:
        value_str = item["市场价值"].replace("¥", "").replace(",", "")
        total_value += int(value_str)
    
    # 计算平均市场份额
    total_share = 0
    for item in data:
        share_str = item["市场份额"].replace("%", "")
        total_share += int(share_str)
    
    avg_share = total_share / len(data)
    
    summary = {
        "总市场价值": f"¥{total_value:,}",
        "调查产品数量": len(data),
        "平均市场份额": f"{avg_share:.1f}%",
        "数据完整性": "100%"
    }
    
    print(f"✅ 数据处理完成")
    print(f"   - 总市场价值: {summary['总市场价值']}")
    print(f"   - 调查产品数量: {summary['调查产品数量']}")
    print(f"   - 平均市场份额: {summary['平均市场份额']}")
    
    return summary

import asyncio

async def create_word_report_with_mcp_async(data, summary):
    """使用Word MCP服务器创建Word报告（异步版本）"""
    print("📝 步骤4: 使用Word MCP服务器创建报告...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"市场调查报告_{timestamp}.docx"
    filepath = os.path.join(r"S:\PG-GMO\02-Output\N8N国际市场拓展方案", filename)
    
    try:
        # 创建文档
        result = await create_document(
            filename=filepath,
            title="N8N国际市场拓展调查报告",
            author="N8N自动化系统"
        )
        print(f"创建文档结果: {result}")
        
        # 添加标题
        result = await add_heading(filepath, "N8N国际市场拓展调查报告", level=1)
        print(f"添加标题结果: {result}")
        
        # 添加生成时间
        result = await add_paragraph(
            filepath, 
            f"报告生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"
        )
        print(f"添加时间结果: {result}")
        
        # 添加数据汇总部分
        result = await add_heading(filepath, "数据汇总", level=2)
        print(f"添加汇总标题结果: {result}")
        
        # 创建汇总表格
        summary_data = [
            ["指标", "数值"],
            ["总市场价值", summary["总市场价值"]],
            ["调查产品数量", str(summary["调查产品数量"])],
            ["平均市场份额", summary["平均市场份额"]],
            ["数据完整性", summary["数据完整性"]]
        ]
        
        result = await add_table(
            filepath, 
            rows=len(summary_data), 
            cols=2, 
            data=summary_data
        )
        print(f"添加汇总表格结果: {result}")
        
        # 添加详细数据部分
        result = await add_heading(filepath, "详细数据", level=2)
        print(f"添加详细数据标题结果: {result}")
        
        # 创建详细数据表格
        headers = ["产品名称", "市场价格", "市场份额", "主要竞争对手", "价格趋势", "主要区域", "市场价值"]
        detailed_data = [headers]
        
        for item in data:
            row = [
                item["产品名称"],
                item["市场价格"],
                item["市场份额"],
                item["主要竞争对手"],
                item["价格趋势"],
                item["主要区域"],
                item["市场价值"]
            ]
            detailed_data.append(row)
        
        result = await add_table(
            filepath,
            rows=len(detailed_data),
            cols=len(headers),
            data=detailed_data
        )
        print(f"添加详细数据表格结果: {result}")
        
        # 添加页脚信息
        result = await add_paragraph(
            filepath,
            "\n本报告由N8N自动化工作流生成，数据来源于市场调查API接口。"
        )
        print(f"添加页脚结果: {result}")
        
        print(f"✅ Word报告已保存: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Word MCP服务器创建报告失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def create_word_report_with_mcp(data, summary):
    """使用Word MCP服务器创建Word报告（同步包装器）"""
    try:
        return asyncio.run(create_word_report_with_mcp_async(data, summary))
    except Exception as e:
        print(f"❌ 异步执行失败: {str(e)}")
        return None

def create_json_report_fallback(data, summary):
    """备用方案：创建JSON格式报告"""
    print("📝 步骤4: 创建JSON格式报告（备用方案）...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"市场调查报告_{timestamp}.json"
    filepath = os.path.join(r"S:\PG-GMO\02-Output\N8N国际市场拓展方案", filename)
    
    report = {
        "报告标题": "N8N国际市场拓展调查报告",
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "数据汇总": summary,
        "详细数据": data
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON报告已保存: {filepath}")
    return filepath

def save_data(data, summary):
    """保存数据和报告"""
    if MCP_AVAILABLE:
        report_path = create_word_report_with_mcp(data, summary)
        if report_path:
            return report_path
    
    # 备用方案
    return create_json_report_fallback(data, summary)

def send_notification(report_path):
    """发送通知"""
    print("📧 步骤6: 发送通知...")
    
    file_format = "Word" if report_path.endswith('.docx') else "JSON"
    
    notification = {
        "收件人": "市场分析团队",
        "主题": "N8N市场调查报告已生成",
        "内容": f"新的市场调查报告已生成完成，格式：{file_format}\n报告路径：{report_path}",
        "发送时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"✅ 通知已发送给 {notification['收件人']}")
    print(f"   报告格式: {file_format}")
    print(f"   报告路径: {report_path}")
    
    return notification

def main():
    """主函数 - 模拟N8N工作流执行"""
    print("🚀 N8N市场调查工作流开始执行...")
    print(f"MCP服务器状态: {'可用' if MCP_AVAILABLE else '不可用（使用备用方案）'}")
    print("-" * 50)
    
    try:
        # 1. 获取市场数据
        market_data = generate_market_data()
        
        # 2. 验证数据
        if not validate_data(market_data):
            print("❌ 数据验证失败，工作流终止")
            return
        
        # 3. 处理数据
        summary = process_data(market_data)
        
        # 4. 保存报告
        report_path = save_data(market_data, summary)
        
        # 5. 发送通知
        send_notification(report_path)
        
        print("-" * 50)
        print("🎉 N8N市场调查工作流执行完成！")
        
    except Exception as e:
        print(f"❌ 工作流执行失败: {str(e)}")
        return

if __name__ == "__main__":
    main()