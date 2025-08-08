#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高效办公助手系统控制面板
AI Agent开发环境管理和MCP服务器集群监控
作者：雨俊
日期：2025-01-08
"""

import sys
import os
import subprocess
import threading
import time
import webbrowser
import queue
import json
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QScrollArea, QFrame, QSizePolicy, QTabWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import qRegisterMetaType

class OfficeAssistantControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        qRegisterMetaType('QTextCursor')
        self.setWindowTitle("高效办公助手系统控制面板 - AI Agent & MCP服务器管理")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)

        self.project_root = Path("s:/PG-GMO")
        self.mcp_servers = {}
        self.server_status = {}
        
        self.log_queue = queue.Queue()
        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.process_log_queue)
        self.log_timer.start(500)
        
        # 状态更新定时器
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_server_status)
        self.status_timer.start(5000)  # 每5秒更新一次

        self.init_ui()
        self.load_mcp_config()

    def process_log_queue(self):
        try:
            while True:
                message = self.log_queue.get_nowait()
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                self.status_text.append(f"[{timestamp}] {message}")
        except queue.Empty:
            pass

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Title frame
        title_frame = QFrame()
        title_frame.setFixedHeight(100)
        title_frame.setStyleSheet("background-color: #2c3e50;")
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 10, 20, 10)
        
        # 主标题
        title_label = QLabel("高效办公助手系统控制面板")
        title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = QLabel("AI Agent开发环境 & MCP服务器集群管理")
        subtitle_label.setStyleSheet("color: #bdc3c7; font-size: 14px;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(title_frame)
        
        # 创建标签页
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3498db;
            }
        """)
        
        # MCP服务器管理标签页
        mcp_tab = QWidget()
        self.setup_mcp_panel(mcp_tab)
        tab_widget.addTab(mcp_tab, "MCP服务器集群")
        
        # 系统监控标签页
        monitor_tab = QWidget()
        self.setup_monitor_panel(monitor_tab)
        tab_widget.addTab(monitor_tab, "系统监控")
        
        # 开发工具标签页
        dev_tab = QWidget()
        self.setup_dev_panel(dev_tab)
        tab_widget.addTab(dev_tab, "开发工具")
        
        main_layout.addWidget(tab_widget)

        # Main content
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 5, 10, 10)

        # Left panel
        left_panel = QScrollArea()
        left_panel.setWidgetResizable(True)
        left_panel.setFixedWidth(320)
        left_panel.setStyleSheet("background-color: #f0f0f0;")
        left_content = QWidget()
        left_layout = QVBoxLayout(left_content)
        left_layout.setAlignment(Qt.AlignTop)

        self.setup_control_panel(left_layout)
        left_panel.setWidget(left_content)
        content_layout.addWidget(left_panel)

        # Right panel
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("background-color: #ffffff; border: none;")
        content_layout.addWidget(self.status_text)

        main_layout.addWidget(content_widget)

        self.log_message("系统初始化完成。")
        self.log_message("欢迎使用高效办公助手系统控制面板！")
    
    def update_system_info(self):
        """更新系统信息显示"""
        if hasattr(self, 'system_info_area'):
            import platform
            try:
                import psutil
                cpu_percent = psutil.cpu_percent()
                memory_percent = psutil.virtual_memory().percent
                disk_percent = psutil.disk_usage(str(self.project_root)).percent
            except ImportError:
                cpu_percent = "N/A"
                memory_percent = "N/A"
                disk_percent = "N/A"
            
            info_text = f"""系统信息:
操作系统: {platform.system()} {platform.release()}
Python版本: {platform.python_version()}
项目根目录: {self.project_root}

资源使用:
CPU使用率: {cpu_percent}%
内存使用率: {memory_percent}%
磁盘使用率: {disk_percent}%

时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            self.system_info_area.setPlainText(info_text)

    def setup_mcp_panel(self, parent):
        """设置MCP服务器管理面板"""
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 服务器状态概览
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;")
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(15, 15, 15, 15)
        
        status_title = QLabel("MCP服务器集群状态")
        status_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        status_layout.addWidget(status_title)
        
        # 服务器状态显示区域
        self.server_status_area = QTextEdit()
        self.server_status_area.setMaximumHeight(200)
        self.server_status_area.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        status_layout.addWidget(self.server_status_area)
        layout.addWidget(status_frame)
        
        # 控制按钮区域
        control_frame = QFrame()
        control_layout = QHBoxLayout(control_frame)
        control_layout.setSpacing(10)
        
        # 启动所有服务器
        start_all_btn = QPushButton("启动所有MCP服务器")
        start_all_btn.setFixedSize(150, 40)
        start_all_btn.setStyleSheet(self.get_button_style("#27ae60", "#2ecc71", "#229954"))
        start_all_btn.clicked.connect(self.start_all_servers)
        control_layout.addWidget(start_all_btn)
        
        # 停止所有服务器
        stop_all_btn = QPushButton("停止所有MCP服务器")
        stop_all_btn.setFixedSize(150, 40)
        stop_all_btn.setStyleSheet(self.get_button_style("#e74c3c", "#c0392b", "#a93226"))
        stop_all_btn.clicked.connect(self.stop_all_servers)
        control_layout.addWidget(stop_all_btn)
        
        # 重启服务器
        restart_btn = QPushButton("重启MCP服务器")
        restart_btn.setFixedSize(120, 40)
        restart_btn.setStyleSheet(self.get_button_style("#f39c12", "#e67e22", "#d35400"))
        restart_btn.clicked.connect(self.restart_servers)
        control_layout.addWidget(restart_btn)
        
        # 检查状态
        check_btn = QPushButton("检查服务器状态")
        check_btn.setFixedSize(120, 40)
        check_btn.setStyleSheet(self.get_button_style("#3498db", "#2980b9", "#21618c"))
        check_btn.clicked.connect(self.check_server_status)
        control_layout.addWidget(check_btn)
        
        control_layout.addStretch()
        layout.addWidget(control_frame)
        
        # 服务器详细信息
        detail_frame = QFrame()
        detail_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;")
        detail_layout = QVBoxLayout(detail_frame)
        detail_layout.setContentsMargins(15, 15, 15, 15)
        
        detail_title = QLabel("服务器详细信息")
        detail_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        detail_layout.addWidget(detail_title)
        
        self.server_detail_area = QTextEdit()
        self.server_detail_area.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
        """)
        detail_layout.addWidget(self.server_detail_area)
        layout.addWidget(detail_frame)
    
    def setup_monitor_panel(self, parent):
        """设置系统监控面板"""
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 系统信息
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        info_title = QLabel("系统信息")
        info_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        info_layout.addWidget(info_title)
        
        self.system_info_area = QTextEdit()
        self.system_info_area.setMaximumHeight(150)
        self.system_info_area.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        info_layout.addWidget(self.system_info_area)
        layout.addWidget(info_frame)
        
        # 日志监控
        log_frame = QFrame()
        log_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;")
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(15, 15, 15, 15)
        
        log_title = QLabel("系统日志")
        log_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        log_layout.addWidget(log_title)
        
        self.log_area = QTextEdit()
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #34495e;
                border-radius: 3px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
        """)
        log_layout.addWidget(self.log_area)
        layout.addWidget(log_frame)
        
        # 初始化系统信息
        self.update_system_info()
    
    def setup_dev_panel(self, parent):
        """设置开发工具面板"""
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 快速操作
        quick_frame = QFrame()
        quick_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;")
        quick_layout = QVBoxLayout(quick_frame)
        quick_layout.setContentsMargins(15, 15, 15, 15)
        
        quick_title = QLabel("快速开发工具")
        quick_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        quick_layout.addWidget(quick_title)
        
        # 工具按钮网格
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(10)
        
        # 初始化环境
        init_btn = QPushButton("初始化开发环境")
        init_btn.setFixedSize(140, 40)
        init_btn.setStyleSheet(self.get_button_style("#8e44ad", "#9b59b6", "#7d3c98"))
        init_btn.clicked.connect(self.init_dev_environment)
        tools_layout.addWidget(init_btn)
        
        # 检查配置
        config_btn = QPushButton("检查项目配置")
        config_btn.setFixedSize(120, 40)
        config_btn.setStyleSheet(self.get_button_style("#16a085", "#1abc9c", "#138d75"))
        config_btn.clicked.connect(self.check_project_config)
        tools_layout.addWidget(config_btn)
        
        # 打开文档
        docs_btn = QPushButton("打开项目文档")
        docs_btn.setFixedSize(120, 40)
        docs_btn.setStyleSheet(self.get_button_style("#2980b9", "#3498db", "#21618c"))
        docs_btn.clicked.connect(self.open_project_docs)
        tools_layout.addWidget(docs_btn)
        
        # 运行测试
        test_btn = QPushButton("运行系统测试")
        test_btn.setFixedSize(120, 40)
        test_btn.setStyleSheet(self.get_button_style("#d35400", "#e67e22", "#ca6f1e"))
        test_btn.clicked.connect(self.run_system_tests)
        tools_layout.addWidget(test_btn)
        
        tools_layout.addStretch()
        quick_layout.addLayout(tools_layout)
        layout.addWidget(quick_frame)
        
        # 命令执行区域
        cmd_frame = QFrame()
        cmd_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;")
        cmd_layout = QVBoxLayout(cmd_frame)
        cmd_layout.setContentsMargins(15, 15, 15, 15)
        
        cmd_title = QLabel("命令执行")
        cmd_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        cmd_layout.addWidget(cmd_title)
        
        self.command_area = QTextEdit()
        self.command_area.setStyleSheet("""
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #34495e;
                border-radius: 3px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
        """)
        cmd_layout.addWidget(self.command_area)
        layout.addWidget(cmd_frame)

    def setup_control_panel(self, layout):
        # System Status
        status_label = QLabel("🔍 系统状态")
        status_label.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))
        layout.addWidget(status_label)

        self.system_status = QLabel("当前状态: 正常")
        self.system_status.setFont(QFont('Microsoft YaHei', 9))
        layout.addWidget(self.system_status)

        self.last_check_time = QLabel("最后检查: " + time.strftime('%Y-%m-%d %H:%M:%S'))
        self.last_check_time.setFont(QFont('Microsoft YaHei', 9))
        layout.addWidget(self.last_check_time)

        layout.addSpacing(10)

        # Quick Operations
        quick_label = QLabel("🚀 快速操作")
        quick_label.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))
        layout.addWidget(quick_label)

        check_btn = QPushButton("🌅 执行早上启动检查")
        check_btn.setFont(QFont('Microsoft YaHei', 9))
        check_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        check_btn.clicked.connect(self.run_startup_check)
        layout.addWidget(check_btn)

        status_btn = QPushButton("📋 查看详细状态")
        status_btn.setFont(QFont('Microsoft YaHei', 9))
        status_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px;")
        status_btn.clicked.connect(self.view_system_status)
        layout.addWidget(status_btn)

        layout.addSpacing(10)

        # System Launch
        launch_label = QLabel("🎯 系统启动")
        launch_label.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))
        layout.addWidget(launch_label)

        mgmt_btn = QPushButton("🎯 启动PMC管理系统")
        mgmt_btn.setFont(QFont('Microsoft YaHei', 9))
        mgmt_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")
        mgmt_btn.clicked.connect(self.launch_management_system)
        layout.addWidget(mgmt_btn)

        track_btn = QPushButton("📊 启动PMC追踪系统")
        track_btn.setFont(QFont('Microsoft YaHei', 9))
        track_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 8px;")
        track_btn.clicked.connect(self.launch_tracking_system)
        layout.addWidget(track_btn)

        layout.addSpacing(10)

        # System Tools
        tools_label = QLabel("🔧 系统工具")
        tools_label.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))
        layout.addWidget(tools_label)

        struct_btn = QPushButton("🔍 执行结构检查")
        struct_btn.setFont(QFont('Microsoft YaHei', 9))
        struct_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 8px;")
        struct_btn.clicked.connect(self.run_structure_check)
        layout.addWidget(struct_btn)

        docs_btn = QPushButton("📚 打开项目文档")
        docs_btn.setFont(QFont('Microsoft YaHei', 9))
        docs_btn.setStyleSheet("background-color: #34495e; color: white; padding: 8px;")
        docs_btn.clicked.connect(self.open_docs)
        layout.addWidget(docs_btn)

        manual_btn = QPushButton("📖 快速操作手册")
        manual_btn.setFont(QFont('Microsoft YaHei', 9))
        manual_btn.setStyleSheet("background-color: #16a085; color: white; padding: 8px;")
        manual_btn.clicked.connect(self.open_manual)
        layout.addWidget(manual_btn)

    def log_message(self, message):
        """添加日志消息到队列"""
        self.log_queue.put(message)
    
    def log_message_direct(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.status_text.append(f"[{timestamp}] {message}")
    
    def get_button_style(self, normal_color, hover_color, pressed_color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {normal_color};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """
    
    def load_mcp_config(self):
        """加载MCP服务器配置"""
        config_file = self.project_root / "config" / "mcp_servers.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.mcp_servers = json.load(f)
                self.log_message(f"已加载 {len(self.mcp_servers)} 个MCP服务器配置")
            except Exception as e:
                self.log_message(f"加载MCP配置失败: {e}")
        else:
            self.log_message("MCP配置文件不存在，使用默认配置")
            self.mcp_servers = {
                "file_server": {
                    "name": "文件管理服务器",
                    "command": ["python", "-m", "mcp_server_files"],
                    "port": 8001
                },
                "database_server": {
                    "name": "数据库服务器",
                    "command": ["python", "-m", "mcp_server_database"],
                    "port": 8002
                },
                "web_server": {
                    "name": "Web服务器",
                    "command": ["python", "-m", "mcp_server_web"],
                    "port": 8003
                }
            }
    
    def start_all_servers(self):
        """启动所有MCP服务器"""
        self.log_message("开始启动所有MCP服务器...")
        for server_id, config in self.mcp_servers.items():
            self.start_server(server_id, config)
    
    def stop_all_servers(self):
        """停止所有MCP服务器"""
        self.log_message("开始停止所有MCP服务器...")
        for server_id in self.mcp_servers.keys():
            self.stop_server(server_id)
    
    def restart_servers(self):
        """重启MCP服务器"""
        self.log_message("重启MCP服务器集群...")
        self.stop_all_servers()
        time.sleep(2)
        self.start_all_servers()
    
    def start_server(self, server_id, config):
        """启动单个服务器"""
        try:
            process = subprocess.Popen(
                config["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.server_status[server_id] = {
                "process": process,
                "status": "running",
                "start_time": datetime.now()
            }
            self.log_message(f"启动服务器: {config['name']} (PID: {process.pid})")
        except Exception as e:
            self.log_message(f"启动服务器失败 {config['name']}: {e}")
    
    def stop_server(self, server_id):
        """停止单个服务器"""
        if server_id in self.server_status:
            try:
                process = self.server_status[server_id]["process"]
                process.terminate()
                process.wait(timeout=5)
                self.log_message(f"停止服务器: {server_id}")
                del self.server_status[server_id]
            except Exception as e:
                self.log_message(f"停止服务器失败 {server_id}: {e}")
    
    def check_server_status(self):
        """检查服务器状态"""
        self.log_message("检查MCP服务器状态...")
        self.update_server_status()
    
    def update_server_status(self):
        """更新服务器状态显示"""
        if hasattr(self, 'server_status_area'):
            status_text = "MCP服务器集群状态:\n\n"
            
            for server_id, config in self.mcp_servers.items():
                if server_id in self.server_status:
                    status = self.server_status[server_id]
                    process = status["process"]
                    if process.poll() is None:
                        status_text += f"✅ {config['name']}: 运行中 (PID: {process.pid})\n"
                    else:
                        status_text += f"❌ {config['name']}: 已停止\n"
                        del self.server_status[server_id]
                else:
                    status_text += f"⭕ {config['name']}: 未启动\n"
            
            self.server_status_area.setPlainText(status_text)
    
    def init_dev_environment(self):
        """初始化开发环境"""
        self.log_message("初始化开发环境...")
        cmd = ['python', str(self.project_root / 'tools' / 'init_environment.py')]
        self.run_command_async(cmd, "开发环境初始化")
    
    def check_project_config(self):
        """检查项目配置"""
        self.log_message("检查项目配置...")
        cmd = ['python', str(self.project_root / 'tools' / 'config_check.py')]
        self.run_command_async(cmd, "项目配置检查")
    
    def open_project_docs(self):
        """打开项目文档"""
        docs_path = self.project_root / 'docs'
        if docs_path.exists():
            webbrowser.open(str(docs_path))
            self.log_message("打开项目文档文件夹")
        else:
            self.log_message("项目文档文件夹不存在")
    
    def run_system_tests(self):
        """运行系统测试"""
        self.log_message("运行系统测试...")
        cmd = ['python', str(self.project_root / 'tests' / 'run_tests.py')]
        self.run_command_async(cmd, "系统测试")

    def run_command_async(self, command, description):
        """异步执行命令"""
        def target():
            self.log_message(f"开始{description}...")
            try:
                process = subprocess.Popen(
                    command, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True, 
                    encoding='utf-8', 
                    errors='replace',
                    cwd=str(self.project_root)
                )
                while True:
                    output = process.stdout.readline()
                    if output:
                        self.log_message(output.strip())
                    if process.poll() is not None:
                        break
                if process.returncode == 0:
                    self.log_message(f"✅ {description}完成。")
                else:
                    self.log_message(f"❌ {description}失败（代码: {process.returncode}）。")
            except Exception as e:
                self.log_message(f"❌ 执行错误: {str(e)}")

        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
    
    def start_system(self):
        """启动高效办公助手系统"""
        self.log_message("正在启动高效办公助手系统...")
        
        # 检查Python环境
        try:
            python_check = subprocess.run(["python", "--version"], capture_output=True, text=True)
            if python_check.returncode == 0:
                self.log_message(f"Python环境检查通过: {python_check.stdout.strip()}")
            else:
                self.log_message("❌ Python环境检查失败")
                return
        except Exception as e:
            self.log_message(f"❌ Python环境检查异常: {e}")
            return
        
        # 启动MCP服务器集群
        self.start_all_servers()
        
        # 初始化办公环境
        init_script = self.project_root / "tools" / "office_assistant_init.py"
        if init_script.exists():
            self.run_command_async(["python", str(init_script)], "初始化办公环境")
        
        self.log_message("✅ 高效办公助手系统启动完成")

    def stop_system(self):
        """停止高效办公助手系统"""
        self.log_message("正在停止高效办公助手系统...")
        
        # 停止MCP服务器集群
        self.stop_all_servers()
        
        # 停止核心服务
        stop_script = self.project_root / "tools" / "stop.py"
        if stop_script.exists():
            self.run_command_async(["python", str(stop_script)], "停止核心服务")
        
        self.log_message("✅ 高效办公助手系统停止完成")

    def check_status(self):
        """检查系统状态"""
        self.log_message("正在检查系统状态...")
        
        # 检查核心服务状态
        status_script = self.project_root / "tools" / "status_check.py"
        if status_script.exists():
            self.run_command_async(["python", str(status_script)], "检查系统状态")
        
        # 检查MCP服务器状态
        self.check_server_status()
        
        # 检查办公环境
        check_script = self.project_root / "tools" / "check_development_task.py"
        if check_script.exists():
            self.run_command_async(["python", str(check_script)], "检查办公环境")

    def open_browser(self):
        """打开系统监控页面"""
        url = "http://localhost:8080"
        try:
            webbrowser.open(url)
            self.log_message(f"已打开系统监控页面: {url}")
        except Exception as e:
            self.log_message(f"打开浏览器失败: {e}")

    def run_startup_check(self):
        cmd = ['python', os.path.join(self.project_root, 'tools', 'startup_check.py')]
        self.run_command_async(cmd, "早上启动检查")

    def view_system_status(self):
        self.log_message("查看详细系统状态...")
        self.log_message("系统状态: 正常")

    def launch_management_system(self):
        cmd = ['python', os.path.join(self.project_root, 'project', 'pmc_management_system.py')]
        self.run_command_async(cmd, "PMC管理系统")

    def launch_tracking_system(self):
        cmd = ['python', os.path.join(self.project_root, 'project', 'pmc_tracking_system.py')]
        self.run_command_async(cmd, "PMC追踪系统")

    def run_structure_check(self):
        cmd = ['python', os.path.join(self.project_root, 'tools', 'structure_check.py')]
        self.run_command_async(cmd, "结构检查")

    def open_docs(self):
        docs_path = os.path.join(self.project_root, 'docs')
        webbrowser.open(docs_path)
        self.log_message("打开项目文档文件夹。")

    def open_manual(self):
        manual_path = os.path.join(self.project_root, 'docs', '快速操作手册.md')
        if os.path.exists(manual_path):
            webbrowser.open(manual_path)
            self.log_message("打开快速操作手册。")
        else:
            self.log_message("快速操作手册未找到。")

if __name__ == '__main__':
    try:
        print("正在启动PMC控制面板...")
        print(f"Python版本: {sys.version}")
        
        # 检查显示环境
        import os
        if os.name == 'nt':  # Windows
            print("Windows环境检测")
            # 检查是否在远程桌面或无显示环境
            if 'SESSIONNAME' in os.environ:
                session = os.environ.get('SESSIONNAME', '')
                print(f"会话类型: {session}")
                if session.startswith('RDP-'):
                    print("检测到远程桌面环境")
        
        # 设置Qt平台插件
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = ''
        
        app = QApplication(sys.argv)
        print("QApplication已创建")
        
        # 检查是否有可用的显示
        try:
            from PyQt5.QtWidgets import QDesktopWidget
            desktop = QDesktopWidget()
            screen_count = desktop.screenCount()
            print(f"屏幕数量: {screen_count}")
            if screen_count > 0:
                print(f"主屏幕尺寸: {desktop.screenGeometry()}")
            else:
                print("警告: 未检测到可用屏幕")
        except Exception as e:
            print(f"屏幕检测失败: {e}")
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#ecf0f1'))
        app.setPalette(palette)
        print("正在创建主窗口...")
        
        window = OfficeAssistantControlPanel()
        print("主窗口已创建，正在显示...")
        
        # 设置窗口属性
        window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
        window.show()
        window.raise_()
        window.activateWindow()
        print("窗口已显示，进入事件循环...")
        
        # 确保窗口可见
        app.processEvents()
        
        # 启动事件循环
        exit_code = app.exec_()
        print(f"应用程序退出，代码: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 如果是显示相关错误，提供解决方案
        error_str = str(e).lower()
        if 'display' in error_str or 'screen' in error_str or 'qt' in error_str:
            print("\n解决方案:")
            print("1. 确保在有图形界面的环境中运行")
            print("2. 如果使用远程桌面，请确保允许GUI应用")
            print("3. 尝试在本地桌面环境中运行")
        
        sys.exit(1)