
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
