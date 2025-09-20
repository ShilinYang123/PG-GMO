#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地Blender MCP服务器
提供基础的3D建模和渲染功能接口
"""

import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalBlenderMCPServer:
    def __init__(self):
        self.server_name = "Local Blender MCP Server"
        self.version = "1.0.0"
        self.base_dir = Path(__file__).parent
        self.projects_dir = self.base_dir / "blender-projects"
        self.renders_dir = self.base_dir / "blender-renders"
        self.scripts_dir = self.base_dir / "blender-scripts"
        
        # 创建必要目录
        self.projects_dir.mkdir(exist_ok=True)
        self.renders_dir.mkdir(exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
        
        # Blender可执行文件路径（需要用户配置）
        self.blender_path = self._find_blender_path()
        
        logger.info(f"启动 {self.server_name} v{self.version}")
        if self.blender_path:
            logger.info(f"Blender路径: {self.blender_path}")
        else:
            logger.warning("未找到Blender安装路径，某些功能可能无法使用")
    
    def _find_blender_path(self):
        """查找Blender安装路径"""
        possible_paths = [
            "C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe",
            "C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe",
            "C:\\Program Files\\Blender Foundation\\Blender 3.5\\blender.exe",
            "blender"  # 如果在PATH中
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run(
                    [path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        return None
    
    def list_available_functions(self):
        """列出可用功能"""
        functions = [
            "create_3d_project - 创建3D项目",
            "generate_basic_shapes - 生成基础几何体",
            "create_material - 创建材质",
            "setup_lighting - 设置灯光",
            "render_scene - 渲染场景",
            "export_model - 导出模型",
            "create_animation - 创建动画",
            "batch_render - 批量渲染"
        ]
        
        logger.info("支持的功能:")
        for func in functions:
            logger.info(f"  - {func}")
        
        return functions
    
    def create_3d_project(self, project_name, description=""):
        """创建3D项目"""
        project_dir = self.projects_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        project_config = {
            "name": project_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "objects": [],
            "materials": [],
            "lights": [],
            "cameras": [],
            "render_settings": {
                "engine": "CYCLES",
                "samples": 128,
                "resolution_x": 1920,
                "resolution_y": 1080
            }
        }
        
        config_file = project_dir / "project.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(project_config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"创建3D项目: {project_name}")
        return f"项目 '{project_name}' 创建成功"
    
    def generate_blender_script(self, script_name, script_type="basic_scene"):
        """生成Blender Python脚本"""
        scripts = {
            "basic_scene": '''
import bpy
import bmesh
from mathutils import Vector

# 清除默认场景
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 创建立方体
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "MyCube"

# 创建材质
material = bpy.data.materials.new(name="CubeMaterial")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.8, 0.2, 0.2, 1.0)  # 红色
cube.data.materials.append(material)

# 添加灯光
bpy.ops.object.light_add(type='SUN', location=(4, 4, 4))
light = bpy.context.active_object
light.data.energy = 5

# 添加相机
bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)

# 设置渲染引擎
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128

print("基础场景创建完成")
''',
            "animation": '''
import bpy
from mathutils import Vector

# 清除默认场景
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 创建立方体
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "AnimatedCube"

# 设置关键帧动画
frame_start = 1
frame_end = 120

# 起始位置
bpy.context.scene.frame_set(frame_start)
cube.location = (0, 0, 0)
cube.keyframe_insert(data_path="location", index=-1)

# 结束位置
bpy.context.scene.frame_set(frame_end)
cube.location = (5, 0, 0)
cube.keyframe_insert(data_path="location", index=-1)

# 设置动画范围
bpy.context.scene.frame_start = frame_start
bpy.context.scene.frame_end = frame_end

print("动画创建完成")
''',
            "material_nodes": '''
import bpy

# 创建新材质
material = bpy.data.materials.new(name="ProceduralMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# 清除默认节点
nodes.clear()

# 添加节点
output_node = nodes.new(type='ShaderNodeOutputMaterial')
bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
noise_node = nodes.new(type='ShaderNodeTexNoise')
coord_node = nodes.new(type='ShaderNodeTexCoord')

# 设置节点位置
output_node.location = (400, 0)
bsdf_node.location = (200, 0)
noise_node.location = (0, 0)
coord_node.location = (-200, 0)

# 连接节点
links.new(coord_node.outputs['Generated'], noise_node.inputs['Vector'])
links.new(noise_node.outputs['Color'], bsdf_node.inputs['Base Color'])
links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

print("程序化材质创建完成")
'''
        }
        
        script_content = scripts.get(script_type, scripts["basic_scene"])
        script_file = self.scripts_dir / f"{script_name}.py"
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        logger.info(f"生成Blender脚本: {script_name} ({script_type})")
        return f"脚本已生成: {script_file}"
    
    def execute_blender_script(self, script_path, output_file=None):
        """执行Blender脚本"""
        if not self.blender_path:
            return "错误: 未找到Blender安装路径"
        
        try:
            cmd = [self.blender_path, "--background", "--python", str(script_path)]
            
            if output_file:
                cmd.extend(["--render-output", str(output_file)])
                cmd.append("--render-frame", "1")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                logger.info(f"Blender脚本执行成功: {script_path}")
                return f"脚本执行成功: {script_path}"
            else:
                logger.error(f"Blender脚本执行失败: {result.stderr}")
                return f"脚本执行失败: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "错误: 脚本执行超时"
        except Exception as e:
            return f"错误: {str(e)}"
    
    def create_render_job(self, project_name, frame_range=(1, 1)):
        """创建渲染任务"""
        render_config = {
            "project": project_name,
            "frame_start": frame_range[0],
            "frame_end": frame_range[1],
            "output_path": str(self.renders_dir / project_name),
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        job_file = self.renders_dir / f"{project_name}_render_job.json"
        with open(job_file, 'w', encoding='utf-8') as f:
            json.dump(render_config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"创建渲染任务: {project_name}")
        return f"渲染任务已创建: {job_file}"
    
    def run_demo(self):
        """运行演示"""
        logger.info("=== Blender MCP服务器演示 ===")
        
        # 列出功能
        self.list_available_functions()
        
        # 创建示例项目
        self.create_3d_project("示例3D项目", "这是一个示例3D建模项目")
        
        # 生成脚本
        self.generate_blender_script("basic_scene", "basic_scene")
        self.generate_blender_script("cube_animation", "animation")
        self.generate_blender_script("procedural_material", "material_nodes")
        
        # 创建渲染任务
        self.create_render_job("示例3D项目", (1, 120))
        
        logger.info("演示完成！")
        
        if self.blender_path:
            logger.info("可以使用execute_blender_script()方法执行生成的脚本")
        else:
            logger.info("请安装Blender并配置路径以使用完整功能")

def main():
    """主函数"""
    server = LocalBlenderMCPServer()
    server.run_demo()

if __name__ == "__main__":
    main()