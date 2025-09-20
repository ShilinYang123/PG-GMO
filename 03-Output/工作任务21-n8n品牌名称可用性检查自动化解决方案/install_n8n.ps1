# PowerShell 脚本用于安装 n8n 到 D:\Program Files
# 作者: AI Assistant
# 日期: 2025-09-07

# 设置执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

Write-Host "开始安装 n8n..." -ForegroundColor Green

# 检查 D:\Program Files 目录是否存在
if (!(Test-Path "D:\Program Files")) {
    Write-Host "错误: D:\Program Files 目录不存在" -ForegroundColor Red
    exit 1
}

# 创建 n8n 安装目录
$n8nPath = "D:\Program Files\n8n"
if (!(Test-Path $n8nPath)) {
    New-Item -ItemType Directory -Path $n8nPath -Force | Out-Null
    Write-Host "创建目录: $n8nPath" -ForegroundColor Yellow
}

# 检查 Node.js 是否已安装
try {
    $nodeVersion = node --version
    Write-Host "Node.js 已安装: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: Node.js 未安装。请先安装 Node.js。" -ForegroundColor Red
    Write-Host "请访问 https://nodejs.org/zh-cn/ 下载并安装 Node.js LTS 版本。" -ForegroundColor Yellow
    exit 1
}

# 检查 npm 是否已安装
try {
    $npmVersion = npm --version
    Write-Host "npm 已安装: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: npm 未安装。" -ForegroundColor Red
    exit 1
}

# 设置 npm 全局安装路径
npm config set prefix "$n8nPath"

# 安装 n8n
Write-Host "正在安装 n8n..." -ForegroundColor Yellow
try {
    npm install -g n8n
    Write-Host "n8n 安装成功!" -ForegroundColor Green
} catch {
    Write-Host "错误: n8n 安装失败。" -ForegroundColor Red
    exit 1
}

# 创建启动脚本
$startScript = @"
@echo off
echo 启动 n8n...
echo 请在浏览器中访问 http://localhost:5678
echo 按 Ctrl+C 停止服务
echo.
node "$n8nPath\node_modules\n8n\bin\n8n"
pause
"@

$startScriptPath = "$n8nPath\start_n8n.bat"
$startScript | Out-File -FilePath $startScriptPath -Encoding UTF8
Write-Host "创建启动脚本: $startScriptPath" -ForegroundColor Yellow

# 创建配置目录
$configPath = "$env:USERPROFILE\.n8n"
if (!(Test-Path $configPath)) {
    New-Item -ItemType Directory -Path $configPath -Force | Out-Null
    Write-Host "创建配置目录: $configPath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "n8n 安装完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "安装路径: $n8nPath" -ForegroundColor Cyan
Write-Host "配置路径: $configPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "使用方法:" -ForegroundColor Yellow
Write-Host "1. 双击 $startScriptPath 启动 n8n" -ForegroundColor Cyan
Write-Host "2. 在浏览器中访问 http://localhost:5678" -ForegroundColor Cyan
Write-Host "3. 开始使用 n8n 创建自动化工作流" -ForegroundColor Cyan
Write-Host ""
Write-Host "文档参考: https://docs.n8n.io/" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Green

# 暂停以查看结果
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")