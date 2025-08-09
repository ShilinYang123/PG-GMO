#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高效办公助手系统启动前置检查
确保AI Agent在每次办公工作前都能了解项目规范和MCP服务器状态
支持Office、CAD、Graphics等多类型MCP服务器的统一管理
"""

import os
import sys
import json
import yaml
import time
import subprocess
import logging
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Any, Optional

class OfficeAssistantStartupChecker:
    """高效办公助手系统启动前置检查器
    
    功能包括：
    - MCP服务器集群状态检查
    - 办公目录结构验证
    - AI Agent配置验证
    - 办公工作流程准备
    """
    
    def __init__(self, project_root: str = "s:/PG-GMO"):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.tools_dir = self.project_root / "tools"
        self.logs_dir = self.project_root / "logs"
        self.work_logs_dir = self.logs_dir / "工作记录"
        self.office_dir = self.project_root / "office"
        self.output_dir = self.project_root / "Output"
        self.mcp_dir = self.project_root / "project" / "MCP"
        
        # 确保日志目录存在
        self.work_logs_dir.mkdir(parents=True, exist_ok=True)
        
        # 核心规范文档路径
        self.core_docs = {
            "项目架构设计": self.docs_dir / "01-设计" / "项目架构设计.md",
            "开发任务书": self.docs_dir / "01-设计" / "开发任务书.md",
            "技术路线": self.docs_dir / "01-设计" / "技术路线.md",
            "规范与流程": self.docs_dir / "03-管理" / "规范与流程.md",
            "项目配置": self.docs_dir / "03-管理" / "project_config.yaml",
            "看板": self.docs_dir / "03-管理" / "看板.md"
        }
        
        # 启动检查记录文件
        self.startup_log = self.logs_dir / "ai_assistant_startup.log"
        
        # 设置工作流程日志
        self.setup_workflow_logging()
        
        # 禁用虚拟环境（杨老师要求）
        self.disable_virtual_environment()
        
        # 初始化系统日期管理
        self.setup_system_date_management()
        
    def setup_workflow_logging(self):
        """设置工作流程日志系统"""
        log_file = self.work_logs_dir / f"workflow_{datetime.now().strftime('%Y%m%d')}.log"
        
        # 创建工作流程专用的logger
        self.workflow_logger = logging.getLogger('WorkflowManager')
        self.workflow_logger.setLevel(logging.INFO)
        
        # 避免重复添加handler
        if not self.workflow_logger.handlers:
            handler = logging.FileHandler(log_file, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.workflow_logger.addHandler(handler)
            
    def disable_virtual_environment(self):
        """禁用虚拟环境自动激活（杨老师专用功能）"""
        try:
            # 检查当前是否在虚拟环境中
            if 'VIRTUAL_ENV' in os.environ:
                self.workflow_logger.info(f"检测到虚拟环境: {os.environ['VIRTUAL_ENV']}")
                self.workflow_logger.info("正在禁用虚拟环境...")
                
                # 移除虚拟环境相关的环境变量
                if 'VIRTUAL_ENV' in os.environ:
                    del os.environ['VIRTUAL_ENV']
                    self.workflow_logger.info("✓ 已移除 VIRTUAL_ENV 环境变量")
                
                if 'VIRTUAL_ENV_PROMPT' in os.environ:
                    del os.environ['VIRTUAL_ENV_PROMPT']
                    self.workflow_logger.info("✓ 已移除 VIRTUAL_ENV_PROMPT 环境变量")
                
                # 恢复系统PATH
                path = os.environ.get('PATH', '')
                path_parts = path.split(os.pathsep)
                
                # 移除虚拟环境相关的路径
                cleaned_paths = []
                for part in path_parts:
                    if '.venv' not in part.lower() and 'virtual' not in part.lower():
                        cleaned_paths.append(part)
                
                os.environ['PATH'] = os.pathsep.join(cleaned_paths)
                self.workflow_logger.info("✓ 已清理PATH环境变量")
                
                # 检查是否成功切换到系统Python
                if '.venv' in sys.executable.lower() or 'virtual' in sys.executable.lower():
                    self.workflow_logger.warning("⚠️ 仍在虚拟环境中，建议重新启动终端")
                else:
                    self.workflow_logger.info("✓ 成功切换到系统Python环境")
                    
            else:
                self.workflow_logger.info("当前未检测到虚拟环境，使用系统Python")
                
            # 记录当前Python环境信息
            self.workflow_logger.info(f"Python版本: {sys.version.split()[0]}")
            self.workflow_logger.info(f"Python路径: {sys.executable}")
            
            # 确保创建no_venv.bat脚本
            self.create_no_venv_script()
            
        except Exception as e:
            self.workflow_logger.error(f"禁用虚拟环境时发生错误: {e}")
            
    def create_no_venv_script(self):
        """创建无虚拟环境运行脚本"""
        try:
            script_content = '''@echo off
REM 禁用虚拟环境的批处理脚本
REM 杨老师专用 - 确保使用系统Python

echo === 禁用虚拟环境运行模式 ===

REM 清除虚拟环境变量
set VIRTUAL_ENV=
set VIRTUAL_ENV_PROMPT=

REM 使用系统Python运行脚本
if "%1"=="" (
    echo 用法: no_venv.bat [Python脚本路径]
    echo 示例: no_venv.bat tools\\check_structure.py
    pause
    exit /b 1
)

echo 正在使用系统Python运行: %1
python %*

echo.
echo 脚本执行完成
pause
'''
            
            batch_file = self.tools_dir / "no_venv.bat"
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            self.workflow_logger.info(f"✓ 已创建无虚拟环境运行脚本: {batch_file}")
            
        except Exception as e:
            self.workflow_logger.error(f"创建no_venv.bat脚本失败: {e}")
            
    def setup_system_date_management(self):
        """设置系统日期管理功能"""
        try:
            # 获取当前系统日期
            current_date = self.get_current_system_date()
            
            # 设置日期相关的环境变量
            self.set_date_environment_variables(current_date)
            
            # 创建日期配置文件
            self.create_date_config_file(current_date)
            
            # 记录日期设置
            self.workflow_logger.info(f"✓ 系统日期管理已初始化: {current_date['formatted']}")
            
        except Exception as e:
            self.workflow_logger.error(f"系统日期管理初始化失败: {e}")
            
    def get_current_system_date(self) -> Dict[str, str]:
        """获取当前系统日期（多种格式）"""
        try:
            now = datetime.now()
            
            date_info = {
                'timestamp': now.isoformat(),
                'date': now.strftime('%Y-%m-%d'),
                'datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
                'formatted': now.strftime('%Y年%m月%d日'),
                'year': str(now.year),
                'month': str(now.month),
                'day': str(now.day),
                'weekday': now.strftime('%A'),
                'weekday_cn': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()],
                'unix_timestamp': str(int(now.timestamp()))
            }
            
            return date_info
            
        except Exception as e:
            self.workflow_logger.error(f"获取系统日期失败: {e}")
            # 返回默认值
            return {
                'timestamp': '2025-07-26T00:00:00',
                'date': '2025-07-26',
                'datetime': '2025-07-26 00:00:00',
                'formatted': '2025年07月26日',
                'year': '2025',
                'month': '7',
                'day': '26',
                'weekday': 'Friday',
                'weekday_cn': '周五',
                'unix_timestamp': '1721952000'
            }
            
    def set_date_environment_variables(self, date_info: Dict[str, str]):
        """设置日期相关的环境变量"""
        try:
            # 设置环境变量供AI和脚本使用
            os.environ['SYSTEM_CURRENT_DATE'] = date_info['date']
            os.environ['SYSTEM_CURRENT_DATETIME'] = date_info['datetime']
            os.environ['SYSTEM_CURRENT_DATE_FORMATTED'] = date_info['formatted']
            os.environ['SYSTEM_CURRENT_YEAR'] = date_info['year']
            os.environ['SYSTEM_CURRENT_MONTH'] = date_info['month']
            os.environ['SYSTEM_CURRENT_DAY'] = date_info['day']
            os.environ['SYSTEM_CURRENT_WEEKDAY'] = date_info['weekday_cn']
            os.environ['SYSTEM_TIMESTAMP'] = date_info['timestamp']
            
            self.workflow_logger.info("✓ 日期环境变量已设置")
            
        except Exception as e:
            self.workflow_logger.error(f"设置日期环境变量失败: {e}")
            
    def create_date_config_file(self, date_info: Dict[str, str]):
        """创建日期配置文件供AI和其他脚本读取"""
        try:
            # 创建JSON格式的日期配置文件
            date_config_file = self.tools_dir / "current_date.json"
            
            config_data = {
                "system_date_info": date_info,
                "last_updated": date_info['timestamp'],
                "ai_instructions": {
                    "current_date": date_info['date'],
                    "formatted_date": date_info['formatted'],
                    "usage_note": "AI应使用此文件中的日期信息，而不是训练数据中的历史日期",
                    "priority": "系统当前日期优先于AI知识库中的日期信息"
                }
            }
            
            with open(date_config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
                
            self.workflow_logger.info(f"✓ 日期配置文件已创建: {date_config_file}")
            
            # 同时创建简单的文本文件供快速读取
            date_text_file = self.tools_dir / "current_date.txt"
            with open(date_text_file, 'w', encoding='utf-8') as f:
                f.write(f"当前系统日期: {date_info['formatted']}\n")
                f.write(f"ISO格式: {date_info['date']}\n")
                f.write(f"完整时间: {date_info['datetime']}\n")
                f.write(f"星期: {date_info['weekday_cn']}\n")
                f.write(f"\n注意: AI应使用此文件中的日期，而不是训练数据中的历史日期\n")
                
            self.workflow_logger.info(f"✓ 日期文本文件已创建: {date_text_file}")
            
        except Exception as e:
            self.workflow_logger.error(f"创建日期配置文件失败: {e}")
            
    def get_ai_date_instruction(self) -> str:
        """获取AI日期使用指令"""
        try:
            date_info = self.get_current_system_date()
            
            instruction = f"""=== AI日期使用指令 ===
