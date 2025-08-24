# 数据处理类MCP工具集合

本目录包含各种数据处理、数据库操作和数据分析相关的MCP服务器。

## 已配置的工具

### 1. Qdrant向量数据库服务器
- **功能**: 向量搜索、语义检索、文档存储
- **类型**: 向量数据库
- **状态**: 待安装
- **仓库**: https://github.com/qdrant/mcp-server-qdrant
- **应用场景**: 
  - 代码片段语义搜索
  - 文档检索增强生成(RAG)
  - 知识库构建
  - 相似性搜索

### 2. Financial Datasets金融数据服务器
- **功能**: 股票数据、财务报表、市场新闻
- **类型**: 金融数据API
- **状态**: 待安装
- **仓库**: https://github.com/financial-datasets/mcp-server
- **应用场景**:
  - 股票价格查询
  - 财务报表分析
  - 市场数据获取
  - 投资研究

### 3. Markdownify文档转换服务器
- **功能**: 文件和网页内容转换为Markdown
- **类型**: 文档处理
- **状态**: 待安装
- **仓库**: https://github.com/zcaceres/markdownify-mcp
- **应用场景**:
  - 网页内容提取
  - 文档格式转换
  - 内容标准化
  - 文档处理自动化

### 4. 数据库MCP服务器
- **功能**: SQLite、PostgreSQL、MySQL数据库操作
- **类型**: 数据库接口
- **状态**: 待安装
- **仓库**: https://github.com/executeautomation/mcp-database-server
- **应用场景**:
  - 数据库查询
  - 数据分析
  - 报表生成
  - 数据管理

### 5. CSV数据探索服务器
- **功能**: 大型CSV文件分析和处理
- **类型**: 数据分析
- **状态**: 待安装
- **应用场景**:
  - 大数据集分析
  - 数据可视化
  - 统计分析
  - 数据清洗

## 安装说明

运行安装脚本：
```bash
python install_data_processing_tools.py
```

## 配置要求

### Qdrant服务器
- Python 3.8+
- 可选：Docker（用于Qdrant服务）
- 环境变量：QDRANT_URL 或 QDRANT_LOCAL_PATH

### Financial Datasets
- API密钥（从 https://financialdatasets.ai 获取）
- 环境变量：FINANCIAL_DATASETS_API_KEY

### 数据库服务器
- 对应数据库的驱动程序
- 数据库连接信息

## 使用示例

### Qdrant向量搜索
```python
# 存储文档
store_info("Python函数定义语法", {"code": "def function_name():"})

# 搜索相关内容
find_info("如何定义函数")
```

### 金融数据查询
```python
# 获取股票价格
get_stock_price("AAPL")

# 获取财务报表
get_income_statement("AAPL", "2023")
```

### 数据库操作
```python
# 执行SQL查询
execute_query("SELECT * FROM users WHERE age > 25")

# 获取表结构
describe_table("users")
```

## 注意事项

1. **API密钥管理**: 确保妥善保管各服务的API密钥
2. **数据安全**: 处理敏感数据时注意安全性
3. **性能优化**: 大数据处理时注意内存和性能
4. **版本兼容**: 定期更新工具以获得最新功能

## 故障排除

- 检查网络连接
- 验证API密钥有效性
- 确认数据库连接参数
- 查看日志文件获取详细错误信息

---

*最后更新: 2025-08-24*
*维护者: 雨俊*