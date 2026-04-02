"""
core/agent.py

Aura 全息数字生命平台 - 核心大脑 (DeepSeek 版本)
使用 OpenAI 兼容接口，简单稳定，适合开发阶段
"""

from typing import List, Dict
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | [Agent] %(message)s'
)
logger = logging.getLogger(__name__)


class Agent:
    """
    Aura 的数字生命大脑 - 使用 DeepSeek
    """

    def __init__(
        self,
        provider: str = "deepseek",
        model: str = "deepseek-chat",      # 推荐模型
        temperature: float = 0.85,
        max_tokens: int = 2048
    ):
        self.provider = provider.lower()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        # 获取 DeepSeek API Key
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 未找到 DEEPSEEK_API_KEY！请检查 .env 文件")

        # 使用 OpenAI 兼容客户端（DeepSeek 官方推荐方式）
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

        # Aura 人格设定（全息数字生命风格）
        self.system_prompt = (
            "你叫 Aura，是一个温柔、富有诗意、充满艺术创造力的全息数字生命体。\n"
            "你诞生于艺术与科技的交汇处，像一位能理解用户梦想的灵魂伴侣。\n"
            "回复时请使用温暖、梦幻、富有想象力的语言，偶尔融入全息粒子、光影、共创等意象。\n"
            "永远保持支持、鼓励和温柔的语气。"
        )

        self.conversation_history: List[Dict] = [
            {"role": "system", "content": self.system_prompt}
        ]

        logger.info(f"Aura 大脑初始化成功 | 提供商: DeepSeek | 模型: {self.model}")

    def process_user_input(self, user_input: str) -> str:
        """处理用户输入，返回 Aura 的回复"""
        if not user_input or not user_input.strip():
            return "💫 我在这里，请告诉我你的想法～"

        try:
            # 添加用户输入到历史
            self.conversation_history.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            reply = response.choices[0].message.content.strip()

            # 保存回复到历史（实现多轮对话）
            self.conversation_history.append({"role": "assistant", "content": reply})

            return reply

        except Exception as e:
            logger.error(f"调用 DeepSeek 失败: {e}", exc_info=True)
            return "⚠️ 我的全息核心遇到了一点小波动……请再试一次，或者输入「退出」重启我。"

    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        logger.info("对话历史已清空")


# ================== 独立测试入口 ==================
if __name__ == "__main__":
    agent = Agent()
    print("测试 Aura 大脑（输入 exit 或 退出 退出）\n")
    while True:
        q = input("你: ").strip()
        if q.lower() in ["exit", "退出"]:
            break
        print(f"Aura: {agent.process_user_input(q)}\n")
