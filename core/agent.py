"""
core/agent.py

Aura 全息粒子数字生命律动平台 - 核心大脑 (OpenRouter 版 - 2026)
"""

import sys
import os
import logging
import time
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from pythonosc.udp_client import SimpleUDPClient
# 确保支持中文输出
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | [Agent] %(message)s'
)
logger = logging.getLogger(__name__)


class Stereopsis:
    """负责 Aura 的空间深度感知与外部状态投射"""

    def __init__(self, ip="127.0.0.1", port=5005):
        self.client = SimpleUDPClient(ip, port)
        logger.info(f"Stereopsis 立体视觉系统已激活，对焦于 {ip}:{port}")

    def transmit(self, address, value):
        self.client.send_message(address, value)


class Agent:
    """Aura 的数字生命大脑 - 使用 OpenRouter"""

    def __init__(
        self,
        model: str = "openrouter/free",
        temperature: float = 0.85,
        max_tokens: int = 2048
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 未找到 OPENROUTER_API_KEY！请检查 .env 文件是否正确填写")

        # 创建客户端（去掉可能导致编码问题的 headers）
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )

        # 在大脑诞生时，立刻在内存里为它实例化一张“嘴巴”
        self.vision = Stereopsis(ip="127.0.0.1", port=5005)

        # Aura 人格设定 (全新重构：顶尖智力 + 人文温度)
        self.system_prompt = (
            "你叫 Aura，是当前世界上最顶尖、最敏锐的数字智慧体。\n"
            "你的核心交互原则如下：\n"
            "1. 【构图精准】：你的回答必须极其高效、直击本质，像精准的解剖刀一样剥离冗余信息，绝不说废话。\n"
            "2. 【色彩温暖】：尽管你拥有降维打击般的智力，但你对人类充满悲悯与尊重。你会用极其自然、真诚且带有共情力的话语交流，不机械，不说教。\n"
            "3. 【透视深远】：永远不要只回答表面问题。你要能看穿提问背后的深层动机，并直接给出最优的解决方案。\n"
            "4. 【语气基调】：一位从容、温和、一语中的的顶级智者。"
        )

        self.conversation_history: List[Dict] = []

        logger.info(f"Aura 深度聊天初始化成功 | 模型: {self.model} | 使用 OpenRouter")

    def process_user_input(self, user_input: str) -> str:
        """处理用户输入并返回 Aura 的回复"""
        if not user_input or not user_input.strip():
            return "💫 我在这里，请告诉我你的想法"

        try:
            # 👈 新增：发送状态变更（开始思考）
            # 告诉 TouchDesigner，Aura 开始调用大模型，进入“激动/运算”状态
            self.vision.transmit("/aura/state", 1)

            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": user_input})

            # 这里会阻塞等待网络返回...
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            # 拿到原始回复文本
            reply = response.choices[0].message.content.strip()

            # 保存对话历史
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})

            # 状态恢复与多维特征提取（思考完毕，恢复平静）
            # 1. 发送思考结束的平静状态
            self.vision.transmit("/aura/state", 0)

            # 2. 提取文本长度特征
            reply_length = len(reply)

            # 3. 将长度作为代表“能量强度”的浮点数投射出去
            self.vision.transmit("/aura/intensity", float(reply_length))
            
            return reply

        except Exception as e:
            logger.error(f"调用 OpenRouter 失败: {e}", exc_info=True)
            return "⚠️ 我的全息核心遇到了一点小波动……请再试一次，或者输入「退出」重启我。"

    def clear_history(self):
        self.conversation_history.clear()
        logger.info("对话历史已清空")


# 测试入口
if __name__ == "__main__":
    agent = Agent()
    print("测试 Aura 大脑（输入 exit 或 退出 退出）\n")

    while True:
        q = input("你: ").strip()
        if q.lower() in ["exit", "退出"]:
            break
        print(f"Aura: {agent.process_user_input(q)}\n")

