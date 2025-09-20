#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编码规范符合性分析工具
分析项目中的编码问题文件是否违反了项目编码规范
"""

import os
import chardet
from pathlib import Path

def detect_encoding(file_path):
    """检测文件编码"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            if not raw_data:
                return 'empty', 1.0
            
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            
            if encoding is None:
                return 'unknown', 0.0
            
            return encoding, confidence
    except Exception as e:
        return f'error: {str(e)}', 0.0

def is_utf8_compliant(encoding):
    """检查编码是否符合UTF-8规范"""
    if encoding is None:
        return False
    
    encoding_lower = encoding.lower()
    # 严格的UTF-8规范：只接受utf-8，不接受utf-8-sig
    return encoding_lower == 'utf-8'

def is_acceptable_encoding(encoding):
    """检查编码是否可接受（包括UTF-8-SIG）"""
    if encoding is None:
        return False
    
    encoding_lower = encoding.lower()
    # 可接受的编码：utf-8 和 utf-8-sig
    return encoding_lower in ['utf-8', 'utf-8-sig']

def analyze_encoding_compliance():
    """分析编码规范符合性"""
    project_root = Path('S:/PG-GMO')
    
    # 排除的目录
    exclude_dirs = {
        '.git', '.venv', '__pycache__', 'node_modules', '.pytest_cache',
        'venv', 'env', '.env', 'build', 'dist', '.tox', '.coverage',
        'htmlcov', '.mypy_cache', '.idea', '.vscode'
    }
    
    # 需要检查的文件扩展名
    check_extensions = {
        '.py', '.md', '.txt', '.json', '.yaml', '.yml', '.html', '.css', 
        '.js', '.ts', '.xml', '.csv', '.sql', '.sh', '.bat', '.ps1',
        '.rst', '.ini', '.cfg', '.conf', '.toml'
    }
    
    total_files = 0
    problem_files = 0
    strict_violations = 0  # 严格违反UTF-8规范的文件
    acceptable_files = 0   # 可接受但不是严格UTF-8的文件
    
    violations_by_type = {}
    strict_violations_list = []
    acceptable_but_not_strict = []
    
    print("Encoding Compliance Analysis")
    print("=" * 50)
    print("Project Encoding Standard: UTF-8 (strict)")
    print("Acceptable: UTF-8, UTF-8-SIG (with BOM)")
    print("=" * 50)
    
    for root, dirs, files in os.walk(project_root):
        # 排除指定目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = Path(root) / file
            
            # 只检查指定扩展名的文件
            if file_path.suffix.lower() not in check_extensions:
                continue
            
            total_files += 1
            encoding, confidence = detect_encoding(file_path)
            
            # 检查是否符合严格UTF-8规范
            if not is_utf8_compliant(encoding):
                problem_files += 1
                
                # 检查是否至少是可接受的编码
                if is_acceptable_encoding(encoding):
                    acceptable_files += 1
                    acceptable_but_not_strict.append({
                        'file': str(file_path.relative_to(project_root)),
                        'encoding': encoding,
                        'confidence': confidence
                    })
                else:
                    strict_violations += 1
                    strict_violations_list.append({
                        'file': str(file_path.relative_to(project_root)),
                        'encoding': encoding,
                        'confidence': confidence
                    })
                
                # 统计违规类型
                if encoding not in violations_by_type:
                    violations_by_type[encoding] = 0
                violations_by_type[encoding] += 1
    
    # 输出分析结果
    print(f"\nSummary:")
    print(f"Total files checked: {total_files}")
    print(f"Files with encoding issues: {problem_files}")
    print(f"Strict UTF-8 violations: {strict_violations}")
    print(f"Acceptable but not strict UTF-8: {acceptable_files}")
    print(f"Compliant files: {total_files - problem_files}")
    
    compliance_rate = ((total_files - strict_violations) / total_files * 100) if total_files > 0 else 0
    strict_compliance_rate = ((total_files - problem_files) / total_files * 100) if total_files > 0 else 0
    
    print(f"\nCompliance Rates:")
    print(f"Acceptable encoding compliance: {compliance_rate:.1f}%")
    print(f"Strict UTF-8 compliance: {strict_compliance_rate:.1f}%")
    
    print(f"\nViolation Types:")
    for encoding_type, count in sorted(violations_by_type.items()):
        severity = "CRITICAL" if encoding_type.lower() not in ['utf-8-sig'] else "MINOR"
        print(f"  {encoding_type}: {count} files [{severity}]")
    
    # 显示严重违规文件（前10个）
    if strict_violations_list:
        print(f"\nCritical Violations (Non-UTF-8 encodings):")
        for i, violation in enumerate(strict_violations_list[:10]):
            print(f"  {i+1}. {violation['file']} - {violation['encoding']} (confidence: {violation['confidence']:.2f})")
        if len(strict_violations_list) > 10:
            print(f"  ... and {len(strict_violations_list) - 10} more files")
    
    # 显示可接受但不严格的文件（前5个）
    if acceptable_but_not_strict:
        print(f"\nAcceptable but not strict UTF-8 (UTF-8-SIG with BOM):")
        for i, file_info in enumerate(acceptable_but_not_strict[:5]):
            print(f"  {i+1}. {file_info['file']} - {file_info['encoding']}")
        if len(acceptable_but_not_strict) > 5:
            print(f"  ... and {len(acceptable_but_not_strict) - 5} more files")
    
    print(f"\nConclusion:")
    if strict_violations == 0:
        if acceptable_files == 0:
            print("✅ All files comply with UTF-8 encoding standard.")
        else:
            print(f"⚠️  All files use acceptable encodings, but {acceptable_files} files use UTF-8-SIG (with BOM).")
            print("   Consider converting UTF-8-SIG files to pure UTF-8 for strict compliance.")
    else:
        print(f"❌ {strict_violations} files violate the UTF-8 encoding standard.")
        print("   These files must be converted to UTF-8 encoding to comply with project standards.")
    
    return {
        'total_files': total_files,
        'problem_files': problem_files,
        'strict_violations': strict_violations,
        'acceptable_files': acceptable_files,
        'violations_by_type': violations_by_type,
        'compliance_rate': compliance_rate,
        'strict_compliance_rate': strict_compliance_rate
    }

if __name__ == '__main__':
    analyze_encoding_compliance()