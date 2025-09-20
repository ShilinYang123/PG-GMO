# n8n CSV文件保存问题快速修复脚本
# 运行此脚本解决文件保存路径和权限问题

Write-Host "=== n8n CSV文件保存问题修复脚本 ===" -ForegroundColor Green
Write-Host ""

# 1. 创建必要的目录
Write-Host "1. 创建文件保存目录..." -ForegroundColor Yellow

$directories = @(
    "C:\temp",
    "C:\temp\n8n-files",
    "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\results"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ 创建目录: $dir" -ForegroundColor Green
    } else {
        Write-Host "  ✓ 目录已存在: $dir" -ForegroundColor Gray
    }
}

# 2. 设置目录权限
Write-Host ""
Write-Host "2. 设置目录权限..." -ForegroundColor Yellow

foreach ($dir in $directories) {
    try {
        icacls $dir /grant Everyone:F /T /Q | Out-Null
        Write-Host "  ✓ 权限设置成功: $dir" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ 权限设置失败: $dir" -ForegroundColor Red
    }
}

# 3. 创建测试文件验证权限
Write-Host ""
Write-Host "3. 验证文件写入权限..." -ForegroundColor Yellow

$testContent = "name,domainAvailable,youtubeAvailable,checkTime`nTestBrand,true,false,2024-01-16T10:30:00.000Z"

foreach ($dir in $directories) {
    $testFile = Join-Path $dir "test_write_permission.csv"
    try {
        $testContent | Out-File -FilePath $testFile -Encoding UTF8
        if (Test-Path $testFile) {
            Remove-Item $testFile -Force
            Write-Host "  ✓ 写入权限正常: $dir" -ForegroundColor Green
        }
    } catch {
        Write-Host "  ✗ 写入权限异常: $dir" -ForegroundColor Red
    }
}

# 4. 显示推荐的n8n配置
Write-Host ""
Write-Host "4. 推荐的n8n节点配置:" -ForegroundColor Yellow
Write-Host ""
Write-Host "在'保存文件到磁盘'节点中，将fileName参数设置为以下之一:" -ForegroundColor Cyan
Write-Host ""
Write-Host "选项1 (推荐): C:\\temp\\n8n-files\\{{ `$json.fileName }}" -ForegroundColor White
Write-Host "选项2: C:\\temp\\{{ `$json.fileName }}" -ForegroundColor White
Write-Host "选项3: S:\\PG-GMO\\03-Output\\工作任务21-n8n品牌名称可用性检查自动化解决方案\\results\\{{ `$json.fileName }}" -ForegroundColor White

# 5. 检查n8n进程
Write-Host ""
Write-Host "5. 检查n8n服务状态..." -ForegroundColor Yellow

$n8nProcess = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -eq "node" }
if ($n8nProcess) {
    Write-Host "  ✓ 发现Node.js进程 (可能是n8n)" -ForegroundColor Green
    Write-Host "    进程ID: $($n8nProcess.Id)" -ForegroundColor Gray
} else {
    Write-Host "  ⚠ 未发现n8n相关进程" -ForegroundColor Yellow
    Write-Host "    请确保n8n服务正在运行" -ForegroundColor Gray
}

# 6. 生成配置建议
Write-Host ""
Write-Host "6. 生成配置文件..." -ForegroundColor Yellow

$currentTime = Get-Date
$configLines = @(
    "# n8n文件保存配置建议",
    "# 生成时间: $currentTime",
    "",
    "## 环境变量配置 (可选)",
    "N8N_DEFAULT_BINARY_DATA_MODE=filesystem",
    "N8N_BINARY_DATA_STORAGE_PATH=C:\temp\n8n-files",
    "",
    "## 推荐的文件保存路径",
    "1. C:\temp\n8n-files\{{ `$json.fileName }}",
    "2. C:\temp\{{ `$json.fileName }}",
    "3. S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\results\{{ `$json.fileName }}",
    "",
    "## 故障排除",
    "- 确保目录存在且有写入权限",
    "- 检查文件名不包含非法字符",
    "- 验证n8n服务正在运行",
    "- 查看n8n控制台日志获取详细错误信息"
)

$configFile = "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
$configLines | Out-File -FilePath $configFile -Encoding UTF8
Write-Host "  ✓ 配置建议已保存到: $configFile" -ForegroundColor Green

# 7. 完成提示
Write-Host ""
Write-Host "=== 修复完成 ===" -ForegroundColor Green
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Cyan
Write-Host "1. 在n8n中打开工作流" -ForegroundColor White
Write-Host "2. 编辑'保存文件到磁盘'节点" -ForegroundColor White
Write-Host "3. 将fileName参数改为上述推荐路径之一" -ForegroundColor White
Write-Host "4. 保存并重新执行工作流" -ForegroundColor White
Write-Host "5. 检查指定目录是否生成CSV文件" -ForegroundColor White
Write-Host ""
Write-Host "如果问题仍然存在，请查看生成的配置建议文件获取更多帮助。" -ForegroundColor Yellow

Pause