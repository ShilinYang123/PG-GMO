#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地Figma MCP服务器
提供基础的设计文件处理和代码生成功能
"""

import json
import logging
from pathlib import Path
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalFigmaMCPServer:
    def __init__(self):
        self.server_name = "Local Figma MCP Server"
        self.version = "1.0.0"
        self.base_dir = Path(__file__).parent
        self.designs_dir = self.base_dir / "figma-designs"
        self.exports_dir = self.base_dir / "figma-exports"
        
        # 创建必要目录
        self.designs_dir.mkdir(exist_ok=True)
        self.exports_dir.mkdir(exist_ok=True)
        
        logger.info(f"启动 {self.server_name} v{self.version}")
    
    def list_available_functions(self):
        """列出可用功能"""
        functions = [
            "create_design_project - 创建设计项目",
            "import_design_file - 导入设计文件",
            "export_design_assets - 导出设计资源",
            "generate_component_code - 生成组件代码",
            "analyze_design_system - 分析设计系统",
            "create_style_guide - 创建样式指南",
            "batch_export_assets - 批量导出资源"
        ]
        
        logger.info("支持的功能:")
        for func in functions:
            logger.info(f"  - {func}")
        
        return functions
    
    def create_design_project(self, project_name, description=""):
        """创建设计项目"""
        project_dir = self.designs_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        project_config = {
            "name": project_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "components": [],
            "assets": [],
            "style_guide": {}
        }
        
        config_file = project_dir / "project.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(project_config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"创建设计项目: {project_name}")
        return f"项目 '{project_name}' 创建成功"
    
    def generate_component_code(self, component_name, framework="react"):
        """生成组件代码"""
        templates = {
            "react": '''
import React from 'react';
import './{{component_name}}.css';

interface {{component_name}}Props {
  // 定义组件属性
}

const {{component_name}}: React.FC<{{component_name}}Props> = (props) => {
  return (
    <div className="{{component_name_lower}}">
      {/* 组件内容 */}
    </div>
  );
};

export default {{component_name}};
''',
            "vue": '''
<template>
  <div class="{{component_name_lower}}">
    <!-- 组件内容 -->
  </div>
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style scoped>
.{{component_name_lower}} {
  /* 组件样式 */
}
</style>
''',
            "html": '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{component_name}}</title>
    <style>
        .{{component_name_lower}} {
            /* 组件样式 */
        }
    </style>
</head>
<body>
    <div class="{{component_name_lower}}">
        <!-- 组件内容 -->
    </div>
</body>
</html>
'''
        }
        
        template = templates.get(framework, templates["react"])
        code = template.replace("{{component_name}}", component_name)
        code = code.replace("{{component_name_lower}}", component_name.lower())
        
        # 保存生成的代码
        export_file = self.exports_dir / f"{component_name}_{framework}.{self._get_file_extension(framework)}"
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"生成 {framework} 组件代码: {component_name}")
        return f"组件代码已生成: {export_file}"
    
    def _get_file_extension(self, framework):
        """获取文件扩展名"""
        extensions = {
            "react": "tsx",
            "vue": "vue",
            "html": "html"
        }
        return extensions.get(framework, "txt")
    
    def create_style_guide(self, project_name):
        """创建样式指南"""
        style_guide = {
            "colors": {
                "primary": "#007bff",
                "secondary": "#6c757d",
                "success": "#28a745",
                "danger": "#dc3545",
                "warning": "#ffc107",
                "info": "#17a2b8"
            },
            "typography": {
                "font_family": "'Helvetica Neue', Arial, sans-serif",
                "font_sizes": {
                    "h1": "2.5rem",
                    "h2": "2rem",
                    "h3": "1.75rem",
                    "h4": "1.5rem",
                    "h5": "1.25rem",
                    "h6": "1rem",
                    "body": "1rem",
                    "small": "0.875rem"
                }
            },
            "spacing": {
                "xs": "0.25rem",
                "sm": "0.5rem",
                "md": "1rem",
                "lg": "1.5rem",
                "xl": "3rem"
            },
            "breakpoints": {
                "xs": "0px",
                "sm": "576px",
                "md": "768px",
                "lg": "992px",
                "xl": "1200px"
            }
        }
        
        style_file = self.exports_dir / f"{project_name}_style_guide.json"
        with open(style_file, 'w', encoding='utf-8') as f:
            json.dump(style_guide, f, ensure_ascii=False, indent=2)
        
        logger.info(f"创建样式指南: {project_name}")
        return f"样式指南已创建: {style_file}"
    
    def run_demo(self):
        """运行演示"""
        logger.info("=== Figma MCP服务器演示 ===")
        
        # 列出功能
        self.list_available_functions()
        
        # 创建示例项目
        self.create_design_project("示例项目", "这是一个示例设计项目")
        
        # 生成组件代码
        self.generate_component_code("Button", "react")
        self.generate_component_code("Card", "vue")
        
        # 创建样式指南
        self.create_style_guide("示例项目")
        
        logger.info("演示完成！")

def main():
    """主函数"""
    server = LocalFigmaMCPServer()
    server.run_demo()

if __name__ == "__main__":
    main()