# n8n 品牌检查工作流文件保存配置说明

## 问题分析

根据您提供的截图和n8n官方文档，之前的工作流无法保存文件的原因是：

1. **缺少必要的节点组合**：n8n中保存文件需要两个节点配合使用：
   - `Convert to File` 节点：将数据转换为文件格式
   - `Read/Write Files from Disk` 节点：将文件写入磁盘

2. **数据格式不正确**：直接在Code节点中生成CSV字符串无法被文件保存节点识别

## 解决方案

### 新工作流文件：`n8n_brand_checker_workflow_with_file_save.json`

这个新版本工作流包含以下关键改进：

#### 1. 添加了文件保存节点组合

```json
// 转换为CSV文件节点
{
  "parameters": {
    "operation": "toCsv",
    "options": {
      "fileName": "brand_check_results_{{ new Date().toISOString().slice(0,19).replace(/:/g, '-') }}.csv"
    }
  },
  "name": "转换为CSV文件",
  "type": "n8n-nodes-base.convertToFile"
}

// 保存文件到磁盘节点
{
  "parameters": {
    "operation": "write",
    "fileName": "={{ $json.fileName }}",
    "options": {}
  },
  "name": "保存文件到磁盘",
  "type": "n8n-nodes-base.readWriteFile"
}
```

#### 2. 动态文件名生成

文件名使用时间戳自动生成，格式如：`brand_check_results_2024-01-15T10-30-45.csv`

#### 3. 正确的数据流

```
生成最终报告 → 转换为CSV文件 → 保存文件到磁盘
```

## 使用步骤

### 1. 导入工作流

1. 在n8n界面中点击 "Import from File"
2. 选择 `n8n_brand_checker_workflow_with_file_save.json` 文件
3. 点击 "Import" 导入工作流

### 2. 配置文件保存路径（重要）

根据n8n官方文档，需要确保n8n有权限写入文件。推荐配置：

#### Docker环境
```bash
# 创建本地文件目录
mkdir local-files

# 在docker-compose.yml中添加卷映射
volumes:
  - ./local-files:/files
```

#### 本地安装
确保n8n进程有权限写入指定目录，建议使用：
- Windows: `C:\temp\n8n-files\`
- Linux/Mac: `/tmp/n8n-files/`

### 3. 修改文件保存路径

在 "保存文件到磁盘" 节点中，将 `fileName` 参数修改为完整路径：

```javascript
// Windows示例
="C:\\temp\\n8n-files\\{{ $json.fileName }}"

// Linux/Mac示例
="/tmp/n8n-files/{{ $json.fileName }}"

// Docker环境示例
="/files/{{ $json.fileName }}"
```

### 4. 运行工作流

1. 点击 "Execute Workflow" 按钮
2. 工作流将依次执行所有节点
3. 最后会在指定目录生成CSV文件

## 故障排除

### 如果仍然无法保存文件：

1. **检查权限**：确保n8n进程有写入目标目录的权限
2. **检查路径**：确保目标目录存在
3. **查看日志**：在n8n界面查看执行日志，寻找错误信息
4. **测试简单路径**：先尝试保存到 `/tmp/` 或 `C:\temp\` 等简单路径

### 常见错误及解决方案：

1. **"Permission denied"**：权限问题，需要修改目录权限或更换保存路径
2. **"Directory not found"**：目标目录不存在，需要先创建目录
3. **"Invalid file name"**：文件名包含非法字符，检查动态文件名生成逻辑

## 验证文件保存

工作流执行完成后：
1. 检查指定目录是否生成了CSV文件
2. 打开CSV文件验证内容是否正确
3. 文件应包含品牌名称、域名可用性、YouTube可用性等信息

## 进一步优化建议

1. **添加错误处理**：在文件保存节点后添加错误处理逻辑
2. **文件路径配置**：将文件保存路径设置为环境变量
3. **文件格式选择**：根据需要支持JSON、Excel等其他格式
4. **自动清理**：定期清理旧的结果文件

---

**注意**：请确保按照上述配置正确设置文件保存路径，这是文件保存成功的关键因素。