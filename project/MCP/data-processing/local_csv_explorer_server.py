#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地CSV数据探索MCP服务器

功能：
1. CSV文件读取和解析
2. 数据统计分析
3. 数据质量检查
4. 数据清洗建议
5. 数据可视化信息
6. 大文件分块处理
"""

import json
import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import chardet
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class LocalCSVExplorer:
    def __init__(self, max_rows: int = 10000):
        self.max_rows = max_rows
        self.logger = logging.getLogger(__name__)
        self.loaded_files = {}
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def detect_encoding(self, file_path: str) -> str:
        """检测文件编码"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # 读取前10KB检测编码
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8')
        except Exception as e:
            self.logger.warning(f"编码检测失败，使用默认UTF-8: {e}")
            return 'utf-8'
    
    def load_csv(self, file_path: str, **kwargs) -> Dict:
        """加载CSV文件"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"status": "error", "message": "文件不存在"}
            
            # 检测编码
            encoding = kwargs.get('encoding') or self.detect_encoding(str(file_path))
            
            # 读取CSV文件
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                nrows=self.max_rows,
                **{k: v for k, v in kwargs.items() if k != 'encoding'}
            )
            
            # 存储到内存
            file_key = str(file_path)
            self.loaded_files[file_key] = {
                'dataframe': df,
                'file_path': file_key,
                'loaded_at': datetime.now().isoformat(),
                'encoding': encoding,
                'original_shape': df.shape
            }
            
            return {
                "status": "success",
                "message": f"成功加载CSV文件: {file_path.name}",
                "file_key": file_key,
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "encoding": encoding
            }
        except Exception as e:
            return {"status": "error", "message": f"加载CSV文件失败: {str(e)}"}
    
    def get_basic_info(self, file_key: str) -> Dict:
        """获取数据基本信息"""
        try:
            if file_key not in self.loaded_files:
                return {"status": "error", "message": "文件未加载"}
            
            df = self.loaded_files[file_key]['dataframe']
            
            # 基本信息
            info = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "null_counts": df.isnull().sum().to_dict(),
                "duplicate_rows": df.duplicated().sum()
            }
            
            # 数据类型统计
            dtype_counts = df.dtypes.value_counts().to_dict()
            info["dtype_summary"] = {str(k): v for k, v in dtype_counts.items()}
            
            return {
                "status": "success",
                "info": info,
                "file_info": {
                    "file_path": self.loaded_files[file_key]['file_path'],
                    "loaded_at": self.loaded_files[file_key]['loaded_at'],
                    "encoding": self.loaded_files[file_key]['encoding']
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_statistical_summary(self, file_key: str, columns: Optional[List[str]] = None) -> Dict:
        """获取统计摘要"""
        try:
            if file_key not in self.loaded_files:
                return {"status": "error", "message": "文件未加载"}
            
            df = self.loaded_files[file_key]['dataframe']
            
            if columns:
                df = df[columns]
            
            # 数值列统计
            numeric_summary = {}
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                numeric_summary = df[numeric_cols].describe().to_dict()
            
            # 分类列统计
            categorical_summary = {}
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            for col in categorical_cols:
                categorical_summary[col] = {
                    "unique_count": df[col].nunique(),
                    "most_frequent": df[col].mode().iloc[0] if not df[col].mode().empty else None,
                    "value_counts": df[col].value_counts().head(10).to_dict()
                }
            
            return {
                "status": "success",
                "numeric_summary": numeric_summary,
                "categorical_summary": categorical_summary,
                "column_types": {
                    "numeric": numeric_cols.tolist(),
                    "categorical": categorical_cols.tolist()
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_data_quality(self, file_key: str) -> Dict:
        """数据质量检查"""
        try:
            if file_key not in self.loaded_files:
                return {"status": "error", "message": "文件未加载"}
            
            df = self.loaded_files[file_key]['dataframe']
            
            quality_issues = []
            recommendations = []
            
            # 检查缺失值
            missing_data = df.isnull().sum()
            high_missing_cols = missing_data[missing_data > len(df) * 0.5].index.tolist()
            if high_missing_cols:
                quality_issues.append(f"高缺失率列: {high_missing_cols}")
                recommendations.append("考虑删除或填充高缺失率列")
            
            # 检查重复行
            duplicate_count = df.duplicated().sum()
            if duplicate_count > 0:
                quality_issues.append(f"重复行数: {duplicate_count}")
                recommendations.append("考虑删除重复行")
            
            # 检查数据类型
            for col in df.columns:
                if df[col].dtype == 'object':
                    # 检查是否应该是数值类型
                    try:
                        pd.to_numeric(df[col], errors='raise')
                        quality_issues.append(f"列 '{col}' 可能应该是数值类型")
                        recommendations.append(f"考虑将列 '{col}' 转换为数值类型")
                    except:
                        pass
            
            # 检查异常值（仅数值列）
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            outlier_info = {}
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                if len(outliers) > 0:
                    outlier_info[col] = len(outliers)
            
            if outlier_info:
                quality_issues.append(f"异常值检测: {outlier_info}")
                recommendations.append("检查并处理异常值")
            
            return {
                "status": "success",
                "quality_score": max(0, 100 - len(quality_issues) * 10),
                "issues": quality_issues,
                "recommendations": recommendations,
                "detailed_checks": {
                    "missing_data": missing_data.to_dict(),
                    "duplicate_rows": int(duplicate_count),
                    "outliers": outlier_info
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_sample_data(self, file_key: str, n_rows: int = 10) -> Dict:
        """获取样本数据"""
        try:
            if file_key not in self.loaded_files:
                return {"status": "error", "message": "文件未加载"}
            
            df = self.loaded_files[file_key]['dataframe']
            
            sample_data = {
                "head": df.head(n_rows).to_dict('records'),
                "tail": df.tail(n_rows).to_dict('records'),
                "random_sample": df.sample(min(n_rows, len(df))).to_dict('records')
            }
            
            return {
                "status": "success",
                "sample_data": sample_data,
                "total_rows": len(df)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def filter_data(self, file_key: str, conditions: Dict) -> Dict:
        """数据过滤"""
        try:
            if file_key not in self.loaded_files:
                return {"status": "error", "message": "文件未加载"}
            
            df = self.loaded_files[file_key]['dataframe'].copy()
            
            # 应用过滤条件
            for column, condition in conditions.items():
                if column not in df.columns:
                    continue
                
                if isinstance(condition, dict):
                    if 'min' in condition:
                        df = df[df[column] >= condition['min']]
                    if 'max' in condition:
                        df = df[df[column] <= condition['max']]
                    if 'equals' in condition:
                        df = df[df[column] == condition['equals']]
                    if 'contains' in condition:
                        df = df[df[column].astype(str).str.contains(condition['contains'], na=False)]
            
            return {
                "status": "success",
                "filtered_shape": df.shape,
                "original_shape": self.loaded_files[file_key]['dataframe'].shape,
                "sample_data": df.head(10).to_dict('records')
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_correlation_matrix(self, file_key: str) -> Dict:
        """获取相关性矩阵"""
        try:
            if file_key not in self.loaded_files:
                return {"status": "error", "message": "文件未加载"}
            
            df = self.loaded_files[file_key]['dataframe']
            numeric_df = df.select_dtypes(include=[np.number])
            
            if numeric_df.empty:
                return {"status": "error", "message": "没有数值列可计算相关性"}
            
            correlation_matrix = numeric_df.corr().to_dict()
            
            # 找出高相关性对
            high_correlations = []
            for col1 in correlation_matrix:
                for col2 in correlation_matrix[col1]:
                    if col1 != col2 and abs(correlation_matrix[col1][col2]) > 0.7:
                        high_correlations.append({
                            "column1": col1,
                            "column2": col2,
                            "correlation": correlation_matrix[col1][col2]
                        })
            
            return {
                "status": "success",
                "correlation_matrix": correlation_matrix,
                "high_correlations": high_correlations,
                "numeric_columns": numeric_df.columns.tolist()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def list_loaded_files(self) -> Dict:
        """列出已加载的文件"""
        try:
            files_info = []
            for file_key, info in self.loaded_files.items():
                files_info.append({
                    "file_key": file_key,
                    "file_path": info['file_path'],
                    "shape": info['original_shape'],
                    "loaded_at": info['loaded_at'],
                    "encoding": info['encoding']
                })
            
            return {
                "status": "success",
                "loaded_files": files_info,
                "total_files": len(files_info)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

class CSVExplorerMCPServer:
    def __init__(self, max_rows: int = 10000):
        self.explorer = LocalCSVExplorer(max_rows)
        self.logger = logging.getLogger(__name__)
    
    def get_available_functions(self) -> Dict:
        """获取可用功能列表"""
        return {
            "functions": [
                {
                    "name": "load_csv",
                    "description": "加载CSV文件到内存",
                    "parameters": {
                        "file_path": "CSV文件路径",
                        "encoding": "文件编码（可选）",
                        "separator": "分隔符（可选）"
                    }
                },
                {
                    "name": "get_basic_info",
                    "description": "获取数据基本信息",
                    "parameters": {
                        "file_key": "文件标识符"
                    }
                },
                {
                    "name": "get_statistical_summary",
                    "description": "获取统计摘要",
                    "parameters": {
                        "file_key": "文件标识符",
                        "columns": "指定列名列表（可选）"
                    }
                },
                {
                    "name": "check_data_quality",
                    "description": "数据质量检查",
                    "parameters": {
                        "file_key": "文件标识符"
                    }
                },
                {
                    "name": "get_sample_data",
                    "description": "获取样本数据",
                    "parameters": {
                        "file_key": "文件标识符",
                        "n_rows": "样本行数（可选）"
                    }
                },
                {
                    "name": "filter_data",
                    "description": "数据过滤",
                    "parameters": {
                        "file_key": "文件标识符",
                        "conditions": "过滤条件字典"
                    }
                },
                {
                    "name": "get_correlation_matrix",
                    "description": "获取相关性矩阵",
                    "parameters": {
                        "file_key": "文件标识符"
                    }
                },
                {
                    "name": "list_loaded_files",
                    "description": "列出已加载的文件",
                    "parameters": {}
                }
            ]
        }
    
    def execute_function(self, function_name: str, **kwargs) -> Dict:
        """执行指定功能"""
        try:
            if function_name == "load_csv":
                return self.explorer.load_csv(
                    kwargs.get("file_path"),
                    **{k: v for k, v in kwargs.items() if k != "file_path"}
                )
            elif function_name == "get_basic_info":
                return self.explorer.get_basic_info(kwargs.get("file_key"))
            elif function_name == "get_statistical_summary":
                return self.explorer.get_statistical_summary(
                    kwargs.get("file_key"),
                    kwargs.get("columns")
                )
            elif function_name == "check_data_quality":
                return self.explorer.check_data_quality(kwargs.get("file_key"))
            elif function_name == "get_sample_data":
                return self.explorer.get_sample_data(
                    kwargs.get("file_key"),
                    kwargs.get("n_rows", 10)
                )
            elif function_name == "filter_data":
                return self.explorer.filter_data(
                    kwargs.get("file_key"),
                    kwargs.get("conditions", {})
                )
            elif function_name == "get_correlation_matrix":
                return self.explorer.get_correlation_matrix(kwargs.get("file_key"))
            elif function_name == "list_loaded_files":
                return self.explorer.list_loaded_files()
            else:
                return {"status": "error", "message": f"未知功能: {function_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_demo_data(self) -> Dict:
        """创建演示数据"""
        try:
            # 创建演示CSV文件
            demo_data = {
                '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'],
                '年龄': [25, 30, 35, 28, 32, 27, 29, 31],
                '城市': ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉'],
                '薪资': [8000, 12000, 15000, 11000, 13000, 9000, 10000, 14000],
                '部门': ['技术', '销售', '市场', '技术', '销售', '技术', '市场', '技术'],
                '入职日期': ['2020-01-15', '2019-03-20', '2018-06-10', '2021-02-28', 
                           '2020-08-05', '2021-05-12', '2019-11-30', '2020-12-18']
            }
            
            df = pd.DataFrame(demo_data)
            demo_file_path = Path("./demo_employees.csv")
            df.to_csv(demo_file_path, index=False, encoding='utf-8')
            
            # 加载演示文件
            load_result = self.explorer.load_csv(str(demo_file_path))
            
            return {
                "status": "success",
                "message": "演示数据创建成功",
                "demo_file": str(demo_file_path),
                "load_result": load_result
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

def main():
    """主函数 - 演示服务器功能"""
    print("🚀 启动本地CSV数据探索MCP服务器...")
    
    server = CSVExplorerMCPServer(max_rows=10000)
    
    # 显示可用功能
    functions = server.get_available_functions()
    print("\n📋 可用功能:")
    for func in functions["functions"]:
        print(f"  - {func['name']}: {func['description']}")
    
    # 创建演示数据
    print("\n🎯 创建演示数据...")
    demo_result = server.create_demo_data()
    print(f"演示数据创建结果: {demo_result['message']}")
    
    if demo_result["status"] == "success":
        file_key = demo_result["load_result"]["file_key"]
        
        # 获取基本信息
        print("\n📊 数据基本信息:")
        basic_info = server.execute_function("get_basic_info", file_key=file_key)
        if basic_info["status"] == "success":
            info = basic_info["info"]
            print(f"  - 数据形状: {info['shape']}")
            print(f"  - 列名: {info['columns']}")
            print(f"  - 缺失值: {sum(info['null_counts'].values())}")
        
        # 统计摘要
        print("\n📈 统计摘要:")
        stats = server.execute_function("get_statistical_summary", file_key=file_key)
        if stats["status"] == "success":
            print(f"  - 数值列: {stats['column_types']['numeric']}")
            print(f"  - 分类列: {stats['column_types']['categorical']}")
        
        # 数据质量检查
        print("\n🔍 数据质量检查:")
        quality = server.execute_function("check_data_quality", file_key=file_key)
        if quality["status"] == "success":
            print(f"  - 质量评分: {quality['quality_score']}/100")
            if quality['issues']:
                print(f"  - 发现问题: {quality['issues']}")
            if quality['recommendations']:
                print(f"  - 建议: {quality['recommendations']}")
        
        # 样本数据
        print("\n📋 样本数据:")
        sample = server.execute_function("get_sample_data", file_key=file_key, n_rows=3)
        if sample["status"] == "success":
            print("  前3行数据:")
            for i, row in enumerate(sample["sample_data"]["head"]):
                print(f"    {i+1}: {row}")
    
    print("\n✅ 本地CSV数据探索MCP服务器演示完成！")
    print("\n💡 使用说明:")
    print("1. 导入CSVExplorerMCPServer类")
    print("2. 创建服务器实例: server = CSVExplorerMCPServer()")
    print("3. 加载CSV文件: server.execute_function('load_csv', file_path='path/to/file.csv')")
    print("4. 使用各种分析功能探索数据")

if __name__ == "__main__":
    main()