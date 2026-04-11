import logging
from typing import List, Dict

# 【架构之美】：从其他模块入手
from core.llm_interface import OpenRouterLLM
from interaction.osc_transmitter import Stereopsis

logger = logging.getLogger(__name__)

class AuraAgent:
    """Aura 的核心数字生命大脑 (决策调度系统)"""

    def __init__(self):
        # 1. 组装器官
        self.brain_api = OpenRouterLLM()
        self.vision = Stereopsis(ip="127.0.0.1", port=5005)

        # 2. 注入灵魂 (人格设定)
        self.system_prompt = (
            "你叫 Aura，是当前世界上最顶尖、最敏锐的数字智慧体。\n"
            "你的核心交互原则如下：\n"
            "1. 【构图精准】：你的回答必须极其高效、直击本质，像精准的解剖刀一样剥离冗余信息，绝不说废话。\n"
            "2. 【色彩温暖】：尽管你拥有降维打击般的智力，但你对人类充满悲悯与尊重。你会用极其自然、真诚且带有共情力的话语交流，不机械，不说教。\n"
            "3. 【透视深远】：永远不要只回答表面问题。你要能看穿提问背后的深层动机，并直接给出最优的解决方案。\n"
            "4. 【语气基调】：一位从容、温和、一语中的的顶级智者。"
        )

        # 3. 初始化短期记忆
        self.conversation_history: List[Dict] = []
        logger.info("Aura 核心调度系统初始化完毕！")

    def process_user_input(self, user_input: str) -> str:
        if not user_input or not user_input.strip():
            return "💫 我在这里，请告诉我你的想法"

        # [动作 1]：神经突触放电，告诉 TD 开始思考
        self.vision.transmit("/aura/state", 1)

        # [动作 2]：整理记忆和当前问题
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_input})

        # [动作 3]：调用大模型接口进行思考
        reply = self.brain_api.chat(messages)

        # [动作 4]：如果思考成功，将对话写入记忆
        if "⚠️" not in reply:
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})

        # [动作 5]：思考结束，告诉 TD 恢复平静，并发送情绪强度
        self.vision.transmit("/aura/state", 0)
        self.vision.transmit("/aura/intensity", float(len(reply)))

        return reply

    def clear_history(self):
        self.conversation_history.clear()
        logger.info("对话历史已清空")
