import bpy

# 1. 找到我们的主角
obj = bpy.data.objects.get("Cube")
if obj:
    # --- 视觉升级：从“弹珠”变“星尘” ---
    pset = obj.particle_systems[0].settings
    pset.count = 8000           # 数量增加到 8000（更致密）
    pset.particle_size = 0.005  # 半径缩小到原来的 1/20（变细碎）
    pset.size_random = 0.8      # 增加随机感，不那么死板
    
    # --- 材质升级：高频脉冲蓝 ---
    mat = bpy.data.materials.get("Jarvis_Glow")
    if mat:
        nodes = mat.node_tree.nodes
        emit_node = nodes.get("Emission") # 找到发光节点
        if emit_node:
            # 颜色调成电磁蓝 (R:0, G:0.5, B:1)
            emit_node.inputs[0].default_value = (0, 0.5, 1, 1) 
            # 亮度暴增到 50 (产生过曝的科幻感)
            emit_node.inputs[1].default_value = 50.0

    # --- 环境升级：关掉画室的灯 ---
    # 把背景世界调成纯黑
    world = bpy.data.worlds.get("World")
    if world:
        world.node_tree.nodes["Background"].inputs[1].default_value = 0.0

    # --- 引擎升级：开启灵魂辉光 ---
    bpy.context.scene.eevee.use_bloom = True
    bpy.context.scene.eevee.bloom_intensity = 0.08 # 辉光强度
    bpy.context.scene.eevee.bloom_radius = 6.5    # 辉光半径

    print("视觉协议已更新，请在渲染模式下观察星尘！")
