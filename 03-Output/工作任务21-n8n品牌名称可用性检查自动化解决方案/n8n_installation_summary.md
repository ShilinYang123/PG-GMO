# n8n 安装准备工作完成

## 概述
我们已经为您完成了在 D:\Program Files 目录下安装 n8n 的所有准备工作。由于直接在当前环境中执行安装命令存在问题，我们提供了完整的安装指南和自动化脚本。

## 已完成的工作

### 1. 创建了安装指南
- 文件路径: `s:\PG-GMO\tools\n8n_installation_guide.md`
- 包含详细的安装步骤和配置说明

### 2. 创建了自动化安装脚本
- PowerShell 脚本: `s:\PG-GMO\tools\install_n8n.ps1`
- 批处理脚本: `s:\PG-GMO\tools\install_n8n.bat`
- 可自动完成大部分安装过程

### 3. 创建了使用指南
- 文件路径: `s:\PG-GMO\tools\n8n_usage_guide.md`
- 包含详细的使用说明和最佳实践

## 安装步骤

### 1. 安装 Node.js
由于系统中未检测到 Node.js，您需要先安装它:
1. 访问 https://nodejs.org/zh-cn/
2. 下载 LTS 版本的 Windows 安装程序
3. 运行安装程序完成安装
4. 重启命令提示符或 PowerShell

### 2. 运行安装脚本
选择以下任一方式运行安装:

**方法一: 使用批处理脚本**
```
s:\PG-GMO\tools\install_n8n.bat
```

**方法二: 使用 PowerShell 脚本**
```powershell
PowerShell -ExecutionPolicy Bypass -File "s:\PG-GMO\tools\install_n8n.ps1"
```

### 3. 验证安装
安装完成后，n8n 将被安装在:
```
D:\Program Files\n8n\
```

## 启动 n8n

安装完成后，您可以通过以下方式启动 n8n:

1. 双击 `D:\Program Files\n8n\start_n8n.bat`
2. 或在命令行中执行:
   ```
   cd /d "D:\Program Files\n8n"
   node node_modules\n8n\bin\n8n
   ```

## 访问 n8n 界面

启动成功后，在浏览器中访问:
```
http://localhost:5678
```

## 注意事项

### 1. 权限要求
建议以管理员身份运行安装脚本以确保正确安装。

### 2. 磁盘空间
确保 D:\Program Files 目录有足够的磁盘空间（至少 1GB）。

### 3. 网络连接
安装过程中需要下载 npm 包，请确保网络连接正常。

### 4. 防火墙设置
如果防火墙阻止了 n8n 的网络访问，请添加相应的例外规则。

## 故障排除

### 1. Node.js 未找到
确保 Node.js 已正确安装并添加到系统 PATH 中。

### 2. 权限问题
以管理员身份运行安装脚本。

### 3. 网络问题
检查网络连接，确保可以访问 npm registry。

### 4. 磁盘空间不足
清理磁盘空间或选择其他安装目录。

## 支持资源

- 安装指南: `s:\PG-GMO\tools\n8n_installation_guide.md`
- 使用指南: `s:\PG-GMO\tools\n8n_usage_guide.md`
- 官方文档: https://docs.n8n.io/
- 社区支持: https://community.n8n.io/

## 后续步骤

1. 安装 Node.js
2. 运行安装脚本
3. 启动 n8n 服务
4. 访问 Web 界面开始使用

如有任何问题，请参考提供的文档或联系技术支持。