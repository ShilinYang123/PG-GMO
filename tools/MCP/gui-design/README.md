# GUI设计器 MCP 服务器

基于Pygubu的可视化GUI设计和布局优化工具，专为Tkinter应用程序设计。

## 功能特性

### 🎨 可视化设计
- 拖拽式界面设计器
- 实时预览功能
- 网格对齐和吸附
- 多种布局管理器支持

### 🔧 代码生成
- 自动生成Python代码
- 支持类和函数两种模式
- 代码格式化和注释
- UTF-8编码支持

### 📐 布局优化
- 自动调整组件大小
- 响应式设计支持
- 最小化嵌套结构
- 智能间距优化

### 🚀 快速操作
- 预设布局模板
- 常用组件库
- 批量操作支持
- 项目管理功能

## 安装要求

```bash
pip install pygubu pygubu-designer
```

## 使用方法

### 1. 启动设计器
```python
from local_gui_designer_server import LocalGUIDesignerServer

server = LocalGUIDesignerServer()
server.launch_designer()
```

### 2. 创建新项目
```python
project_info = server.create_project("我的GUI项目", "项目描述")
```

### 3. 生成代码
```python
code = server.generate_code("project.ui", "MyApp")
```

### 4. 优化布局
```python
optimized = server.optimize_layout("project.ui")
```

## 支持的组件

- **容器组件**: Frame, LabelFrame, Notebook, PanedWindow
- **输入组件**: Entry, Text, Spinbox, Scale
- **选择组件**: Checkbutton, Radiobutton, Combobox, Listbox
- **显示组件**: Label, Button, Canvas, Progressbar
- **菜单组件**: Menu, Menubutton, OptionMenu

## 布局管理器

- **Pack**: 简单的垂直/水平布局
- **Grid**: 网格布局，适合复杂界面
- **Place**: 绝对定位，精确控制

## 项目结构

```
gui-design/
├── local_gui_designer_server.py  # MCP服务器主文件
├── gui_designer_config.json      # 配置文件
├── gui-projects/                 # 项目文件夹
├── gui-templates/                # 模板文件夹
├── gui-exports/                  # 导出文件夹
└── gui-backups/                  # 备份文件夹
```

## 配置选项

编辑 `gui_designer_config.json` 文件来自定义：

- 默认窗口大小和主题
- 代码生成选项
- 布局优化设置
- 项目目录结构

## 最佳实践

1. **使用网格布局**: 对于复杂界面，推荐使用Grid布局管理器
2. **合理嵌套**: 避免过深的组件嵌套，影响性能
3. **响应式设计**: 使用相对大小和权重，适应不同屏幕
4. **代码规范**: 生成的代码遵循PEP8规范
5. **版本控制**: .ui文件是XML格式，便于版本管理

## 故障排除

### 常见问题

**Q: 设计器无法启动**
A: 检查pygubu-designer是否正确安装，运行 `pip show pygubu-designer`

**Q: 生成的代码有错误**
A: 确保.ui文件格式正确，检查组件名称是否重复

**Q: 布局显示异常**
A: 检查布局管理器设置，避免混用不同的布局方式

### 调试模式

启用调试模式获取详细日志：

```python
server = LocalGUIDesignerServer(debug=True)
```

## 更新日志

### v1.0.0 (2025-09-19)
- 初始版本发布
- 支持基本的GUI设计功能
- 集成Pygubu设计器
- 提供代码生成和布局优化

---

**技术支持**: PG-GMO Team  
**最后更新**: 2025-09-19