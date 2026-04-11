import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
logger = logging.getLogger(__name__)

class OpenRouterLLM:
    """Aura 的大模型 API 驱动层"""

    def __init__(self, model="openrouter/free", temperature=0.85, max_tokens=2048):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 未找到 OPENROUTER_API_KEY！请检查 .env 文件")

        # 实例化真正的 OpenAI 客户端
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )

    def chat(self, messages_list):
        """接收完整的历史消息列表，请求 API 并返回纯文本"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages_list,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"调用 OpenRouter 失败: {e}", exc_info=True)
            return "⚠️ 我的全息核心遇到了一点小波动……请检查网络连接。"
