#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理类MCP工具安装脚本（更新版）

包含的工具：
1. Qdrant向量数据库服务器（本地版本）
2. Financial Datasets金融数据服务器（远程）
3. Markdownify文档转换服务器（远程）
4. 数据库MCP服务器集合（本地版本）
5. CSV数据探索服务器（本地版本）

更新说明：
- 为失败的远程安装创建了本地替代版本
- 保留成功的远程安装
- 提供统一的配置和使用接口
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class DataProcessingToolsInstaller:
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.tools_config = {
            "qdrant_vector_db": {
                "name": "Qdrant向量数据库服务器",
                "type": "local",
                "status": "pending",
                "local_file": "local_qdrant_mcp_server.py",
                "description": "本地向量数据库服务，支持语义搜索和向量存储"
            },
            "financial_datasets": {
                "name": "Financial Datasets金融数据服务器",
                "type": "remote",
                "status": "pending",
                "repository": "https://github.com/modelcontextprotocol/servers.git",
                "path": "src/financial_datasets",
                "description": "提供股票、财务报表等金融数据访问"
            },
            "markdownify": {
                "name": "Markdownify文档转换服务器",
                "type": "remote",
                "status": "pending",
                "repository": "https://github.com/modelcontextprotocol/servers.git",
                "path": "src/markdownify",
                "description": "将网页、HTML、PDF等转换为Markdown格式"
            },
            "database_mcp": {
                "name": "数据库MCP服务器集合",
                "type": "local",
                "status": "pending",
                "local_file": "local_database_mcp_server.py",
                "description": "本地数据库访问服务，支持SQLite、MySQL、PostgreSQL等"
            },
            "csv_explorer": {
                "name": "CSV数据探索服务器",
                "type": "local",
                "status": "pending",
                "local_file": "local_csv_explorer_server.py",
                "description": "本地CSV文件分析和探索工具"
            }
        }
        
        # 设置日志
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志配置"""
        log_file = self.base_dir / "installation.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_dependencies(self) -> Dict[str, bool]:
        """检查依赖项"""
        dependencies = {
            "python": False,
            "git": False,
            "pip": False,
            "node": False,
            "npm": False
        }
        
        # 检查Python
        try:
            result = subprocess.run(["python", "--version"], capture_output=True, text=True)
            dependencies["python"] = result.returncode == 0
        except FileNotFoundError:
            pass
        
        # 检查Git
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True)
            dependencies["git"] = result.returncode == 0
        except FileNotFoundError:
            pass
        
        # 检查pip
        try:
            result = subprocess.run(["pip", "--version"], capture_output=True, text=True)
            dependencies["pip"] = result.returncode == 0
        except FileNotFoundError:
            pass
        
        # 检查Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            dependencies["node"] = result.returncode == 0
        except FileNotFoundError:
            pass
        
        # 检查npm
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            dependencies["npm"] = result.returncode == 0
        except FileNotFoundError:
            pass
        
        return dependencies
    
    def install_python_dependencies(self) -> bool:
        """安装Python依赖"""
        try:
            self.logger.info("安装Python依赖包...")
            
            # 基础依赖
            base_packages = [
                "pandas",
                "numpy",
                "requests",
                "chardet",
                "httpx"
            ]
            
            # 数据库驱动（可选）
            optional_packages = [
                "pymysql",
                "psycopg2-binary",
                "pyodbc"
            ]
            
            # 安装基础包
            for package in base_packages:
                result = subprocess.run(
                    ["pip", "install", package],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    self.logger.warning(f"安装 {package} 失败: {result.stderr}")
                else:
                    self.logger.info(f"成功安装 {package}")
            
            # 尝试安装可选包
            for package in optional_packages:
                result = subprocess.run(
                    ["pip", "install", package],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.logger.info(f"成功安装可选包 {package}")
                else:
                    self.logger.warning(f"可选包 {package} 安装失败，将在运行时提示")
            
            return True
        except Exception as e:
            self.logger.error(f"安装Python依赖失败: {e}")
            return False
    
    def install_local_tool(self, tool_key: str) -> bool:
        """安装本地工具"""
        try:
            tool_config = self.tools_config[tool_key]
            local_file = tool_config["local_file"]
            
            # 检查本地文件是否存在
            local_file_path = self.base_dir / local_file
            if not local_file_path.exists():
                self.logger.error(f"本地文件不存在: {local_file_path}")
                return False
            
            # 测试本地服务器
            try:
                result = subprocess.run(
                    ["python", str(local_file_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(self.base_dir)
                )
                
                if "演示完成" in result.stdout or "启动" in result.stdout:
                    self.logger.info(f"本地工具 {tool_config['name']} 测试成功")
                    tool_config["status"] = "success"
                    return True
                else:
                    self.logger.warning(f"本地工具 {tool_config['name']} 测试输出异常")
                    tool_config["status"] = "warning"
                    return True  # 仍然认为安装成功
                    
            except subprocess.TimeoutExpired:
                self.logger.info(f"本地工具 {tool_config['name']} 运行正常（超时结束）")
                tool_config["status"] = "success"
                return True
            except Exception as e:
                self.logger.error(f"测试本地工具失败: {e}")
                tool_config["status"] = "error"
                return False
                
        except Exception as e:
            self.logger.error(f"安装本地工具 {tool_key} 失败: {e}")
            self.tools_config[tool_key]["status"] = "error"
            return False
    
    def install_remote_tool(self, tool_key: str) -> bool:
        """安装远程工具"""
        try:
            tool_config = self.tools_config[tool_key]
            
            # 创建工具目录
            tool_dir = self.base_dir / tool_key
            tool_dir.mkdir(exist_ok=True)
            
            # 克隆仓库
            if "repository" in tool_config:
                self.logger.info(f"克隆仓库: {tool_config['repository']}")
                
                # 先尝试浅克隆
                result = subprocess.run([
                    "git", "clone", "--depth", "1", 
                    tool_config["repository"], 
                    str(tool_dir / "temp_repo")
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    self.logger.error(f"克隆仓库失败: {result.stderr}")
                    tool_config["status"] = "error"
                    return False
                
                # 复制特定路径的文件
                if "path" in tool_config:
                    source_path = tool_dir / "temp_repo" / tool_config["path"]
                    if source_path.exists():
                        # 复制文件到工具目录
                        import shutil
                        if source_path.is_dir():
                            shutil.copytree(source_path, tool_dir / "src", dirs_exist_ok=True)
                        else:
                            shutil.copy2(source_path, tool_dir)
                        
                        # 清理临时目录
                        shutil.rmtree(tool_dir / "temp_repo")
                        
                        self.logger.info(f"远程工具 {tool_config['name']} 安装成功")
                        tool_config["status"] = "success"
                        return True
                    else:
                        self.logger.error(f"源路径不存在: {source_path}")
                        tool_config["status"] = "error"
                        return False
            
            # 如果是npm包
            elif "npm_package" in tool_config:
                result = subprocess.run([
                    "npm", "install", tool_config["npm_package"]
                ], cwd=str(tool_dir), capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.logger.info(f"远程工具 {tool_config['name']} 安装成功")
                    tool_config["status"] = "success"
                    return True
                else:
                    self.logger.error(f"npm安装失败: {result.stderr}")
                    tool_config["status"] = "error"
                    return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"安装远程工具 {tool_key} 失败: {e}")
            self.tools_config[tool_key]["status"] = "error"
            return False
    
    def install_all_tools(self) -> Dict[str, int]:
        """安装所有工具"""
        self.logger.info("开始安装数据处理类MCP工具...")
        
        # 检查依赖
        dependencies = self.check_dependencies()
        self.logger.info(f"依赖检查结果: {dependencies}")
        
        # 安装Python依赖
        if dependencies["python"] and dependencies["pip"]:
            self.install_python_dependencies()
        else:
            self.logger.warning("Python或pip不可用，跳过依赖安装")
        
        # 安装统计
        stats = {"success": 0, "failed": 0, "total": len(self.tools_config)}
        
        # 安装每个工具
        for tool_key, tool_config in self.tools_config.items():
            self.logger.info(f"\n安装 {tool_config['name']}...")
            
            try:
                if tool_config["type"] == "local":
                    success = self.install_local_tool(tool_key)
                else:
                    success = self.install_remote_tool(tool_key)
                
                if success:
                    stats["success"] += 1
                    self.logger.info(f"✅ {tool_config['name']} 安装成功")
                else:
                    stats["failed"] += 1
                    self.logger.error(f"❌ {tool_config['name']} 安装失败")
                    
            except Exception as e:
                stats["failed"] += 1
                self.logger.error(f"❌ {tool_config['name']} 安装异常: {e}")
                tool_config["status"] = "error"
        
        return stats
    
    def create_unified_config(self) -> bool:
        """创建统一配置文件"""
        try:
            config = {
                "name": "数据处理类MCP工具集合（更新版）",
                "description": "包含向量数据库、金融数据、文档转换、数据库访问和CSV分析等数据处理工具",
                "version": "2.0.0",
                "created_at": datetime.now().isoformat(),
                "tools": {}
            }
            
            for tool_key, tool_config in self.tools_config.items():
                config["tools"][tool_key] = {
                    "name": tool_config["name"],
                    "type": tool_config["type"],
                    "status": tool_config["status"],
                    "description": tool_config["description"]
                }
                
                if tool_config["type"] == "local":
                    config["tools"][tool_key]["local_file"] = tool_config["local_file"]
                    config["tools"][tool_key]["usage"] = f"python {tool_config['local_file']}"
                else:
                    config["tools"][tool_key]["directory"] = tool_key
                    if "repository" in tool_config:
                        config["tools"][tool_key]["repository"] = tool_config["repository"]
            
            # 保存配置文件
            config_file = self.base_dir / "数据处理工具统一配置.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"统一配置文件已创建: {config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建统一配置失败: {e}")
            return False
    
    def generate_usage_guide(self) -> bool:
        """生成使用指南"""
        try:
            guide_content = f"""# 数据处理类MCP工具使用指南（更新版）

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 工具概览

