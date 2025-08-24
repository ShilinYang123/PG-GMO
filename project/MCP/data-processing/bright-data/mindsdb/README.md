# MindsDB MCP Server 安装说明

## 概述
MindsDB MCP Server (minds-mcp) 是一个基于Model Context Protocol (MCP)的服务器，允许LLM通过标准化接口与Minds SDK进行交互。<mcreference link="https://github.com/mindsdb/minds-mcp" index="1">1</mcreference>

## 功能特性
- 通过MCP协议与Minds SDK交互
- 支持AI分析引擎功能
- 可连接和统一多种数据源
- 支持200+数据源连接（数据库、数据仓库、SaaS应用）<mcreference link="https://github.com/mindsdb/mindsdb" index="2">2</mcreference>

## 安装状态
✅ **已安装** - 从GitHub源代码安装成功

## 安装路径
```
S:\PG-GMO\project\MCP\servers\bright-data\mindsdb\minds-mcp
```

## 安装方法

### 1. 克隆仓库
```bash
git clone https://github.com/mindsdb/minds-mcp.git
cd minds-mcp
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行服务器
```bash
python server.py
```

## 项目依赖
- mcp==1.5.0
- minds_sdk==1.3.0

## 配置要求
- Python 3.7+
- 需要配置Minds API密钥
- 可选：Docker环境（用于容器化部署）

## 使用示例

### 基本启动
```bash
python server.py --help
```

### Docker部署
```bash
docker-compose up
```

## Claude Desktop配置示例
```json
{
  "mcpServers": {
    "minds-mcp": {
      "command": "python",
      "args": ["path/to/minds-mcp/server.py"],
      "env": {
        "MINDS_API_KEY": "your-api-key"
      }
    }
  }
}
```

## 可用工具
- 数据源连接和查询
- AI分析和预测
- 数据统一和联邦查询
- 知识库管理

## 注意事项
- 安装过程中可能出现依赖版本冲突警告，但不影响基本功能
- 需要有效的Minds API密钥才能正常使用
- 支持本地和云端部署

## 相关链接
- [GitHub仓库](https://github.com/mindsdb/minds-mcp)
- [MindsDB主项目](https://github.com/mindsdb/mindsdb)
- [MCP协议文档](https://modelcontextprotocol.io/)

## 安装日期
2025年8月21日

## 状态
安装完成，可正常使用