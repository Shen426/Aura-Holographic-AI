# 文件路径：core/llm_interface.py
import requests # 或 openai 库，取决于你怎么连的

class OpenRouterLLM:
    def __init__(self):
        # 【装】：把钥匙装进自己口袋
        self.api_key = "sk-or-v1-你的密钥"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "你的免费大模型名字"

    def chat(self, prompt):
        # 【封】：发请求的具体复杂代码全藏在这里
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        
        # 假设这里是发送请求并获取回复的代码
        # response = requests.post(...)
        # return response.json()['choices'][0]['message']['content']
        
        return "这是来自 OpenRouter 封装类的回复测试"