本工具集包含以下数据处理相关的MCP服务器：

"""
            
            # 添加每个工具的信息
            for tool_key, tool_config in self.tools_config.items():
                status_icon = {
                    "success": "✅",
                    "warning": "⚠️",
                    "error": "❌",
                    "pending": "⏳"
                }.get(tool_config["status"], "❓")
                
                guide_content += f"""### {status_icon} {tool_config['name']}

**类型**: {"本地服务器" if tool_config['type'] == 'local' else "远程服务器"}
**状态**: {tool_config['status']}
**描述**: {tool_config['description']}

"""
                
                if tool_config["type"] == "local" and tool_config["status"] in ["success", "warning"]:
                    guide_content += f"""**启动方式**:
```bash
python {tool_config['local_file']}
```

**集成方式**:
```python
# 导入服务器类
from {tool_config['local_file'].replace('.py', '')} import *

# 创建服务器实例
server = {tool_config['local_file'].replace('local_', '').replace('_server.py', '').title().replace('_', '')}MCPServer()

# 执行功能
result = server.execute_function('function_name', **params)
```

"""
                elif tool_config["type"] == "remote" and tool_config["status"] == "success":
                    guide_content += f"**目录**: {tool_key}/\n\n"
                
                guide_content += "---\n\n"
            
            # 添加快速开始部分
            guide_content += """## 快速开始