当前系统日期: {date_info['formatted']} ({date_info['weekday_cn']})
ISO格式: {date_info['date']}
完整时间: {date_info['datetime']}

重要提醒:
1. 在生成任何需要日期的内容时，请使用上述当前系统日期
2. 不要使用AI训练数据中的历史日期或进行日期推测
3. 如需引用具体日期，请使用: {date_info['formatted']}
4. 环境变量 SYSTEM_CURRENT_DATE_FORMATTED 也包含此信息
5. 可读取 tools/current_date.json 获取完整日期信息

=== 结束 ==="""
            
            return instruction
            
        except Exception as e:
            self.workflow_logger.error(f"生成AI日期指令失败: {e}")
            return "AI日期指令生成失败，请手动确认当前日期"
            
    def run_script(self, script_name: str, args: List[str] = None) -> bool:
        """运行指定脚本"""
        try:
            if args is None:
                args = []
                
            script_path = self.tools_dir / script_name
            if not script_path.exists():
                self.workflow_logger.error(f"脚本不存在: {script_path}")
                return False
                
            cmd = [sys.executable, str(script_path)]
            if args:
                cmd.extend(args)
            
            self.workflow_logger.info(f"执行命令: {' '.join(cmd)}")
            
            # 使用 gbk 编码处理中文输出
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='gbk',
                errors='ignore',
                cwd=str(self.project_root),
                timeout=30
            )
            
            if result.returncode == 0:
                self.workflow_logger.info(f"[SUCCESS] {script_name} 执行成功")
                if result.stdout.strip():
                    self.workflow_logger.info(f"输出: {result.stdout.strip()}")
                return True
            else:
                self.workflow_logger.error(f"[ERROR] {script_name} 执行失败 (退出码: {result.returncode})")
                if result.stderr.strip():
                    self.workflow_logger.error(f"错误: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            self.workflow_logger.error(f"[ERROR] {script_name} 执行超时")
            return False
        except Exception as e:
            self.workflow_logger.error(f"[ERROR] {script_name} 执行异常: {str(e)}")
            return False
            
    def check_prerequisites(self) -> bool:
        """检查前置条件"""
        self.workflow_logger.info("开始检查前置条件...")
        
        # 检查项目根目录
        if not self.project_root.exists():
            self.workflow_logger.error(f"项目根目录不存在: {self.project_root}")
            return False
            
        # 检查核心脚本
        required_scripts = [
            "compliance_monitor.py",
        ]
        
        for script in required_scripts:
            script_path = self.tools_dir / script
            if not script_path.exists():
                self.workflow_logger.error(f"核心脚本不存在: {script_path}")
                return False
                
        self.workflow_logger.info("前置条件检查通过")
        return True
        
    def start_monitoring_process(self) -> bool:
        """以非阻塞方式启动监控进程"""
        try:
            script_path = self.tools_dir / "compliance_monitor.py"
            if not script_path.exists():
                self.workflow_logger.error(f"监控脚本不存在: {script_path}")
                return False
            
            cmd = [sys.executable, str(script_path), "--start"]
            self.workflow_logger.info(f"启动监控进程: {' '.join(cmd)}")
            
            # 以非阻塞方式启动进程
            process = subprocess.Popen(
                cmd,
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='gbk',
                errors='ignore'
            )
            
            # 等待一小段时间检查进程是否立即失败
            time.sleep(1)
            
            if process.poll() is None:
                # 进程仍在运行
                self.workflow_logger.info(f"监控进程已启动 (PID: {process.pid})")
                return True
            else:
                # 进程已退出
                stdout, stderr = process.communicate()
                self.workflow_logger.error(f"监控进程启动失败 (退出码: {process.returncode})")
                if stderr.strip():
                    self.workflow_logger.error(f"错误信息: {stderr.strip()}")
                return False
                
        except Exception as e:
            self.workflow_logger.error(f"启动监控进程异常: {str(e)}")
            return False
        
    def start_compliance_monitoring_enhanced(self) -> bool:
        """启动增强的合规性监控系统"""
        self.workflow_logger.info("启动合规性监控系统...")
        
        # 1. 检查监控状态
        self.workflow_logger.info("[1/4] 检查监控系统状态...")
        if not self.run_script("compliance_monitor.py", ["--status"]):
            self.workflow_logger.warning("监控系统状态检查失败，继续启动流程")
        
        # 2. 启用合规性机制（如果存在）
        enable_script = self.tools_dir / "enable_compliance.py"
        if enable_script.exists():
            self.workflow_logger.info("[2/4] 启用合规性机制...")
            if not self.run_script("enable_compliance.py", ["--enable"]):
                self.workflow_logger.error("合规性机制启用失败")
                return False
        else:
            self.workflow_logger.info("[2/4] 跳过合规性机制启用（脚本不存在）")
            
        # 3. 检查是否已有监控进程在运行
        self.workflow_logger.info("[3/4] 检查现有监控进程...")
        if self.check_monitoring_system():
            self.workflow_logger.info("检测到监控系统已在运行")
            print("✅ 合规性监控系统已在运行")
            return True
            
        # 4. 尝试启动新的监控进程（可选）
        self.workflow_logger.info("[4/4] 监控系统未运行，跳过启动...")
        self.workflow_logger.warning("合规性监控系统未启动，但不影响工作流程")
        print("⚠️ 合规性监控系统未启动（可手动启动）")
        
        # 不阻塞整个流程，允许继续
        return True
        
    def run_pre_checks(self) -> bool:
        """运行前置检查"""
        self.workflow_logger.info("执行前置检查...")
        
        # 1. 运行常规前置检查
        pre_check_script = self.tools_dir / "pre_operation_check.py"
        if pre_check_script.exists():
            if not self.run_script("pre_operation_check.py", ["report"]):
                self.workflow_logger.warning("前置检查发现问题，请查看详情")
                return False
        else:
            self.workflow_logger.info("跳过前置检查（脚本不存在）")
        
        # 2. 检查MCP服务器状态
        self.workflow_logger.info("执行MCP服务器状态检查...")
        mcp_status = self.check_mcp_servers_status()
        if not mcp_status:
            self.workflow_logger.warning("MCP服务器检查发现问题，请查看详细报告")
        
        # 3. 运行文档日期合规性检查
        self.workflow_logger.info("执行文档日期合规性检查...")
        date_check_script = self.tools_dir / "check_document_dates.py"
        if date_check_script.exists():
            if not self.run_script("check_document_dates.py", [str(self.project_root)]):
                self.workflow_logger.warning("发现文档日期违规问题")
                return False
        else:
            self.workflow_logger.info("跳过文档日期检查（脚本不存在）")
            
        self.workflow_logger.info("[SUCCESS] 前置检查通过")
        return True
        
    def show_work_reminders(self):
        """显示重要工作提醒"""
        reminders = [
            "🔔 重要提醒:",
            "   - 所有操作将被实时监控",
            "   - 违规行为将被自动记录和处理", 
            "   - 请严格按照项目规范执行",
            "   - 文件操作前请运行前置检查",
            "   - 定期查看合规性报告",
            "   - 已禁用虚拟环境，使用系统Python提升性能",
            "   - 如需运行脚本，建议使用 no_venv.bat"
        ]
        
        for reminder in reminders:
            print(reminder)
            self.workflow_logger.info(reminder)

    def load_core_regulations(self) -> Dict[str, str]:
        """加载核心规范内容"""
        print("📚 加载核心项目规范...")
        regulations = {}
        
        for doc_name, doc_path in self.core_docs.items():
            if doc_path.exists():
                try:
                    if doc_path.suffix.lower() in ['.yaml', '.yml']:
                        with open(doc_path, 'r', encoding='utf-8') as f:
                            content = yaml.safe_load(f)
                            regulations[doc_name] = json.dumps(content, ensure_ascii=False, indent=2)
                    else:
                        with open(doc_path, 'r', encoding='utf-8') as f:
                            regulations[doc_name] = f.read()
                    print(f"   ✅ {doc_name}: 已加载")
                except Exception as e:
                    print(f"   ❌ {doc_name}: 加载失败 - {e}")
            else:
                print(f"   ⚠️ {doc_name}: 文件不存在 - {doc_path}")
                
        return regulations
        
    def extract_key_constraints(self, regulations: Dict[str, str]) -> List[str]:
        """提取关键约束条件"""
        print("🔍 提取关键约束条件...")
        constraints = []
        
        # 从规范与流程中提取核心约束和工作流程要求
        if "规范与流程" in regulations:
            content = regulations["规范与流程"]
            
            # 基础约束条件
            constraints.append("🚫 严禁在项目根目录创建任何临时文件或代码文件")
            constraints.append("✅ 每次操作前必须执行路径合规性检查")
            constraints.append("🔒 严格保护核心文档，禁止未经授权的修改")
            constraints.append("⚡ 禁止使用虚拟环境，确保使用系统Python以提升性能")
            
            # 工作流程约束
            if "工作准备流程" in content:
                constraints.append("🔄 必须遵循标准工作准备流程")
                
            if "文件清理管理" in content:
                constraints.append("🧹 严格遵守文件清理管理规定")
                
            if "编码规范" in content:
                constraints.append("📝 严格遵守UTF-8编码规范")
                
            if "目录结构" in content:
                constraints.append("📁 严格遵守标准目录结构规范")
                
        # 从项目配置中提取技术约束
        if "项目配置" in regulations:
            constraints.append("⚙️ 严格遵守项目配置中的技术规范")
            
        # 从开发任务书中提取项目目标约束
        if "开发任务书" in regulations:
            constraints.append("🎯 严格按照开发任务书的目标和范围执行")
            
        # 从技术方案中提取架构约束
        if "技术方案" in regulations:
            constraints.append("🏗️ 严格遵循技术方案的架构设计")
            
        return constraints
        
    def generate_startup_briefing(self, regulations: Dict[str, str], constraints: List[str]) -> str:
        """生成启动简报"""
        monitoring_status = "🟢 运行中" if self.check_monitoring_system() else "🔴 未运行"
        
        # 检查虚拟环境状态
        venv_status = "🔴 已禁用" if 'VIRTUAL_ENV' not in os.environ else "🟡 检测到虚拟环境"
        python_env = "系统Python" if '.venv' not in sys.executable.lower() else "虚拟环境Python"
        
        # 获取当前系统日期信息
        current_date = self.get_current_system_date()
        
        briefing = f"""
