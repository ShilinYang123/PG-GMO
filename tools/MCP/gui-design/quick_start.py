#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI设计器快速启动脚本
提供简单的命令行接口来使用GUI设计器功能
"""

import sys
import argparse
from pathlib import Path
from local_gui_designer_server import LocalGUIDesignerServer

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="GUI设计器快速启动工具")
    parser.add_argument("--designer", "-d", action="store_true", 
                       help="启动Pygubu设计器")
    parser.add_argument("--test", "-t", action="store_true", 
                       help="启动测试工具")
    parser.add_argument("--create", "-c", metavar="PROJECT_NAME", 
                       help="创建新项目")
    parser.add_argument("--generate", "-g", metavar="UI_FILE", 
                       help="从UI文件生成Python代码")
    parser.add_argument("--class-name", metavar="CLASS_NAME", default="App",
                       help="生成代码的类名 (默认: App)")
    parser.add_argument("--optimize", "-o", metavar="UI_FILE", 
                       help="优化UI文件布局")
    parser.add_argument("--list", "-l", action="store_true", 
                       help="列出所有可用功能")
    
    args = parser.parse_args()
    
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # 初始化服务器
    try:
        server = LocalGUIDesignerServer()
        print("✅ GUI设计器服务器初始化成功")
    except Exception as e:
        print(f"❌ 服务器初始化失败: {e}")
        return
    
    # 处理命令
    try:
        if args.designer:
            print("🚀 启动Pygubu设计器...")
            result = server.launch_designer()
            print(f"启动结果: {result}")
            
        elif args.test:
            print("🧪 启动测试工具...")
            import subprocess
            subprocess.run([sys.executable, "test_gui_designer.py"])
            
        elif args.create:
            print(f"📁 创建项目: {args.create}")
            result = server.create_project(args.create, f"项目 {args.create} 的描述")
            print(f"创建结果: {result}")
            
        elif args.generate:
            ui_file = Path(args.generate)
            if not ui_file.exists():
                print(f"❌ UI文件不存在: {ui_file}")
                return
                
            print(f"🔧 生成代码: {ui_file} -> {args.class_name}")
            code = server.generate_code(str(ui_file), args.class_name)
            
            # 保存到文件
            output_file = ui_file.with_suffix('.py')
            output_file.write_text(code, encoding='utf-8')
            print(f"✅ 代码已保存到: {output_file}")
            
        elif args.optimize:
            ui_file = Path(args.optimize)
            if not ui_file.exists():
                print(f"❌ UI文件不存在: {ui_file}")
                return
                
            print(f"⚡ 优化布局: {ui_file}")
            result = server.optimize_layout(str(ui_file))
            print(f"优化结果: {result}")
            
        elif args.list:
            print("📋 可用功能列表:")
            tools = server.list_tools()
            for i, tool in enumerate(tools, 1):
                print(f"{i:2d}. {tool['name']}")
                print(f"     {tool['description']}")
                print()
                
    except Exception as e:
        print(f"❌ 执行失败: {e}")

if __name__ == "__main__":
    main()