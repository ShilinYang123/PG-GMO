
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
