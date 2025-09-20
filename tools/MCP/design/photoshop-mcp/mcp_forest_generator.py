#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入 Photoshop MCP 服务器功能
from psMCP import (
    open_photoshop,
    create_new_psd,
    export_as_png,
    save_current_psd
)

def create_forest_image_with_mcp():
    """使用 Photoshop MCP 服务器创建森林图像"""
    try:
        print("正在启动 Photoshop...")
        # 启动 Photoshop
        result = open_photoshop(True)
        print(f"Photoshop 启动结果: {result}")
        
        # 等待 Photoshop 完全启动
        time.sleep(5)
        
        print("创建新文档 (600x800)...")
        # 创建新文档
        result = create_new_psd("Forest", 600, 800, 72, "RGB", "white")
        print(f"文档创建结果: {result}")
        
        # 等待文档创建完成
        time.sleep(2)
        
        print("保存 PSD 文件...")
        # 保存 PSD 文件
        psd_result = save_current_psd("forest_600x800_mcp")
        print(f"PSD 保存结果: {psd_result}")
        
        print("导出为 PNG...")
        # 导出为 PNG
        png_result = export_as_png("forest_600x800_mcp")
        print(f"PNG 导出结果: {png_result}")
        
        print("森林图像创建完成！")
        return True
        
    except Exception as e:
        print(f"创建森林图像时出错: {e}")
        return False

if __name__ == "__main__":
    success = create_forest_image_with_mcp()
    if success:
        print("\n图像已成功通过 Photoshop MCP 服务器创建！")
        # 检查输出目录
        output_dir = os.path.join("..", "..", "02-Output", "画图")
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            forest_files = [f for f in files if "forest" in f.lower()]
            if forest_files:
                print(f"在 {output_dir} 中找到以下文件:")
                for file in forest_files:
                    print(f"  - {file}")
            else:
                print(f"在 {output_dir} 中未找到森林图像文件")
        else:
            print(f"输出目录 {output_dir} 不存在")
    else:
        print("\n图像创建失败")