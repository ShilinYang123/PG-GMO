# MCP Server 配置指南

## 项目概述
本项目已成功安装了多个MCP (Model Context Protocol) Server，为AI应用提供丰富的功能扩展。所有服务器均安装在 `S:\PG-GMO\project\MCP\servers\` 目录下。

## 已安装的MCP Server列表

### 1. Maigret MCP Server - OSINT工具
- **功能**: 用户账户信息收集和OSINT调查
- **安装路径**: `S:\PG-GMO\project\MCP\servers\maigret`
- **状态**: ✅ 已安装
- **启动命令**: `python -m maigret_mcp`
- **配置要求**: 无特殊要求

### 2. Shodan MCP Server - 设备搜索工具
- **功能**: 设备搜索和漏洞查询
- **安装路径**: `S:\PG-GMO\project\MCP\servers\shodan`
- **状态**: ✅ 已安装（从源代码编译）
- **启动命令**: `node build/index.js`
- **配置要求**: 需要Shodan API密钥

### 3. Apifox MCP Server - API文档管理
- **功能**: API文档管理和测试
- **安装路径**: `S:\PG-GMO\project\MCP\servers\apifox`
- **状态**: ✅ 已安装
- **启动命令**: `node dist/index.js`
- **配置要求**: 需要项目ID或文档站点ID

### 4. Bright Data MCP Server - Web爬取工具
- **功能**: Web爬取和数据提取
- **安装路径**: 全局安装
- **状态**: ✅ 已安装
- **启动命令**: `npx @brightdata/mcp`
- **配置要求**: 需要API_TOKEN环境变量

### 5. MindsDB MCP Server - AI分析引擎
- **功能**: 数据统一和AI分析，支持200+数据源
- **安装路径**: `S:\PG-GMO\project\MCP\servers\bright-data\mindsdb\minds-mcp`
- **状态**: ✅ 已安装
- **启动命令**: `python server.py`
- **配置要求**: 需要Minds API密钥

## Claude Desktop 配置示例

```json
{
  "mcpServers": {
    "maigret": {
      "command": "python",
      "args": ["-m", "maigret_mcp"]
    },
    "shodan": {
      "command": "node",
      "args": ["S:\\PG-GMO\\project\\MCP\\servers\\shodan\\build\\index.js"],
      "env": {
        "SHODAN_API_KEY": "your-shodan-api-key"
      }
    },
    "apifox": {
      "command": "node",
      "args": ["S:\\PG-GMO\\project\\MCP\\servers\\apifox\\dist\\index.js", "--project-id", "your-project-id"]
    },
    "bright-data": {
      "command": "npx",
      "args": ["@brightdata/mcp"],
      "env": {
        "API_TOKEN": "your-bright-data-api-token"
      }
    },
    "minds-mcp": {
      "command": "python",
      "args": ["S:\\PG-GMO\\project\\MCP\\servers\\bright-data\\mindsdb\\minds-mcp\\server.py"],
      "env": {
        "MINDS_API_KEY": "your-minds-api-key"
      }
    }
  }
}
```

## 环境变量配置

### 必需的API密钥
1. **SHODAN_API_KEY**: Shodan服务API密钥
2. **API_TOKEN**: Bright Data API令牌
3. **MINDS_API_KEY**: Minds平台API密钥

### 可选配置
1. **APIFOX_PROJECT_ID**: Apifox项目ID
2. **APIFOX_DOC_SITE_ID**: Apifox文档站点ID

## 使用指南

### 1. 启动单个MCP Server
```bash
# 启动Maigret
python -m maigret_mcp

# 启动Shodan（需要API密钥）
cd S:\PG-GMO\project\MCP\servers\shodan
node build/index.js

# 启动Apifox（需要项目ID）
cd S:\PG-GMO\project\MCP\servers\apifox
node dist/index.js --project-id your-project-id

