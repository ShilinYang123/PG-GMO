# Office-Word-MCP-Server 简单安装脚本
# 作者：雨俊

Write-Host "=== Office-Word-MCP-Server 安装脚本 ===" -ForegroundColor Green
Write-Host "技术负责人：雨俊" -ForegroundColor Cyan
Write-Host "开始时间：$(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# 1. 检查 Python
Write-Host "[步骤 1] 检查 Python 环境..." -ForegroundColor Blue
try {
    $pythonPath = (Get-Command python).Source
    Write-Host "Python 路径：$pythonPath" -ForegroundColor Green
    
    $pythonVersion = python --version
    Write-Host "Python 版本：$pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误：Python 未安装" -ForegroundColor Red
    exit 1
}

# 2. 检查项目目录
Write-Host "`n[步骤 2] 检查项目目录..." -ForegroundColor Blue
$projectPath = "S:\PG-GMO\Office-Word-MCP-Server"
if (Test-Path $projectPath) {
    Write-Host "项目目录存在" -ForegroundColor Green
    Set-Location $projectPath
} else {
    Write-Host "错误：项目目录不存在" -ForegroundColor Red
    exit 1
}

# 3. 安装依赖
Write-Host "`n[步骤 3] 安装依赖包..." -ForegroundColor Blue
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "依赖包安装完成" -ForegroundColor Green
} else {
    Write-Host "错误：未找到 requirements.txt" -ForegroundColor Red
    exit 1
}

# 4. 创建配置文件
Write-Host "`n[步骤 4] 创建 Claude 配置..." -ForegroundColor Blue
$claudeConfigDir = "$env:APPDATA\Claude"
$claudeConfigFile = "$claudeConfigDir\claude_desktop_config.json"

if (!(Test-Path $claudeConfigDir)) {
    New-Item -ItemType Directory -Path $claudeConfigDir -Force | Out-Null
    Write-Host "创建配置目录" -ForegroundColor Green
}

# 生成配置
$pythonEscaped = $pythonPath.Replace('\', '\\')
$projectEscaped = $projectPath.Replace('\', '\\')

# 创建配置内容
$config = '{
  "mcpServers": {
    "word-document-server": {
      "command": "' + $pythonEscaped + '",
      "args": [
        "' + $projectEscaped + '\\word_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "' + $projectEscaped + '",
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}'

$config | Out-File -FilePath $claudeConfigFile -Encoding UTF8
Write-Host "配置文件已创建：$claudeConfigFile" -ForegroundColor Green

# 5. 测试服务器
Write-Host "`n[步骤 5] 测试 MCP Server..." -ForegroundColor Blue
try {
    $testProcess = Start-Process -FilePath "python" -ArgumentList "word_mcp_server.py" -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2
    
    if (!$testProcess.HasExited) {
        Write-Host "MCP Server 启动成功" -ForegroundColor Green
        $testProcess.Kill()
        Write-Host "测试完成" -ForegroundColor Green
    } else {
        Write-Host "MCP Server 可能有问题" -ForegroundColor Yellow
    }
} catch {
    Write-Host "测试遇到问题：$($_.Exception.Message)" -ForegroundColor Yellow
}

# 6. 完成
Write-Host "`n=== 安装完成 ===" -ForegroundColor Green
Write-Host "Office-Word-MCP-Server 已安装配置" -ForegroundColor Green
Write-Host "Claude Desktop 配置已更新" -ForegroundColor Green
Write-Host "`n下一步：" -ForegroundColor Yellow
Write-Host "1. 重启 Claude Desktop" -ForegroundColor White
Write-Host "2. 测试：'帮我创建一个Word文档'" -ForegroundColor White
Write-Host "3. 手动测试：python word_mcp_server.py" -ForegroundColor White

Write-Host "`n完成时间：$(Get-Date)" -ForegroundColor Cyan