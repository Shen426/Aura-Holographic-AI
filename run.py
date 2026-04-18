import sys
import logging
from rich.console import Console
from rich.markdown import Markdown

# 确保支持中文输出
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

# 引入核心大脑
from core.agent import AuraAgent


def main():
    #程序启动时，实例化这个超级控制台
    console = Console()
    
    print("==================================================")
    print("  ✨ Aura Holographic Digital Life - OS v2.0 ✨  ")
    print("==================================================\n")

    # 实例化数字生命
    aura = AuraAgent()

    while True:
        user_text = input("你: ").strip()

        if user_text.lower() in ["exit", "quit", "退出"，"bye"]:
            console.print("[dim]Aura 沉睡，系统安全关闭。[/dim]")
            break

        if user_text == "清空记忆":
            aura.clear_history()
            console.print("[dim italic]Aura 记忆已归零...[/dim italic]")
            continue

        # 核心交互逻辑：大脑思考返回字符串 （不涉及UI）
        reply = aura.process_user_input(user_text)

       console.print("\n[bold cyan]Aura:[/bold cyan]")
       console.print(Markdown(reply))#将字符串包装成 Markdown 对象交给 console 渲染
       console.print("\n")


if __name__ == "__main__":
    main()
