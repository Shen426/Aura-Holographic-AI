from machine import Pin, PWM
import time  # 从工具箱里拿出一块“时间怀表”

servo = PWM(Pin(15))     # 抓取15号引脚，接上手电筒
servo.freq(50)           # 设定每秒闪烁50次的心跳

servo.duty_u16(4000)     # 发送指令：转到左边的安全位置
time.sleep(1)            # 看着怀表，让大脑在原地死等 1 秒钟（此时舵机保持不动）
servo.duty_u16(7000)     # 1秒钟后发送新指令：转到右边的安全位置