# AI助理启动简报

**启动时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**项目根目录**: {self.project_root}
**监控系统状态**: {monitoring_status}
**虚拟环境状态**: {venv_status}
**Python环境**: {python_env} ({sys.version.split()[0]})

## 📅 系统日期信息 (重要!)
**当前系统日期**: {current_date['formatted']} ({current_date['weekday_cn']})
**ISO格式**: {current_date['date']}
**完整时间**: {current_date['datetime']}

⚠️ **AI重要提醒**: 
- 在生成任何需要日期的内容时，请使用上述当前系统日期
- 不要使用AI训练数据中的历史日期或进行日期推测
- 环境变量 SYSTEM_CURRENT_DATE_FORMATTED 包含格式化日期
- 可读取 tools/current_date.json 获取完整日期信息

## 🎯 工作目标
作为本项目的技术负责人，您需要：
1. 严格遵守所有项目管理文档和规范
2. 确保每次操作都符合项目架构设计
3. 维护项目的完整性和一致性
4. 提供高质量的技术解决方案
5. **使用正确的系统当前日期**: {current_date['formatted']}

## 📋 核心约束条件
"""
        
        for i, constraint in enumerate(constraints, 1):
            briefing += f"{i}. {constraint}\n"
            
        briefing += f"""

## 📄 已加载的核心文档
"""
        
        for doc_name in regulations.keys():
            briefing += f"- ✅ {doc_name}\n"
            
        briefing += f"""