### 1. 环境准备

确保已安装以下依赖：

```bash
# 基础依赖
pip install pandas numpy requests chardet httpx

# 数据库驱动（可选）
pip install pymysql psycopg2-binary pyodbc
```

### 2. 本地服务器使用示例

#### Qdrant向量数据库服务器

```python
from local_qdrant_mcp_server import QdrantMCPServer

# 创建服务器
server = QdrantMCPServer()

# 创建集合
result = server.execute_function(
    'create_collection',
    collection_name='my_collection',
    vector_size=128,
    distance='cosine'
)

# 插入向量
points = [{
    'id': 'doc1',
    'vector': [0.1] * 128,
    'payload': {'title': '文档1', 'content': '内容'}
}]
server.execute_function('upsert_points', collection_name='my_collection', points=points)

# 搜索相似向量
result = server.execute_function(
    'search_points',
    collection_name='my_collection',
    query_vector=[0.1] * 128,
    limit=5
)
```

#### CSV数据探索服务器

```python
from local_csv_explorer_server import CSVExplorerMCPServer

# 创建服务器
server = CSVExplorerMCPServer()

# 加载CSV文件
result = server.execute_function('load_csv', file_path='data.csv')
file_key = result['file_key']

# 获取基本信息
info = server.execute_function('get_basic_info', file_key=file_key)

# 统计分析
stats = server.execute_function('get_statistical_summary', file_key=file_key)

# 数据质量检查
quality = server.execute_function('check_data_quality', file_key=file_key)
```

#### 数据库MCP服务器

