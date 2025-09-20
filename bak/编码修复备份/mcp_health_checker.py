#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP工具完整性检查器
解决每次使用MCP工具时都需要临时安装依赖的问题

功能：
1. 检查所有MCP服务器的依赖是否已安装
2. 进行基本功能测试
3. 生成详细的健康报告
4. 提供一键修复功能
"""

import os
import sys
import subprocess
import importlib
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class MCPHealthChecker:
    def __init__(self, mcp_root_dir: str = "S:\\PG-GMO\\tools\\MCP"):
        self.mcp_root = Path(mcp_root_dir)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "servers": {},
            "summary": {
                "total_servers": 0,
                "healthy_servers": 0,
                "unhealthy_servers": 0,
                "missing_dependencies": [],
                "failed_tests": []
            }
        }
    
    def find_mcp_servers(self) -> List[Path]:
        """查找所有MCP服务器目录"""
        servers = []
        for item in self.mcp_root.rglob("*"):
            if item.is_dir() and (item / "requirements.txt").exists():
                servers.append(item)
        return servers
    
    def check_dependencies(self, requirements_file: Path) -> Tuple[List[str], List[str]]:
        """检查依赖是否已安装"""
        installed = []
        missing = []
        
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            for req in requirements:
                # 简化包名（去除版本号等）
                package_name = req.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].strip()
                
                try:
                    importlib.import_module(package_name.replace('-', '_'))
                    installed.append(package_name)
                except ImportError:
                    try:
                        # 尝试使用pip show检查
                        result = subprocess.run(['pip', 'show', package_name], 
                                              capture_output=True, text=True)
                        if result.returncode == 0:
                            installed.append(package_name)
                        else:
                            missing.append(package_name)
                    except:
                        missing.append(package_name)
        
        except Exception as e:
            print(f"读取requirements.txt失败: {e}")
            return [], []
        
        return installed, missing
    
    def test_server_functionality(self, server_path: Path) -> Dict[str, any]:
        """测试服务器基本功能"""
        test_result = {
            "import_test": False,
            "basic_function_test": False,
            "error_messages": []
        }
        
        # 测试主要Python文件是否可以导入
        main_files = list(server_path.glob("*.py"))
        if main_files:
            try:
                # 临时添加服务器路径到sys.path
                sys.path.insert(0, str(server_path))
                
                for py_file in main_files:
                    if py_file.name.startswith('__'):
                        continue
                    
                    module_name = py_file.stem
                    try:
                        importlib.import_module(module_name)
                        test_result["import_test"] = True
                        break
                    except Exception as e:
                        test_result["error_messages"].append(f"导入{module_name}失败: {str(e)}")
                
                # 移除临时路径
                sys.path.remove(str(server_path))
                
            except Exception as e:
                test_result["error_messages"].append(f"测试失败: {str(e)}")
        
        return test_result
    
    def check_server(self, server_path: Path) -> Dict[str, any]:
        """检查单个MCP服务器"""
        server_name = server_path.name
        print(f"检查服务器: {server_name}")
        
        result = {
            "name": server_name,
            "path": str(server_path),
            "status": "unknown",
            "dependencies": {
                "installed": [],
                "missing": []
            },
            "functionality_test": {},
            "recommendations": []
        }
        
        # 检查依赖
        requirements_file = server_path / "requirements.txt"
        if requirements_file.exists():
            installed, missing = self.check_dependencies(requirements_file)
            result["dependencies"]["installed"] = installed
            result["dependencies"]["missing"] = missing
            
            if missing:
                result["recommendations"].append(f"需要安装依赖: {', '.join(missing)}")
                self.results["summary"]["missing_dependencies"].extend(missing)
        
        # 功能测试
        if not result["dependencies"]["missing"]:
            result["functionality_test"] = self.test_server_functionality(server_path)
            if not result["functionality_test"]["import_test"]:
                result["recommendations"].append("导入测试失败，可能存在代码问题")
                self.results["summary"]["failed_tests"].append(server_name)
        else:
            result["functionality_test"] = {"skipped": "由于缺少依赖而跳过功能测试"}
        
        # 确定整体状态
        if not result["dependencies"]["missing"] and result["functionality_test"].get("import_test", False):
            result["status"] = "healthy"
            self.results["summary"]["healthy_servers"] += 1
        else:
            result["status"] = "unhealthy"
            self.results["summary"]["unhealthy_servers"] += 1
        
        return result
    
    def generate_master_requirements(self, servers: List[Path]) -> str:
        """生成主依赖文件"""
        all_requirements = set()
        
        for server_path in servers:
            requirements_file = server_path / "requirements.txt"
            if requirements_file.exists():
                try:
                    with open(requirements_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                all_requirements.add(line)
                except Exception as e:
                    print(f"读取{requirements_file}失败: {e}")
        
        return '\n'.join(sorted(all_requirements))
    
    def install_missing_dependencies(self) -> bool:
        """安装所有缺失的依赖"""
        missing_deps = list(set(self.results["summary"]["missing_dependencies"]))
        if not missing_deps:
            print("没有缺失的依赖需要安装")
            return True
        
        print(f"准备安装 {len(missing_deps)} 个缺失的依赖...")
        
        for dep in missing_deps:
            try:
                print(f"安装 {dep}...")
                result = subprocess.run(['pip', 'install', dep], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {dep} 安装成功")
                else:
                    print(f"❌ {dep} 安装失败: {result.stderr}")
                    return False
            except Exception as e:
                print(f"❌ 安装 {dep} 时出错: {e}")
                return False
        
        return True
    
    def check_all_servers(self) -> Dict[str, any]:
        """检查所有服务器"""
        print("🔍 开始MCP工具完整性检查...")
        print(f"MCP根目录: {self.mcp_root}")
        
        servers = self.find_mcp_servers()
        self.results["summary"]["total_servers"] = len(servers)
        
        print(f"发现 {len(servers)} 个MCP服务器")
        
        for server_path in servers:
            server_result = self.check_server(server_path)
            self.results["servers"][server_result["name"]] = server_result
        
        # 生成主依赖文件
        master_requirements = self.generate_master_requirements(servers)
        master_req_file = self.mcp_root / "master_requirements.txt"
        
        try:
            with open(master_req_file, 'w', encoding='utf-8') as f:
                f.write(master_requirements)
            print(f"✅ 主依赖文件已生成: {master_req_file}")
        except Exception as e:
            print(f"❌ 生成主依赖文件失败: {e}")
        
        return self.results
    
    def print_summary(self):
        """打印检查摘要"""
        summary = self.results["summary"]
        
        print("\n" + "="*60)
        print("📋 MCP工具健康检查报告")
        print("="*60)
        print(f"检查时间: {self.results['timestamp']}")
        print(f"总服务器数: {summary['total_servers']}")
        print(f"健康服务器: {summary['healthy_servers']} ✅")
        print(f"不健康服务器: {summary['unhealthy_servers']} ❌")
        
        if summary['missing_dependencies']:
            print(f"\n缺失依赖 ({len(set(summary['missing_dependencies']))})个):")
            for dep in sorted(set(summary['missing_dependencies'])):
                print(f"  - {dep}")
        
        if summary['failed_tests']:
            print(f"\n功能测试失败的服务器:")
            for server in summary['failed_tests']:
                print(f"  - {server}")
        
        print("\n" + "="*60)
        
        # 详细服务器状态
        print("\n📊 详细服务器状态:")
        for name, server in self.results["servers"].items():
            status_icon = "✅" if server["status"] == "healthy" else "❌"
            print(f"  {status_icon} {name}: {server['status']}")
            
            if server["dependencies"]["missing"]:
                print(f"    缺失依赖: {', '.join(server['dependencies']['missing'])}")
            
            if server["recommendations"]:
                for rec in server["recommendations"]:
                    print(f"    建议: {rec}")
    
    def save_report(self, output_file: str = None):
        """保存详细报告"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"S:\\PG-GMO\\logs\\mcp_health_report_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"\n📄 详细报告已保存: {output_file}")
        except Exception as e:
            print(f"❌ 保存报告失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='MCP服务器健康检查工具')
    parser.add_argument('--auto-install', action='store_true', help='自动安装缺失的依赖')
    args = parser.parse_args()
    
    checker = MCPHealthChecker()
    
    # 运行完整检查
    results = checker.check_all_servers()
    
    # 打印摘要
    checker.print_summary()
    
    # 保存报告
    checker.save_report()
    
    # 处理缺失依赖
    if checker.results["summary"]["missing_dependencies"]:
        if args.auto_install:
            print("\n🚀 自动安装模式：开始安装缺失依赖...")
            if checker.install_missing_dependencies():
                print("\n✅ 所有依赖安装完成！建议重新运行检查验证。")
            else:
                print("\n❌ 部分依赖安装失败，请手动检查。")
        else:
            print("\n🔧 发现缺失的依赖，是否自动安装？")
            response = input("输入 'y' 或 'yes' 确认安装: ").lower().strip()
            
            if response in ['y', 'yes']:
                print("\n🚀 开始自动安装缺失依赖...")
                if checker.install_missing_dependencies():
                    print("\n✅ 所有依赖安装完成！建议重新运行检查验证。")
                else:
                    print("\n❌ 部分依赖安装失败，请手动检查。")
            else:
                print("\n⏭️ 跳过自动安装。您可以稍后手动安装缺失的依赖。")
    
    return results

if __name__ == "__main__":
    main()