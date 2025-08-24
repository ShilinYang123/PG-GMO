# Bright Data MCP Server 安装说明

## 概述
Bright Data MCP Server 是官方的 Model Context Protocol 服务器，使 LLM 能够访问公共网络数据。该服务器允许 MCP 客户端（如 Claude Desktop、Cursor、Windsurf 等）基于网络上可用的信息做出决策。

## 功能特性
- **实时网络访问**：直接从网络获取最新信息
- **绕过地理限制**：无论位置限制如何都能访问内容
- **Web Unlocker**：具有机器人检测保护的网站导航
- **浏览器控制**：可选的远程浏览器自动化功能
- **无缝集成**：与所有兼容 MCP 的 AI 助手配合使用

## 安装状态
✅ **已安装** - 通过 npm 全局安装

## 安装命令
```bash
npm install -g @brightdata/mcp
```

## 配置要求
- 需要 Bright Data API Token
- 可选：Web Unlocker Zone 名称
- 可选：Browser Zone 名称

## 使用示例
```bash
# 需要设置环境变量
export API_TOKEN="your-api-token-here"
npx @brightdata/mcp
```

## Claude Desktop 配置示例
```json
{
  "mcpServers": {
    "Bright Data": {
      "command": "npx",
      "args": ["@brightdata/mcp"],
      "env": {
        "API_TOKEN": "<insert-your-api-token-here>",
        "WEB_UNLOCKER_ZONE": "<optional-zone-name>",
        "BROWSER_ZONE": "<optional-browser-zone>"
      }
    }
  }
}
```

## 可用工具
- search_engine：搜索引擎功能
- scrape_as_markdown：网页抓取为 Markdown 格式
- Pro 模式下提供更多高级工具（需要额外费用）

## 注意事项
- 免费层提供每月 5000 次请求（前 3 个月）
- Pro 模式工具会产生额外费用
- 需要在 brightdata.com 创建账户获取 API Token

## 相关链接
- GitHub 仓库：https://github.com/brightdata/brightdata-mcp
- 官方文档：https://docs.brightdata.com/api-reference/MCP-Server
- Bright Data 官网：https://brightdata.com

安装时间：2025年8月21日
安装方式：npm 全局安装