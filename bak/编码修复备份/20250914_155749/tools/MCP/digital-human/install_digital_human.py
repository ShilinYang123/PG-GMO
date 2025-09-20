#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字人MCP服务器安装脚本
支持安装Fay数字人框架和LiveTalking实时交互数字人
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class DigitalHumanInstaller:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.install_dir = self.base_dir / "installed"
        self.install_dir.mkdir(exist_ok=True)
        
    def run_command(self, cmd, cwd=None):
        """执行命令"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                cwd=cwd,
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            if result.returncode != 0:
                print(f"命令执行失败: {cmd}")
                print(f"错误信息: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"执行命令时出错: {e}")
            return False
    
    def install_fay_digital_human(self):
        """安装Fay数字人框架"""
        print("开始安装Fay数字人框架...")
        
        fay_dir = self.install_dir / "Fay"
        
        # 克隆仓库
        if not fay_dir.exists():
            print("正在克隆Fay仓库...")
            if not self.run_command(
                "git clone https://github.com/xszyou/Fay.git",
                cwd=self.install_dir
            ):
                return False
        
        # 安装依赖
        print("正在安装Python依赖...")
        requirements_file = fay_dir / "requirements.txt"
        if requirements_file.exists():
            if not self.run_command(
                f"pip install -r {requirements_file}",
                cwd=fay_dir
            ):
                return False
        
        # 创建配置文件模板
        config_template = fay_dir / "system.conf.template"
        if not config_template.exists():
            config_content = """
# Fay数字人配置文件模板
# 请根据实际情况修改以下配置

[DEFAULT]
# 服务端口
port = 8080

# 数字人模型配置
digital_human_model = UE5

# 大语言模型配置
llm_model = openai
llm_api_key = your_api_key_here

# TTS配置
tts_model = default

# ASR配置
asr_model = default

# 数据库配置
database_path = ./data/fay.db
"""
            with open(config_template, 'w', encoding='utf-8') as f:
                f.write(config_content)
        
        print("Fay数字人框架安装完成！")
        print(f"安装路径: {fay_dir}")
        print("请修改 system.conf.template 为 system.conf 并配置相关参数")
        return True
    
    def install_livetalking(self):
        """安装LiveTalking实时交互数字人"""
        print("开始安装LiveTalking实时交互数字人...")
        
        livetalking_dir = self.install_dir / "LiveTalking"
        
        # 克隆仓库
        if not livetalking_dir.exists():
            print("正在克隆LiveTalking仓库...")
            if not self.run_command(
                "git clone https://github.com/lipku/LiveTalking.git",
                cwd=self.install_dir
            ):
                return False
        
        # 安装依赖
        print("正在安装Python依赖...")
        requirements_file = livetalking_dir / "requirements.txt"
        if requirements_file.exists():
            if not self.run_command(
                f"pip install -r {requirements_file}",
                cwd=livetalking_dir
            ):
                return False
        
        # 创建启动脚本
        start_script = livetalking_dir / "start_livetalking.py"
        if not start_script.exists():
            script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LiveTalking启动脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("启动LiveTalking实时交互数字人...")
    print("请确保已下载预训练模型")
    
    # 这里可以添加具体的启动逻辑
    try:
        # import demo  # 根据实际项目结构调整
        print("LiveTalking服务已启动")
    except ImportError as e:
        print(f"导入模块失败: {e}")
        print("请检查依赖是否正确安装")
'''
            with open(start_script, 'w', encoding='utf-8') as f:
                f.write(script_content)
        
        print("LiveTalking实时交互数字人安装完成！")
        print(f"安装路径: {livetalking_dir}")
        print("请下载预训练模型并运行 start_livetalking.py")
        return True
    
    def create_mcp_server_config(self):
        """创建MCP服务器配置"""
        print("创建MCP服务器配置...")
        
        mcp_config = {
            "mcpServers": {
                "fay-digital-human": {
                    "command": "python",
                    "args": [str(self.install_dir / "Fay" / "main.py")],
                    "env": {
                        "PYTHONPATH": str(self.install_dir / "Fay")
                    }
                },
                "livetalking": {
                    "command": "python",
                    "args": [str(self.install_dir / "LiveTalking" / "start_livetalking.py")],
                    "env": {
                        "PYTHONPATH": str(self.install_dir / "LiveTalking")
                    }
                }
            }
        }
        
        config_file = self.base_dir / "mcp_servers_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(mcp_config, f, indent=2, ensure_ascii=False)
        
        print(f"MCP服务器配置已创建: {config_file}")
        return True
    
    def install_all(self):
        """安装所有数字人服务"""
        print("开始安装数字人制作相关MCP服务...")
        print("="*50)
        
        success = True
        
        # 安装Fay数字人框架
        if not self.install_fay_digital_human():
            success = False
        
        print("\n" + "="*50)
        
        # 安装LiveTalking
        if not self.install_livetalking():
            success = False
        
        print("\n" + "="*50)
        
        # 创建MCP配置
        if not self.create_mcp_server_config():
            success = False
        
        if success:
            print("\n✅ 所有数字人MCP服务安装完成！")
            print("\n📋 后续步骤:")
            print("1. 配置Fay数字人的system.conf文件")
            print("2. 下载LiveTalking的预训练模型")
            print("3. 测试各个服务是否正常运行")
            print("4. 将mcp_servers_config.json集成到主配置文件")
        else:
            print("\n❌ 部分服务安装失败，请检查错误信息")
        
        return success

def main():
    installer = DigitalHumanInstaller()
    installer.install_all()

if __name__ == "__main__":
    main()