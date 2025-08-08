#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高效办公助手系统快速完成脚本

快速版本：只执行核心必要步骤
1. 备份操作（核心文件）
2. Git推送

作者：雨俊
创建时间：2025-01-09
"""

import sys
import subprocess
import logging
from datetime import datetime
from pathlib import Path
import argparse

# 设置项目根目录
PROJECT_ROOT = Path("s:/PG-GMO")
TOOLS_DIR = PROJECT_ROOT / "tools"

# 添加项目路径到Python路径
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_DIR))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("finish_fast")

def run_git_push():
    """执行Git推送"""
    try:
        backup_repo_dir = PROJECT_ROOT / "bak" / "github_repo"
        if not backup_repo_dir.exists():
            logger.warning("备份仓库目录不存在，跳过Git推送")
            return True
            
        # 检查是否有未提交的更改
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(backup_repo_dir),
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            logger.info("发现未提交的更改，开始提交...")
            
            # 添加所有更改
            subprocess.run(
                ["git", "add", "."],
                cwd=str(backup_repo_dir),
                check=True
            )
            
            # 提交更改
            commit_message = f"快速更新 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=str(backup_repo_dir),
                check=True
            )
            logger.info("更改已提交")
        
        # 推送到远程仓库
        subprocess.run(
            ["git", "push"],
            cwd=str(backup_repo_dir),
            check=True
        )
        logger.info("Git推送完成")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Git操作失败: {e}")
        return False
    except Exception as e:
        logger.error(f"Git推送异常: {e}")
        return False

def run_quick_backup():
    """执行快速备份（只备份核心文件）"""
    try:
        backup_repo_dir = PROJECT_ROOT / "bak" / "github_repo"
        backup_repo_dir.mkdir(parents=True, exist_ok=True)
        
        # 只同步核心目录
        core_dirs = ["tools", "project"]
        
        for dir_name in core_dirs:
            source_dir = PROJECT_ROOT / dir_name
            target_dir = backup_repo_dir / dir_name
            
            if source_dir.exists():
                logger.info(f"同步目录: {dir_name}")
                if target_dir.exists():
                    import shutil
                    shutil.rmtree(target_dir)
                shutil.copytree(source_dir, target_dir)
                logger.info(f"✅ {dir_name} 目录同步完成")
            else:
                logger.warning(f"源目录不存在，跳过: {dir_name}")
        
        logger.info("快速备份完成")
        return True
        
    except Exception as e:
        logger.error(f"快速备份失败: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='高效办公助手系统快速完成脚本')
    parser.add_argument('--backup-only', action='store_true', help='只执行备份操作')
    args = parser.parse_args()
    
    try:
        logger.info("启动高效办公助手系统快速完成流程")
        logger.info(f"项目根目录: {PROJECT_ROOT}")
        logger.info("[模式] 快速模式（只执行核心步骤）")
        logger.info("-" * 60)
        
        success_count = 0
        total_steps = 1 if args.backup_only else 2
        
        # 1. 快速备份
        logger.info("\n[STEP 1] 快速备份")
        if run_quick_backup():
            success_count += 1
            logger.info("[SUCCESS] 快速备份完成")
        else:
            logger.error("[FAILED] 快速备份失败")
        
        if not args.backup_only:
            # 2. Git推送
            logger.info("\n[STEP 2] Git推送")
            if run_git_push():
                success_count += 1
                logger.info("[SUCCESS] Git推送完成")
            else:
                logger.error("[FAILED] Git推送失败")
        
        # 总结
        logger.info("\n" + "=" * 60)
        logger.info(f"[SUMMARY] 完成情况: {success_count}/{total_steps} 步骤成功")
        
        if success_count == total_steps:
            logger.info("[COMPLETE] 快速完成流程执行成功！")
            return 0
        else:
            logger.warning("[WARNING] 部分步骤失败，请检查日志")
            return 1
            
    except Exception as e:
        logger.error(f"执行过程中发生异常: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())