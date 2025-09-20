# n8n 安装指南

## 概述
本指南将指导您如何在 Windows 系统上安装 n8n 自动化工作流工具，并将其安装到 D:\Program Files 目录下。

## 系统要求
- Windows 10 或更高版本
- 至少 4GB RAM
- 至少 1GB 可用磁盘空间
- 管理员权限

## 安装步骤

### 1. 安装 Node.js

1. 访问 Node.js 官方网站: https://nodejs.org/zh-cn/
2. 下载 LTS 版本的 Windows 安装程序 (推荐使用 .msi 安装包)
3. 运行安装程序，按照提示完成安装
4. 安装完成后，重启命令提示符或 PowerShell
5. 验证安装:
   ```cmd
   node --version
   npm --version
   ```

### 2. 安装 n8n

打开命令提示符或 PowerShell，执行以下命令:

```cmd
# 全局安装 n8n
npm install -g n8n

# 或者如果您想安装到特定目录
npm install -g --prefix "D:\Program Files\n8n" n8n
```

### 3. 配置环境变量 (可选)

为了方便使用 n8n，您可以将 n8n 的安装路径添加到系统环境变量中:

1. 打开"系统属性" → "高级" → "环境变量"
2. 在"系统变量"中找到 Path，点击"编辑"
3. 添加 n8n 的安装路径: `D:\Program Files\n8n\node_modules\.bin`
4. 点击"确定"保存更改

### 4. 启动 n8n

安装完成后，可以通过以下命令启动 n8n:

```cmd
# 直接启动
n8n

# 或指定端口启动
n8n --port 5678

# 或使用 Node.js 直接运行
node "D:\Program Files\n8n\node_modules\n8n\bin\n8n"
```

### 5. 访问 n8n 界面

启动成功后，在浏览器中访问以下地址:
```
http://localhost:5678
```

### 6. 设置为 Windows 服务 (可选)

为了使 n8n 在系统启动时自动运行，可以将其设置为 Windows 服务:

1. 安装 Windows Service 工具:
   ```cmd
   npm install -g node-windows
   ```

2. 创建服务脚本:
   ```cmd
   nssm install n8n "D:\Program Files\nodejs\node.exe" "D:\Program Files\n8n\node_modules\n8n\bin\n8n"
   ```

3. 启动服务:
   ```cmd
   nssm start n8n
   ```

## 目录结构

安装完成后，n8n 的目录结构如下:
```
D:\Program Files\n8n\
├── bin\
├── lib\
├── node_modules\
│   └── n8n\
├── package.json
└── ...
```

## 配置文件

n8n 的配置文件默认位于用户目录下:
```
%USERPROFILE%\.n8n\
```

您可以在此目录中找到:
- `config` - 配置文件
- `database.sqlite` - 数据库文件
- `nodes` - 自定义节点目录

## 常用命令

```cmd
# 启动 n8n
n8n

# 启动并指定端口
n8n --port 5678

# 启动并指定配置文件
n8n --config /path/to/config

# 查看帮助
n8n --help

# 查看版本
n8n --version
```

## 故障排除

### 1. Node.js 未找到
确保 Node.js 已正确安装并添加到系统 PATH 中。

### 2. 权限问题
以管理员身份运行命令提示符或 PowerShell。

### 3. 端口冲突
使用 `--port` 参数指定其他端口。

### 4. 内存不足
增加 Node.js 的内存限制:
```cmd
node --max-old-space-size=4096 "D:\Program Files\n8n\node_modules\n8n\bin\n8n"
```

## 安全建议

1. 不要在公网直接暴露 n8n 界面
2. 使用强密码保护 n8n 界面
3. 定期更新 n8n 到最新版本
4. 限制对 n8n 配置文件的访问权限

## 升级 n8n

要升级到最新版本，执行以下命令:
```cmd
npm update -g n8n
```

## 卸载 n8n

要卸载 n8n，执行以下命令:
```cmd
npm uninstall -g n8n
```

然后手动删除以下目录:
- `D:\Program Files\n8n\`
- `%USERPROFILE%\.n8n\`

## 支持和文档

- 官方文档: https://docs.n8n.io/
- GitHub 仓库: https://github.com/n8n-io/n8n
- 社区论坛: https://community.n8n.io/

## 联系信息

如有问题，请联系技术支持团队。