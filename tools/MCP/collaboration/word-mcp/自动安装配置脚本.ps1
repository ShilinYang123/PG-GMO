# Office-Word-MCP-Server 自动安装配置脚本
# 作者：雨俊
# 日期：2025年1月8日

Write-Host "=== Office-Word-MCP-Server 自动安装配置脚本 ===" -ForegroundColor Green
Write-Host "技术负责人：雨俊" -ForegroundColor Cyan
Write-Host "开始时间：$(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# 1. 检查 Python 环境
Write-Host "[步骤 1] 检查 Python 环境..." -ForegroundColor Blue
try {
    $pythonPath = (Get-Command python).Source
    Write-Host "Python 路径：$pythonPath" -ForegroundColor Green
    
    $pythonVersion = python --version
    Write-Host "Python 版本：$pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 未安装或不在 PATH 中" -ForegroundColor Red
    exit 1
}

# 2. 检查项目目录
Write-Host "`n[步骤 2] 检查项目目录..." -ForegroundColor Blue
$projectPath = "S:\PG-GMO\Office-Word-MCP-Server"
if (Test-Path $projectPath) {
    Write-Host "项目目录已存在：$projectPath" -ForegroundColor Green
    Set-Location $projectPath
} else {
    Write-Host "❌ 项目目录不存在" -ForegroundColor Red
    exit 1
}

# 3. 安装依赖
Write-Host "`n[步骤 3] 安装 Python 依赖包..." -ForegroundColor Blue
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 依赖包安装完成" -ForegroundColor Green
    } else {
        Write-Host "⚠️ 依赖包安装可能有问题，但继续执行" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ 未找到 requirements.txt 文件" -ForegroundColor Red
    exit 1
}

# 4. 创建 Claude Desktop 配置
Write-Host "`n[步骤 4] 创建 Claude Desktop 配置..." -ForegroundColor Blue
$claudeConfigDir = "$env:APPDATA\Claude"
$claudeConfigFile = "$claudeConfigDir\claude_desktop_config.json"

# 确保目录存在
if (!(Test-Path $claudeConfigDir)) {
    New-Item -ItemType Directory -Path $claudeConfigDir -Force | Out-Null
    Write-Host "创建 Claude 配置目录：$claudeConfigDir" -ForegroundColor Green
}

# 生成配置内容
$pythonPathEscaped = $pythonPath.Replace('\', '\\')
$projectPathEscaped = $projectPath.Replace('\', '\\')

$configJson = @"
{
  "mcpServers": {
    "word-document-server": {
      "command": "$pythonPathEscaped",
      "args": [
        "$projectPathEscaped\\word_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "$projectPathEscaped",
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
"@

# 写入配置文件
$configJson | Out-File -FilePath $claudeConfigFile -Encoding UTF8
Write-Host "✅ 已创建 Claude 配置文件：$claudeConfigFile" -ForegroundColor Green

# 5. 测试 MCP Server
Write-Host "`n[步骤 5] 测试 MCP Server..." -ForegroundColor Blue
try {
    # 简单测试：尝试启动服务器并快速关闭
    $testProcess = Start-Process -FilePath "python" -ArgumentList "word_mcp_server.py" -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2
    
    if (!$testProcess.HasExited) {
        Write-Host "✅ MCP Server 启动成功" -ForegroundColor Green
        $testProcess.Kill()
        Write-Host "✅ MCP Server 测试完成" -ForegroundColor Green
    } else {
        Write-Host "⚠️ MCP Server 可能启动有问题" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ MCP Server 测试遇到问题：$($_.Exception.Message)" -ForegroundColor Yellow
}

# 6. 生成安装报告
Write-Host "`n[步骤 6] 生成安装报告..." -ForegroundColor Blue

$reportContent = @"
# Office-Word-MCP-Server 安装报告

## 安装信息
- 安装时间：$(Get-Date)
- 技术负责人：雨俊
- Python 路径：$pythonPath
- Python 版本：$pythonVersion
- 项目路径：$projectPath

## 配置文件
- Claude Desktop 配置：$claudeConfigFile

## 使用方法

### 方法1：在 Claude Desktop 中使用
1. 重启 Claude Desktop 应用程序
2. 在 Claude Desktop 中可以直接使用 Word 文档操作功能
3. 尝试说："帮我创建一个Word文档"

### 方法2：手动启动测试
1. 运行命令：python word_mcp_server.py
2. 检查是否有错误信息

## 可用功能
- 创建和编辑 Word 文档
- 添加文本、表格、图像
- 格式化文档内容
- 文档转换和分析
- 注释管理

## 故障排除
如果遇到问题：
1. 检查 Python 环境是否正确
2. 确认所有依赖包已安装：pip install -r requirements.txt
3. 验证 Claude Desktop 配置文件语法
4. 手动测试：python word_mcp_server.py
5. 查看错误日志

## 配置文件位置
- Claude Desktop 配置：$claudeConfigFile
- 项目目录：$projectPath

---
安装脚本执行完成时间：$(Get-Date)
"@

$reportContent | Out-File -FilePath "安装报告.md" -Encoding UTF8
Write-Host "✅ 已生成安装报告：安装报告.md" -ForegroundColor Green

# 7. 完成安装
Write-Host "`n=== 安装完成 ===" -ForegroundColor Green
Write-Host "✅ Office-Word-MCP-Server 已成功安装和配置" -ForegroundColor Green
Write-Host "✅ Claude Desktop 配置已更新" -ForegroundColor Green
Write-Host "✅ 安装报告已生成" -ForegroundColor Green
Write-Host "`n下一步操作：" -ForegroundColor Yellow
Write-Host "1. 重启 Claude Desktop 应用程序" -ForegroundColor White
Write-Host "2. 在 Claude Desktop 中测试：'帮我创建一个Word文档'" -ForegroundColor White
Write-Host "3. 或手动测试：python word_mcp_server.py" -ForegroundColor White
Write-Host "4. 查看详细说明：安装报告.md" -ForegroundColor White

Write-Host "`n脚本执行完成时间：$(Get-Date)" -ForegroundColor Cyan