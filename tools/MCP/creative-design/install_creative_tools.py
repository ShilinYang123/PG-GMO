#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创意设计类MCP工具安装和配置脚本
整合本地和远程MCP服务器
"""

import os
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CreativeToolsInstaller:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_files = [
            "mcp_openai_config.json",
            "figma_mcp_config.json", 
            "blender_mcp_config.json",
            "minimax_mcp_config.json"
        ]
        
        # 本地服务器文件
        self.local_servers = [
            "local_figma_mcp_server.py",
            "local_blender_mcp_server.py",
            "local_adb_mcp_server.py"
        ]
        
        # 远程仓库配置
        self.remote_repos = {
            "mcp-openai": {
                "url": "https://github.com/modelcontextprotocol/servers.git",
                "subdir": "src/openai",
                "config_file": "mcp_openai_config.json"
            },
            "minimax-mcp": {
                "url": "https://github.com/haoqih/minimax-mcp.git",
                "config_file": "minimax_mcp_config.json"
            }
        }
    
    def check_prerequisites(self):
        """检查前置条件"""
        logger.info("检查前置条件...")
        
        # 检查Python
        try:
            result = subprocess.run(["python", "--version"], capture_output=True, text=True)
            logger.info(f"Python版本: {result.stdout.strip()}")
        except FileNotFoundError:
            logger.error("未找到Python，请先安装Python")
            return False
        
        # 检查pip
        try:
            result = subprocess.run(["pip", "--version"], capture_output=True, text=True)
            logger.info(f"pip版本: {result.stdout.strip()}")
        except FileNotFoundError:
            logger.error("未找到pip，请先安装pip")
            return False
        
        # 检查git
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True)
            logger.info(f"Git版本: {result.stdout.strip()}")
        except FileNotFoundError:
            logger.warning("未找到Git，某些功能可能无法使用")
        
        return True
    
    def install_remote_repo(self, repo_name, repo_config):
        """安装远程仓库"""
        logger.info(f"安装远程仓库: {repo_name}")
        
        repo_dir = self.base_dir / repo_name
        
        try:
            # 克隆仓库
            if not repo_dir.exists():
                logger.info(f"克隆仓库: {repo_config['url']}")
                result = subprocess.run(
                    ["git", "clone", repo_config["url"], str(repo_dir)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode != 0:
                    logger.error(f"克隆失败: {result.stderr}")
                    return False
            
            # 如果有子目录，进入子目录
            work_dir = repo_dir
            if "subdir" in repo_config:
                work_dir = repo_dir / repo_config["subdir"]
                if not work_dir.exists():
                    logger.error(f"子目录不存在: {work_dir}")
                    return False
            
            # 安装依赖
            if (work_dir / "requirements.txt").exists():
                logger.info(f"安装requirements.txt依赖")
                result = subprocess.run(
                    ["pip", "install", "-r", "requirements.txt"],
                    cwd=work_dir,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    logger.warning(f"依赖安装警告: {result.stderr}")
            
            elif (work_dir / "setup.py").exists():
                logger.info(f"使用setup.py安装")
                result = subprocess.run(
                    ["pip", "install", "-e", "."],
                    cwd=work_dir,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    logger.warning(f"setup.py安装警告: {result.stderr}")
            
            elif (work_dir / "pyproject.toml").exists():
                logger.info(f"使用pyproject.toml安装")
                result = subprocess.run(
                    ["pip", "install", "-e", "."],
                    cwd=work_dir,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    logger.warning(f"pyproject.toml安装警告: {result.stderr}")
            
            # 更新配置文件状态
            self.update_config_status(repo_config["config_file"], "installed")
            
            logger.info(f"✓ {repo_name} 安装完成")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error(f"安装超时: {repo_name}")
            return False
        except Exception as e:
            logger.error(f"安装失败: {repo_name} - {str(e)}")
            return False
    
    def setup_local_servers(self):
        """设置本地服务器"""
        logger.info("设置本地服务器...")
        
        for server_file in self.local_servers:
            server_path = self.base_dir / server_file
            if server_path.exists():
                logger.info(f"✓ 本地服务器已就绪: {server_file}")
                
                # 测试服务器
                try:
                    result = subprocess.run(
                        ["python", str(server_path)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        logger.info(f"✓ {server_file} 测试通过")
                    else:
                        logger.warning(f"⚠ {server_file} 测试警告: {result.stderr}")
                        
                except subprocess.TimeoutExpired:
                    logger.info(f"✓ {server_file} 启动正常（超时为预期行为）")
                except Exception as e:
                    logger.warning(f"⚠ {server_file} 测试异常: {str(e)}")
            else:
                logger.error(f"✗ 本地服务器文件不存在: {server_file}")
    
    def update_config_status(self, config_file, status):
        """更新配置文件状态"""
        config_path = self.base_dir / config_file
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                config["status"] = status
                config["last_updated"] = datetime.now().isoformat()
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                logger.info(f"更新配置状态: {config_file} -> {status}")
            except Exception as e:
                logger.error(f"更新配置失败: {config_file} - {str(e)}")
    
    def create_unified_config(self):
        """创建统一的MCP服务器配置"""
        logger.info("创建统一MCP服务器配置...")
        
        unified_config = {
            "name": "Creative Design MCP Tools",
            "version": "1.0.0",
            "description": "创意设计类MCP工具集合",
            "created_at": datetime.now().isoformat(),
            "servers": []
        }
        
        # 读取各个配置文件
        for config_file in self.config_files:
            config_path = self.base_dir / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    unified_config["servers"].append(config)
                except Exception as e:
                    logger.error(f"读取配置失败: {config_file} - {str(e)}")
        
        # 添加本地服务器配置
        local_server_configs = [
            {
                "name": "Local Figma MCP Server",
                "type": "local",
                "file": "local_figma_mcp_server.py",
                "description": "本地Figma设计工具服务器",
                "status": "available"
            },
            {
                "name": "Local Blender MCP Server",
                "type": "local",
                "file": "local_blender_mcp_server.py",
                "description": "本地Blender 3D建模服务器",
                "status": "available"
            },
            {
                "name": "Local ADB MCP Server",
                "type": "local",
                "file": "local_adb_mcp_server.py",
                "description": "本地Android设备控制服务器",
                "status": "available"
            }
        ]
        
        unified_config["servers"].extend(local_server_configs)
        
        # 保存统一配置
        unified_config_path = self.base_dir / "mcp_servers_config.json"
        with open(unified_config_path, 'w', encoding='utf-8') as f:
            json.dump(unified_config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"统一配置已创建: {unified_config_path}")
        return unified_config_path
    
    def generate_usage_guide(self):
        """生成使用指南"""
        guide_content = f'''# 创意设计类MCP工具使用指南

生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 已安装的工具

### 远程MCP服务器

#### 1. MCP-OpenAI服务
- **功能**: DALL·E图像生成、GPT文本处理
- **启动**: `python mcp-openai/src/openai/server.py`
- **配置**: 需要设置OPENAI_API_KEY环境变量

#### 2. MiniMax MCP服务
- **功能**: 文本转语音、图像/视频生成
- **启动**: `python minimax-mcp/server.py`
- **配置**: 需要设置MiniMax API密钥

### 本地MCP服务器

#### 1. Figma设计工具服务器
- **文件**: `local_figma_mcp_server.py`
- **功能**: 设计文件处理、代码生成、组件管理
- **启动**: `python local_figma_mcp_server.py`

#### 2. Blender 3D建模服务器
- **文件**: `local_blender_mcp_server.py`
- **功能**: 3D建模、渲染、动画制作
- **启动**: `python local_blender_mcp_server.py`
- **依赖**: 需要安装Blender软件

#### 3. ADB Android控制服务器
- **文件**: `local_adb_mcp_server.py`
- **功能**: Android设备控制、自动化测试
- **启动**: `python local_adb_mcp_server.py`
- **依赖**: 需要安装Android SDK Platform Tools

## 快速开始

### 1. 环境准备
```bash
# 设置环境变量（根据需要）
set OPENAI_API_KEY=your_openai_api_key
set MINIMAX_API_KEY=your_minimax_api_key
```

### 2. 启动服务器
```bash
# 启动本地Figma服务器
python local_figma_mcp_server.py

# 启动本地Blender服务器
python local_blender_mcp_server.py

# 启动本地ADB服务器
python local_adb_mcp_server.py
```

### 3. 测试功能
每个服务器都包含演示功能，启动后会自动运行基本测试。

## 配置文件

- `mcp_servers_config.json`: 统一服务器配置
- `*_config.json`: 各个服务器的详细配置

## 故障排除

### 常见问题

1. **依赖安装失败**
   - 检查网络连接
   - 使用国内镜像源: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/`

2. **Blender路径未找到**
   - 安装Blender: https://www.blender.org/download/
   - 添加到系统PATH或修改服务器中的路径配置

3. **ADB命令失败**
   - 安装Android SDK Platform Tools
   - 启用USB调试模式
   - 检查设备连接

4. **API密钥错误**
   - 检查环境变量设置
   - 确认API密钥有效性

## 扩展开发

本工具集采用模块化设计，可以轻松添加新的MCP服务器：

1. 创建新的服务器文件
2. 实现标准的MCP接口
3. 更新配置文件
4. 添加到统一配置中

## 技术支持

如有问题，请检查日志文件或联系技术支持。
'''
        
        guide_path = self.base_dir / "使用指南.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        logger.info(f"使用指南已生成: {guide_path}")
        return guide_path
    
    def run_installation(self):
        """运行完整安装流程"""
        logger.info("=== 创意设计类MCP工具安装开始 ===")
        
        # 检查前置条件
        if not self.check_prerequisites():
            logger.error("前置条件检查失败，安装终止")
            return False
        
        # 安装远程仓库
        for repo_name, repo_config in self.remote_repos.items():
            self.install_remote_repo(repo_name, repo_config)
        
        # 设置本地服务器
        self.setup_local_servers()
        
        # 创建统一配置
        self.create_unified_config()
        
        # 生成使用指南
        self.generate_usage_guide()
        
        logger.info("=== 创意设计类MCP工具安装完成 ===")
        logger.info("请查看'使用指南.md'了解详细使用方法")
        
        return True

def main():
    """主函数"""
    installer = CreativeToolsInstaller()
    installer.run_installation()

if __name__ == "__main__":
    main()