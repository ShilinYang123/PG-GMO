# n8n 品牌名称可用性检查工作流使用指南

## 📋 概述
这个工作流可以自动检查品牌名称在以下平台的可用性：
- .com 域名
- YouTube 用户名

## 🚀 快速开始

### 1. 导入工作流
1. 打开 n8n 界面：http://localhost:5678
2. 点击右上角的 "Import from file" 或 "+" 按钮
3. 选择工作流文件：`S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_brand_checker_workflow.json`
4. 点击 "Import" 导入工作流

### 2. 准备输入文件
输入文件位置：`S:\PG-GMO\02-Input\工作任务21-n8n品牌名称可用性检查自动化解决方案\brand_names.csv`

格式示例：
```csv
name
HaloQuip
hqpmade
hqpelectric
hqpfactory
```

### 3. 运行工作流
1. 在 n8n 中打开导入的工作流
2. 点击 "手动触发" 节点
3. 点击 "Execute Workflow" 按钮
4. 等待执行完成

### 4. 查看结果
结果将在n8n界面中显示，也可以配置保存到指定位置

结果格式：
```csv
name,domainAvailable,youtubeAvailable,checkTime
HaloQuip,true,false,2024-01-15T10:30:00.000Z
hqpmade,false,true,2024-01-15T10:30:01.000Z
```

## 🔧 工作流节点说明

### 1. 手动触发
- 用于启动工作流
- 点击即可开始执行

### 2. 读取CSV文件
- 读取品牌名称列表
- 路径：`s:\PG-GMO\brand_names.csv`

### 3. 解析CSV
- 将CSV内容转换为JSON格式
- 处理每个品牌名称

### 4. 检查域名
- 使用 Google DNS API 检查 .com 域名
- 返回状态码 3 表示域名可用

### 5. 检查YouTube
- 访问 YouTube 用户页面
- 404 状态码表示用户名可用

### 6. 合并结果
- 整合所有检查结果
- 生成最终报告数据

### 7. 保存结果
- 将结果保存为CSV文件
- 输出路径：`s:\PG-GMO\brand_check_results.csv`

## 📊 结果解读

### domainAvailable 字段
- `true`: 域名可注册
- `false`: 域名已被注册
- `unknown`: 检查失败（网络问题等）

### youtubeAvailable 字段
- `true`: YouTube 用户名可用
- `false`: YouTube 用户名已被占用
- `unknown`: 检查失败

## 🛠️ 自定义配置

### 修改输入文件路径
在 "读取CSV文件" 节点中修改 `filePath` 参数

### 修改输出文件路径
在 "保存结果" 节点中修改 `filePath` 参数

### 添加更多平台检查
可以添加新的 HTTP Request 节点来检查其他平台：
- Instagram: `https://www.instagram.com/{{$json.name}}/`
- Facebook: `https://www.facebook.com/{{$json.name}}`
- TikTok: `https://www.tiktok.com/@{{$json.name}}`

## ⚠️ 注意事项

1. **网络限制**：某些平台可能有反爬虫机制
2. **请求频率**：避免过于频繁的请求，可能被限制
3. **准确性**：结果仅供参考，建议人工确认重要的品牌名
4. **API限制**：Google DNS API 有使用限制

## 🔄 扩展功能

### 批量处理优化
- 可以添加延时节点避免请求过快
- 使用 "Split In Batches" 节点分批处理大量数据

### 结果通知
- 添加邮件或Slack通知节点
- 在检查完成后自动发送报告

### 数据库存储
- 将结果存储到数据库
- 便于历史查询和分析

## 🐛 故障排除

### 常见问题
1. **文件读取失败**：检查文件路径和权限
2. **网络请求超时**：增加超时时间或检查网络连接
3. **CSV解析错误**：确保文件格式正确，使用UTF-8编码

### 调试技巧
- 在每个节点后添加 "Set" 节点查看数据
- 使用 "Execute Workflow" 的单步执行模式
- 查看节点的输出数据和错误信息

## 📈 性能优化

1. **并行处理**：当前域名和YouTube检查是并行的
2. **缓存结果**：可以添加缓存避免重复检查
3. **批量API**：使用支持批量查询的API服务

---

**提示**：这是一个基础版本，您可以根据需要添加更多平台检查和功能。建议先用少量数据测试，确认工作流正常后再处理大批量数据。