import sys
import logging

# 确保支持中文输出
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

# 引入核心大脑
from core.agent import AuraAgent


def main():
    print("==================================================")
    print("  ✨ Aura Holographic Digital Life - OS v2.0 ✨  ")
    print("==================================================\n")

    # 实例化数字生命
    aura = AuraAgent()

    while True:
        user_text = input("你: ").strip()

        if user_text.lower() in ["exit", "quit", "退出"]:
            print("Aura 沉睡，系统安全关闭。")
            break

        if user_text == "清空记忆":
            aura.clear_history()
            continue

        # 核心交互逻辑只有极其优雅的一行代码
        reply = aura.process_user_input(user_text)

        print(f"Aura: {reply}")



if __name__ == "__main__":
    main()
