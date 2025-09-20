
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
