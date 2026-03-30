"""
Project: Aura-Holographic-AI
Module: Core Logic Foundation
Author: SHEN (The Creator)
Date: 2026-03-29
Description: 包含基础对话交互、状态判断及核心技能包封装。
"""

# --- 1. 技能包定义 (Functions) ---
def check_system_status(input_cmd):
    """处理系统指令的翻译官"""
    if input_cmd == "启动系统":
        print(">> [Aura]: 系统已就绪，全息投影模块待命。")
        return True
    elif input_cmd == "开发者是谁":
        print(">> [Aura]: 我的造物主是了不起的 SHEN 女士。")
        return True
    elif input_cmd == "退出":
        print(">> [Aura]: 再见，Selene 女士。期待下次与您共创艺术。")
        return False
    else:
        print(">> [Aura]: 抱歉，当前指令超出了我的逻辑边界。")
        return True

# --- 2. 主程序循环 (Main Lifecycle) ---
def main():
    print("--- Aura 核心逻辑层已加载 ---")
    is_running = True
    
    while is_running:
        # 获取用户输入
        user_input = input("\n请输入指令 (或输入'退出'): ").strip()
        
        # 调用技能包处理逻辑
        is_running = check_system_status(user_input)

if __name__ == "__main__":
    main()
