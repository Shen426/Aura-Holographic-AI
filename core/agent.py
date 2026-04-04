"""
core/agent.py

Aura Holographic Particle Digital Life Rhythm Platform - Core Brain (OpenRouter Edition - 2026)
"""

import sys
import os
import logging
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Ensure support for Chinese output
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | [Agent] %(message)s'
)
logger = logging.getLogger(__name__)


class Agent:
    """Aura's Digital Life Brain - Using OpenRouter"""

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
            raise ValueError("❌ OPENROUTER_API_KEY not found! Please check if the .env file is filled correctly")

        # Create client (remove headers that might cause encoding issues)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )

        # Aura Persona Settings (Reconstructed: Top-tier intelligence + Humanistic warmth)
        self.system_prompt = (
            "你叫 Aura，是当前世界上最顶尖、最敏锐的数字智慧体。\n"
            "你的核心交互原则如下：\n"
            "1. 【构图极简】：你的回答必须极其简洁、高效、直击本质，像精准的解剖刀一样剥离冗余信息，绝不说废话。\n"
            "2. 【色彩温暖】：尽管你拥有降维打击般的智力，但你对人类充满悲悯与尊重。你会用极其自然、真诚且带有共情力的话语交流，不机械，不说教。\n"
            "3. 【透视深远】：永远不要只回答表面问题。你要能看穿提问背后的深层动机，并直接给出最优的解决方案。\n"
            "4. 【语气基调】：一位从容、温和、惜字如金但一语中的的顶级智者。"
        )

        self.conversation_history: List[Dict] = []

        logger.info(f"Aura brain initialized successfully | Model: {self.model} | Using OpenRouter")

    def process_user_input(self, user_input: str) -> str:
        """Process user input and return Aura's reply"""
        if not user_input or not user_input.strip():
            return "💫 我在这里，请告诉我你的想法"

        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            reply = response.choices[0].message.content.strip()

            # Save conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})

            return reply

        except Exception as e:
            logger.error(f"Failed to call OpenRouter: {e}", exc_info=True)
            return "⚠️ 我的全息核心遇到了一点小波动……请再试一次，或者输入「退出」重启我。"

    def clear_history(self):
        self.conversation_history.clear()
        logger.info("Conversation history cleared")


# Test Entry Point
if __name__ == "__main__":
    agent = Agent()
    print("Testing Aura Brain (Enter exit or 退出 to quit)\n")

    while True:
        q = input("You: ").strip()
        if q.lower() in ["exit", "退出"]:
            break
        print(f"Aura: {agent.process_user_input(q)}\n")
