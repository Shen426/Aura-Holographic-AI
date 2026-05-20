import machine, neopixel, time, math

# 初始化 12 颗灯珠
ring = neopixel.NeoPixel(machine.Pin(13), 12)

# 【关键点1：设定最高亮度封印】 把它控制在温润的 40
MAX_BRIGHTNESS = 40 

try:
    # 建立一个时间变量，作为生命流动的标尺
    t = 0.0 
    
    while True:
        # 【关键点2：使用数学引擎生成丝滑曲线】
        # math.sin(t) 会在 -1.0 到 1.0 之间平滑起伏
        # 我们用 (sin(t) + 1) / 2 把它转换成 0 到 1 之间的完美比例系数
        organic_factor = (math.sin(t) + 1.0) / 2.0
        
        # 将系数乘以我们设定的最高亮度，得到当前这一瞬间的真实亮度
        current_b = int(organic_factor * MAX_BRIGHTNESS)
        
        # 赋予全环 Aura 标志性的生命之绿
        ring.fill((0, current_b, 0))
        ring.write()
        
        # 【关键点3：心率控制】
        # t 每次增加的数值，决定了心脏跳动的快慢。
        # 0.06 是一个极其接近人类深度睡眠/深呼吸的平缓频率。
        t += 0.06 
        
        # 保持 60帧/秒 的极高刷新率，拒绝卡顿
        time.sleep(0.016) 
            
except KeyboardInterrupt:
    ring.fill((0, 0, 0))
    ring.write()