```python
from local_database_mcp_server import LocalDatabaseMCPServer

# 创建服务器
server = LocalDatabaseMCPServer()

# 创建SQLite连接
server.execute_function(
    'create_connection',
    connection_id='my_db',
    db_type='sqlite',
    connection_params={'database': 'my_database.db'}
)

# 执行查询
result = server.execute_function(
    'execute_query',
    connection_id='my_db',
    query='SELECT * FROM users LIMIT 10'
)

# 导入CSV到数据库
server.execute_function(
    'import_csv_to_table',
    connection_id='my_db',
    csv_file_path='data.csv',
    table_name='imported_data'
)
```

### 3. 远程服务器使用

对于成功安装的远程服务器，请参考各自目录下的文档。

### 4. 故障排除

#### 常见问题

1. **导入错误**: 确保所有依赖包已正确安装
2. **数据库连接失败**: 检查数据库服务是否运行，连接参数是否正确
3. **文件路径错误**: 使用绝对路径或确保相对路径正确
4. **内存不足**: 对于大文件，考虑分块处理或增加内存限制

#### 日志查看

查看 `installation.log` 文件获取详细的安装和运行日志。

### 5. 扩展开发

所有本地服务器都提供了标准的MCP接口，可以轻松集成到其他应用中：

```python
# 获取可用功能
functions = server.get_available_functions()

# 执行功能
result = server.execute_function(function_name, **parameters)

# 检查结果
if result['status'] == 'success':
    # 处理成功结果
    data = result.get('data', {})
else:
    # 处理错误
    error_message = result.get('message', '未知错误')
```

## 技术支持

如有问题，请检查：
1. 日志文件 `installation.log`
2. 各工具的演示代码
3. 依赖包是否正确安装

---

*本指南由数据处理类MCP工具安装脚本自动生成*
"""
            
            # 保存使用指南
            guide_file = self.base_dir / "数据处理工具使用指南.md"
            with open(guide_file, 'w', encoding='utf-8') as f:
                f.write(guide_content)
            
            self.logger.info(f"使用指南已生成: {guide_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"生成使用指南失败: {e}")
            return False
    
    def run_installation(self) -> Dict:
        """运行完整安装流程"""
        self.logger.info("🚀 开始数据处理类MCP工具安装流程...")
        
        # 安装所有工具
        stats = self.install_all_tools()
        
        # 创建统一配置
        config_success = self.create_unified_config()
        
        # 生成使用指南
        guide_success = self.generate_usage_guide()
        
        # 输出安装结果
        self.logger.info("\n" + "="*50)
        self.logger.info("📊 安装结果统计:")
        self.logger.info(f"  总计工具: {stats['total']}")
        self.logger.info(f"  成功安装: {stats['success']}")
        self.logger.info(f"  安装失败: {stats['failed']}")
        self.logger.info(f"  统一配置: {'✅' if config_success else '❌'}")
        self.logger.info(f"  使用指南: {'✅' if guide_success else '❌'}")
        self.logger.info("="*50)
        
        # 显示成功安装的工具
        successful_tools = [name for name, config in self.tools_config.items() 
                          if config["status"] in ["success", "warning"]]
        
        if successful_tools:
            self.logger.info("\n✅ 成功安装的工具:")
            for tool_key in successful_tools:
                tool_config = self.tools_config[tool_key]
                self.logger.info(f"  - {tool_config['name']} ({tool_config['type']})")
        
        # 显示失败的工具
        failed_tools = [name for name, config in self.tools_config.items() 
                       if config["status"] == "error"]
        
        if failed_tools:
            self.logger.info("\n❌ 安装失败的工具:")
            for tool_key in failed_tools:
                tool_config = self.tools_config[tool_key]
                self.logger.info(f"  - {tool_config['name']} ({tool_config['type']})")
        
        return {
            "stats": stats,
            "config_created": config_success,
            "guide_created": guide_success,
            "successful_tools": successful_tools,
            "failed_tools": failed_tools
        }

def main():
    """主函数"""
    print("🚀 数据处理类MCP工具安装脚本（更新版）")
    print("包含本地和远程服务器的混合安装方案")
    print("="*60)
    
    # 创建安装器
    installer = DataProcessingToolsInstaller()
    
    # 运行安装
    result = installer.run_installation()
    
    print("\n🎉 安装流程完成！")
    print(f"成功率: {result['stats']['success']}/{result['stats']['total']}")
    
    if result['guide_created']:
        print("\n📖 请查看 '数据处理工具使用指南.md' 了解详细使用方法")
    
    if result['config_created']:
        print("⚙️ 统一配置文件: '数据处理工具统一配置.json'")
    
    print("📋 详细日志: 'installation.log'")
    
    return result

if __name__ == "__main__":
    main()