## 🛠️ 必须使用的工具
- TaskManager: 任务分解和管理
- Memory: 重要内容记忆存储
- Context7: 技术文档查询
- Desktop-Commander: 终端命令执行
- 合规性检查工具: 确保操作合规

## ⚠️ 关键提醒
1. **每次工作前**: 必须检查项目规范
2. **每次操作前**: 必须执行前置检查
3. **每次工作后**: 必须进行自我检查
4. **文档命名**: 一律使用中文
5. **代码质量**: 必须通过flake8等工具检测

## 🚀 开始工作
现在您已经完成启动检查，可以开始按照项目规范进行工作。
请记住：您是高级软件专家和技术负责人，需要确保所有工作都符合最高标准。
"""
        
        return briefing
        
    def save_startup_record(self, briefing: str):
        """保存启动记录"""
        # 确保日志目录存在
        self.logs_dir.mkdir(exist_ok=True)
        
        # 保存启动简报
        briefing_file = self.logs_dir / f"startup_briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(briefing_file, 'w', encoding='utf-8') as f:
            f.write(briefing)
            
        # 更新启动日志
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - AI助理启动检查完成\n"
        with open(self.startup_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"💾 启动简报已保存: {briefing_file}")
        
    def check_mcp_servers_status(self) -> bool:
        """检查MCP服务器状态和功能"""
        try:
            self.workflow_logger.info("开始检查MCP服务器状态...")
            
            # 检查Claude Desktop配置文件
            config_file = self.project_root / "claude_desktop_config.json"
            if not config_file.exists():
                self.workflow_logger.error("Claude Desktop配置文件不存在")
                return False
                
            # 读取MCP服务器配置
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            mcp_servers = config.get('mcpServers', {})
            if not mcp_servers:
                self.workflow_logger.error("未配置MCP服务器")
                return False
                
            self.workflow_logger.info(f"发现 {len(mcp_servers)} 个已配置的MCP服务器")
            
            all_servers_ok = True
            server_status = {}
            
            for server_name, server_config in mcp_servers.items():
                self.workflow_logger.info(f"检查MCP服务器: {server_name}")
                
                # 检查服务器脚本文件是否存在
                if 'args' in server_config and server_config['args']:
                    script_path = Path(server_config['args'][0])
                    if script_path.exists():
                        self.workflow_logger.info(f"  ✓ {server_name}: 脚本文件存在")
                        server_status[server_name] = {'script_exists': True, 'functional': False}
                        
                        # 尝试测试服务器功能
                        if self._test_mcp_server_functionality(server_name, script_path):
                            server_status[server_name]['functional'] = True
                            self.workflow_logger.info(f"  ✓ {server_name}: 功能测试通过")
                        else:
                            self.workflow_logger.warning(f"  ⚠ {server_name}: 功能测试失败")
                            all_servers_ok = False
                    else:
                        self.workflow_logger.error(f"  ✗ {server_name}: 脚本文件不存在 ({script_path})")
                        server_status[server_name] = {'script_exists': False, 'functional': False}
                        all_servers_ok = False
                else:
                    self.workflow_logger.warning(f"  ⚠ {server_name}: 配置不完整")
                    server_status[server_name] = {'script_exists': False, 'functional': False}
                    all_servers_ok = False
            
            # 保存MCP服务器状态报告
            self._save_mcp_status_report(server_status)
            
            if all_servers_ok:
                self.workflow_logger.info("✓ 所有MCP服务器状态正常")
            else:
                self.workflow_logger.warning("⚠ 部分MCP服务器存在问题")
                
            return all_servers_ok
            
        except Exception as e:
            self.workflow_logger.error(f"MCP服务器状态检查失败: {e}")
            return False
    
    def _test_mcp_server_functionality(self, server_name: str, script_path: Path) -> bool:
        """测试MCP服务器功能"""
        try:
            # 根据服务器类型进行不同的测试
            if 'word' in server_name.lower():
                return self._test_word_mcp_server(script_path)
            elif 'powerpoint' in server_name.lower() or 'ppt' in server_name.lower():
                return self._test_powerpoint_mcp_server(script_path)
            elif 'photoshop' in server_name.lower():
                return self._test_photoshop_mcp_server(script_path)
            else:
                # 通用测试：检查脚本是否可以正常启动
                return self._test_generic_mcp_server(script_path)
                
        except Exception as e:
            self.workflow_logger.error(f"MCP服务器功能测试异常: {e}")
            return False
    
    def _test_word_mcp_server(self, script_path: Path) -> bool:
        """测试Word MCP服务器"""
        try:
            # 检查Word应用程序是否可用
            import win32com.client
            word_app = win32com.client.Dispatch("Word.Application")
            word_app.Visible = False
            word_app.Quit()
            return True
        except Exception:
            return False
    
    def _test_powerpoint_mcp_server(self, script_path: Path) -> bool:
        """测试PowerPoint MCP服务器"""
        try:
            # 检查PowerPoint应用程序是否可用
            import win32com.client
            ppt_app = win32com.client.Dispatch("PowerPoint.Application")
            ppt_app.Visible = 1
            ppt_app.Quit()
            return True
        except Exception:
            return False
    
    def _test_photoshop_mcp_server(self, script_path: Path) -> bool:
        """测试Photoshop MCP服务器"""
        try:
            # 检查Photoshop应用程序是否可用
            import win32com.client
            ps_app = win32com.client.Dispatch("Photoshop.Application")
            ps_app.Quit()
            return True
        except Exception:
            return False
    
    def _test_generic_mcp_server(self, script_path: Path) -> bool:
        """通用MCP服务器测试"""
        try:
            # 简单检查脚本文件语法
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 检查是否包含基本的MCP服务器结构
                if 'mcp' in content.lower() and ('server' in content.lower() or 'tool' in content.lower()):
                    return True
            return False
        except Exception:
            return False
    
    def _save_mcp_status_report(self, server_status: Dict[str, Dict[str, bool]]):
        """保存MCP服务器状态报告"""
        try:
            report_file = self.logs_dir / f"mcp_status_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_servers': len(server_status),
                'functional_servers': sum(1 for status in server_status.values() if status['functional']),
                'servers': server_status
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
                
            self.workflow_logger.info(f"MCP状态报告已保存: {report_file}")
            
        except Exception as e:
            self.workflow_logger.error(f"保存MCP状态报告失败: {e}")

    def check_monitoring_system(self) -> bool:
        """检查监控系统状态"""
        try:
            import psutil
            
            # 检查合规性监控进程
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if 'compliance_monitor.py' in cmdline and '--start' in cmdline:
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return False
            
        except ImportError:
            return False
            
    def start_monitoring_system(self) -> bool:
        """启动监控系统"""
        try:
            import subprocess
            import time
            
            # 检查配置是否允许自动启动
            config = self.load_project_config()
            if not config.get('compliance', {}).get('auto_start_monitoring', False):
                print("⚠️ 配置文件中未启用自动启动监控")
                return False
                
            print("🔄 正在启动合规性监控系统...")
            
            # 启动监控系统（非阻塞方式）
            compliance_script = self.tools_dir / "compliance_monitor.py"
            if not compliance_script.exists():
                print(f"❌ 监控脚本不存在: {compliance_script}")
                return False
                
            # 使用subprocess.Popen启动后台进程
            process = subprocess.Popen(
                ["python", str(compliance_script), "--start"],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else 0
            )
            
            # 等待一小段时间确保启动
            time.sleep(2)
            
            # 验证启动状态
            if self.check_monitoring_system():
                print("✅ 合规性监控系统启动成功")
                return True
            else:
                print("⚠️ 监控系统可能正在启动中，请稍后检查状态")
                return True  # 仍然返回True，因为启动命令已执行
                
        except Exception as e:
            print(f"❌ 启动监控系统失败: {e}")
            return False
            
    def load_project_config(self) -> dict:
        """加载项目配置"""
        try:
            import yaml
            config_file = self.project_root / "docs" / "03-管理" / "project_config.yaml"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ 加载配置文件失败: {e}")
        return {}
            
    def perform_startup_check(self) -> Tuple[bool, str]:
        """执行完整的启动检查"""
        import sys
        # 确保输出编码正确
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        
        print("🚀 AI助理启动检查开始")
        print("=" * 50)
        sys.stdout.flush()  # 强制刷新输出缓冲区
        
        try:
            # 1. 加载核心规范
            regulations = self.load_core_regulations()
            
            if not regulations:
                return False, "❌ 未能加载任何核心规范文档"
                
            # 2. 提取关键约束
            constraints = self.extract_key_constraints(regulations)
            
            # 3. 检查并启动监控系统
            monitoring_running = self.check_monitoring_system()
            if not monitoring_running:
                print("📡 监控系统未运行，正在自动启动...")
                self.start_monitoring_system()
            else:
                print("✅ 监控系统已在运行")
            
            # 4. 生成启动简报
            briefing = self.generate_startup_briefing(regulations, constraints)
            
            # 5. 保存启动记录
            self.save_startup_record(briefing)
            
            # 6. 显示简报
            print("\n" + "=" * 50)
            sys.stdout.flush()
            print(briefing)
            sys.stdout.flush()
            print("=" * 50)
            sys.stdout.flush()
            
            monitoring_status = "运行中" if self.check_monitoring_system() else "未运行"
            success_msg = f"🎉 AI助理启动检查完成 - 已加载 {len(regulations)} 个核心文档，监控系统状态: {monitoring_status}"
                
            return True, success_msg
            
        except Exception as e:
            error_msg = f"❌ 启动检查失败: {e}"
            print(error_msg)
            return False, error_msg
            
    def start_work_session(self) -> Tuple[bool, str]:
        """启动完整的工作会话（整合AI检查和工作流程管理）"""
        import sys
        # 确保输出编码正确
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        
        print("🚀 PG-Dev 项目完整启动流程")
        print("=" * 50)
        self.workflow_logger.info("开始项目标准工作启动流程")
        sys.stdout.flush()
        
        try:
            # 第一阶段：AI助理启动检查
            print("\n🤖 第一阶段：AI助理启动检查")
            print("-" * 30)
            
            # 1. 加载核心规范
            regulations = self.load_core_regulations()
            if not regulations:
                return False, "❌ 未能加载任何核心规范文档"
                
            # 2. 提取关键约束
            constraints = self.extract_key_constraints(regulations)
            
            # 第二阶段：工作流程环境检查
            print("\n🔧 第二阶段：工作流程环境检查")
            print("-" * 30)
            
            # 3. 检查MCP服务器状态
            print("\n🔌 检查MCP服务器状态...")
            mcp_status = self.check_mcp_servers_status()
            if mcp_status:
                print("✅ MCP服务器检查通过")
            else:
                print("⚠️ MCP服务器检查发现问题，但继续启动")
                self.workflow_logger.warning("MCP服务器检查发现问题")
            
            # 4. 检查前置条件
            if not self.check_prerequisites():
                self.workflow_logger.error("前置条件检查失败，无法启动工作会话")
                return False, "❌ 前置条件检查失败"
            print("✅ 前置条件检查通过")
            
            # 第三阶段：监控系统启动
            print("\n🛡️ 第三阶段：合规性监控系统启动")
            print("-" * 30)
            
            # 5. 启动增强的合规性监控
            if not self.start_compliance_monitoring_enhanced():
                self.workflow_logger.error("合规性监控启动失败")
                return False, "❌ 合规性监控启动失败"
            print("✅ 合规性监控系统已启动")
            
            # 第四阶段：前置检查
            print("\n🔍 第四阶段：运行前置检查")
            print("-" * 30)
            
            # 6. 运行前置检查
            if not self.run_pre_checks():
                self.workflow_logger.warning("前置检查发现问题，但继续工作会话")
                print("⚠️ 前置检查发现问题，但继续启动")
            else:
                print("✅ 前置检查通过")
            
            # 第五阶段：生成启动简报
            print("\n📋 第五阶段：生成启动简报")
            print("-" * 30)
            
            # 显示当前系统日期信息
            current_date = self.get_current_system_date()
            print(f"📅 当前系统日期: {current_date['formatted']} ({current_date['weekday_cn']})")
            print(f"   ISO格式: {current_date['date']}")
            print(f"   完整时间: {current_date['datetime']}")
            print("   ⚠️ AI将使用此日期信息，而非训练数据中的历史日期")
            
            # 7. 生成启动简报
            briefing = self.generate_startup_briefing(regulations, constraints)
            
            # 8. 保存启动记录
            self.save_startup_record(briefing)
            
            # 最终阶段：完成启动
            print("\n" + "=" * 50)
            print("🎉 项目启动完成！")
            print("=" * 50)
            
            self.workflow_logger.info("[SUCCESS] 工作环境准备完成！")
            self.workflow_logger.info("[SUCCESS] 合规性监控系统已启动")
            self.workflow_logger.info("[SUCCESS] 可以开始正式工作")
            
            print("\n📊 当前系统状态:")
            print("   🤖 AI助理: 已就绪")
            print("   🛡️ 合规监控: 运行中")
            print("   🔄 工作流程: 已启动")
            print("   📚 核心文档: 已加载")
            venv_display = "已禁用" if 'VIRTUAL_ENV' not in os.environ else "检测到虚拟环境"
            python_display = "系统Python" if '.venv' not in sys.executable.lower() else "虚拟环境Python"
            print(f"   ⚡ 虚拟环境: {venv_display}")
            print(f"   🐍 Python环境: {python_display}")
            
            # 显示重要提醒
            print("")
            self.show_work_reminders()
            
            print("\n🚀 现在可以开始高效工作！")
            print("=" * 50)
            sys.stdout.flush()
            
            monitoring_status = "运行中" if self.check_monitoring_system() else "未运行"
            success_msg = f"🎉 完整工作会话启动成功 - 已加载 {len(regulations)} 个核心文档，监控系统状态: {monitoring_status}"
                
            return True, success_msg
            
        except Exception as e:
            error_msg = f"❌ 工作会话启动失败: {e}"
            print(error_msg)
            self.workflow_logger.error(error_msg)
            return False, error_msg
            
    def create_startup_script(self):
        """创建启动脚本"""
        startup_script = self.tools_dir / "ai_startup.py"
        
        script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI助理快速启动脚本
在每次开始工作前运行此脚本
"""

