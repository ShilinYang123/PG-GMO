# PowerPoint MCP Server 重启 Claude Desktop 指南

## 当前状态

✅ **PowerPoint MCP Server 安装完成**
- 仓库已克隆到: `S:\PG-GMO\Office-PowerPoint-MCP-Server`
- 依赖包已安装: `mcp[cli]`, `python-pptx`, `Pillow`, `fonttools`
- 功能测试全部通过
- 配置文件已添加到 Claude Desktop

## 需要重启 Claude Desktop

**重要**: 新添加的 MCP Server 配置需要重启 Claude Desktop 才能生效。

### 重启步骤

1. **完全关闭 Claude Desktop**
   - 右键点击任务栏中的 Claude 图标
   - 选择 "退出" 或 "Exit"
   - 确保 Claude Desktop 完全关闭

2. **重新启动 Claude Desktop**
   - 从开始菜单或桌面快捷方式启动 Claude Desktop
   - 等待应用完全加载

3. **验证 PowerPoint 功能**
   - 重启后，在 Claude 中输入: "请创建一个测试 PowerPoint 演示文稿"
   - 如果能正常调用 PowerPoint 功能，说明配置成功

## 配置详情

已添加到 Claude Desktop 配置文件的内容:

```json
"powerpoint-mcp-server": {
  "command": "C:\\Users\\YDS-workroom\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
  "args": [
    "S:\\PG-GMO\\Office-PowerPoint-MCP-Server\\ppt_mcp_server.py"
  ],
  "env": {
    "PYTHONPATH": "S:\\PG-GMO\\Office-PowerPoint-MCP-Server",
    "PPT_TEMPLATE_PATH": "S:\\PG-GMO\\Office-PowerPoint-MCP-Server\\templates",
    "MCP_TRANSPORT": "stdio"
  }
}
```

## PowerPoint MCP Server 功能

重启后可使用的 PowerPoint 功能包括:

### 演示文稿管理
- 创建新演示文稿
- 打开现有演示文稿
- 保存演示文稿
- 获取演示文稿信息

### 幻灯片操作
- 添加新幻灯片
- 删除幻灯片
- 复制幻灯片
- 移动幻灯片

### 内容编辑
- 添加文本内容
- 插入图片
- 创建表格
- 添加图表

### 模板和样式
- 应用幻灯片模板
- 设置主题
- 自定义样式
- 专业效果

## 故障排除

如果重启后仍无法使用 PowerPoint 功能:

1. **检查配置文件**
   ```powershell
   Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

2. **手动测试 MCP Server**
   ```powershell
   cd "S:\PG-GMO\Office-PowerPoint-MCP-Server"
   python ppt_mcp_server.py
   ```

3. **检查 Python 环境**
   ```powershell
   python -c "import pptx; print('python-pptx 可用')"
   ```

## 测试文件

已生成的测试文件:
- `S:\PG-GMO\Office-PowerPoint-MCP-Server\PowerPoint功能测试演示文稿.pptx`
- `S:\PG-GMO\Office-PowerPoint-MCP-Server\PowerPoint功能测试.py`

---

**技术负责人**: 雨俊  
**完成时间**: 2025-01-08  
**状态**: ✅ 安装完成，等待重启验证