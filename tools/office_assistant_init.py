#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楂樻晥鍔炲叕鍔╂墜绯荤粺鍒濆鍖栧伐鍏?蹇€熻缃瓵I Agent寮€鍙戠幆澧冨拰MCP鏈嶅姟鍣ㄩ泦缇?浣滆€咃細闆ㄤ繆
鏃ユ湡锛?025-01-08
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 娣诲姞褰撳墠鐩綍鍒癙ython璺緞
sys.path.insert(0, str(Path(__file__).parent))

try:
    from utils import (
        get_project_root, ensure_dir_exists, create_office_structure,
        validate_office_environment, get_system_info
    )
    from mcp_server_manager import MCPServerManager
    from config_loader import load_project_config
except ImportError as e:
    print(f"璀﹀憡: 鏃犳硶瀵煎叆鏌愪簺妯″潡: {e}")
    print("灏嗕娇鐢ㄥ熀纭€鍔熻兘缁х画鍒濆鍖?)

class OfficeAssistantInitializer:
    """楂樻晥鍔炲叕鍔╂墜绯荤粺鍒濆鍖栧櫒
    
    鍔熻兘鍖呮嫭锛?    - 绯荤粺鐜妫€鏌ュ拰璁剧疆
    - MCP鏈嶅姟鍣ㄩ泦缇ゅ垵濮嬪寲
    - 鍔炲叕鐩綍缁撴瀯鍒涘缓
    - 閰嶇疆鏂囦欢楠岃瘉鍜屾洿鏂?    - AI Agent寮€鍙戠幆澧冨噯澶?    """
    
    def __init__(self, project_root: str = "s:/PG-GMO"):
        self.project_root = Path(project_root)
        self.setup_logging()
        
    def setup_logging(self):
        """璁剧疆鏃ュ織绯荤粺"""
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
        """妫€鏌ョ郴缁熻姹?""
        self.logger.info("寮€濮嬫鏌ョ郴缁熻姹?..")
        
        requirements = {
            'python_version': sys.version_info >= (3, 8),
            'project_root_exists': self.project_root.exists(),
            'write_permission': os.access(self.project_root, os.W_OK) if self.project_root.exists() else False
        }
        
        # 妫€鏌ュ繀瑕佺殑Python鍖?        required_packages = ['pathlib', 'json', 'logging', 'datetime']
        for package in required_packages:
            try:
                __import__(package)
                requirements[f'package_{package}'] = True
            except ImportError:
                requirements[f'package_{package}'] = False
                
        return requirements
        
    def create_project_structure(self):
        """鍒涘缓椤圭洰鐩綍缁撴瀯"""
        self.logger.info("鍒涘缓椤圭洰鐩綍缁撴瀯...")
        
        # 鍩虹鐩綍
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
            self.logger.info(f"鐩綍宸插垱寤? {dir_path}")
            
    def create_mcp_server_templates(self):
        """鍒涘缓MCP鏈嶅姟鍣ㄦā鏉挎枃浠?""
        self.logger.info("鍒涘缓MCP鏈嶅姟鍣ㄦā鏉挎枃浠?..")
        
        # MCP鏈嶅姟鍣ㄦā鏉?        mcp_template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{server_name} MCP鏈嶅姟鍣?楂樻晥鍔炲叕鍔╂墜绯荤粺 - {category}绫籑CP鏈嶅姟鍣?浣滆€咃細闆ㄤ繆
鏃ユ湡锛歿date}
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime

class {class_name}:
    """MCP鏈嶅姟鍣ㄧ被"""
    
    def __init__(self):
        self.server_name = "{server_name}"
        self.version = "1.0.0"
        self.capabilities = []
        
    def initialize(self):
        """鍒濆鍖朚CP鏈嶅姟鍣?""
        logging.info(f"鍒濆鍖?{{self.server_name}} MCP鏈嶅姟鍣?)
        
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """澶勭悊MCP璇锋眰"""
        return {{
            "status": "success",
            "data": "MCP鏈嶅姟鍣ㄥ搷搴?,
            "timestamp": datetime.now().isoformat()
        }}
        
if __name__ == "__main__":
    server = {class_name}()
    server.initialize()
'''
        
        # 鍒涘缓鍚勭被MCP鏈嶅姟鍣ㄦā鏉?        mcp_servers = {
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
                    self.logger.info(f"MCP鏈嶅姟鍣ㄦā鏉垮凡鍒涘缓: {server_file}")
                    
    def create_config_files(self):
        """鍒涘缓閰嶇疆鏂囦欢"""
        self.logger.info("鍒涘缓閰嶇疆鏂囦欢...")
        
        # 鍒涘缓MCP鏈嶅姟鍣ㄩ厤缃?        mcp_config = {
            "version": "1.0.0",
            "description": "楂樻晥鍔炲叕鍔╂墜绯荤粺MCP鏈嶅姟鍣ㄩ泦缇ら厤缃?,
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
        self.logger.info(f"MCP閰嶇疆鏂囦欢宸插垱寤? {config_file}")
        
    def generate_initialization_report(self) -> str:
        """鐢熸垚鍒濆鍖栨姤鍛?""
        system_info = {
            'system': 'Windows',
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'project_root': str(self.project_root),
            'initialization_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        report = []
        report.append("\n" + "="*80)
        report.append("楂樻晥鍔炲叕鍔╂墜绯荤粺鍒濆鍖栨姤鍛?)
        report.append("="*80)
        report.append(f"鍒濆鍖栨椂闂? {system_info['initialization_time']}")
        report.append(f"椤圭洰鏍圭洰褰? {system_info['project_root']}")
        report.append(f"Python鐗堟湰: {system_info['python_version']}")
        report.append(f"鎿嶄綔绯荤粺: {system_info['system']}")
        report.append("")
        
        # 妫€鏌ョ郴缁熻姹?        requirements = self.check_system_requirements()
        report.append("绯荤粺瑕佹眰妫€鏌?")
        for req, status in requirements.items():
            status_icon = "鉁? if status else "鉂?
            report.append(f"  {status_icon} {req}: {'閫氳繃' if status else '澶辫触'}")
        report.append("")
        
        # 鐩綍缁撴瀯
        report.append("鐩綍缁撴瀯:")
        directories = [
            'project/', 'project/office/', 'project/02-Output/', 'project/MCP/',
            'project/MCP/office/', 'project/MCP/design/', 'project/MCP/cad/', 
            'project/MCP/graphics/', 'logs/', 'docs/', 'tools/'
        ]
        for directory in directories:
            dir_path = self.project_root / directory
            status_icon = "鉁? if dir_path.exists() else "鉂?
            report.append(f"  {status_icon} {directory}")
        report.append("")
        
        report.append("MCP鏈嶅姟鍣ㄩ泦缇?")
        mcp_servers = [
            'office/excel_mcp_server.py', 'office/word_mcp_server.py', 
            'office/powerpoint_mcp_server.py', 'design/photoshop_mcp_server.py',
            'cad/autocad_mcp_server.py', 'cad/general_cad_mcp_server.py',
            'graphics/illustrator_mcp_server.py', 'graphics/excalidraw_mcp_server.py'
        ]
        for server in mcp_servers:
            server_path = self.project_root / 'project' / 'MCP' / server
            status_icon = "鉁? if server_path.exists() else "鉂?
            report.append(f"  {status_icon} {server}")
        report.append("")
        
        report.append("鍒濆鍖栧畬鎴愮姸鎬?")
        all_passed = all(requirements.values())
        if all_passed:
            report.append("  鉁?楂樻晥鍔炲叕鍔╂墜绯荤粺鍒濆鍖栨垚鍔?)
            report.append("  鉁?AI Agent寮€鍙戠幆澧冨凡鍑嗗灏辩华")
            report.append("  鉁?MCP鏈嶅姟鍣ㄩ泦缇ゅ凡閰嶇疆瀹屾垚")
        else:
            report.append("  鉂?鍒濆鍖栬繃绋嬩腑鍙戠幇闂锛岃妫€鏌ヤ笂杩板け璐ラ」")
            
        report.append("="*80)
        
        return "\n".join(report)
        
    def initialize_system(self):
        """鎵ц瀹屾暣鐨勭郴缁熷垵濮嬪寲"""
        self.logger.info("寮€濮嬮珮鏁堝姙鍏姪鎵嬬郴缁熷垵濮嬪寲...")
        
        try:
            # 1. 妫€鏌ョ郴缁熻姹?            requirements = self.check_system_requirements()
            if not all(requirements.values()):
                self.logger.warning("绯荤粺瑕佹眰妫€鏌ュ彂鐜伴棶棰橈紝浣嗙户缁垵濮嬪寲")
                
            # 2. 鍒涘缓椤圭洰缁撴瀯
            self.create_project_structure()
            
            # 3. 鍒涘缓MCP鏈嶅姟鍣ㄦā鏉?            self.create_mcp_server_templates()
            
            # 4. 鍒涘缓閰嶇疆鏂囦欢
            self.create_config_files()
            
            # 5. 鐢熸垚鎶ュ憡
            report = self.generate_initialization_report()
            print(report)
            
            # 6. 淇濆瓨鎶ュ憡
            report_file = self.project_root / 'logs' / f'init_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            self.logger.info("楂樻晥鍔炲叕鍔╂墜绯荤粺鍒濆鍖栧畬鎴?)
            
        except Exception as e:
            self.logger.error(f"鍒濆鍖栬繃绋嬩腑鍙戠敓閿欒: {e}")
            raise
            
def main():
    """涓诲嚱鏁?""
    print("\n馃殌 楂樻晥鍔炲叕鍔╂墜绯荤粺鍒濆鍖栧伐鍏?)
    print("浣滆€咃細闆ㄤ繆")
    print(f"鏃堕棿锛歿datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    try:
        initializer = OfficeAssistantInitializer()
        initializer.initialize_system()
        
        print("\n鉁?鍒濆鍖栧畬鎴愶紒")
        print("\n涓嬩竴姝ユ搷浣滃缓璁?")
        print("1. 妫€鏌?project/MCP/ 鐩綍涓嬬殑鏈嶅姟鍣ㄦā鏉?)
        print("2. 鏍规嵁闇€瑕佷慨鏀?MCP 鏈嶅姟鍣ㄩ厤缃?)
        print("3. 杩愯 python tools/mcp_server_manager.py 妫€鏌ユ湇鍔″櫒鐘舵€?)
        print("4. 寮€濮?AI Agent 寮€鍙戝伐浣?)
        
    except Exception as e:
        print(f"\n鉂?鍒濆鍖栧け璐? {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
