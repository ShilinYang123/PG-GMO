# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from ..check_structure import EnhancedStructureChecker  # check_structure.py 现在位于tools根目录

def main():
    root_path = Path(__file__).parent.parent.absolute()  # 项目根目录
    whitelist_file = root_path / 'docs' / '01-设计' / '目录结构标准清单.md'
    checker = EnhancedStructureChecker(str(root_path), str(whitelist_file))
    # 执行检查
    whitelist_structure = checker.parse_whitelist()
    current_structure = checker.scan_current_structure()
    checker.compare_structures(whitelist_structure, current_structure)
    
    # 输出检查结果
    compliance_rate = checker.stats.get("compliance_rate", 0)
    missing_items = checker.results.get("missing_items", [])
    extra_items = checker.results.get("extra_items", [])
    
    print(f"\n[STATS] 检查统计信息:")
    print(f"   [DIR] 目录数量: {checker.stats['total_dirs_actual']} (标准: {checker.stats['total_dirs_expected']})")
    print(f"   [FILE] 文件数量: {checker.stats['total_files_actual']} (标准: {checker.stats['total_files_expected']})")
    print(f"   [SUCCESS] 合规率: {compliance_rate:.1f}%")
    print(f"   [ERROR] 缺失数量: {len(missing_items)}")
    print(f"   [WARNING] 多余数量: {len(extra_items)}")
    
    sys.exit(0)

if __name__ == '__main__':
    main()