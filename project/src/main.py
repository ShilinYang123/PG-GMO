#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PG-GMO项目主程序入口

这是项目的主要入口点，负责初始化和启动应用程序。
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core import *
from src.ai import *
from src.ui import *
from src.utils import *


def main():
    """
    主程序入口函数
    """
    print("PG-GMO项目启动中...")
    print(f"项目根目录: {project_root}")
    print("系统初始化完成")
    
    # TODO: 在这里添加具体的应用程序逻辑
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)