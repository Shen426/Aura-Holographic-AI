import bpy

# ==========================================
# 【参数调节区】在这里修改数值即可改变效果
# ==========================================
PARTICLE_DENSITY = 5      # 粒子密度 (必须是整数，数值越大粒子越多)
RING_RADIUS = 3.5         # 环/球体的整体半径
PARTICLE_SIZE = 0.002      # 每个粒子的大小
PARTICLE_COLOR = (0.3, 1.6, 1.5, 1000.0) # 颜色 (红, 绿, 蓝, 透明度)
GLOW_STRENGTH = 10000.0      # 发光强度

# --- 波动设置 ---
WAVE_STRENGTH = 0.0005     # 波动幅度 (数值越大位移越明显)
WAVE_SCALE = 0.01          # 波动频率 (数值越大波浪越细碎)
WAVE_SPEED = 0.01           # 波动速度 (数值越大动画越快)
# ==========================================

# 1. 初始化场景：清理旧物体
if "HoloRing" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["HoloRing"], do_unlink=True)

# 2. 创建基础网格
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=int(PARTICLE_DENSITY), radius=RING_RADIUS)
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

# --- 波动逻辑节点 ---
n_set_pos = nodes.new('GeometryNodeSetPosition')
n_noise = nodes.new('ShaderNodeTexNoise')
n_time = nodes.new('GeometryNodeInputSceneTime')
n_math_mul = nodes.new('ShaderNodeVectorMath')
n_math_add = nodes.new('ShaderNodeVectorMath')

# 设置节点属性
n_ico.inputs[0].default_value = PARTICLE_SIZE
n_set_mat.inputs[2].default_value = mat
n_noise.inputs['Scale'].default_value = WAVE_SCALE
n_math_mul.operation = 'SCALE'
n_math_mul.inputs[3].default_value = WAVE_STRENGTH
n_math_add.operation = 'ADD'

# --- 连接逻辑 ---
# 1. 基础转换
links.new(n_in.outputs[0], n_pts.inputs[0])

# 2. 计算波动位移 (Noise + Time)
# 使用位置 + 时间作为噪声的输入
links.new(n_time.outputs['Seconds'], n_math_add.inputs[0])
links.new(n_math_add.outputs[0], n_noise.inputs['Vector'])
# 将噪声结果缩放后作为偏移量
links.new(n_noise.outputs['Color'], n_math_mul.inputs[0])
links.new(n_math_mul.outputs[0], n_set_pos.inputs['Offset'])

# 3. 将点连入 Set Position 进行位移
links.new(n_pts.outputs[0], n_set_pos.inputs['Geometry'])

# 4. 实例化与渲染
links.new(n_set_pos.outputs[0], n_inst.inputs[0])
links.new(n_ico.outputs[0], n_inst.inputs[2])
links.new(n_inst.outputs[0], n_set_mat.inputs[0])
links.new(n_set_mat.outputs[0], n_realize.inputs[0])
links.new(n_realize.outputs[0], n_out.inputs[0])

# 5. 视图设置
if not obj.data.materials:
    obj.data.materials.append(mat)
else:
    obj.data.materials[0] = mat

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces.active.shading.type = 'RENDERED'
        with bpy.context.temp_override(area=area, region=area.regions[-1]):
            bpy.ops.view3d.view_selected()