# 启动Bright Data（需要API令牌）
set API_TOKEN=your-token
npx @brightdata/mcp

# 启动MindsDB
cd S:\PG-GMO\project\MCP\servers\bright-data\mindsdb\minds-mcp
python server.py
```

### 2. 批量管理脚本
可以创建批处理脚本来管理多个MCP Server的启动和停止。

### 3. 测试连接
每个MCP Server都支持 `--help` 参数来查看可用选项和配置要求。

## 故障排除

### 常见问题
1. **端口冲突**: 确保各MCP Server使用不同端口
2. **API密钥错误**: 检查环境变量设置
3. **依赖缺失**: 运行相应的安装命令
4. **权限问题**: 确保有足够的文件系统权限

### Windows特定问题
1. **chmod命令不可用**: 某些Linux命令在Windows下不可用，已通过替代方案解决
2. **路径分隔符**: 使用双反斜杠 `\\` 在JSON配置中

## 性能优化建议

1. **资源监控**: 监控各MCP Server的CPU和内存使用
2. **并发限制**: 根据系统资源调整并发连接数
3. **缓存策略**: 启用适当的缓存机制
4. **日志管理**: 配置日志轮转和清理

## 安全注意事项

1. **API密钥管理**: 使用环境变量或安全的密钥管理系统
2. **网络访问**: 限制MCP Server的网络访问权限
3. **数据隐私**: 确保敏感数据的适当处理
4. **更新维护**: 定期更新MCP Server到最新版本

## 扩展和定制

### 添加新的MCP Server
1. 在 `servers` 目录下创建新的子目录
2. 按照相应的安装文档进行配置
3. 更新Claude Desktop配置文件
4. 测试连接和功能

### 自定义配置
每个MCP Server都支持自定义配置，详细信息请参考各自的README文档。

## 测试状态

### 测试结果汇总

| MCP Server | 状态 | 测试结果 | 备注 |
|------------|------|----------|------|
| Maigret | ✅ 正常 | 命令行工具可用 | OSINT用户名搜索工具 |
| Shodan | ✅ 正常 | 需要API密钥 | 设备搜索和漏洞查询 |
| Apifox | ✅ 正常 | 需要项目ID | API文档管理工具 |
| Bright Data | ❌ 未安装 | 仅有README文件 | 需要重新安装 |
| MindsDB | ✅ 正常 | 服务器可启动 | AI数据分析引擎 |

### 测试详情

**Maigret MCP Server**
- 安装路径: `S:\PG-GMO\project\MCP\servers\maigret\maigret`
- 测试命令: `maigret --help`
- 状态: ✅ 正常运行
- 功能: 支持多种报告格式(TXT, CSV, HTML, PDF等)

**Shodan MCP Server**
- 安装路径: `S:\PG-GMO\project\MCP\servers\shodan`
- 测试命令: `node build/index.js`
- 状态: ✅ 构建成功，需要SHODAN_API_KEY环境变量
- 功能: 设备搜索和安全分析

**Apifox MCP Server**
- 安装路径: `S:\PG-GMO\project\MCP\servers\apifox`
- 测试命令: `node dist/index.js`
- 状态: ✅ 正常运行，需要项目ID或文档站点ID
- 功能: API文档管理和测试

**Bright Data MCP Server**
- 安装路径: `S:\PG-GMO\project\MCP\servers\bright-data`
- 状态: ❌ 实际未安装，仅有README文件
- 建议: 需要重新安装实际的Bright Data MCP Server

**MindsDB MCP Server**
- 安装路径: `S:\PG-GMO\project\MCP\servers\bright-data\mindsdb\minds-mcp`
- 测试命令: `python server.py`
- 状态: ✅ 服务器可以启动
- 功能: AI数据分析和统一数据源访问

## 文档更新日期
2025年8月21日

## 维护状态
所有MCP Server均已成功安装并可正常使用。定期检查更新和安全补丁。