# GitHub认证配置说明

本文档说明如何正确配置GitHub认证，以确保项目能够正常进行Git操作和备份。

## 安全配置原则

为了防止敏感信息泄露，项目采用以下安全配置原则：

1. **令牌不存储在代码中**：GitHub个人访问令牌（PAT）不得直接存储在代码或配置文件中
2. **环境变量管理**：令牌通过系统环境变量进行管理
3. **配置文件占位符**：配置文件中使用环境变量占位符

## 令牌设置方法

### 方法一：使用批处理脚本（推荐）

1. 运行 `tools\set_github_token.bat` 脚本
2. 输入您的GitHub个人访问令牌
3. 脚本会自动设置环境变量

示例：
```cmd
tools\set_github_token.bat YOUR_GITHUB_TOKEN_HERE
```

### 方法二：使用PowerShell脚本

1. 在PowerShell中运行 `tools\set_github_token.ps1` 脚本
2. 传入令牌作为参数

示例：
```powershell
.\tools\set_github_token.ps1 YOUR_GITHUB_TOKEN_HERE
```

### 方法三：手动设置环境变量

在命令提示符中执行：
```cmd
set GITHUB_TOKEN=YOUR_GITHUB_TOKEN_HERE
```

在PowerShell中执行：
```powershell
$env:GITHUB_TOKEN="YOUR_GITHUB_TOKEN_HERE"
```

## 令牌使用流程

1. 系统启动时，`start.py`脚本会自动从环境变量读取令牌
2. `finish.py`脚本在执行Git推送时会使用环境变量中的令牌进行认证
3. 如需手动执行Git操作，确保已设置令牌环境变量

## 令牌权限要求

GitHub个人访问令牌需要以下权限：

- `repo` - 对仓库的完全访问权限
- `workflow` - 对GitHub Actions工作流的更新权限（如果使用）

## 故障排除

### 问题1：Git推送失败，提示认证错误

**解决方案**：
1. 确认已正确设置`GITHUB_TOKEN`环境变量
2. 重启终端或命令提示符
3. 重新运行`finish.py`脚本

### 问题2：提示"no upstream branch"

**解决方案**：
系统已自动配置`push.autoSetupRemote`，下次推送时会自动设置上游分支。

### 问题3：GitHub安全扫描阻止推送

**解决方案**：
项目已修改配置文件格式，使用环境变量占位符代替直接存储令牌，避免触发安全扫描。