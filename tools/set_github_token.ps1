# 设置GitHub令牌环境变量
# 使用方法: .\set_github_token.ps1 [令牌值]

param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

# 设置环境变量
$env:GITHUB_TOKEN = $Token

# 显示确认信息
Write-Host "已设置GitHub令牌环境变量"
Write-Host "令牌前缀: $($Token.Substring(0, [Math]::Min(10, $Token.Length)))******"

# 同时设置到用户环境变量中（持久化）
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $Token, "User")
Write-Host "令牌已同时设置为用户环境变量（持久化）"