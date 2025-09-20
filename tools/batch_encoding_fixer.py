#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量编码修复工具
功能：分类修复项目中的编码问题文件
作者：AI Assistant
创建时间：2025-01-14
"""

import os
import shutil
import chardet
from pathlib import Path
from datetime import datetime
import json
import logging
from typing import Dict, List, Tuple

class BatchEncodingFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "bak" / "编码修复备份" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.project_root / "logs" / "encoding_fix.log"
        
        # 创建必要目录
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 修复统计
        self.stats = {
            'utf8_sig_fixed': 0,
            'windows_1254_fixed': 0,
            'windows_1252_fixed': 0,
            'macroman_fixed': 0,
            'iso_8859_1_fixed': 0,
            'failed_files': [],
            'skipped_files': []
        }
    
    def detect_encoding(self, file_path: Path) -> Tuple[str, float]:
        """检测文件编码"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                return result['encoding'], result['confidence']
        except Exception as e:
            self.logger.error(f"检测编码失败 {file_path}: {e}")
            return None, 0.0
    
    def backup_file(self, file_path: Path) -> Path:
        """备份文件"""
        relative_path = file_path.relative_to(self.project_root)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def fix_utf8_sig(self, file_path: Path) -> bool:
        """修复UTF-8-SIG编码（移除BOM）"""
        try:
            # 备份文件
            self.backup_file(file_path)
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # 重新保存为UTF-8（无BOM）
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.stats['utf8_sig_fixed'] += 1
            self.logger.info(f"UTF-8-SIG修复成功: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"UTF-8-SIG修复失败 {file_path}: {e}")
            self.stats['failed_files'].append(str(file_path))
            return False
    
    def fix_windows_encoding(self, file_path: Path, encoding: str) -> bool:
        """修复Windows编码"""
        try:
            # 备份文件
            self.backup_file(file_path)
            
            # 读取文件内容
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # 检查是否包含中文字符
            if any('\u4e00' <= char <= '\u9fff' for char in content):
                self.logger.warning(f"文件包含中文字符，需要人工验证: {file_path}")
            
            # 重新保存为UTF-8
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if encoding == 'Windows-1254':
                self.stats['windows_1254_fixed'] += 1
            elif encoding == 'Windows-1252':
                self.stats['windows_1252_fixed'] += 1
            
            self.logger.info(f"{encoding}修复成功: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"{encoding}修复失败 {file_path}: {e}")
            self.stats['failed_files'].append(str(file_path))
            return False
    
    def fix_special_encoding(self, file_path: Path, encoding: str) -> bool:
        """修复特殊编码（MacRoman, ISO-8859-1等）"""
        try:
            # 备份文件
            self.backup_file(file_path)
            
            # 读取文件内容
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # 重新保存为UTF-8
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if encoding == 'MacRoman':
                self.stats['macroman_fixed'] += 1
            elif encoding == 'ISO-8859-1':
                self.stats['iso_8859_1_fixed'] += 1
            
            self.logger.info(f"{encoding}修复成功: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"{encoding}修复失败 {file_path}: {e}")
            self.stats['failed_files'].append(str(file_path))
            return False
    
    def should_skip_file(self, file_path: Path) -> bool:
        """判断是否应该跳过文件"""
        # 跳过二进制文件
        binary_extensions = {'.exe', '.dll', '.so', '.dylib', '.bin', '.dat'}
        if file_path.suffix.lower() in binary_extensions:
            return True
        
        # 跳过特定目录
        skip_dirs = {'.git', '__pycache__', '.venv', 'node_modules'}
        if any(part in skip_dirs for part in file_path.parts):
            return True
        
        return False
    
    def fix_phase_1_utf8_sig(self) -> None:
        """第一阶段：修复UTF-8-SIG编码问题"""
        self.logger.info("开始第一阶段：修复UTF-8-SIG编码问题")
        
        # 读取编码检查结果
        encoding_result_file = self.project_root / "encoding_check_result_utf8.txt"
        if not encoding_result_file.exists():
            self.logger.error("编码检查结果文件不存在，请先运行编码检查")
            return
        
        utf8_sig_files = []
        try:
            with open(encoding_result_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('[ERROR]') and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if 'UTF-8-SIG' in next_line:
                        # 提取文件路径
                        path_part = line[7:].strip()  # 去掉 '[ERROR] '
                        file_path = self.project_root / path_part
                        if file_path.exists() and not self.should_skip_file(file_path):
                            utf8_sig_files.append(file_path)
        
        except Exception as e:
            self.logger.error(f"读取编码检查结果文件失败: {e}")
            return
        
        self.logger.info(f"发现 {len(utf8_sig_files)} 个UTF-8-SIG文件需要修复")
        
        for file_path in utf8_sig_files:
            self.fix_utf8_sig(file_path)
    
    def fix_phase_2_windows_encoding(self) -> None:
        """第二阶段：修复Windows编码问题"""
        self.logger.info("开始第二阶段：修复Windows编码问题")
        
        encoding_result_file = self.project_root / "encoding_check_result_utf8.txt"
        windows_files = []
        
        try:
            with open(encoding_result_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('[ERROR]') and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if 'Windows-1254' in next_line or 'Windows-1252' in next_line:
                        # 提取文件路径
                        path_part = line[7:].strip()  # 去掉 '[ERROR] '
                        file_path = self.project_root / path_part
                        encoding = 'Windows-1254' if 'Windows-1254' in next_line else 'Windows-1252'
                        if file_path.exists() and not self.should_skip_file(file_path):
                            windows_files.append((file_path, encoding))
        
        except Exception as e:
            self.logger.error(f"读取编码检查结果文件失败: {e}")
            return
        
        self.logger.info(f"发现 {len(windows_files)} 个Windows编码文件需要修复")
        
        for file_path, encoding in windows_files:
            self.fix_windows_encoding(file_path, encoding)
    
    def fix_phase_3_special_encoding(self) -> None:
        """第三阶段：修复特殊编码问题"""
        self.logger.info("开始第三阶段：修复特殊编码问题")
        
        encoding_result_file = self.project_root / "encoding_check_result_utf8.txt"
        special_files = []
        
        try:
            with open(encoding_result_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('[ERROR]') and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if 'MacRoman' in next_line or 'ISO-8859-1' in next_line:
                        # 提取文件路径
                        path_part = line[7:].strip()  # 去掉 '[ERROR] '
                        file_path = self.project_root / path_part
                        encoding = 'MacRoman' if 'MacRoman' in next_line else 'ISO-8859-1'
                        if file_path.exists() and not self.should_skip_file(file_path):
                            special_files.append((file_path, encoding))
        
        except Exception as e:
            self.logger.error(f"读取编码检查结果文件失败: {e}")
            return
        
        self.logger.info(f"发现 {len(special_files)} 个特殊编码文件需要修复")
        
        for file_path, encoding in special_files:
            self.fix_special_encoding(file_path, encoding)
    
    def generate_report(self) -> None:
        """生成修复报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'backup_location': str(self.backup_dir),
            'statistics': self.stats,
            'total_fixed': sum([
                self.stats['utf8_sig_fixed'],
                self.stats['windows_1254_fixed'],
                self.stats['windows_1252_fixed'],
                self.stats['macroman_fixed'],
                self.stats['iso_8859_1_fixed']
            ])
        }
        
        report_file = self.project_root / "logs" / "encoding_fix_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"修复报告已生成: {report_file}")
        self.logger.info(f"总计修复文件: {report['total_fixed']} 个")
        self.logger.info(f"备份位置: {self.backup_dir}")
    
    def run_all_phases(self) -> None:
        """运行所有修复阶段"""
        self.logger.info("开始批量编码修复")
        
        try:
            self.fix_phase_1_utf8_sig()
            self.fix_phase_2_windows_encoding()
            self.fix_phase_3_special_encoding()
            self.generate_report()
            
            self.logger.info("批量编码修复完成")
            
        except Exception as e:
            self.logger.error(f"批量修复过程中出现错误: {e}")
            raise

def main():
    """主函数"""
    import sys
    
    project_root = "S:\\PG-GMO"
    fixer = BatchEncodingFixer(project_root)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--auto-fix-all':
            print("自动修复模式：运行所有阶段")
            fixer.run_all_phases()
            return
        elif sys.argv[1] == '--phase-1':
            print("运行第一阶段：修复UTF-8-SIG问题")
            fixer.fix_phase_1_utf8_sig()
            fixer.generate_report()
            return
        elif sys.argv[1] == '--phase-2':
            print("运行第二阶段：修复Windows编码问题")
            fixer.fix_phase_2_windows_encoding()
            fixer.generate_report()
            return
        elif sys.argv[1] == '--phase-3':
            print("运行第三阶段：修复特殊编码问题")
            fixer.fix_phase_3_special_encoding()
            fixer.generate_report()
            return
    
    print("批量编码修复工具")
    print("=================")
    print("1. 第一阶段：修复UTF-8-SIG问题（低风险）")
    print("2. 第二阶段：修复Windows编码问题（中风险）")
    print("3. 第三阶段：修复特殊编码问题（高风险）")
    print("4. 运行所有阶段")
    print("0. 退出")
    print("\n提示：可使用命令行参数 --auto-fix-all 直接运行所有阶段")
    
    while True:
        try:
            choice = input("\n请选择操作 (0-4): ").strip()
        except EOFError:
            print("\n检测到非交互模式，退出程序")
            break
        
        if choice == '0':
            break
        elif choice == '1':
            fixer.fix_phase_1_utf8_sig()
            fixer.generate_report()
        elif choice == '2':
            fixer.fix_phase_2_windows_encoding()
            fixer.generate_report()
        elif choice == '3':
            fixer.fix_phase_3_special_encoding()
            fixer.generate_report()
        elif choice == '4':
            try:
                confirm = input("确认运行所有修复阶段？这将修复数百个文件 (y/N): ")
                if confirm.lower() == 'y':
                    fixer.run_all_phases()
                else:
                    print("操作已取消")
            except EOFError:
                print("\n检测到非交互模式，自动确认运行所有阶段")
                fixer.run_all_phases()
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()