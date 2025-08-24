#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地Qdrant向量数据库MCP服务器

功能：
1. 向量存储和检索
2. 语义搜索
3. 集合管理
4. 向量相似度计算
5. 批量操作
6. 元数据过滤
"""

import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np
from pathlib import Path

# 模拟Qdrant客户端功能
class LocalQdrantClient:
    def __init__(self, data_dir: str = "./qdrant_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.collections = {}
        self.logger = logging.getLogger(__name__)
        self._load_collections()
    
    def _load_collections(self):
        """加载已存在的集合"""
        collections_file = self.data_dir / "collections.json"
        if collections_file.exists():
            try:
                with open(collections_file, 'r', encoding='utf-8') as f:
                    self.collections = json.load(f)
                self.logger.info(f"加载了 {len(self.collections)} 个集合")
            except Exception as e:
                self.logger.error(f"加载集合失败: {e}")
    
    def _save_collections(self):
        """保存集合信息"""
        collections_file = self.data_dir / "collections.json"
        try:
            with open(collections_file, 'w', encoding='utf-8') as f:
                json.dump(self.collections, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存集合失败: {e}")
    
    def create_collection(self, collection_name: str, vector_size: int, distance: str = "cosine") -> Dict:
        """创建向量集合"""
        try:
            if collection_name in self.collections:
                return {"status": "error", "message": "集合已存在"}
            
            collection_info = {
                "name": collection_name,
                "vector_size": vector_size,
                "distance": distance,
                "created_at": datetime.now().isoformat(),
                "points_count": 0,
                "vectors": {},
                "metadata": {}
            }
            
            self.collections[collection_name] = collection_info
            self._save_collections()
            
            return {
                "status": "success",
                "message": f"集合 '{collection_name}' 创建成功",
                "collection": collection_info
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def list_collections(self) -> Dict:
        """列出所有集合"""
        try:
            collections_info = []
            for name, info in self.collections.items():
                collections_info.append({
                    "name": name,
                    "vector_size": info["vector_size"],
                    "distance": info["distance"],
                    "points_count": info["points_count"],
                    "created_at": info["created_at"]
                })
            
            return {
                "status": "success",
                "collections": collections_info,
                "total": len(collections_info)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def upsert_points(self, collection_name: str, points: List[Dict]) -> Dict:
        """插入或更新向量点"""
        try:
            if collection_name not in self.collections:
                return {"status": "error", "message": "集合不存在"}
            
            collection = self.collections[collection_name]
            updated_count = 0
            
            for point in points:
                point_id = str(point.get("id", len(collection["vectors"])))
                vector = point.get("vector", [])
                payload = point.get("payload", {})
                
                if len(vector) != collection["vector_size"]:
                    continue
                
                collection["vectors"][point_id] = vector
                collection["metadata"][point_id] = {
                    "payload": payload,
                    "updated_at": datetime.now().isoformat()
                }
                updated_count += 1
            
            collection["points_count"] = len(collection["vectors"])
            self._save_collections()
            
            return {
                "status": "success",
                "message": f"成功更新 {updated_count} 个向量点",
                "updated_count": updated_count
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def search_points(self, collection_name: str, query_vector: List[float], limit: int = 10, score_threshold: float = 0.0) -> Dict:
        """搜索相似向量"""
        try:
            if collection_name not in self.collections:
                return {"status": "error", "message": "集合不存在"}
            
            collection = self.collections[collection_name]
            if not collection["vectors"]:
                return {"status": "success", "results": []}
            
            # 计算相似度
            results = []
            query_vector = np.array(query_vector)
            
            for point_id, vector in collection["vectors"].items():
                vector_array = np.array(vector)
                
                # 计算余弦相似度
                if collection["distance"] == "cosine":
                    similarity = np.dot(query_vector, vector_array) / (np.linalg.norm(query_vector) * np.linalg.norm(vector_array))
                    score = (similarity + 1) / 2  # 转换到0-1范围
                else:
                    # 欧几里得距离
                    distance = np.linalg.norm(query_vector - vector_array)
                    score = 1 / (1 + distance)  # 转换为相似度分数
                
                if score >= score_threshold:
                    results.append({
                        "id": point_id,
                        "score": float(score),
                        "payload": collection["metadata"][point_id]["payload"]
                    })
            
            # 按分数排序并限制结果数量
            results.sort(key=lambda x: x["score"], reverse=True)
            results = results[:limit]
            
            return {
                "status": "success",
                "results": results,
                "total_found": len(results)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_point(self, collection_name: str, point_id: str) -> Dict:
        """获取特定向量点"""
        try:
            if collection_name not in self.collections:
                return {"status": "error", "message": "集合不存在"}
            
            collection = self.collections[collection_name]
            if point_id not in collection["vectors"]:
                return {"status": "error", "message": "向量点不存在"}
            
            return {
                "status": "success",
                "point": {
                    "id": point_id,
                    "vector": collection["vectors"][point_id],
                    "payload": collection["metadata"][point_id]["payload"]
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def delete_points(self, collection_name: str, point_ids: List[str]) -> Dict:
        """删除向量点"""
        try:
            if collection_name not in self.collections:
                return {"status": "error", "message": "集合不存在"}
            
            collection = self.collections[collection_name]
            deleted_count = 0
            
            for point_id in point_ids:
                if point_id in collection["vectors"]:
                    del collection["vectors"][point_id]
                    del collection["metadata"][point_id]
                    deleted_count += 1
            
            collection["points_count"] = len(collection["vectors"])
            self._save_collections()
            
            return {
                "status": "success",
                "message": f"成功删除 {deleted_count} 个向量点",
                "deleted_count": deleted_count
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def delete_collection(self, collection_name: str) -> Dict:
        """删除集合"""
        try:
            if collection_name not in self.collections:
                return {"status": "error", "message": "集合不存在"}
            
            del self.collections[collection_name]
            self._save_collections()
            
            return {
                "status": "success",
                "message": f"集合 '{collection_name}' 删除成功"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

class QdrantMCPServer:
    def __init__(self):
        self.client = LocalQdrantClient()
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
                    "name": "create_collection",
                    "description": "创建新的向量集合",
                    "parameters": {
                        "collection_name": "集合名称",
                        "vector_size": "向量维度",
                        "distance": "距离度量方式 (cosine/euclidean)"
                    }
                },
                {
                    "name": "list_collections",
                    "description": "列出所有向量集合",
                    "parameters": {}
                },
                {
                    "name": "upsert_points",
                    "description": "插入或更新向量点",
                    "parameters": {
                        "collection_name": "集合名称",
                        "points": "向量点列表"
                    }
                },
                {
                    "name": "search_points",
                    "description": "搜索相似向量",
                    "parameters": {
                        "collection_name": "集合名称",
                        "query_vector": "查询向量",
                        "limit": "返回结果数量",
                        "score_threshold": "相似度阈值"
                    }
                },
                {
                    "name": "get_point",
                    "description": "获取特定向量点",
                    "parameters": {
                        "collection_name": "集合名称",
                        "point_id": "向量点ID"
                    }
                },
                {
                    "name": "delete_points",
                    "description": "删除向量点",
                    "parameters": {
                        "collection_name": "集合名称",
                        "point_ids": "向量点ID列表"
                    }
                },
                {
                    "name": "delete_collection",
                    "description": "删除向量集合",
                    "parameters": {
                        "collection_name": "集合名称"
                    }
                }
            ]
        }
    
    def execute_function(self, function_name: str, **kwargs) -> Dict:
        """执行指定功能"""
        try:
            if function_name == "create_collection":
                return self.client.create_collection(
                    kwargs.get("collection_name"),
                    kwargs.get("vector_size"),
                    kwargs.get("distance", "cosine")
                )
            elif function_name == "list_collections":
                return self.client.list_collections()
            elif function_name == "upsert_points":
                return self.client.upsert_points(
                    kwargs.get("collection_name"),
                    kwargs.get("points", [])
                )
            elif function_name == "search_points":
                return self.client.search_points(
                    kwargs.get("collection_name"),
                    kwargs.get("query_vector"),
                    kwargs.get("limit", 10),
                    kwargs.get("score_threshold", 0.0)
                )
            elif function_name == "get_point":
                return self.client.get_point(
                    kwargs.get("collection_name"),
                    kwargs.get("point_id")
                )
            elif function_name == "delete_points":
                return self.client.delete_points(
                    kwargs.get("collection_name"),
                    kwargs.get("point_ids", [])
                )
            elif function_name == "delete_collection":
                return self.client.delete_collection(
                    kwargs.get("collection_name")
                )
            else:
                return {"status": "error", "message": f"未知功能: {function_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_demo_collection(self) -> Dict:
        """创建演示集合和数据"""
        try:
            # 创建演示集合
            result = self.client.create_collection("demo_collection", 128, "cosine")
            if result["status"] != "success":
                return result
            
            # 添加演示数据
            demo_points = [
                {
                    "id": "doc1",
                    "vector": np.random.rand(128).tolist(),
                    "payload": {
                        "title": "Python编程指南",
                        "content": "这是一个关于Python编程的文档",
                        "category": "编程"
                    }
                },
                {
                    "id": "doc2",
                    "vector": np.random.rand(128).tolist(),
                    "payload": {
                        "title": "机器学习基础",
                        "content": "介绍机器学习的基本概念和算法",
                        "category": "AI"
                    }
                },
                {
                    "id": "doc3",
                    "vector": np.random.rand(128).tolist(),
                    "payload": {
                        "title": "数据库设计",
                        "content": "关系型数据库设计的最佳实践",
                        "category": "数据库"
                    }
                }
            ]
            
            upsert_result = self.client.upsert_points("demo_collection", demo_points)
            
            return {
                "status": "success",
                "message": "演示集合和数据创建成功",
                "collection_result": result,
                "upsert_result": upsert_result
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

def main():
    """主函数 - 演示服务器功能"""
    print("🚀 启动本地Qdrant MCP服务器...")
    
    server = QdrantMCPServer()
    
    # 显示可用功能
    functions = server.get_available_functions()
    print("\n📋 可用功能:")
    for func in functions["functions"]:
        print(f"  - {func['name']}: {func['description']}")
    
    # 创建演示数据
    print("\n🎯 创建演示集合和数据...")
    demo_result = server.create_demo_collection()
    print(f"演示数据创建结果: {demo_result['message']}")
    
    # 列出集合
    print("\n📊 当前集合列表:")
    collections = server.execute_function("list_collections")
    if collections["status"] == "success":
        for collection in collections["collections"]:
            print(f"  - {collection['name']}: {collection['points_count']} 个向量点")
    
    # 演示搜索功能
    print("\n🔍 演示向量搜索...")
    query_vector = np.random.rand(128).tolist()
    search_result = server.execute_function(
        "search_points",
        collection_name="demo_collection",
        query_vector=query_vector,
        limit=3
    )
    
    if search_result["status"] == "success":
        print(f"找到 {search_result['total_found']} 个相似结果:")
        for result in search_result["results"]:
            print(f"  - ID: {result['id']}, 相似度: {result['score']:.4f}, 标题: {result['payload']['title']}")
    
    print("\n✅ 本地Qdrant MCP服务器演示完成！")
    print("\n💡 使用说明:")
    print("1. 导入QdrantMCPServer类")
    print("2. 创建服务器实例: server = QdrantMCPServer()")
    print("3. 调用功能: server.execute_function('function_name', **params)")
    print("4. 数据存储在 './qdrant_data' 目录中")

if __name__ == "__main__":
    main()