#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
N8N管理工具
用于管理N8N工作流和配置的工具脚本
"""

import json
import os
import sys
import requests
from pathlib import Path

class N8NManager:
    def __init__(self, base_url="http://localhost:5678"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def load_workflow(self, workflow_file):
        """加载N8N工作流文件"""
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            return workflow
        except Exception as e:
            print(f"加载工作流文件失败: {e}")
            return None
    
    def deploy_workflow(self, workflow_file):
        """部署N8N工作流"""
        workflow = self.load_workflow(workflow_file)
        if not workflow:
            return False
        
        try:
            # 检查是否已存在同名工作流
            response = requests.get(f"{self.base_url}/api/v1/workflows")
            if response.status_code == 200:
                workflows = response.json().get('data', [])
                for wf in workflows:
                    if wf.get('name') == workflow.get('name'):
                        # 更新现有工作流
                        workflow_id = wf.get('id')
                        update_response = requests.patch(
                            f"{self.base_url}/api/v1/workflows/{workflow_id}",
                            headers=self.headers,
                            data=json.dumps(workflow)
                        )
                        if update_response.status_code in [200, 201]:
                            print(f"工作流 '{workflow.get('name')}' 更新成功")
                            return True
                        else:
                            print(f"更新工作流失败: {update_response.text}")
                            return False
            
            # 创建新工作流
            response = requests.post(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers,
                data=json.dumps(workflow)
            )
            
            if response.status_code in [200, 201]:
                print(f"工作流 '{workflow.get('name')}' 部署成功")
                return True
            else:
                print(f"部署工作流失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"部署工作流时发生错误: {e}")
            return False
    
    def list_workflows(self):
        """列出所有工作流"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/workflows")
            if response.status_code == 200:
                workflows = response.json().get('data', [])
                print("当前N8N工作流列表:")
                for wf in workflows:
                    print(f"- {wf.get('name')} (ID: {wf.get('id')})")
                return workflows
            else:
                print(f"获取工作流列表失败: {response.text}")
                return []
        except Exception as e:
            print(f"获取工作流列表时发生错误: {e}")
            return []
    
    def delete_workflow(self, workflow_id):
        """删除工作流"""
        try:
            response = requests.delete(f"{self.base_url}/api/v1/workflows/{workflow_id}")
            if response.status_code == 200:
                print(f"工作流 {workflow_id} 删除成功")
                return True
            else:
                print(f"删除工作流失败: {response.text}")
                return False
        except Exception as e:
            print(f"删除工作流时发生错误: {e}")
            return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python n8n_manager.py deploy <工作流文件路径>")
        print("  python n8n_manager.py list")
        print("  python n8n_manager.py delete <工作流ID>")
        return
    
    manager = N8NManager()
    
    command = sys.argv[1]
    
    if command == "deploy":
        if len(sys.argv) < 3:
            print("请提供工作流文件路径")
            return
        workflow_file = sys.argv[2]
        manager.deploy_workflow(workflow_file)
    
    elif command == "list":
        manager.list_workflows()
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("请提供工作流ID")
            return
        workflow_id = sys.argv[2]
        manager.delete_workflow(workflow_id)
    
    else:
        print(f"未知命令: {command}")
        print("可用命令: deploy, list, delete")

if __name__ == "__main__":
    main()