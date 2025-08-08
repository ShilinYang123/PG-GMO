#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高效办公助手系统初始化工具
快速设置AI Agent开发环境和MCP服务器集群
作者：雨俊
日期：2025-01-08
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from utils import (
        get_project_root, ensure_dir_exists, create_office_structure,
        validate_office_environment, get_system_info
    )
    from mcp_server_manager import MCPServerManager
    from config_loader import load_project_config
except ImportError as e:
    print(f"警告: 无法导入某些模块: {e}")
    print("将使用基础功能继续初始化")

class OfficeAssistantInitializer:
    """高效办公助手系统初始化器
    
    功能包括：
    - 系统环境检查和设置
    - MCP服务器集群初始化
    - 办公目录结构创建
    - 配置文件验证和更新
    - AI Agent开发环境准备
    """
    
    def __init__(self, project_root: str = "s:/PG-GMO"):
        self.project_root = Path(project_root)
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志系统"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"office_init_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def check_system_requirements(self) -> Dict[str, bool]:
        """检查系统要求"""
        self.logger.info("开始检查系统要求...")
        
        requirements = {
            'python_version': sys.version_info >= (3, 8),
            'project_root_exists': self.project_root.exists(),
            'write_permission': os.access(self.project_root, os.W_OK) if self.project_root.exists() else False
        }
        
        # 检查必要的Python包
        required_packages = ['pathlib', 'json', 'logging', 'datetime']
        for package in required_packages:
            try:
                __import__(package)
                requirements[f'package_{package}'] = True
            except ImportError:
                requirements[f'package_{package}'] = False
                
        return requirements
        
    def create_project_structure(self):
        """创建项目目录结构"""
        self.logger.info("创建项目目录结构...")
        
        # 基础目录
        directories = [
            'project',
            'project/office',
            'project/output', 
            'project/MCP',
            'project/MCP/office',
            'project/MCP/design',
            'project/MCP/cad',
            'project/MCP/graphics',
            'logs',
            'docs',
            'tools'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            ensure_dir_exists(str(dir_path))
            self.logger.info(f"目录已创建: {dir_path}")
            
    def create_mcp_server_templates(self):
        """创建MCP服务器模板文件"""
        self.logger.info("创建MCP服务器模板文件...")
        
        # MCP服务器模板
        mcp_template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{server_name} MCP服务器
高效办公助手系统 - {category}类MCP服务器
作者：雨俊
日期：{date}
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime

class {class_name}:
    """MCP服务器类"""
    
    def __init__(self):
        self.server_name = "{server_name}"
        self.version = "1.0.0"
        self.capabilities = []
        
    def initialize(self):
        """初始化MCP服务器"""
        logging.info(f"初始化 {{self.server_name}} MCP服务器")
        
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理MCP请求"""
        return {{
            "status": "success",
            "data": "MCP服务器响应",
            "timestamp": datetime.now().isoformat()
        }}
        
if __name__ == "__main__":
    server = {class_name}()
    server.initialize()
'''
        
        # 创建各类MCP服务器模板
        mcp_servers = {
            'office': [
                ('Excel MCP Server', 'ExcelMCPServer', 'excel_mcp_server.py'),
                ('Word MCP Server', 'WordMCPServer', 'word_mcp_server.py'),
                ('PowerPoint MCP Server', 'PowerPointMCPServer', 'powerpoint_mcp_server.py')
            ],
            'design': [
                ('Photoshop MCP Server', 'PhotoshopMCPServer', 'photoshop_mcp_server.py')
            ],
            'cad': [
                ('AutoCAD MCP Server', 'AutoCADMCPServer', 'autocad_mcp_server.py'),
                ('General CAD MCP Server', 'GeneralCADMCPServer', 'general_cad_mcp_server.py')
            ],
            'graphics': [
                ('Illustrator MCP Server', 'IllustratorMCPServer', 'illustrator_mcp_server.py'),
                ('Excalidraw MCP Server', 'ExcalidrawMCPServer', 'excalidraw_mcp_server.py')
            ]
        }
        
        for category, servers in mcp_servers.items():
            category_dir = self.project_root / 'project' / 'MCP' / category
            for server_name, class_name, filename in servers:
                server_file = category_dir / filename
                if not server_file.exists():
                    content = mcp_template.format(
                        server_name=server_name,
                        category=category.upper(),
                        date=datetime.now().strftime('%Y-%m-%d'),
                        class_name=class_name
                    )
                    with open(server_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.logger.info(f"MCP服务器模板已创建: {server_file}")
                    
    def create_config_files(self):
        """创建配置文件"""
        self.logger.info("创建配置文件...")
        
        # 创建MCP服务器配置
        mcp_config = {
            "version": "1.0.0",
            "description": "高效办公助手系统MCP服务器集群配置",
            "created_at": datetime.now().isoformat(),
            "servers": {
                "office": {
                    "excel": {"port": 8001, "enabled": True},
                    "word": {"port": 8002, "enabled": True},
                    "powerpoint": {"port": 8003, "enabled": True}
                },
                "design": {
                    "photoshop": {"port": 8004, "enabled": True}
                },
                "cad": {
                    "autocad": {"port": 8005, "enabled": True},
                    "general_cad": {"port": 8006, "enabled": True}
                },
                "graphics": {
                    "illustrator": {"port": 8007, "enabled": True},
                    "excalidraw": {"port": 8008, "enabled": True}
                }
            }
        }
        
        config_file = self.project_root / 'project' / 'MCP' / 'mcp_config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(mcp_config, f, ensure_ascii=False, indent=2)
        self.logger.info(f"MCP配置文件已创建: {config_file}")
        
    def generate_initialization_report(self) -> str:
        """生成初始化报告"""
        system_info = {
            'system': 'Windows',
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'project_root': str(self.project_root),
            'initialization_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        report = []
        report.append("\n" + "="*80)
        report.append("高效办公助手系统初始化报告")
        report.append("="*80)
        report.append(f"初始化时间: {system_info['initialization_time']}")
        report.append(f"项目根目录: {system_info['project_root']}")
        report.append(f"Python版本: {system_info['python_version']}")
        report.append(f"操作系统: {system_info['system']}")
        report.append("")
        
        # 检查系统要求
        requirements = self.check_system_requirements()
        report.append("系统要求检查:")
        for req, status in requirements.items():
            status_icon = "✅" if status else "❌"
            report.append(f"  {status_icon} {req}: {'通过' if status else '失败'}")
        report.append("")
        
        # 目录结构
        report.append("目录结构:")
        directories = [
            'project/', 'project/office/', 'project/output/', 'project/MCP/',
            'project/MCP/office/', 'project/MCP/design/', 'project/MCP/cad/', 
            'project/MCP/graphics/', 'logs/', 'docs/', 'tools/'
        ]
        for directory in directories:
            dir_path = self.project_root / directory
            status_icon = "✅" if dir_path.exists() else "❌"
            report.append(f"  {status_icon} {directory}")
        report.append("")
        
        report.append("MCP服务器集群:")
        mcp_servers = [
            'office/excel_mcp_server.py', 'office/word_mcp_server.py', 
            'office/powerpoint_mcp_server.py', 'design/photoshop_mcp_server.py',
            'cad/autocad_mcp_server.py', 'cad/general_cad_mcp_server.py',
            'graphics/illustrator_mcp_server.py', 'graphics/excalidraw_mcp_server.py'
        ]
        for server in mcp_servers:
            server_path = self.project_root / 'project' / 'MCP' / server
            status_icon = "✅" if server_path.exists() else "❌"
            report.append(f"  {status_icon} {server}")
        report.append("")
        
        report.append("初始化完成状态:")
        all_passed = all(requirements.values())
        if all_passed:
            report.append("  ✅ 高效办公助手系统初始化成功")
            report.append("  ✅ AI Agent开发环境已准备就绪")
            report.append("  ✅ MCP服务器集群已配置完成")
        else:
            report.append("  ❌ 初始化过程中发现问题，请检查上述失败项")
            
        report.append("="*80)
        
        return "\n".join(report)
        
    def initialize_system(self):
        """执行完整的系统初始化"""
        self.logger.info("开始高效办公助手系统初始化...")
        
        try:
            # 1. 检查系统要求
            requirements = self.check_system_requirements()
            if not all(requirements.values()):
                self.logger.warning("系统要求检查发现问题，但继续初始化")
                
            # 2. 创建项目结构
            self.create_project_structure()
            
            # 3. 创建MCP服务器模板
            self.create_mcp_server_templates()
            
            # 4. 创建配置文件
            self.create_config_files()
            
            # 5. 生成报告
            report = self.generate_initialization_report()
            print(report)
            
            # 6. 保存报告
            report_file = self.project_root / 'logs' / f'init_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            self.logger.info("高效办公助手系统初始化完成")
            
        except Exception as e:
            self.logger.error(f"初始化过程中发生错误: {e}")
            raise
            
def main():
    """主函数"""
    print("\n🚀 高效办公助手系统初始化工具")
    print("作者：雨俊")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    try:
        initializer = OfficeAssistantInitializer()
        initializer.initialize_system()
        
        print("\n✅ 初始化完成！")
        print("\n下一步操作建议:")
        print("1. 检查 project/MCP/ 目录下的服务器模板")
        print("2. 根据需要修改 MCP 服务器配置")
        print("3. 运行 python tools/mcp_server_manager.py 检查服务器状态")
        print("4. 开始 AI Agent 开发工作")
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()