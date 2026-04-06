import bpy

# ==========================================
# 【参数调节区】在这里修改数值即可改变效果
# ==========================================
PARTICLE_DENSITY = 5      # 粒子密度 (建议 3-6，数值越大粒子越多)
RING_RADIUS = 3.5        # 环/球体的整体半径
PARTICLE_SIZE = 0.002      # 每个粒子的大小
PARTICLE_COLOR = (0.3, 1.6, 1.5, 1000.0) # 颜色 (红, 绿, 蓝, 透明度)
GLOW_STRENGTH = 10000.0      # 发光强度 (数值越大越闪亮)
# ==========================================

# 1. 初始化场景：清理旧物体
if "HoloRing" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["HoloRing"], do_unlink=True)

# 2. 创建基础网格 (作为粒子的分布载体)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=PARTICLE_DENSITY, radius=RING_RADIUS)
obj = bpy.context.active_object
obj.name = "HoloRing"

# 3. 创建发光材质
mat_name = "HoloMat"
mat = bpy.data.materials.get(mat_name) or bpy.data.materials.new(name=mat_name)
mat.use_nodes = True
m_nodes = mat.node_tree.nodes
m_nodes.clear()

m_out = m_nodes.new('ShaderNodeOutputMaterial')
m_em = m_nodes.new('ShaderNodeEmission')
m_em.inputs[0].default_value = PARTICLE_COLOR
m_em.inputs[1].default_value = GLOW_STRENGTH
mat.node_tree.links.new(m_em.outputs[0], m_out.inputs[0])

# 4. 设置几何节点
gn_mod = obj.modifiers.new(name="HoloParticles", type='NODES')
nt = bpy.data.node_groups.new('HoloGN', 'GeometryNodeTree')
gn_mod.node_group = nt
nodes = nt.nodes
links = nt.links
nodes.clear()

# 定义接口
nt.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
nt.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

# 创建节点
n_in = nodes.new('NodeGroupInput')
n_out = nodes.new('NodeGroupOutput')
n_pts = nodes.new('GeometryNodeMeshToPoints')
n_inst = nodes.new('GeometryNodeInstanceOnPoints')
n_ico = nodes.new('GeometryNodeMeshIcoSphere')
n_set_mat = nodes.new('GeometryNodeSetMaterial')
n_realize = nodes.new('GeometryNodeRealizeInstances')

# 设置节点内部参数
n_ico.inputs[0].default_value = PARTICLE_SIZE
n_ico.inputs[1].default_value = 2  # 粒子本身的圆滑度
n_set_mat.inputs[2].default_value = mat

# --- 连接逻辑 ---
links.new(n_in.outputs[0], n_pts.inputs[0])           # 输入 -> 转点
links.new(n_pts.outputs[0], n_inst.inputs[0])        # 点 -> 实例化位置
links.new(n_ico.outputs[0], n_inst.inputs[2])        # 小球 -> 实例形状
links.new(n_inst.outputs[0], n_set_mat.inputs[0])    # 实例化结果 -> 设材质
links.new(n_set_mat.outputs[0], n_realize.inputs[0]) # 材质结果 -> 意识到实例
links.new(n_realize.outputs[0], n_out.inputs[0])     # 最终输出

# 5. 视图与环境设置
if not obj.data.materials:
    obj.data.materials.append(mat)
else:
    obj.data.materials[0] = mat

# 修复 5.1 中的 View Selected 报错并自动对焦
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces.active.shading.type = 'RENDERED'
        # 使用新的 temp_override 语法修复报错
        with bpy.context.temp_override(area=area, region=area.regions[-1]):
            bpy.ops.view3d.view_selected()
