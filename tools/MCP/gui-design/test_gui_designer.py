#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI设计器测试脚本
测试Pygubu GUI设计器的各项功能
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from local_gui_designer_server import LocalGUIDesignerServer
except ImportError as e:
    print(f"导入错误: {e}")
    sys.exit(1)

class GUIDesignerTester:
    """GUI设计器测试类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI设计器测试工具")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 初始化GUI设计器服务器
        try:
            self.server = LocalGUIDesignerServer()
            self.status_text = "✅ GUI设计器服务器初始化成功"
        except Exception as e:
            self.server = None
            self.status_text = f"❌ GUI设计器服务器初始化失败: {e}"
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="GUI设计器测试工具", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 状态显示
        status_frame = ttk.LabelFrame(main_frame, text="状态信息", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = ttk.Label(status_frame, text=self.status_text)
        self.status_label.pack()
        
        # 功能测试按钮
        button_frame = ttk.LabelFrame(main_frame, text="功能测试", padding="10")
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("启动Pygubu设计器", self.test_launch_designer),
            ("检查安装状态", self.test_check_installation),
            ("创建测试项目", self.test_create_project),
            ("加载模板文件", self.test_load_template),
            ("生成Python代码", self.test_generate_code),
            ("优化布局", self.test_optimize_layout),
            ("获取功能列表", self.test_list_tools),
            ("打开项目目录", self.open_project_directory),
            ("查看配置文件", self.view_config_file),
            ("运行完整测试", self.run_full_test)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = ttk.Button(button_frame, text=text, command=command, width=25)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # 配置网格权重
        for i in range(2):
            button_frame.columnconfigure(i, weight=1)
        
        # 输出区域
        output_frame = ttk.LabelFrame(main_frame, text="输出信息", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # 文本框和滚动条
        text_frame = ttk.Frame(output_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=10)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 清除按钮
        clear_btn = ttk.Button(output_frame, text="清除输出", command=self.clear_output)
        clear_btn.pack(pady=(10, 0))
        
    def log_output(self, message):
        """输出日志信息"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        self.root.update()
        
    def clear_output(self):
        """清除输出"""
        self.output_text.delete(1.0, tk.END)
        
    def test_check_installation(self):
        """测试检查安装状态"""
        self.log_output("=== 检查安装状态 ===")
        try:
            # 检查pygubu安装
            import pygubu
            self.log_output(f"✅ pygubu版本: {pygubu.__version__}")
            
            # 检查pygubu-designer
            result = subprocess.run(["pygubu-designer", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_output("✅ pygubu-designer已安装")
            else:
                self.log_output("❌ pygubu-designer未正确安装")
                
        except ImportError:
            self.log_output("❌ pygubu未安装")
        except subprocess.TimeoutExpired:
            self.log_output("⚠️ pygubu-designer检查超时")
        except Exception as e:
            self.log_output(f"❌ 检查失败: {e}")
            
    def test_launch_designer(self):
        """测试启动设计器"""
        self.log_output("=== 启动Pygubu设计器 ===")
        if not self.server:
            self.log_output("❌ 服务器未初始化")
            return
            
        try:
            result = self.server.launch_designer()
            self.log_output(f"启动结果: {result}")
        except Exception as e:
            self.log_output(f"❌ 启动失败: {e}")
            
    def test_create_project(self):
        """测试创建项目"""
        self.log_output("=== 创建测试项目 ===")
        if not self.server:
            self.log_output("❌ 服务器未初始化")
            return
            
        try:
            project_name = "测试项目_" + str(int(tk.time.time()))
            result = self.server.create_project(project_name, "这是一个测试项目")
            self.log_output(f"项目创建结果: {result}")
        except Exception as e:
            self.log_output(f"❌ 创建项目失败: {e}")
            
    def test_load_template(self):
        """测试加载模板"""
        self.log_output("=== 加载模板文件 ===")
        if not self.server:
            self.log_output("❌ 服务器未初始化")
            return
            
        template_path = current_dir / "gui-templates" / "basic_form.ui"
        if template_path.exists():
            try:
                result = self.server.load_ui_file(str(template_path))
                self.log_output(f"模板加载结果: {result}")
            except Exception as e:
                self.log_output(f"❌ 加载模板失败: {e}")
        else:
            self.log_output("❌ 模板文件不存在")
            
    def test_generate_code(self):
        """测试生成代码"""
        self.log_output("=== 生成Python代码 ===")
        if not self.server:
            self.log_output("❌ 服务器未初始化")
            return
            
        template_path = current_dir / "gui-templates" / "basic_form.ui"
        if template_path.exists():
            try:
                code = self.server.generate_code(str(template_path), "TestApp")
                self.log_output("✅ 代码生成成功")
                self.log_output(f"代码长度: {len(code)} 字符")
                self.log_output("代码预览:")
                self.log_output(code[:500] + "..." if len(code) > 500 else code)
            except Exception as e:
                self.log_output(f"❌ 生成代码失败: {e}")
        else:
            self.log_output("❌ 模板文件不存在")
            
    def test_optimize_layout(self):
        """测试布局优化"""
        self.log_output("=== 优化布局 ===")
        if not self.server:
            self.log_output("❌ 服务器未初始化")
            return
            
        template_path = current_dir / "gui-templates" / "basic_form.ui"
        if template_path.exists():
            try:
                result = self.server.optimize_layout(str(template_path))
                self.log_output(f"布局优化结果: {result}")
            except Exception as e:
                self.log_output(f"❌ 布局优化失败: {e}")
        else:
            self.log_output("❌ 模板文件不存在")
            
    def test_list_tools(self):
        """测试获取功能列表"""
        self.log_output("=== 获取功能列表 ===")
        if not self.server:
            self.log_output("❌ 服务器未初始化")
            return
            
        try:
            tools = self.server.list_tools()
            self.log_output(f"可用功能数量: {len(tools)}")
            for tool in tools:
                self.log_output(f"- {tool['name']}: {tool['description']}")
        except Exception as e:
            self.log_output(f"❌ 获取功能列表失败: {e}")
            
    def open_project_directory(self):
        """打开项目目录"""
        self.log_output("=== 打开项目目录 ===")
        project_dir = current_dir / "gui-projects"
        try:
            if sys.platform == "win32":
                os.startfile(str(project_dir))
            else:
                subprocess.run(["xdg-open", str(project_dir)])
            self.log_output("✅ 项目目录已打开")
        except Exception as e:
            self.log_output(f"❌ 打开目录失败: {e}")
            
    def view_config_file(self):
        """查看配置文件"""
        self.log_output("=== 查看配置文件 ===")
        config_path = current_dir / "gui_designer_config.json"
        try:
            if sys.platform == "win32":
                os.startfile(str(config_path))
            else:
                subprocess.run(["xdg-open", str(config_path)])
            self.log_output("✅ 配置文件已打开")
        except Exception as e:
            self.log_output(f"❌ 打开配置文件失败: {e}")
            
    def run_full_test(self):
        """运行完整测试"""
        self.log_output("=== 开始完整测试 ===")
        
        # 依次运行各项测试
        tests = [
            self.test_check_installation,
            self.test_create_project,
            self.test_load_template,
            self.test_generate_code,
            self.test_optimize_layout,
            self.test_list_tools
        ]
        
        for test in tests:
            try:
                test()
                self.log_output("")  # 空行分隔
            except Exception as e:
                self.log_output(f"❌ 测试失败: {e}")
                
        self.log_output("=== 完整测试结束 ===")
        
    def run(self):
        """运行测试工具"""
        self.root.mainloop()

def main():
    """主函数"""
    print("启动GUI设计器测试工具...")
    
    # 检查当前目录
    if not current_dir.exists():
        print(f"错误: 目录不存在 {current_dir}")
        return
        
    # 启动测试工具
    try:
        tester = GUIDesignerTester()
        tester.run()
    except Exception as e:
        print(f"启动失败: {e}")
        messagebox.showerror("错误", f"启动失败: {e}")

if __name__ == "__main__":
    main()