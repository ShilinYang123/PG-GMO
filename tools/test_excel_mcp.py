#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel MCP服务器功能测试脚本
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加Excel MCP服务器路径
sys.path.append(r'S:\PG-GMO\project\MCP\office')

try:
    from excel_mcp_server import create_workbook, write_data, format_cells, get_workbook_info
except ImportError as e:
    print(f"导入Excel MCP模块失败: {e}")
    sys.exit(1)

async def test_excel_mcp():
    """
    测试Excel MCP服务器的主要功能
    """
    print("=== Excel MCP服务器功能测试 ===")
    
    # 测试文件路径
    test_file = r'S:\PG-GMO\Output\Excel测试工作簿.xlsx'
    
    try:
        # 1. 创建工作簿
        print("\n1. 测试创建工作簿...")
        result1 = await create_workbook(test_file, ['数据表', '图表表', '统计表'])
        print(f"创建结果: {result1}")
        
        # 2. 写入数据
        print("\n2. 测试写入数据...")
        data = [
            ['姓名', '年龄', '部门', '工资'],
            ['张三', 25, '技术部', 8000],
            ['李四', 30, '销售部', 9000],
            ['王五', 28, '市场部', 7500],
            ['赵六', 32, '技术部', 10000],
            ['钱七', 26, '销售部', 8500]
        ]
        result2 = await write_data(test_file, '数据表', data, 'A1')
        print(f"写入结果: {result2}")
        
        # 3. 格式化单元格
        print("\n3. 测试格式化单元格...")
        format_options = {
            'font_name': '微软雅黑',
            'font_size': 12,
            'bold': True,
            'font_color': [0, 0, 255],  # 蓝色
            'bg_color': [255, 255, 0],   # 黄色背景
            'alignment': 'center'
        }
        result3 = await format_cells(test_file, '数据表', 'A1:D1', format_options)
        print(f"格式化结果: {result3}")
        
        # 4. 获取工作簿信息
        print("\n4. 测试获取工作簿信息...")
        result4 = await get_workbook_info(test_file)
        print(f"工作簿信息: {result4}")
        
        # 5. 检查文件是否存在
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"\n✅ 测试成功！Excel文件已创建: {test_file}")
            print(f"文件大小: {file_size} 字节")
        else:
            print(f"\n❌ 测试失败！文件未创建: {test_file}")
            
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    主函数
    """
    print("启动Excel MCP功能测试...")
    
    # 确保输出目录存在
    output_dir = Path(r'S:\PG-GMO\Output')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 运行异步测试
    asyncio.run(test_excel_mcp())
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()