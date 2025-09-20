#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
N8N MCP集成工具
用于将N8N与MCP服务器集成的工具脚本
"""

import json
import os
import sys
import requests
from pathlib import Path

class N8NMCPIntegration:
    def __init__(self, n8n_base_url="http://localhost:5678"):
        self.n8n_base_url = n8n_base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def create_mcp_workflow_template(self, template_name, mcp_nodes):
        """创建MCP集成工作流模板"""
        workflow_template = {
            "name": template_name,
            "version": 1,
            "nodes": [
                {
                    "parameters": {},
                    "id": "1",
                    "name": "Start",
                    "type": "n8n-nodes-base.manualTrigger",
                    "typeVersion": 1,
                    "position": [250, 300]
                }
            ],
            "connections": {}
        }
        
        # 添加MCP节点
        position_x = 450
        position_y = 300
        node_id = 2
        
        for i, mcp_node in enumerate(mcp_nodes):
            node = {
                "parameters": mcp_node.get("parameters", {}),
                "id": str(node_id + i),
                "name": mcp_node.get("name", f"MCP Node {i+1}"),
                "type": mcp_node.get("type", "n8n-nodes-base.httpRequest"),
                "typeVersion": 1,
                "position": [position_x + i * 200, position_y]
            }
            workflow_template["nodes"].append(node)
            
            # 添加连接
            if i == 0:
                workflow_template["connections"]["Start"] = {
                    "main": [[{
                        "node": node["name"],
                        "type": "main",
                        "index": 0
                    }]]
                }
            else:
                prev_node_name = mcp_nodes[i-1].get("name", f"MCP Node {i}")
                workflow_template["connections"][prev_node_name] = {
                    "main": [[{
                        "node": node["name"],
                        "type": "main",
                        "index": 0
                    }]]
                }
        
        return workflow_template
    
    def save_workflow_template(self, workflow, output_file):
        """保存工作流模板到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(workflow, f, ensure_ascii=False, indent=2)
            print(f"工作流模板已保存到: {output_file}")
            return True
        except Exception as e:
            print(f"保存工作流模板失败: {e}")
            return False
    
    def integrate_with_office_mcp(self, workflow_name):
        """与Office MCP集成示例"""
        mcp_nodes = [
            {
                "name": "Excel MCP",
                "type": "n8n-nodes-base.httpRequest",
                "parameters": {
                    "method": "POST",
                    "url": "http://localhost:3000/api/excel/process",
                    "authentication": "none",
                    "sendBinaryData": True
                }
            },
            {
                "name": "Word MCP",
                "type": "n8n-nodes-base.httpRequest",
                "parameters": {
                    "method": "POST",
                    "url": "http://localhost:3001/api/word/generate",
                    "authentication": "none",
                    "sendBinaryData": True
                }
            }
        ]
        
        workflow = self.create_mcp_workflow_template(workflow_name, mcp_nodes)
        output_file = f"{workflow_name.replace(' ', '_')}_mcp_integration.json"
        return self.save_workflow_template(workflow, output_file)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python n8n_mcp_integration.py create-template <模板名称>")
        print("  python n8n_mcp_integration.py integrate-office <工作流名称>")
        return
    
    integration = N8NMCPIntegration()
    
    command = sys.argv[1]
    
    if command == "create-template":
        if len(sys.argv) < 3:
            print("请提供模板名称")
            return
        template_name = sys.argv[2]
        # 这里可以添加具体的MCP节点配置
        print(f"模板 '{template_name}' 创建功能占位符")
    
    elif command == "integrate-office":
        if len(sys.argv) < 3:
            print("请提供工作流名称")
            return
        workflow_name = sys.argv[2]
        integration.integrate_with_office_mcp(workflow_name)
    
    else:
        print(f"未知命令: {command}")
        print("可用命令: create-template, integrate-office")

if __name__ == "__main__":
    main()