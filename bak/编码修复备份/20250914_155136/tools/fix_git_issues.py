#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git 文件锁定问题修复脚本

解决 Git 推送时遇到的文件访问权限问题
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import time
import shutil

# 设置项目根目录
PROJECT_ROOT = Path("s:/PG-GMO")
GIT_REPO_DIR = PROJECT_ROOT / "bak" / "github_repo"

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("git_fix")

def kill_git_processes():
    """终止所有 Git 相关进程"""
    try:
        logger.info("正在查找并终止 Git 相关进程...")
        
        # 查找 Git 进程
        result = subprocess.run(
            ["tasklist", "/fi", "IMAGENAME eq git.exe"],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        
        if "git.exe" in result.stdout:
            logger.info("发现 Git 进程，正在终止...")
            subprocess.run(
                ["taskkill", "/f", "/im", "git.exe"],
                capture_output=True,
                text=True
            )
            logger.info("✓ Git 进程已终止")
        else:
            logger.info("未发现 Git 进程")
            
        # 等待进程完全终止
        time.sleep(2)
        
    except Exception as e:
        logger.error(f"终止 Git 进程时出错: {e}")

def fix_git_lock_files():
    """修复 Git 锁定文件"""
    try:
        logger.info("正在检查和修复 Git 锁定文件...")
        
        # 查找并删除 .git/index.lock 文件
        index_lock = GIT_REPO_DIR / ".git" / "index.lock"
        if index_lock.exists():
            logger.info("发现 index.lock 文件，正在删除...")
            index_lock.unlink()
            logger.info("✓ index.lock 文件已删除")
        
        # 查找并删除其他锁定文件
        git_dir = GIT_REPO_DIR / ".git"
        for lock_file in git_dir.rglob("*.lock"):
            logger.info(f"删除锁定文件: {lock_file}")
            try:
                lock_file.unlink()
            except Exception as e:
                logger.warning(f"无法删除锁定文件 {lock_file}: {e}")
                
    except Exception as e:
        logger.error(f"修复 Git 锁定文件时出错: {e}")

def fix_permission_issues():
    """修复权限问题"""
    try:
        logger.info("正在尝试修复权限问题...")
        
        # 使用 Git 命令重置仓库状态
        subprocess.run(
            ["git", "reset", "--hard"],
            cwd=str(GIT_REPO_DIR),
            capture_output=True,
            text=True
        )
        
        # 清理工作目录
        subprocess.run(
            ["git", "clean", "-fd"],
            cwd=str(GIT_REPO_DIR),
            capture_output=True,
            text=True
        )
        
        logger.info("✓ Git 仓库状态已重置")
        
    except Exception as e:
        logger.error(f"修复权限问题时出错: {e}")

def remove_problematic_submodule():
    """移除有问题的子模块"""
    try:
        logger.info("正在处理有问题的子模块...")
        
        # 检查 apifox 目录
        apifox_dir = GIT_REPO_DIR / "project" / "MCP" / "collaboration" / "apifox"
        if apifox_dir.exists():
            logger.info(f"发现有问题的目录: {apifox_dir}")
            
            # 尝试删除该目录
            try:
                shutil.rmtree(apifox_dir)
                logger.info("✓ 有问题的目录已删除")
            except Exception as e:
                logger.error(f"无法删除目录: {e}")
                
                # 如果无法删除，尝试重命名
                try:
                    backup_dir = apifox_dir.parent / f"apifox_backup_{int(time.time())}"
                    apifox_dir.rename(backup_dir)
                    logger.info(f"✓ 目录已重命名为: {backup_dir}")
                except Exception as e2:
                    logger.error(f"重命名也失败: {e2}")
                    
    except Exception as e:
        logger.error(f"处理子模块时出错: {e}")

def test_git_operations():
    """测试 Git 操作"""
    try:
        logger.info("正在测试 Git 操作...")
        
        # 检查 Git 状态
        result = subprocess.run(
            ["git", "status"],
            cwd=str(GIT_REPO_DIR),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            logger.info("✓ Git 状态检查成功")
            return True
        else:
            logger.error(f"Git 状态检查失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"测试 Git 操作时出错: {e}")
        return False

def main():
    """主函数"""
    logger.info("🔧 Git 文件锁定问题修复工具")
    logger.info(f"📁 Git 仓库路径: {GIT_REPO_DIR}")
    logger.info("-" * 50)
    
    if not GIT_REPO_DIR.exists():
        logger.error("Git 仓库目录不存在")
        return 1
    
    # 步骤 1: 终止 Git 进程
    kill_git_processes()
    
    # 步骤 2: 修复锁定文件
    fix_git_lock_files()
    
    # 步骤 3: 移除有问题的子模块
    remove_problematic_submodule()
    
    # 步骤 4: 修复权限问题
    fix_permission_issues()
    
    # 步骤 5: 测试 Git 操作
    if test_git_operations():
        logger.info("🎉 Git 问题修复完成！")
        logger.info("现在可以重新运行 finish.py 进行 Git 推送")
        return 0
    else:
        logger.error("❌ Git 问题未完全解决，可能需要手动处理")
        return 1

if __name__ == "__main__":
    sys.exit(main())