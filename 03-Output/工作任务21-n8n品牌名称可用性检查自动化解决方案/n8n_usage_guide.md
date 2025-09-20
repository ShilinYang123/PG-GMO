# n8n 使用指南

## 概述
n8n 是一个开源的工作流自动化工具，可以帮助您连接不同的应用程序和服务，创建自动化工作流。

## 启动 n8n

### 方法一: 使用启动脚本
双击 `D:\Program Files\n8n\start_n8n.bat` 文件启动 n8n。

### 方法二: 命令行启动
打开命令提示符，执行以下命令:
```cmd
cd /d "D:\Program Files\n8n"
node node_modules\n8n\bin\n8n
```

### 方法三: 全局命令启动
如果已将 n8n 添加到系统 PATH:
```cmd
n8n
```

## 访问 n8n 界面

启动成功后，在浏览器中访问:
```
http://localhost:5678
```

首次访问会要求您创建账户。

## 基本概念

### 1. 工作流 (Workflow)
工作流是一系列连接的节点，定义了自动化的业务逻辑。

### 2. 节点 (Node)
节点是工作流的基本构建块，每个节点执行特定的功能。

### 3. 连接 (Connection)
连接定义了节点之间的数据流和执行顺序。

### 4. 触发器 (Trigger)
触发器是工作流的起点，决定何时执行工作流。

## 创建第一个工作流

### 1. 创建新工作流
1. 点击左侧菜单的 "Workflows"
2. 点击 "Add Workflow"
3. 输入工作流名称和描述

### 2. 添加触发器
1. 点击 "+" 添加节点
2. 选择触发器类型 (如 HTTP Request, Cron, Manual Trigger 等)
3. 配置触发器参数

### 3. 添加操作节点
1. 点击 "+" 添加新节点
2. 选择应用程序或服务
3. 配置连接参数
4. 设置操作参数

### 4. 连接节点
拖拽节点之间的连接点来建立数据流。

### 5. 测试工作流
点击 "Test workflow" 按钮测试工作流。

### 6. 激活工作流
点击 "Activate" 按钮使工作流在触发条件满足时自动执行。

## 常用节点类型

### 1. HTTP Request
发送 HTTP 请求到指定的 URL。

### 2. Email
发送电子邮件。

### 3. Slack
与 Slack 集成，发送消息。

### 4. Telegram
与 Telegram 集成，发送消息。

### 5. Webhook
接收和处理 Webhook 请求。

### 6. Cron
基于时间调度执行工作流。

### 7. Manual Trigger
手动触发工作流执行。

## 配置管理

### 1. 环境变量
在 `D:\Program Files\n8n\.env` 文件中设置环境变量:
```env
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_HOST=localhost
DB_TYPE=sqlite
```

### 2. 数据库配置
n8n 默认使用 SQLite 数据库，数据存储在:
```
%USERPROFILE%\.n8n\database.sqlite
```

### 3. 日志配置
日志文件默认存储在:
```
%USERPROFILE%\.n8n\n8n.log
```

## 高级功能

### 1. 自定义节点
您可以创建自定义节点来扩展 n8n 的功能。

### 2. 凭据管理
n8n 提供安全的凭据存储和管理功能。

### 3. Webhook URL
每个工作流可以有唯一的 Webhook URL 用于外部触发。

### 4. 执行数据
可以查看和分析工作流的执行历史和数据。

## 安全最佳实践

### 1. 访问控制
- 设置强密码
- 启用双因素认证
- 限制对 n8n 界面的访问

### 2. 网络安全
- 不要在公网直接暴露 n8n
- 使用反向代理 (如 Nginx) 和 SSL
- 配置防火墙规则

### 3. 数据安全
- 定期备份数据库
- 加密敏感数据
- 审计凭据使用

## 故障排除

### 1. 无法启动
- 检查端口是否被占用
- 检查 Node.js 版本兼容性
- 查看日志文件获取错误信息

### 2. 节点连接失败
- 检查网络连接
- 验证凭据配置
- 查看节点文档获取帮助

### 3. 性能问题
- 增加 Node.js 内存限制
- 优化工作流设计
- 考虑使用外部数据库

## 备份和恢复

### 1. 备份数据库
```cmd
copy "%USERPROFILE%\.n8n\database.sqlite" "备份路径\database_backup.sqlite"
```

### 2. 备份配置
备份以下文件和目录:
- `%USERPROFILE%\.n8n\`
- `D:\Program Files\n8n\`

### 3. 恢复数据
将备份文件复制回原位置。

## 升级 n8n

### 1. 备份当前版本
在升级前务必备份数据。

### 2. 执行升级
```cmd
npm update -g n8n
```

### 3. 验证升级
启动 n8n 并检查版本信息。

## API 使用

n8n 提供 REST API 用于程序化管理:
- 工作流管理
- 执行管理
- 凭据管理
- 用户管理

API 文档请参考官方文档。

## 社区和资源

### 1. 官方资源
- 官网: https://n8n.io/
- 文档: https://docs.n8n.io/
- GitHub: https://github.com/n8n-io/n8n

### 2. 社区资源
- 论坛: https://community.n8n.io/
- 示例工作流: https://n8n.io/workflows
- 教程: https://docs.n8n.io/courses

## 常见问题

### 1. 如何更改默认端口?
在启动时使用 `--port` 参数:
```cmd
n8n --port 3000
```

### 2. 如何使用外部数据库?
配置环境变量:
```env
DB_TYPE=postgres
DB_POSTGRES_HOST=localhost
DB_POSTGRES_PORT=5432
DB_POSTGRES_USER=user
DB_POSTGRES_PASSWORD=password
DB_POSTGRES_DATABASE=n8n
```

### 3. 如何设置 SSL?
使用反向代理 (如 Nginx) 配置 SSL 终止。

### 4. 如何限制访问?
配置基本认证或使用反向代理的身份验证功能。