#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高效办公助手系统工具函数模块
提供系统通用工具函数和MCP服务器相关工具
作者：雨俊
日期：2025-01-08
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

# 导入错误处理机制
try:
    from exceptions import ValidationError, ErrorHandler
    # 初始化错误处理器
    error_handler = ErrorHandler()
except ImportError:
    # 如果没有exceptions模块，创建简单的错误处理
    class ValidationError(Exception):
        pass
    
    class ErrorHandler:
        def handle_error(self, error):
            logging.error(f"Error: {error}")
    
    error_handler = ErrorHandler()

logger = logging.getLogger(__name__)


def execute_command(command, args=None, cwd=None, shell=False, check=True):
    """Executes a system command and returns its output.

    Args:
        command (str): The command to execute.
        args (list, optional): A list of arguments for the command. Defaults to None.
        cwd (str, optional): The working directory for the command. Defaults to None.
        shell (bool, optional): Whether to use the shell to execute the command.
                           Defaults to False.
                           SECURITY WARNING: Using shell=True can be a security
                           hazard if command or args are constructed from external
                           input. Use with caution.
        check (bool, optional): If True, raises a CalledProcessError if the
                                command returns a non-zero exit code.
                                Defaults to True.

    Returns:
        subprocess.CompletedProcess: The result of the command execution.

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit
                                       code and check is True.
        FileNotFoundError: If the command is not found.
        Exception: For other potential errors during command execution.
    """
    if args is None:
        args = []

    command_list = [command] + args
    logging.info(
        f"Executing command: {
            ' '.join(command_list)} in {
            cwd or os.getcwd()}"
    )

    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            cwd=cwd,
            shell=shell,
            check=check,  # This will raise CalledProcessError for non-zero exit codes
        )
        logging.info(f"Command executed successfully. STDOUT: {result.stdout[:200]}...")
        if result.stderr:
            logging.warning(f"Command STDERR: {result.stderr[:200]}...")
        return result
    except subprocess.CalledProcessError as e:
        logging.error(
            f"Command '{' '.join(command_list)}' failed with exit code "
            f"{e.returncode}."
        )
        logging.error(f"STDOUT: {e.stdout}")
        logging.error(f"STDERR: {e.stderr}")
        raise
    except FileNotFoundError:
        logging.error(
            f"Command '{command}' not found. Please check if it's "
            "installed and in PATH."
        )
        raise
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while executing command '{command}': {e}"
        )
        raise


def get_project_root(marker_filename="project_config.yaml"):
    """获取高效办公助手系统项目根目录

    优先使用固定路径 s:/PG-GMO，然后搜索标记文件

    Args:
        marker_filename (str, optional): 标记文件名. 默认为 "project_config.yaml".

    Returns:
        str: 项目根目录的绝对路径

    Raises:
        FileNotFoundError: 如果无法确定项目根目录
    """
    # 高效办公助手系统固定路径
    fixed_path = Path("s:/PG-GMO")
    if fixed_path.exists() and (fixed_path / "docs" / "03-管理" / marker_filename).exists():
        logging.info(f"项目根目录找到: {fixed_path} (固定路径)")
        return str(fixed_path)
    
    current_path = os.path.abspath(os.path.dirname(__file__))
    project_root_candidate = os.path.abspath(os.path.join(current_path, ".."))

    # Search upwards from the script's directory
    search_path = current_path
    while True:
        # Check for .git directory
        if os.path.isdir(os.path.join(search_path, ".git")):
            logging.info(
                f"Project root found at '{search_path}' (contains .git directory)."
            )
            return search_path

        # Check for marker file in 'docs/03-管理/' relative to current search_path
        # This is specific to the current project structure for project_config.yaml
        # For a truly generic template, this marker might be directly in the
        # root.
        potential_marker_dir = os.path.join(search_path, "docs", "03-管理")
        if os.path.isfile(os.path.join(potential_marker_dir, marker_filename)):
            logging.info(
                f"Project root found at '{search_path}' "
                f"(marker '{marker_filename}' found in 'docs/03-管理/')."
            )
            return search_path

        # Check for marker file directly in the current search_path (more
        # generic)
        if os.path.isfile(os.path.join(search_path, marker_filename)):
            logging.info(
                f"Project root found at '{search_path}' "
                f"(marker '{marker_filename}' found)."
            )
            return search_path

        parent_path = os.path.dirname(search_path)
        if parent_path == search_path:
            # Reached the filesystem root
            logging.warning(
                f"Could not determine project root by .git or marker file "
                f"'{marker_filename}'. Falling back to default: "
                f"'{project_root_candidate}' (parent of utils.py)."
            )
            # Before returning the fallback, ensure it's a plausible project structure
            # For example, check if 'tools' and 'docs' subdirectories exist
            if os.path.isdir(
                os.path.join(project_root_candidate, "tools")
            ) and os.path.isdir(os.path.join(project_root_candidate, "docs")):
                return project_root_candidate
            else:
                logging.error(
                    f"Fallback project root '{project_root_candidate}' "
                    "does not seem to be a valid project structure. "
                    "(Missing 'tools' or 'docs' "
                    "directories)."
                )
                raise FileNotFoundError(
                    "Project root could not be determined. Ensure the script is "
                    "run from within the project, or that a '.git' directory or "
                    "marker file (e.g., 'project_config.yaml') exists in the root."
                )
        search_path = parent_path


