#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录结构更新工具

功能:
- 扫描项目目录结构
- 生成标准化的目录结构清单
- 支持排除特定目录和文件
- 生成Markdown格式的结构文档

作者: 雨俊
创建时间: 2025-07-08
最后更新: 2025-07-08
"""

import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import argparse
import yaml
import asyncio

# import aiofiles  # 暂时不使用异步文件操作
from concurrent.futures import ThreadPoolExecutor
import time
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
# 移除hashlib导入 - 不再需要缓存功能


# 导入工具模块
from utils import get_project_root

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class DirectoryStructureGenerator:
    """目录结构生成器"""

    def __init__(self):
        # 设置项目根目录
        self.project_root = get_project_root()

        # 加载配置文件
        self.config = self._load_config()

        # 从配置文件中获取生成器配置
        structure_config = self.config.get("structure_check", {})
        generator_config = structure_config.get("generator", {})

        # 排除规则配置 - 根据项目架构设计优化
        self.excluded_dirs = set(
            generator_config.get(
                "excluded_dirs",
                [
                    "__pycache__",
                    ".git",
                    ".pytest_cache",
                    ".coverage",
                    "htmlcov",
                    "dist",
                    "build",
                    "*.egg-info",
                    ".tox",
                    ".mypy_cache",
                    ".DS_Store",
                    "Thumbs.db",
                    "node_modules",
                    ".venv",
                    "venv",
                    "env",
                    # 排除虚拟环境目录
                ],
            )
        )

        self.excluded_files = set(
            generator_config.get(
                "excluded_files",
                [
                    ".DS_Store",
                    "Thumbs.db",
                    "*.pyc",
                    "*.pyo",
                    "*.pyd",
                    "__pycache__",
                    "*.so",
                    "*.dylib",
                    "*.dll",
                    # 保留 .gitkeep 文件以显示目录结构
                ],
            )
        )

        # 允许的隐藏文件/目录
        self.allowed_hidden_items = set(
            generator_config.get(
                "allowed_hidden_items",
                [
                    ".env",
                    ".env.example",
                    ".gitignore",
                    ".dockerignore",
                    ".eslintrc.js",
                    ".prettierrc",
                    ".pre-commit-config.yaml",
                    ".devcontainer",
                    ".github",
                ],
            )
        )

        # 特殊目录配置 - 根据项目架构设计更新
        self.special_dirs = generator_config.get(
            "special_dirs",
            {
                "bak": [
                    "github_repo",
                    "迁移备份",
                    "专项备份",
                    "待清理资料",
                    "常规备份",
                ],
                "logs": ["工作记录", "检查报告", "其他日志", "archive"],
                "AI调度表": [  # 新增：AI调度表目录配置
                    "项目A_小家电产品开发",
                    "项目B_生产线优化",
                    "项目模板",
                ],
                "data": [  # 新增：数据目录配置
                    "database",
                    "uploads",
                    "exports",
                    "cache",
                    "temp",
                ],
            },
        )

        # 输出格式配置
        self.output_formats = generator_config.get("output_formats", ["markdown"])

        # 性能配置 - 禁用异步模式避免卡死
        self.performance = generator_config.get(
            "performance", {"max_workers": 4, "batch_size": 100, "enable_async": False}
        )

        # 移除缓存配置 - 确保每次都进行实时扫描

        # 性能统计
        self.perf_stats = {
            "scan_start_time": None,
            "scan_end_time": None,
            "total_scan_time": 0,
            "async_enabled": self.performance.get("enable_async", True),
        }

        # 统计信息
        self.stats = {"total_dirs": 0, "total_files": 0}

    # 移除所有缓存相关方法 - 确保实时扫描

    # 移除所有缓存相关方法 - 确保实时扫描

    def _load_config(self) -> Dict:
        """加载项目配置文件"""
        try:
            project_root = get_project_root()
            config_file = (
                Path(project_root) / "docs" / "03-管理" / "project_config.yaml"
            )

            if config_file.exists():
                with open(config_file, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            else:
                print(f"⚠️  配置文件不存在: {config_file}")
                return {}
        except Exception as e:
            print(f"⚠️  加载配置文件失败: {e}")
            return {}

    def should_exclude(self, path: Path) -> bool:
        """判断是否应该排除某个路径（与check_structure.py保持一致）"""

        # 排除隐藏目录和文件（除了特定的配置文件）
        if path.name.startswith(".") and path.name not in {
            ".env",
            ".env.local",
            ".env.production",
            ".env.template",
            ".env.example",
            ".env.sqlserver",
            ".gitignore",
            ".dockerignore",
            ".eslintrc.js",
            ".prettierrc",
            ".pre-commit-config.yaml",
            ".devcontainer",
            ".github",
            ".venv",
            ".cache",
            ".coverage",
            ".pytest_cache",
            ".vscode",
        }:
            return True

        # 排除特定目录
        if path.name in self.excluded_dirs:
            return True

        # 排除特定文件
        if path.is_file() and path.name in self.excluded_files:
            return True

        return False

    def should_filter_special_directory(self, relative_path: str, entry: Path) -> bool:
        """判断是否应该过滤特殊目录中的项目"""

        # 从配置中获取允许的子目录
        allowed_bak_dirs = set(self.special_dirs.get("bak", []))
        allowed_logs_dirs = set(self.special_dirs.get("logs", []))
        allowed_ai_dirs = set(self.special_dirs.get("AI调度表", []))
        allowed_data_dirs = set(self.special_dirs.get("data", []))

        # 检查是否在bak/目录下
        if relative_path.startswith("bak/"):
            # 如果是bak/下的直接子项，检查是否在允许列表中
            if relative_path.count("/") == 1:  # bak/xxx 格式
                dir_name = relative_path.split("/")[-1]
                if entry.is_dir() and dir_name not in allowed_bak_dirs:
                    return True  # 过滤掉不在允许列表中的目录
                elif entry.is_file():
                    return True  # 过滤掉bak/下的所有文件
            elif relative_path.count("/") > 1:  # bak/xxx/yyy 格式
                return True  # 过滤掉bak/子目录下的所有内容

        # 检查是否在logs/目录下
        elif relative_path.startswith("logs/"):
            # 如果是logs/下的直接子项，检查是否在允许列表中
            if relative_path.count("/") == 1:  # logs/xxx 格式
                dir_name = relative_path.split("/")[-1]
                if entry.is_dir() and dir_name not in allowed_logs_dirs:
                    return True  # 过滤掉不在允许列表中的目录
                elif entry.is_file():
                    return True  # 过滤掉logs/下的所有文件
            elif relative_path.count("/") > 1:  # logs/xxx/yyy 格式
                return True  # 过滤掉logs/子目录下的所有内容

        # 检查是否在AI调度表/目录下
        elif relative_path.startswith("AI调度表/"):
            # 如果是AI调度表/下的直接子项，检查是否在允许列表中
            if relative_path.count("/") == 1:  # AI调度表/xxx 格式
                dir_name = relative_path.split("/")[-1]
                if entry.is_dir() and dir_name not in allowed_ai_dirs:
                    return True  # 过滤掉不在允许列表中的目录
                elif entry.is_file():
                    return True  # 过滤掉AI调度表/下的所有文件
            elif relative_path.count("/") > 1:  # AI调度表/xxx/yyy 格式
                return True  # 过滤掉AI调度表/子目录下的所有内容

        # 检查是否在data/目录下
        elif relative_path.startswith("data/"):
            # 如果是data/下的直接子项，检查是否在允许列表中
            if relative_path.count("/") == 1:  # data/xxx 格式
                dir_name = relative_path.split("/")[-1]
                if entry.is_dir() and dir_name not in allowed_data_dirs:
                    return True  # 过滤掉不在允许列表中的目录
                elif entry.is_file():
                    return True  # 过滤掉data/下的所有文件
            elif relative_path.count("/") > 1:  # data/xxx/yyy 格式
                return True  # 过滤掉data/子目录下的所有内容

        return False

    def scan_filtered_directory(self, dir_path: Path, relative_path: str) -> List[Dict]:
        """扫描经过特殊过滤的目录（bak/、logs/、AI调度表/和data/）"""
        items = []

        # 从配置中获取允许的子目录
        if relative_path == "bak":
            allowed_dirs = set(self.special_dirs.get("bak", []))
        elif relative_path == "logs":
            allowed_dirs = set(self.special_dirs.get("logs", []))
        elif relative_path == "AI调度表":
            allowed_dirs = set(self.special_dirs.get("AI调度表", []))
        elif relative_path == "data":
            allowed_dirs = set(self.special_dirs.get("data", []))
        else:
            return items

        try:
            # 只扫描允许的子目录
            entries = sorted(dir_path.iterdir(), key=lambda x: x.name.lower())
            for entry in entries:
                if entry.is_dir() and entry.name in allowed_dirs:
                    # 添加允许的子目录，但不递归扫描其内容
                    items.append(
                        {
                            "type": "directory",
                            "name": entry.name,
                            "path": f"{relative_path}/{entry.name}/",
                            "children": [],  # 不扫描子目录内容
                        }
                    )
                    self.stats["total_dirs"] += 1
        except Exception as e:
            print(f"❌ 扫描过滤目录时出错: {dir_path} - {type(e).__name__}: {e}")

        return items

    async def scan_directory_async(
        self,
        dir_path: Path,
        relative_path: str = "",
        semaphore: asyncio.Semaphore = None,
        executor: ThreadPoolExecutor = None,
    ) -> List[Dict]:
        """异步扫描目录结构

        Args:
            dir_path: 要扫描的目录路径
            relative_path: 相对路径前缀
            semaphore: 并发控制信号量

        Returns:
            目录结构列表
        """
        if semaphore is None:
            semaphore = asyncio.Semaphore(self.performance.get("max_workers", 4))

        if executor is None:
            executor = ThreadPoolExecutor(
                max_workers=self.performance.get("max_workers", 4)
            )
            should_close_executor = True
        else:
            should_close_executor = False

        items = []

        try:
            # 使用线程池执行同步的目录读取操作
            loop = asyncio.get_event_loop()
            entries = await loop.run_in_executor(executor, list, dir_path.iterdir())

            # 按名称排序，目录在前
            entries.sort(key=lambda x: (x.is_file(), x.name.lower()))

            # 分批处理条目以避免过多并发
            batch_size = self.performance.get("batch_size", 100)
            for i in range(0, len(entries), batch_size):
                batch = entries[i : i + batch_size]
                batch_tasks = []

                for entry in batch:
                    if self.should_exclude(entry):
                        continue

                    # 构建相对路径
                    if relative_path:
                        item_relative_path = f"{relative_path}/{entry.name}"
                    else:
                        item_relative_path = entry.name

                    # 特殊处理bak/和logs/目录
                    if self.should_filter_special_directory(item_relative_path, entry):
                        continue

                    # 创建异步任务
                    task = self._process_entry_async(
                        entry, item_relative_path, semaphore, executor
                    )
                    batch_tasks.append(task)

                # 等待当前批次完成
                if batch_tasks:
                    batch_results = await asyncio.gather(
                        *batch_tasks, return_exceptions=True
                    )
                    for result in batch_results:
                        if isinstance(result, Exception):
                            print(f"⚠️  处理条目时出错: {result}")
                        elif result is not None:
                            items.append(result)

        except Exception as e:
            print(f"❌ 异步扫描目录时出错: {dir_path} - {type(e).__name__}: {e}")
        finally:
            # 如果是我们创建的executor，需要关闭它
            if should_close_executor:
                executor.shutdown(wait=True)

        return items

    async def _process_entry_async(
        self,
        entry: Path,
        item_relative_path: str,
        semaphore: asyncio.Semaphore,
        executor: ThreadPoolExecutor,
    ) -> Dict:
        """异步处理单个条目

        Args:
            entry: 文件或目录路径
            item_relative_path: 相对路径
            semaphore: 并发控制信号量
            executor: 共享的线程池执行器

        Returns:
            条目信息字典
        """
        async with semaphore:
            try:
                if entry.is_dir():
                    # 目录处理
                    self.stats["total_dirs"] += 1

                    # 对于特殊目录，使用同步方法
                    if item_relative_path in ["bak", "logs", "AI调度表", "data"]:
                        children = self.scan_filtered_directory(
                            entry, item_relative_path
                        )
                    else:
                        children = await self.scan_directory_async(
                            entry, item_relative_path, semaphore, executor
                        )

                    return {
                        "type": "directory",
                        "name": entry.name,
                        "path": item_relative_path,
                        "children": children,
                    }
                else:
                    # 文件处理
                    self.stats["total_files"] += 1

                    # 异步获取文件大小
                    file_size = await self._get_file_size_async(entry, executor)

                    return {
                        "type": "file",
                        "name": entry.name,
                        "path": item_relative_path,
                        "size": file_size,
                    }

            except Exception as e:
                print(f"⚠️  处理条目时出错: {entry} - {type(e).__name__}: {e}")
                return None

    async def _get_file_size_async(
        self, file_path: Path, executor: ThreadPoolExecutor
    ) -> int:
        """异步获取文件大小

        Args:
            file_path: 文件路径
            executor: 共享的线程池执行器

        Returns:
            文件大小（字节），失败时返回-1
        """
        try:
            loop = asyncio.get_event_loop()
            stat_result = await loop.run_in_executor(
                executor, lambda: file_path.stat() if file_path.exists() else None
            )
            return stat_result.st_size if stat_result else -1
        except Exception as e:
            print(f"⚠️  异步获取文件大小失败: {file_path} - {e}")
            return -1

    def scan_directory(self, dir_path: Path, relative_path: str = "") -> List[Dict]:
        """扫描目录结构

        Args:
            dir_path: 要扫描的目录路径
            relative_path: 相对路径前缀

        Returns:
            目录结构列表
        """
        items = []

        try:
            # 获取目录下所有项目
            entries = list(dir_path.iterdir())
            # 按名称排序，目录在前
            entries.sort(key=lambda x: (x.is_file(), x.name.lower()))

            for entry in entries:
                if self.should_exclude(entry):
                    continue

                # 构建相对路径
                if relative_path:
                    item_relative_path = f"{relative_path}/{entry.name}"
                else:
                    item_relative_path = entry.name

                # 特殊处理bak/和logs/目录，只显示指定的子目录名
                if self.should_filter_special_directory(item_relative_path, entry):
                    continue

                if entry.is_dir():
                    # 目录
                    self.stats["total_dirs"] += 1

                    # 对于特殊目录，只扫描允许的子目录
                    children = []
                    if item_relative_path in ["bak", "logs", "AI调度表", "data"]:
                        children = self.scan_filtered_directory(
                            entry, item_relative_path
                        )
                    else:
                        children = self.scan_directory(entry, item_relative_path)

                    item = {
                        "type": "directory",
                        "name": entry.name,
                        "path": item_relative_path,
                        "children": children,
                    }
                    items.append(item)

                else:
                    # 文件
                    self.stats["total_files"] += 1

                    # 安全获取文件大小
                    file_size = 0
                    try:
                        if entry.exists():
                            file_size = entry.stat().st_size
                    except (PermissionError, OSError, FileNotFoundError) as e:
                        print(f"⚠️  无法获取文件大小: {entry} - {e}")
                        file_size = -1  # 标记为无法获取
                    except Exception as e:
                        print(
                            f"⚠️  获取文件信息时出错: {entry} - "
                            f"{type(e).__name__}: {e}"
                        )
                        file_size = -1

                    item = {
                        "type": "file",
                        "name": entry.name,
                        "path": item_relative_path,
                        "size": file_size,
                    }
                    items.append(item)

        except PermissionError as e:
            print(f"⚠️  权限不足，跳过目录: {dir_path} - {e}")
        except FileNotFoundError as e:
            print(f"❌ 目录不存在: {dir_path} - {e}")
        except OSError as e:
            if e.errno == 36:  # 文件名过长
                print(f"⚠️  文件名过长，跳过目录: {dir_path}")
            elif e.errno == 2:  # 文件不存在
                print(f"❌ 路径不存在: {dir_path}")
            elif e.errno == 13:  # 权限拒绝
                print(f"⚠️  访问被拒绝，跳过目录: {dir_path}")
            else:
                print(f"❌ 系统错误，跳过目录: {dir_path} - {e}")
        except UnicodeDecodeError as e:
            print(f"⚠️  编码错误，跳过目录: {dir_path} - {e}")
        except RecursionError as e:
            print(f"❌ 递归深度超限，跳过目录: {dir_path} - {e}")
        except MemoryError as e:
            print(f"❌ 内存不足，跳过目录: {dir_path} - {e}")
        except Exception as e:
            print(f"❌ 未知错误，跳过目录: {dir_path} - {type(e).__name__}: {e}")

        return items

    async def scan_directory_with_performance(self, dir_path: Path) -> List[Dict]:
        """实时目录扫描方法（移除缓存，确保每次都获取最新数据）

        Args:
            dir_path: 要扫描的目录路径

        Returns:
            目录结构列表
        """
        # 记录开始时间
        self.perf_stats["scan_start_time"] = time.time()

        print(
            f"🚀 启动{'异步' if self.perf_stats['async_enabled'] else '同步'}实时扫描模式"
        )
        print(
            f"⚙️  配置: 最大工作线程={self.performance.get('max_workers', 4)}, "
            f"批处理大小={self.performance.get('batch_size', 100)}"
        )

        try:
            if self.perf_stats["async_enabled"]:
                # 使用异步扫描
                structure = await self.scan_directory_async(dir_path)
            else:
                # 使用同步扫描
                structure = self.scan_directory(dir_path)

            # 记录结束时间
            self.perf_stats["scan_end_time"] = time.time()
            self.perf_stats["total_scan_time"] = (
                self.perf_stats["scan_end_time"] - self.perf_stats["scan_start_time"]
            )

            print(f"⏱️  实时扫描耗时: {self.perf_stats['total_scan_time']:.2f}秒")
            print(
                f"📊 扫描统计: {self.stats['total_dirs']}个目录, "
                f"{self.stats['total_files']}个文件"
            )

            return structure

        except Exception as e:
            print(f"❌ 扫描失败: {type(e).__name__}: {e}")
            raise

    def generate_markdown(
        self, structure: List[Dict], title: str = "项目目录结构"
    ) -> str:
        """生成Markdown格式的目录结构

        Args:
            structure: 目录结构数据
            title: 文档标题

        Returns:
            Markdown格式的字符串
        """
        lines = []
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("## 目录结构")
        lines.append("")
        lines.append("```")

        def generate_tree(
            items: List[Dict], prefix: str = "", is_last_list: List[bool] = None
        ) -> None:
            """生成目录树结构"""
            if is_last_list is None:
                is_last_list = []

            for i, item in enumerate(items):
                is_last = i == len(items) - 1

                # 构建当前行的前缀
                current_prefix = ""
                for j, is_last_parent in enumerate(is_last_list):
                    if j == len(is_last_list) - 1:
                        continue
                    current_prefix += "│   " if not is_last_parent else "    "

                # 添加当前项的连接符
                if is_last_list:
                    current_prefix += "└── " if is_last else "├── "

                # 输出当前项
                if item["type"] == "directory":
                    lines.append(f"{current_prefix}{item['name']}/")
                    # 递归处理子目录
                    children = item.get("children", [])
                    if children:
                        new_is_last_list = is_last_list + [is_last]
                        generate_tree(children, current_prefix, new_is_last_list)
                else:
                    lines.append(f"{current_prefix}{item['name']}")

        # 生成目录树
        generate_tree(structure)

        lines.append("```")
        lines.append("")

        # 添加统计信息
        lines.append("## 统计信息")
        lines.append("")
        lines.append(f"- **目录数量**: {self.stats['total_dirs']}")
        lines.append(f"- **文件数量**: {self.stats['total_files']}")
        lines.append("")

        # 添加说明
        lines.append("## 说明")
        lines.append("")
        lines.append("- 此文档由目录结构更新工具自动生成")
        lines.append("- 已排除常见的临时文件和缓存目录")
        lines.append("- 目录路径以 / 结尾，文件路径不带结尾符号")
        lines.append("")

        return "\n".join(lines)

    def generate_json(self, structure: List[Dict]) -> str:
        """生成JSON格式的目录结构

        Args:
            structure: 目录结构数据

        Returns:
            JSON格式的字符串
        """
        output_data = {
            "metadata": {
                "generated_time": datetime.now().isoformat(),
                "title": "项目目录结构",
                "statistics": {
                    "total_dirs": self.stats["total_dirs"],
                    "total_files": self.stats["total_files"],
                },
            },
            "structure": structure,
        }
        return json.dumps(output_data, ensure_ascii=False, indent=2)

    def generate_yaml(self, structure: List[Dict]) -> str:
        """生成YAML格式的目录结构

        Args:
            structure: 目录结构数据

        Returns:
            YAML格式的字符串
        """
        output_data = {
            "metadata": {
                "generated_time": datetime.now().isoformat(),
                "title": "项目目录结构",
                "statistics": {
                    "total_dirs": self.stats["total_dirs"],
                    "total_files": self.stats["total_files"],
                },
            },
            "structure": structure,
        }
        return yaml.dump(output_data, allow_unicode=True, default_flow_style=False)

    def generate_xml(self, structure: List[Dict]) -> str:
        """生成XML格式的目录结构

        Args:
            structure: 目录结构数据

        Returns:
            XML格式的字符串
        """
        root = ET.Element("project_structure")

        # 添加元数据
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "generated_time").text = datetime.now().isoformat()
        ET.SubElement(metadata, "title").text = "项目目录结构"

        statistics = ET.SubElement(metadata, "statistics")
        ET.SubElement(statistics, "total_dirs").text = str(self.stats["total_dirs"])
        ET.SubElement(statistics, "total_files").text = str(self.stats["total_files"])

        # 添加结构数据
        structure_elem = ET.SubElement(root, "structure")

        def add_items_to_xml(parent_elem, items):
            """递归添加项目到XML"""
            for item in items:
                item_elem = ET.SubElement(parent_elem, "item")
                item_elem.set("type", item["type"])
                item_elem.set("name", item["name"])
                item_elem.set("path", item["path"])

                if item["type"] == "file" and "size" in item:
                    item_elem.set("size", str(item["size"]))

                if "children" in item and item["children"]:
                    children_elem = ET.SubElement(item_elem, "children")
                    add_items_to_xml(children_elem, item["children"])

        add_items_to_xml(structure_elem, structure)

        # 格式化XML
        rough_string = ET.tostring(root, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def save_structure(
        self, structure: List[Dict], output_file: Path, formats: List[str] = None
    ) -> None:
        """保存目录结构到文件

        Args:
            structure: 目录结构数据
            output_file: 输出文件路径
            formats: 输出格式列表，如果为None则使用配置文件中的格式
        """
        try:
            # 确保输出目录存在
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # 获取输出格式
            if formats is None:
                formats = self.config.get("output_formats", ["markdown"])

            generated_files = []

            for format_type in formats:
                if format_type == "markdown":
                    content = self.generate_markdown(structure)
                    file_path = output_file
                elif format_type == "json":
                    content = self.generate_json(structure)
                    file_path = output_file.with_suffix(".json")
                elif format_type == "yaml":
                    content = self.generate_yaml(structure)
                    file_path = output_file.with_suffix(".yaml")
                elif format_type == "xml":
                    content = self.generate_xml(structure)
                    file_path = output_file.with_suffix(".xml")
                else:
                    print(f"⚠️  不支持的输出格式: {format_type}")
                    continue

                # 写入文件
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                generated_files.append(file_path)

            print("\n✅ 目录结构标准清单已生成:")
            for file_path in generated_files:
                print(f"   {file_path}")

        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
            raise


async def main_async(formats: List[str] = None):
    """异步主函数

    Args:
        formats: 指定的输出格式列表
    """
    try:
        # 获取项目根目录
        project_root_str = get_project_root()
        project_root = Path(project_root_str)
        print(f"📁 项目根目录: {project_root}")

        # 创建生成器
        generator = DirectoryStructureGenerator()

        # 扫描目录结构（带性能优化）
        print("🔍 正在扫描目录结构...")
        structure = await generator.scan_directory_with_performance(project_root)

        # 生成输出文件路径
        output_file = project_root / "docs" / "01-设计" / "目录结构标准清单.md"

        # 保存结构
        generator.save_structure(structure, output_file, formats)

    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("生成完成")
    print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="生成项目目录结构标准清单",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""支持的输出格式:
  markdown  - Markdown格式 (默认)
  json      - JSON格式
  yaml      - YAML格式
  xml       - XML格式

示例:
  python update_structure.py                    # 使用配置文件中的格式
  python update_structure.py -f markdown        # 仅生成Markdown格式
  python update_structure.py -f json yaml       # 生成JSON和YAML格式
  python update_structure.py -f all             # 生成所有支持的格式""",
    )

    parser.add_argument(
        "-f",
        "--formats",
        nargs="*",
        choices=["markdown", "json", "yaml", "xml", "all"],
        help="指定输出格式 (可指定多个)",
    )

    args = parser.parse_args()

    # 处理格式参数
    formats = None
    if args.formats:
        if "all" in args.formats:
            formats = ["markdown", "json", "yaml", "xml"]
        else:
            formats = args.formats

    asyncio.run(main_async(formats))


if __name__ == "__main__":
    main()
