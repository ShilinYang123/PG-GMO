#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高效办公助手系统完成脚本

核心功能：
1. 调用check_structure.py进行目录结构检查
2. 执行备份操作
3. Git推送
4. MCP服务器状态检查
5. 办公文档整理

作者：雨俊
创建时间：2025-01-08
"""


import sys
import subprocess
import logging
import yaml
import shutil
import json
import os
import time
from datetime import datetime
from pathlib import Path

# Windows平台下设置控制台编码为UTF-8
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# 设置项目根目录
PROJECT_ROOT = Path("s:/PG-GMO")
TOOLS_DIR = PROJECT_ROOT / "tools"
OFFICE_DIR = PROJECT_ROOT / "office"
OUTPUT_DIR = PROJECT_ROOT / "02-Output"

# 添加项目路径到Python路径
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_DIR))

# 导入日志系统
try:
    from project.src.utils.logger import get_logger
    logger = get_logger("finish")
except ImportError:
    # 如果导入失败，使用标准logging
    import logging
    # 如果导入失败，使用标准logging
    log_file = PROJECT_ROOT / "logs" / "finish_log.txt"
    # 确保logs目录存在
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout) # 仍然输出到控制台
        ]
    )
    logger = logging.getLogger("finish")


# 读取项目配置
def load_project_config():
    """加载项目配置文件"""
    config_file = PROJECT_ROOT / "docs" / "03-管理" / "project_config.yaml"
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return {}


def load_github_config():
    """加载GitHub配置"""
    github_config_file = TOOLS_DIR / ".github_config.json"
    try:
        if github_config_file.exists():
            with open(github_config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            logger.warning("GitHub配置文件不存在")
            return {}
    except Exception as e:
        logger.error(f"加载GitHub配置失败: {e}")
        return {}


def setup_git_authentication():
    """设置Git认证"""
    github_config = load_github_config()
    github_info = github_config.get('github', {})
    
    username = github_info.get('username')
    token = github_info.get('token')
    repo_url = github_info.get('repository', {}).get('url')
    
    if not all([username, token, repo_url]):
        logger.warning("GitHub配置信息不完整，使用默认Git配置")
        return False
        
    try:
        # 设置环境变量
        os.environ['GITHUB_USERNAME'] = username
        os.environ['GITHUB_TOKEN'] = token
        os.environ['GITHUB_REPO_URL'] = repo_url
        
        # 配置Git用户信息
        subprocess.run(
            ["git", "config", "--global", "user.name", username],
            capture_output=True,
            text=True,
            check=True
        )
        
        subprocess.run(
            ["git", "config", "--global", "user.email", f"{username}@users.noreply.github.com"],
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"✓ Git认证配置完成 - 用户: {username}")
        return True
        
    except Exception as e:
        logger.error(f"设置Git认证失败: {e}")
        return False


# 加载配置
project_config = load_project_config()
git_config = project_config.get("git", {})
GIT_REPO_DIR = PROJECT_ROOT / "bak" / git_config.get("repo_dir_name", "github_repo")


def run_structure_check():
    """运行目录结构检查"""
    logger.info("开始高效办公助手系统结构检查...")

    check_script = TOOLS_DIR / "check_structure.py"
    if not check_script.exists():
        logger.error(f"检查脚本不存在: {check_script}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(check_script)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        # 根据退出码判断结果
        # 0: 优秀/良好 (>=95%)
        # 1: 合格/需要改进 (80-95%)
        # 2: 不合格 (<80%)
        # 3+: 系统错误
        if result.returncode == 0:
            logger.info("高效办公助手系统结构检查完成 - 优秀/良好")
            return True
        elif result.returncode == 1:
            logger.info("系统结构检查完成 - 合格状态，允许继续")
            # 显示检查结果但不阻止流程
            if result.stdout:
                print(result.stdout)
            return True
        elif result.returncode == 2:
            logger.error("系统结构检查失败 - 不合格状态")
            if result.stdout:
                print(result.stdout)
            return False
        else:
            logger.error(f"系统结构检查系统错误 (退出码: {result.returncode}): {result.stderr}")
            return False

    except Exception as e:
        logger.error(f"运行系统结构检查时出错: {e}")
        return False


def check_mcp_servers():
    """检查MCP服务器状态"""
    logger.info("检查MCP服务器集群状态...")
    
    try:
        mcp_manager_script = TOOLS_DIR / "mcp_server_manager.py"
        if mcp_manager_script.exists():
            result = subprocess.run(
                [sys.executable, str(mcp_manager_script), "status"],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                logger.info("MCP服务器状态检查完成")
                if result.stdout:
                    # 清理输出中的特殊字符，避免编码问题
                    clean_output = result.stdout.encode('ascii', 'ignore').decode('ascii')
                    logger.info(f"MCP状态报告:\n{clean_output}")
                return True
            else:
                logger.warning(f"MCP服务器状态检查异常: {result.stderr}")
                return False
        else:
            logger.warning("MCP服务器管理脚本不存在，跳过检查")
            return True
            
    except Exception as e:
        logger.error(f"检查MCP服务器状态时发生异常: {e}")
        return False


def organize_office_documents():
    """整理办公文档"""
    logger.info("开始整理办公文档...")
    
    try:
        # 检查办公目录
        if OFFICE_DIR.exists():
            # 统计文档数量
            doc_count = len(list(OFFICE_DIR.rglob("*.docx")))
            excel_count = len(list(OFFICE_DIR.rglob("*.xlsx")))
            ppt_count = len(list(OFFICE_DIR.rglob("*.pptx")))
            
            logger.info(f"办公文档统计: Word文档 {doc_count} 个, Excel文档 {excel_count} 个, PowerPoint文档 {ppt_count} 个")
        
        # 检查输出目录
        if OUTPUT_DIR.exists():
            output_files = len(list(OUTPUT_DIR.rglob("*.*")))
            logger.info(f"输出文件统计: {output_files} 个文件")
        
        return True
        
    except Exception as e:
        logger.error(f"整理办公文档时发生异常: {e}")
        return False


def run_backup(full_backup=False):
    """执行备份操作
    
    Args:
        full_backup (bool): 是否进行全量zip压缩备份
    """
    logger.info("开始备份操作...")

    try:
        if full_backup:
            # 全量zip压缩备份
            return run_full_zip_backup()
        else:
            # 核心文件备份
            return run_core_files_backup()

    except Exception as e:
        logger.error(f"执行备份时出错: {e}")
        return False


def run_core_files_backup():
    """执行核心文件备份"""
    logger.info("开始核心文件备份...")
    
    try:
        # 创建备份目录
        backup_base_dir = PROJECT_ROOT / "bak" / "专项备份"
        backup_base_dir.mkdir(parents=True, exist_ok=True)

        # 生成备份目录名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = backup_base_dir / f"自动备份_{timestamp}"
        backup_dir.mkdir(exist_ok=True)

        # 定义需要备份的核心文件
        core_files = [
            "docs/01-设计/开发任务书.md",
            "docs/01-设计/技术方案.md",
            "docs/01-设计/项目架构设计.md",
            "docs/01-设计/目录结构标准清单.md",
            "docs/03-管理/规范与流程.md",
            "docs/03-管理/project_config.yaml",
            "tools/finish.py",
            "tools/control.py",
            "tools/check_structure.py",
            "tools/update_structure.py",
            "tools/start.py",
        ]

        backup_count = 0
        for file_path in core_files:
            source_file = PROJECT_ROOT / file_path
            if source_file.exists():
                # 创建目标目录
                target_file = backup_dir / file_path
                target_file.parent.mkdir(parents=True, exist_ok=True)

                # 复制文件
                shutil.copy2(source_file, target_file)
                backup_count += 1

        logger.info(f"核心文件备份完成，已备份 {backup_count} 个文件到: {backup_dir}")
        return True

    except Exception as e:
        logger.error(f"执行核心文件备份时出错: {e}")
        return False


def run_full_zip_backup():
    """执行全量zip压缩备份"""
    logger.info("开始全量zip压缩备份...")
    
    try:
        import zipfile
        
        # 创建常规备份目录
        backup_base_dir = PROJECT_ROOT / "bak" / "常规备份"
        backup_base_dir.mkdir(parents=True, exist_ok=True)

        # 生成备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_base_dir / f"全量备份_{timestamp}.zip"
        
        # 需要备份的目录（全量备份包含office、02-Output、01-Input和03-WorkTask目录）
        backup_dirs = ["docs", "project", "tools", "data", "docker", "AI调度表", "office", "02-Output", "01-Input", "03-WorkTask"]
        
        total_files = 0
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dir_name in backup_dirs:
                source_dir = PROJECT_ROOT / dir_name
                if source_dir.exists():
                    logger.info(f"正在压缩目录: {dir_name}")
                    for file_path in source_dir.rglob('*'):
                        if file_path.is_file():
                            # 计算相对路径
                            relative_path = file_path.relative_to(PROJECT_ROOT)
                            zipf.write(file_path, relative_path)
                            total_files += 1
                            
                            # 每100个文件输出一次进度
                            if total_files % 100 == 0:
                                logger.info(f"已压缩 {total_files} 个文件...")
                else:
                    logger.warning(f"目录不存在，跳过: {dir_name}")
        
        # 获取压缩文件大小
        file_size_mb = backup_file.stat().st_size / (1024 * 1024)
        
        logger.info(f"全量zip压缩备份完成！")
        logger.info(f"备份文件: {backup_file}")
        logger.info(f"压缩文件数: {total_files}")
        logger.info(f"文件大小: {file_size_mb:.2f} MB")
        
        return True

    except Exception as e:
        logger.error(f"执行全量zip压缩备份时出错: {e}")
        return False


def run_pre_commit_check():
    """运行Git提交前检查"""
    logger.info("开始Git提交前检查...")

    check_script = GIT_REPO_DIR / "tools" / "git_pre_commit_check.py"
    if not check_script.exists():
        logger.warning(f"提交前检查脚本不存在: {check_script}")
        return True  # 如果脚本不存在，允许继续

    try:
        result = subprocess.run(
            [sys.executable, str(check_script)],
            cwd=str(GIT_REPO_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",  # 忽略编码错误
        )

        if result.returncode == 0:
            logger.info("Git提交前检查通过")
            return True
        else:
            logger.error(f"Git提交前检查失败: {result.stderr}")
            print(result.stdout)  # 显示检查结果
            return False

    except Exception as e:
        logger.error(f"运行Git提交前检查时出错: {e}")
        return False


def sync_to_backup_repo():
    """同步当前内容到备份仓库目录"""
    logger.info("开始同步当前内容到备份仓库...")
    
    try:
        # 需要同步的目录
        sync_dirs = ['docs', 'project', 'tools', 'data', 'docker']
        
        for dir_name in sync_dirs:
            source_dir = PROJECT_ROOT / dir_name
            target_dir = GIT_REPO_DIR / dir_name
            
            if source_dir.exists():
                logger.info(f"同步目录: {dir_name}")
                
                # 删除目标目录（如果存在）
                if target_dir.exists():
                    try:
                        shutil.rmtree(target_dir)
                    except Exception as e:
                        logger.warning(f"删除目标目录失败: {e}，尝试重命名")
                        # 如果删除失败，尝试重命名
                        backup_name = f"{target_dir.name}_backup_{int(time.time())}"
                        backup_path = target_dir.parent / backup_name
                        target_dir.rename(backup_path)
                        logger.info(f"目标目录已重命名为: {backup_path}")
                
                # 复制源目录到目标位置（跳过Git子模块）
                copy_directory_excluding_git(source_dir, target_dir)
                logger.info(f"✅ {dir_name} 目录同步完成")
            else:
                logger.warning(f"源目录不存在，跳过: {dir_name}")
        
        logger.info("内容同步到备份仓库完成")
        return True
        
    except Exception as e:
        logger.error(f"同步内容到备份仓库时出错: {e}")
        return False


def copy_directory_excluding_git(source_dir, target_dir):
    """复制目录，但跳过.git文件夹"""
    import shutil
    import time
    
    def ignore_git_dirs(dir_path, names):
        """忽略.git目录、__pycache__目录和其他不需要的文件"""
        ignore_list = []
        for name in names:
            if name == '.git' or name.startswith('.git'):
                ignore_list.append(name)
            elif name == '__pycache__' or name.endswith('.pyc') or name.endswith('.pyo'):
                ignore_list.append(name)
            elif name.endswith('.tmp') or name.endswith('.lock'):
                ignore_list.append(name)
        return ignore_list
    
    try:
        shutil.copytree(source_dir, target_dir, ignore=ignore_git_dirs)
    except Exception as e:
        logger.warning(f"复制目录失败: {e}，尝试手动复制")
        
        # 手动复制文件，跳过有问题的文件
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for item in source_dir.rglob('*'):
            if item.is_file():
                rel_path_parts = str(item.relative_to(source_dir)).split('/')
                
                # 检查是否在.git目录中
                if '.git' in rel_path_parts:
                    continue
                
                # 检查是否在__pycache__目录中或是Python缓存文件
                if '__pycache__' in rel_path_parts or item.suffix in ['.pyc', '.pyo']:
                    continue
                    
                # 计算目标文件路径
                rel_path = item.relative_to(source_dir)
                target_file = target_dir / rel_path
                
                try:
                    # 创建目标目录
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    # 复制文件
                    shutil.copy2(item, target_file)
                except Exception as file_error:
                    logger.warning(f"复制文件失败 {item}: {file_error}")


def run_git_push():
    """执行Git推送"""
    logger.info("开始Git推送...")
    
    # 设置GitHub认证
    if not setup_git_authentication():
        logger.warning("未能配置GitHub认证，使用默认Git配置")

    # 检查git仓库目录是否存在
    if not GIT_REPO_DIR.exists():
        logger.error(f"Git仓库目录不存在: {GIT_REPO_DIR}")
        return False

    # 检查是否为git仓库
    if not (GIT_REPO_DIR / ".git").exists():
        logger.error(f"目录不是Git仓库: {GIT_REPO_DIR}")
        return False
    
    # 先同步当前内容到备份仓库
    if not sync_to_backup_repo():
        logger.error("同步内容到备份仓库失败，取消Git推送")
        return False

    try:
        # 检查Git状态
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(GIT_REPO_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        if result.stdout.strip():
            # 有未提交的更改
            logger.info("发现未提交的更改，开始提交...")

            # 添加所有更改
            subprocess.run(
                ["git", "add", "."],
                cwd=str(GIT_REPO_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                check=True,
            )

            # 运行提交前检查
            logger.info("执行提交前检查...")
            if not run_pre_commit_check():
                logger.error("提交前检查失败，取消提交")
                return False

            # 提交更改
            commit_prefix = git_config.get("commit_message_prefix", "自动备份")
            commit_msg = (
                f"{commit_prefix} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=str(GIT_REPO_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                check=True,
            )

            logger.info("更改已提交")

        # 推送到远程仓库
        # 先更新远程仓库URL（如果有GitHub配置）
        github_config = load_github_config()
        github_info = github_config.get('github', {})
        if github_info.get('username') and github_info.get('token'):
            username = github_info['username']
            token = github_info['token']
            repo_url = github_info.get('repository', {}).get('url', '')
            
            if repo_url:
                # 使用带认证的URL
                authenticated_url = repo_url.replace("https://", f"https://{username}:{token}@")
                try:
                    subprocess.run(
                        ["git", "remote", "set-url", "origin", authenticated_url],
                        cwd=str(GIT_REPO_DIR),
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    logger.info("✓ 已更新远程仓库URL为带认证的URL")
                except subprocess.CalledProcessError:
                    logger.warning("更新远程仓库URL失败，使用现有配置")
        
        result = subprocess.run(
            ["git", "push"],
            cwd=str(GIT_REPO_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        if result.returncode == 0:
            logger.info("Git推送完成")
            return True
        else:
            logger.error(f"Git推送失败: {result.stderr}")
            return False

    except subprocess.CalledProcessError as e:
        logger.error(f"Git操作失败: {e}")
        return False
    except Exception as e:
        logger.error(f"执行Git推送时出错: {e}")
        return False


def main():
    """主函数"""
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='高效办公助手系统完成脚本')
    parser.add_argument('--full-backup', action='store_true', default=False,
                       help='进行全量zip压缩备份到常规备份目录')
    parser.add_argument('--core-backup', action='store_true', default=True,
                       help='进行核心文件备份（默认启用）')
    parser.add_argument('--backup-only', action='store_true',
                       help='仅执行备份操作，跳过结构检查和Git推送')
    args = parser.parse_args()
    
    # 如果指定了全量备份，则覆盖默认的核心备份
    if args.full_backup:
        args.core_backup = False
    
    try:
        logger.info("启动高效办公助手系统完成流程")
        logger.info(f"项目根目录: {PROJECT_ROOT}")
        if args.full_backup:
            logger.info("[模式] 全量zip压缩备份模式")
        elif args.core_backup:
            logger.info("[模式] 核心文件备份模式（默认）")
        if args.backup_only:
            logger.info("[模式] 仅备份模式")
        logger.info("-" * 60)

        success_count = 0
        total_steps = 1 if args.backup_only else 6  # 包含看板更新、MCP检查、办公文档整理步骤
        logger.debug(f"初始化完成，准备执行 {total_steps} 个步骤")
        
        # 0. 更新看板（在备份和Git推送之前）
        logger.info("\n[STEP 0/6] 更新项目看板")
        kb_success = False
        try:
            kb_script = TOOLS_DIR / "kb.py"
            if kb_script.exists():
                # 使用 kb.py --update 更新看板
                command = [sys.executable, str(kb_script), "--update", "--non-interactive"]
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',

                    cwd=str(TOOLS_DIR)
                )

                # 将 kb.py 的输出通过 logger 记录
                if result.stdout and result.stdout.strip():
                    output = result.stdout.rstrip()
                    logger.info(f"\n---看板更新脚本输出---\n{output}\n----------------------")
                if result.stderr and result.stderr.strip():
                    logger.warning(f"看板更新脚本错误输出:\n{result.stderr.strip()}")

                logger.info("✅ 看板更新完成")
                kb_success = True
            else:
                logger.warning("⚠️ 未找到kb.py脚本")
                kb_success = True  # 如果脚本不存在，视为成功（可选步骤）

        except subprocess.CalledProcessError as e:
            logger.error(f"看板更新失败: {e}")
            if e.stdout and e.stdout.strip():
                logger.error(f"STDOUT: {e.stdout.strip()}")
            if e.stderr and e.stderr.strip():
                logger.error(f"STDERR: {e.stderr.strip()}")
        except Exception as e:
            logger.warning(f"⚠️ 看板更新异常: {e}")

        if kb_success:
            success_count += 1
            logger.info("[SUCCESS] 看板更新完成")
        else:
            logger.error("[FAILED] 看板更新失败")

        if not args.backup_only:
            # 1. 目录结构检查
            logger.info("\n[STEP 1/6] 高效办公助手系统结构检查")
            check_result = run_structure_check()
            logger.debug(f"系统结构检查返回值: {check_result}")
            if check_result:
                success_count += 1
                logger.info("[SUCCESS] 系统结构检查完成")
            else:
                logger.error("[FAILED] 系统结构检查失败")

            # 2. MCP服务器状态检查
            logger.info("\n[STEP 2/6] MCP服务器状态检查")
            mcp_result = check_mcp_servers()
            logger.debug(f"MCP服务器检查返回值: {mcp_result}")
            if mcp_result:
                success_count += 1
                logger.info("[SUCCESS] MCP服务器状态检查完成")
            else:
                logger.warning("[WARNING] MCP服务器状态检查异常，但继续执行")

            # 3. 办公文档整理
            logger.info("\n[STEP 3/6] 办公文档整理")
            office_result = organize_office_documents()
            logger.debug(f"办公文档整理返回值: {office_result}")
            if office_result:
                success_count += 1
                logger.info("[SUCCESS] 办公文档整理完成")
            else:
                logger.warning("[WARNING] 办公文档整理异常，但继续执行")

        # 4. 备份操作
        step_num = "1/1" if args.backup_only else "4/6"
        logger.info(f"\n[STEP {step_num}] 备份操作")
        backup_result = run_backup(full_backup=args.full_backup)
        logger.debug(f"备份操作返回值: {backup_result}")
        if backup_result:
            success_count += 1
            logger.info("[SUCCESS] 备份操作完成")
        else:
            logger.error("[FAILED] 备份操作失败")

        if not args.backup_only:
            # 5. Git推送
            logger.info("\n[STEP 5/6] Git推送")
            if run_git_push():
                success_count += 1
                logger.info("[SUCCESS] Git推送完成")
            else:
                logger.error("[FAILED] Git推送失败")

        # 总结
        logger.info("\n" + "=" * 60)
        logger.info(f"[SUMMARY] 完成情况: {success_count}/{total_steps} 步骤成功")

        if success_count == total_steps:
            logger.info("[COMPLETE] 高效办公助手系统所有步骤都已成功完成！")
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