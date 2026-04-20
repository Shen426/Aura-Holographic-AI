import asyncio
import edge_tts
import pygame  # [新增] 引入喇叭模块
import os

TEXT = "SHEN女士 我是你的全息数字生命管家，Aura系统正在启动。"
VOICE = "zh-CN-XiaoxiaoNeural"
OUTPUT_FILE = "aura_test.mp3"

async def aura_speak():
    # 1. 生成语音 (造声带)
    print("Aura 正在酝酿声音...")
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    print(f"语音已保存为 {OUTPUT_FILE}")

    # 2. 播放语音 (接喇叭)
    print("Aura 开始说话 🔊")
    pygame.mixer.init()  # 初始化喇叭
    pygame.mixer.music.load(OUTPUT_FILE)  # 把音频塞进喇叭
    pygame.mixer.music.play()  # 按下播放键

    # 3. 等待播放结束 (极其重要)
    # 如果不加这句，Python 会瞬间跑完代码并退出，你一个字都听不到
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # 4. [架构师细节] 释放文件占用！
    # 必须把喇叭关掉并拔出音频文件，否则下次 Aura 说话时无法覆盖这个 mp3，会报错！
    pygame.mixer.music.unload()
    pygame.mixer.quit()

if __name__ == "__main__":
    asyncio.run(aura_speak())
