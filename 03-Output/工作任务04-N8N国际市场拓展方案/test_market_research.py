import requests
import json
import time

# N8N API配置
N8N_BASE_URL = "http://localhost:5678"
WORKFLOW_NAME = "市场情报收集工作流"

def check_n8n_status():
    """检查N8N服务状态"""
    try:
        response = requests.get(f"{N8N_BASE_URL}/healthz")
        if response.status_code == 200:
            print("✓ N8N服务运行正常")
            return True
        else:
            print("✗ N8N服务异常")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到N8N服务，请确保服务已启动")
        return False

def get_workflows():
    """获取所有工作流"""
    try:
        response = requests.get(f"{N8N_BASE_URL}/api/v1/workflows")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"✗ 获取工作流列表失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ 获取工作流列表时出错: {e}")
        return None

def find_workflow_by_name(workflows, name):
    """根据名称查找工作流"""
    if not workflows or 'data' not in workflows:
        return None
    
    for workflow in workflows['data']:
        if workflow.get('name') == name:
            return workflow
    return None

def trigger_workflow(workflow_id):
    """手动触发工作流执行"""
    try:
        # 先获取工作流详情
        response = requests.get(f"{N8N_BASE_URL}/api/v1/workflows/{workflow_id}")
        if response.status_code != 200:
            print(f"✗ 无法获取工作流详情: {response.status_code}")
            return False
            
        workflow_data = response.json()
        
        # 准备执行数据
        execute_data = {
            "workflowData": workflow_data['data'],
            "runData": {},
            "startNodes": [],
            "destinationNode": None,
            "executionMode": "manual"
        }
        
        # 触发执行
        response = requests.post(
            f"{N8N_BASE_URL}/api/v1/workflows/{workflow_id}/run",
            headers={"Content-Type": "application/json"},
            data=json.dumps(execute_data)
        )
        
        if response.status_code == 200:
            execution_data = response.json()
            execution_id = execution_data.get('executionId')
            print(f"✓ 工作流已启动执行，执行ID: {execution_id}")
            return execution_id
        else:
            print(f"✗ 工作流执行失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return None
    except Exception as e:
        print(f"✗ 触发工作流执行时出错: {e}")
        return None

def check_execution_status(execution_id):
    """检查执行状态"""
    try:
        response = requests.get(f"{N8N_BASE_URL}/api/v1/executions/{execution_id}")
        if response.status_code == 200:
            execution_data = response.json()
            status = execution_data.get('data', {}).get('status', 'unknown')
            return status
        else:
            print(f"✗ 获取执行状态失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ 检查执行状态时出错: {e}")
        return None

def main():
    print("开始测试N8N市场情报收集工作流...")
    
    # 1. 检查N8N服务状态
    if not check_n8n_status():
        return
    
    # 2. 获取工作流列表
    print("\n正在获取工作流列表...")
    workflows = get_workflows()
    if not workflows:
        return
    
    # 3. 查找目标工作流
    print(f"正在查找工作流: {WORKFLOW_NAME}")
    target_workflow = find_workflow_by_name(workflows, WORKFLOW_NAME)
    if not target_workflow:
        print(f"✗ 未找到工作流: {WORKFLOW_NAME}")
        # 列出所有可用的工作流
        if 'data' in workflows:
            print("可用的工作流:")
            for wf in workflows['data']:
                print(f"  - {wf.get('name', 'Unknown')}")
        return
    
    workflow_id = target_workflow['id']
    print(f"✓ 找到工作流: {WORKFLOW_NAME} (ID: {workflow_id})")
    
    # 4. 触发工作流执行
    print("\n正在触发工作流执行...")
    execution_id = trigger_workflow(workflow_id)
    if not execution_id:
        return
    
    # 5. 监控执行状态
    print("\n监控执行状态...")
    max_attempts = 10
    attempt = 0
    
    while attempt < max_attempts:
        status = check_execution_status(execution_id)
        if status:
            print(f"执行状态: {status}")
            if status in ['success', 'error', 'canceled']:
                break
        else:
            print("无法获取执行状态")
            break
            
        attempt += 1
        time.sleep(3)  # 等待3秒后再次检查
    
    if attempt >= max_attempts:
        print("执行时间过长，停止监控")
    
    print("\n测试完成")

if __name__ == "__main__":
    main()