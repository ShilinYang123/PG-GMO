#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地数据库MCP服务器

支持的数据库类型：
1. SQLite - 轻量级文件数据库
2. MySQL - 关系型数据库（需要连接信息）
3. PostgreSQL - 高级关系型数据库（需要连接信息）
4. SQL Server - 微软数据库（需要连接信息）

功能：
1. 数据库连接管理
2. SQL查询执行
3. 表结构查询
4. 数据导入导出
5. 批量操作
6. 事务管理
"""

import json
import logging
import sqlite3
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime
import pandas as pd
import os

# 尝试导入其他数据库驱动（可选）
try:
    import pymysql
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

try:
    import psycopg2
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False

try:
    import pyodbc
    SQLSERVER_AVAILABLE = True
except ImportError:
    SQLSERVER_AVAILABLE = False

class DatabaseConnection:
    """数据库连接管理器"""
    
    def __init__(self, db_type: str, connection_params: Dict):
        self.db_type = db_type.lower()
        self.connection_params = connection_params
        self.connection = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> Dict:
        """建立数据库连接"""
        try:
            if self.db_type == 'sqlite':
                db_path = self.connection_params.get('database', ':memory:')
                self.connection = sqlite3.connect(db_path)
                self.connection.row_factory = sqlite3.Row  # 返回字典格式结果
                
            elif self.db_type == 'mysql':
                if not MYSQL_AVAILABLE:
                    return {"status": "error", "message": "MySQL驱动未安装，请安装pymysql"}
                
                self.connection = pymysql.connect(
                    host=self.connection_params.get('host', 'localhost'),
                    port=self.connection_params.get('port', 3306),
                    user=self.connection_params.get('user'),
                    password=self.connection_params.get('password'),
                    database=self.connection_params.get('database'),
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                
            elif self.db_type == 'postgresql':
                if not POSTGRESQL_AVAILABLE:
                    return {"status": "error", "message": "PostgreSQL驱动未安装，请安装psycopg2"}
                
                self.connection = psycopg2.connect(
                    host=self.connection_params.get('host', 'localhost'),
                    port=self.connection_params.get('port', 5432),
                    user=self.connection_params.get('user'),
                    password=self.connection_params.get('password'),
                    database=self.connection_params.get('database')
                )
                
            elif self.db_type == 'sqlserver':
                if not SQLSERVER_AVAILABLE:
                    return {"status": "error", "message": "SQL Server驱动未安装，请安装pyodbc"}
                
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.connection_params.get('host', 'localhost')};"
                    f"DATABASE={self.connection_params.get('database')};"
                    f"UID={self.connection_params.get('user')};"
                    f"PWD={self.connection_params.get('password')}"
                )
                self.connection = pyodbc.connect(connection_string)
                
            else:
                return {"status": "error", "message": f"不支持的数据库类型: {self.db_type}"}
            
            return {"status": "success", "message": f"成功连接到{self.db_type}数据库"}
            
        except Exception as e:
            return {"status": "error", "message": f"数据库连接失败: {str(e)}"}
    
    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Dict:
        """执行SQL查询"""
        try:
            if not self.connection:
                return {"status": "error", "message": "数据库未连接"}
            
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # 判断是否为查询语句
            if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN')):
                if self.db_type == 'sqlite':
                    results = [dict(row) for row in cursor.fetchall()]
                else:
                    results = cursor.fetchall()
                
                return {
                    "status": "success",
                    "data": results,
                    "row_count": len(results),
                    "columns": [desc[0] for desc in cursor.description] if cursor.description else []
                }
            else:
                # 非查询语句（INSERT, UPDATE, DELETE等）
                self.connection.commit()
                affected_rows = cursor.rowcount
                
                return {
                    "status": "success",
                    "message": f"操作完成，影响 {affected_rows} 行",
                    "affected_rows": affected_rows
                }
                
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return {"status": "error", "message": f"查询执行失败: {str(e)}"}
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def get_table_info(self, table_name: Optional[str] = None) -> Dict:
        """获取表信息"""
        try:
            if not self.connection:
                return {"status": "error", "message": "数据库未连接"}
            
            if self.db_type == 'sqlite':
                if table_name:
                    # 获取特定表的结构
                    query = f"PRAGMA table_info({table_name})"
                else:
                    # 获取所有表名
                    query = "SELECT name FROM sqlite_master WHERE type='table'"
            
            elif self.db_type == 'mysql':
                if table_name:
                    query = f"DESCRIBE {table_name}"
                else:
                    query = "SHOW TABLES"
            
            elif self.db_type == 'postgresql':
                if table_name:
                    query = f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table_name}'"
                else:
                    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            
            elif self.db_type == 'sqlserver':
                if table_name:
                    query = f"SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
                else:
                    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            
            return self.execute_query(query)
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

class LocalDatabaseMCPServer:
    def __init__(self):
        self.connections = {}
        self.logger = logging.getLogger(__name__)
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def get_available_functions(self) -> Dict:
        """获取可用功能列表"""
        return {
            "functions": [
                {
                    "name": "create_connection",
                    "description": "创建数据库连接",
                    "parameters": {
                        "connection_id": "连接标识符",
                        "db_type": "数据库类型 (sqlite/mysql/postgresql/sqlserver)",
                        "connection_params": "连接参数字典"
                    }
                },
                {
                    "name": "list_connections",
                    "description": "列出所有数据库连接",
                    "parameters": {}
                },
                {
                    "name": "execute_query",
                    "description": "执行SQL查询",
                    "parameters": {
                        "connection_id": "连接标识符",
                        "query": "SQL查询语句",
                        "params": "查询参数（可选）"
                    }
                },
                {
                    "name": "get_table_info",
                    "description": "获取表信息",
                    "parameters": {
                        "connection_id": "连接标识符",
                        "table_name": "表名（可选，不提供则列出所有表）"
                    }
                },
                {
                    "name": "import_csv_to_table",
                    "description": "将CSV文件导入到数据库表",
                    "parameters": {
                        "connection_id": "连接标识符",
                        "csv_file_path": "CSV文件路径",
                        "table_name": "目标表名",
                        "if_exists": "如果表存在的处理方式 (replace/append/fail)"
                    }
                },
                {
                    "name": "export_table_to_csv",
                    "description": "将数据库表导出为CSV文件",
                    "parameters": {
                        "connection_id": "连接标识符",
                        "table_name": "表名",
                        "csv_file_path": "输出CSV文件路径",
                        "query": "自定义查询（可选）"
                    }
                },
                {
                    "name": "close_connection",
                    "description": "关闭数据库连接",
                    "parameters": {
                        "connection_id": "连接标识符"
                    }
                },
                {
                    "name": "get_database_status",
                    "description": "获取数据库驱动状态",
                    "parameters": {}
                }
            ]
        }
    
    def execute_function(self, function_name: str, **kwargs) -> Dict:
        """执行指定功能"""
        try:
            if function_name == "create_connection":
                return self._create_connection(
                    kwargs.get("connection_id"),
                    kwargs.get("db_type"),
                    kwargs.get("connection_params", {})
                )
            elif function_name == "list_connections":
                return self._list_connections()
            elif function_name == "execute_query":
                return self._execute_query(
                    kwargs.get("connection_id"),
                    kwargs.get("query"),
                    kwargs.get("params")
                )
            elif function_name == "get_table_info":
                return self._get_table_info(
                    kwargs.get("connection_id"),
                    kwargs.get("table_name")
                )
            elif function_name == "import_csv_to_table":
                return self._import_csv_to_table(
                    kwargs.get("connection_id"),
                    kwargs.get("csv_file_path"),
                    kwargs.get("table_name"),
                    kwargs.get("if_exists", "replace")
                )
            elif function_name == "export_table_to_csv":
                return self._export_table_to_csv(
                    kwargs.get("connection_id"),
                    kwargs.get("table_name"),
                    kwargs.get("csv_file_path"),
                    kwargs.get("query")
                )
            elif function_name == "close_connection":
                return self._close_connection(kwargs.get("connection_id"))
            elif function_name == "get_database_status":
                return self._get_database_status()
            else:
                return {"status": "error", "message": f"未知功能: {function_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _create_connection(self, connection_id: str, db_type: str, connection_params: Dict) -> Dict:
        """创建数据库连接"""
        try:
            if connection_id in self.connections:
                return {"status": "error", "message": "连接ID已存在"}
            
            db_conn = DatabaseConnection(db_type, connection_params)
            result = db_conn.connect()
            
            if result["status"] == "success":
                self.connections[connection_id] = {
                    "connection": db_conn,
                    "db_type": db_type,
                    "created_at": datetime.now().isoformat(),
                    "connection_params": {k: v for k, v in connection_params.items() if k != 'password'}
                }
            
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _list_connections(self) -> Dict:
        """列出所有连接"""
        try:
            connections_info = []
            for conn_id, info in self.connections.items():
                connections_info.append({
                    "connection_id": conn_id,
                    "db_type": info["db_type"],
                    "created_at": info["created_at"],
                    "connection_params": info["connection_params"]
                })
            
            return {
                "status": "success",
                "connections": connections_info,
                "total": len(connections_info)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _execute_query(self, connection_id: str, query: str, params: Optional[tuple] = None) -> Dict:
        """执行SQL查询"""
        try:
            if connection_id not in self.connections:
                return {"status": "error", "message": "连接不存在"}
            
            db_conn = self.connections[connection_id]["connection"]
            return db_conn.execute_query(query, params)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _get_table_info(self, connection_id: str, table_name: Optional[str] = None) -> Dict:
        """获取表信息"""
        try:
            if connection_id not in self.connections:
                return {"status": "error", "message": "连接不存在"}
            
            db_conn = self.connections[connection_id]["connection"]
            return db_conn.get_table_info(table_name)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _import_csv_to_table(self, connection_id: str, csv_file_path: str, table_name: str, if_exists: str = "replace") -> Dict:
        """导入CSV到数据库表"""
        try:
            if connection_id not in self.connections:
                return {"status": "error", "message": "连接不存在"}
            
            if not Path(csv_file_path).exists():
                return {"status": "error", "message": "CSV文件不存在"}
            
            # 读取CSV文件
            df = pd.read_csv(csv_file_path)
            
            # 获取数据库连接
            db_info = self.connections[connection_id]
            db_type = db_info["db_type"]
            
            if db_type == "sqlite":
                # SQLite使用pandas的to_sql方法
                df.to_sql(table_name, db_info["connection"].connection, if_exists=if_exists, index=False)
            else:
                # 其他数据库需要更复杂的处理
                return {"status": "error", "message": f"暂不支持{db_type}的CSV导入功能"}
            
            return {
                "status": "success",
                "message": f"成功导入 {len(df)} 行数据到表 {table_name}",
                "rows_imported": len(df)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _export_table_to_csv(self, connection_id: str, table_name: str, csv_file_path: str, query: Optional[str] = None) -> Dict:
        """导出表到CSV文件"""
        try:
            if connection_id not in self.connections:
                return {"status": "error", "message": "连接不存在"}
            
            # 构建查询语句
            if query:
                sql_query = query
            else:
                sql_query = f"SELECT * FROM {table_name}"
            
            # 执行查询
            result = self._execute_query(connection_id, sql_query)
            if result["status"] != "success":
                return result
            
            # 转换为DataFrame并保存
            df = pd.DataFrame(result["data"])
            df.to_csv(csv_file_path, index=False, encoding='utf-8')
            
            return {
                "status": "success",
                "message": f"成功导出 {len(df)} 行数据到 {csv_file_path}",
                "rows_exported": len(df),
                "file_path": csv_file_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _close_connection(self, connection_id: str) -> Dict:
        """关闭数据库连接"""
        try:
            if connection_id not in self.connections:
                return {"status": "error", "message": "连接不存在"}
            
            self.connections[connection_id]["connection"].disconnect()
            del self.connections[connection_id]
            
            return {
                "status": "success",
                "message": f"连接 {connection_id} 已关闭"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _get_database_status(self) -> Dict:
        """获取数据库驱动状态"""
        try:
            status = {
                "sqlite": {"available": True, "description": "内置支持"},
                "mysql": {"available": MYSQL_AVAILABLE, "description": "需要pymysql包" if not MYSQL_AVAILABLE else "可用"},
                "postgresql": {"available": POSTGRESQL_AVAILABLE, "description": "需要psycopg2包" if not POSTGRESQL_AVAILABLE else "可用"},
                "sqlserver": {"available": SQLSERVER_AVAILABLE, "description": "需要pyodbc包" if not SQLSERVER_AVAILABLE else "可用"}
            }
            
            return {
                "status": "success",
                "database_drivers": status,
                "active_connections": len(self.connections)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_demo_database(self) -> Dict:
        """创建演示数据库"""
        try:
            # 创建SQLite演示数据库
            demo_db_path = "./demo_database.db"
            
            # 创建连接
            result = self._create_connection(
                "demo_sqlite",
                "sqlite",
                {"database": demo_db_path}
            )
            
            if result["status"] != "success":
                return result
            
            # 创建演示表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                department TEXT,
                salary REAL,
                hire_date TEXT
            )
            """
            
            table_result = self._execute_query("demo_sqlite", create_table_sql)
            if table_result["status"] != "success":
                return table_result
            
            # 插入演示数据
            insert_data = [
                ("张三", 28, "技术部", 8000.0, "2020-01-15"),
                ("李四", 32, "销售部", 12000.0, "2019-03-20"),
                ("王五", 35, "市场部", 15000.0, "2018-06-10"),
                ("赵六", 29, "技术部", 11000.0, "2021-02-28"),
                ("钱七", 31, "销售部", 13000.0, "2020-08-05")
            ]
            
            for data in insert_data:
                insert_sql = "INSERT INTO employees (name, age, department, salary, hire_date) VALUES (?, ?, ?, ?, ?)"
                self._execute_query("demo_sqlite", insert_sql, data)
            
            return {
                "status": "success",
                "message": "演示数据库创建成功",
                "database_path": demo_db_path,
                "connection_id": "demo_sqlite",
                "sample_data": insert_data
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

def main():
    """主函数 - 演示服务器功能"""
    print("🚀 启动本地数据库MCP服务器...")
    
    server = LocalDatabaseMCPServer()
    
    # 显示可用功能
    functions = server.get_available_functions()
    print("\n📋 可用功能:")
    for func in functions["functions"]:
        print(f"  - {func['name']}: {func['description']}")
    
    # 检查数据库驱动状态
    print("\n🔧 数据库驱动状态:")
    status = server.execute_function("get_database_status")
    if status["status"] == "success":
        for db_type, info in status["database_drivers"].items():
            status_icon = "✅" if info["available"] else "❌"
            print(f"  {status_icon} {db_type.upper()}: {info['description']}")
    
    # 创建演示数据库
    print("\n🎯 创建演示数据库...")
    demo_result = server.create_demo_database()
    print(f"演示数据库创建结果: {demo_result['message']}")
    
    if demo_result["status"] == "success":
        # 查询演示数据
        print("\n📊 查询演示数据:")
        query_result = server.execute_function(
            "execute_query",
            connection_id="demo_sqlite",
            query="SELECT * FROM employees LIMIT 3"
        )
        
        if query_result["status"] == "success":
            print(f"  查询到 {query_result['row_count']} 行数据:")
            for i, row in enumerate(query_result["data"]):
                print(f"    {i+1}: {dict(row)}")
        
        # 获取表信息
        print("\n📋 表结构信息:")
        table_info = server.execute_function(
            "get_table_info",
            connection_id="demo_sqlite",
            table_name="employees"
        )
        
        if table_info["status"] == "success":
            print("  表结构:")
            if "data" in table_info and table_info["data"]:
                for column in table_info["data"]:
                    if isinstance(column, dict):
                        print(f"    - {column}")
                    else:
                        print(f"    - {dict(column) if hasattr(column, '_asdict') else column}")
            else:
                print("    - 无表结构数据")
        else:
            print(f"    获取表结构失败: {table_info.get('message', '未知错误')}")
    
    print("\n✅ 本地数据库MCP服务器演示完成！")
    print("\n💡 使用说明:")
    print("1. 导入LocalDatabaseMCPServer类")
    print("2. 创建服务器实例: server = LocalDatabaseMCPServer()")
    print("3. 创建数据库连接: server.execute_function('create_connection', ...)")
    print("4. 执行SQL查询: server.execute_function('execute_query', ...)")
    print("5. 支持SQLite（内置）、MySQL、PostgreSQL、SQL Server")

if __name__ == "__main__":
    main()