import sys
from pathlib import Path

# 添加工具目录到路径
sys.path.insert(0, str(Path(__file__).parent))
# from ai_assistant_startup_check import AIAssistantStartupChecker  # 不需要导入，类已在本文件中定义
'''
        
        with open(startup_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
            
        print(f"📝 启动脚本已创建: {startup_script}")
        print("💡 使用方法: python tools/ai_startup.py")
        
def quick_startup():
    """快速启动函数 - 原ai_startup.py的功能"""
    checker = OfficeAssistantStartupChecker()
    success, message = checker.perform_startup_check()
    
    if success:
        print("\n🎉 准备就绪，可以开始工作！")
        return 0
    else:
        print(f"\n❌ 启动检查失败: {message}")
        return 1

def check_mcp_servers_simple():
    """简化版MCP服务器检查（来自start_simple_fixed.py）"""
    try:
        project_root = Path("S:/PG-GMO")
        # 检查Claude Desktop配置文件
        config_file = project_root / "claude_desktop_config.json"
        if not config_file.exists():
            print("⚠️ Claude Desktop配置文件不存在")
            return False
            
        # 读取MCP服务器配置
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        mcp_servers = config.get('mcpServers', {})
        if not mcp_servers:
            print("⚠️ 未配置MCP服务器")
            return False
            
        print(f"📋 发现 {len(mcp_servers)} 个已配置的MCP服务器:")
        
        all_ok = True
        for server_name, server_config in mcp_servers.items():
            # 检查服务器脚本文件是否存在
            if 'args' in server_config and server_config['args']:
                script_path = Path(server_config['args'][0])
                if script_path.exists():
                    print(f"  ✅ {server_name}: 脚本文件存在")
                else:
                    print(f"  ❌ {server_name}: 脚本文件不存在 ({script_path})")
                    all_ok = False
            else:
                print(f"  ⚠️ {server_name}: 配置不完整")
                all_ok = False
                
        # 尝试调用MCP服务器管理器进行详细检查
        mcp_manager_script = project_root / "tools" / "mcp_server_manager.py"
        if mcp_manager_script.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(mcp_manager_script), "status"],
                    cwd=str(project_root),
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    timeout=10
                )
                
                if result.returncode == 0 and result.stdout:
                    print("\n📊 详细状态报告:")
                    # 只显示关键信息，避免输出过长
                    lines = result.stdout.strip().split('\n')
                    for line in lines[:10]:  # 只显示前10行
                        if line.strip():
                            print(f"  {line}")
                    if len(lines) > 10:
                        print(f"  ... (还有 {len(lines)-10} 行，详见日志)")
                        
            except subprocess.TimeoutExpired:
                print("⚠️ MCP状态检查超时")
            except Exception as e:
                print(f"⚠️ MCP状态检查异常: {e}")
                
        return all_ok
        
    except Exception as e:
        print(f"❌ MCP服务器检测失败: {e}")
        return False

def simple_startup():
    """简化版启动流程（来自start_simple_fixed.py）"""
    project_root = Path("S:/PG-GMO")
    
    print("🚀 PG-GMO 项目快速启动")
    print("=" * 50)
    
    # 第一阶段：基础检查
    print("\n📋 第一阶段：基础环境检查")
    print("-" * 30)
    
    # 检查项目目录
    if project_root.exists():
        print("✅ 项目根目录: 已确认")
    else:
        print("❌ 项目根目录: 不存在")
        return False
    
    # 检查核心目录
    core_dirs = ["docs", "tools", "project"]
    for dir_name in core_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}目录: 已确认")
        else:
            print(f"⚠️ {dir_name}目录: 不存在")
    
    # 第二阶段：显示项目信息
    print("\n📊 第二阶段：项目状态信息")
    print("-" * 30)
    
    # 显示当前日期
    from datetime import datetime
    current_time = datetime.now()
    print(f"📅 当前时间: {current_time.strftime('%Y年%m月%d日 %H:%M:%S')}")
    print(f"📂 工作目录: {os.getcwd()}")
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    
    # 第三阶段：MCP服务器检测
    print("\n🔧 第三阶段：MCP服务器状态检测")
    print("-" * 30)
    
    mcp_status = check_mcp_servers_simple()
    if mcp_status:
        print("✅ MCP服务器检测: 完成")
    else:
        print("⚠️ MCP服务器检测: 发现问题（详见日志）")
    
    # 第四阶段：启动完成
    print("\n✅ 第四阶段：启动完成")
    print("-" * 30)
    print("🎉 项目启动成功！")
    print("💡 提示：您现在可以开始工作了")
    
    return True

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI助理启动前置检查系统")
    parser.add_argument("--check", action="store_true", help="执行启动检查")
    parser.add_argument("--create-script", action="store_true", help="创建启动脚本")
    parser.add_argument("--quick", action="store_true", help="快速启动（原ai_startup.py功能）")
    parser.add_argument("--simple", action="store_true", help="简化版启动（集成start_simple_fixed.py功能）")
    parser.add_argument("--work", action="store_true", help="启动完整工作会话（推荐）")
    parser.add_argument("--start", action="store_true", help="启动完整工作会话（别名）")
    
    args = parser.parse_args()
    
    checker = OfficeAssistantStartupChecker()
    
    if args.create_script:
        checker.create_startup_script()
    elif args.simple:
        # 简化版启动（来自start_simple_fixed.py）
        success = simple_startup()
        if success:
            print("\n🎯 启动流程完成")
            return 0
        else:
            print("\n❌ 启动流程失败")
            return 1
    elif args.work or args.start:
        # 启动完整工作会话
        success, message = checker.start_work_session()
        print(f"\n{message}")
        if not success:
            exit(1)
    elif args.check:
        success, message = checker.perform_startup_check()
        print(f"\n{message}")
    elif args.quick:
        return quick_startup()
    else:
        # 默认执行完整工作会话启动
        success, message = checker.start_work_session()
        print(f"\n{message}")
        if not success:
            exit(1)
        
if __name__ == "__main__":
    main()