def ensure_dir_exists(dir_path):
    """确保目录存在，如果不存在则创建

    Args:
        dir_path (str): 目录路径

    Returns:
        bool: 如果目录存在或创建成功返回True，否则返回False
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"目录已确保存在: '{dir_path}'")
        return True
    except OSError as e:
        logging.error(f"创建目录失败 '{dir_path}': {e}")
        return False


def check_mcp_server_file(server_path: Union[str, Path]) -> bool:
    """检查MCP服务器文件是否存在且有效
    
    Args:
        server_path: MCP服务器文件路径
        
    Returns:
        bool: 文件存在且有效返回True
    """
    try:
        path = Path(server_path)
        if not path.exists():
            logging.warning(f"MCP服务器文件不存在: {path}")
            return False
            
        if not path.is_file():
            logging.warning(f"路径不是文件: {path}")
            return False
            
        if path.suffix != '.py':
            logging.warning(f"不是Python文件: {path}")
            return False
            
        # 检查文件是否可读
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read(100)  # 只读前100个字符检查
            if 'mcp' not in content.lower():
                logging.warning(f"文件可能不是MCP服务器: {path}")
                
        return True
        
    except Exception as e:
        logging.error(f"检查MCP服务器文件失败 {server_path}: {e}")
        return False


def get_office_directories() -> Dict[str, Path]:
    """获取办公相关目录路径
    
    Returns:
        Dict[str, Path]: 包含各种办公目录的字典
    """
    project_root = Path(get_project_root())
    
    directories = {
        'project': project_root / 'project',
        'office': project_root / 'project' / 'office',
        'output': project_root / 'project' / 'output',
        'mcp': project_root / 'project' / 'MCP',
        'logs': project_root / 'logs',
        'docs': project_root / 'docs',
        'tools': project_root / 'tools'
    }
    
    return directories


def create_office_structure():
    """创建高效办公助手系统目录结构"""
    directories = get_office_directories()
    
    # 创建基础目录
    for name, path in directories.items():
        ensure_dir_exists(str(path))
        
    # 创建MCP服务器分类目录
    mcp_categories = ['office', 'design', 'cad', 'graphics']
    for category in mcp_categories:
        category_path = directories['mcp'] / category
        ensure_dir_exists(str(category_path))
        
    logging.info("高效办公助手系统目录结构创建完成")


def validate_office_environment() -> Dict[str, bool]:
    """验证办公环境配置
    
    Returns:
        Dict[str, bool]: 验证结果
    """
    results = {}
    
    # 检查项目根目录
    try:
        project_root = get_project_root()
        results['project_root'] = True
        logging.info(f"项目根目录验证通过: {project_root}")
    except Exception as e:
        results['project_root'] = False
        logging.error(f"项目根目录验证失败: {e}")
        
    # 检查关键目录
    directories = get_office_directories()
    for name, path in directories.items():
        results[f'dir_{name}'] = path.exists()
        if not path.exists():
            logging.warning(f"目录不存在: {name} -> {path}")
            
    # 检查配置文件
    config_file = Path(project_root) / 'docs' / '03-管理' / 'project_config.yaml'
    results['config_file'] = config_file.exists()
    
    return results


def get_system_info() -> Dict[str, str]:
    """获取系统信息
    
    Returns:
        Dict[str, str]: 系统信息字典
    """
    import platform
    
    info = {
        'system': platform.system(),
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'project_root': get_project_root()
    }
    
    return info


if __name__ == "__main__":
    # Example usage (optional, for testing the module directly)
    try:
        logger.info(f"Project Root: {get_project_root()}")

        test_dir = os.path.join(get_project_root(), "temp_test_dir_utils")
        logger.info(f"Ensuring directory exists: {test_dir}")
        ensure_dir_exists(test_dir)

        logger.info(f"Listing contents of {get_project_root()}:")
        try:
            # Example: list files in the project root (use a safe command)
            # On Windows, 'dir' is a shell command. On Linux/macOS, 'ls' is
            # an executable.
            if os.name == "nt":  # Windows
                # 'dir' is a shell built-in, so shell=True is often needed
                # or use 'cmd /c dir'
                # However, to avoid shell=True, we can try to find a common executable.
                # For simplicity, let's assume a common command like 'git status'
                # might work if git is installed.
                # Or, we can just skip this part in the example if it's too
                # complex for a simple demo.
                # result = execute_command(
                # "cmd", args=["/c", "dir"], cwd=get_project_root()
                # )
                logger.info(
                    "(Skipping directory listing example on Windows for simplicity in "
                    "__main__)"
                )
            else:  # Linux/macOS
                result = execute_command("ls", args=["-la"], cwd=get_project_root())
                logger.info(result.stdout)
        except Exception as e:
            error_handler.handle_error(
                ValidationError(f"Error executing command for example: {e}")
            )

        # Clean up the test directory
        if os.path.exists(test_dir):
            try:
                os.rmdir(test_dir)  # rmdir only works on empty directories
                logger.info(f"Cleaned up test directory: {test_dir}")
            except OSError as e:
                logger.warning(
                    f"Could not remove test directory {test_dir}: {e}. "
                    "It might not be empty or permission issues."
                )
    except Exception as e:
        error_handler.handle_error(ValidationError(f"Utils module test failed: {e}"))
