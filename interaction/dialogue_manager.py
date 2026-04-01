"""
interaction/dialogue_manager.py

Aura Holographic Digital Life & Interaction Platform - Dialogue Management Module (Front-desk Receptionist)

Module Responsibilities (Single Responsibility Principle - SRP):
    - Receive user input (Text, expandable to Voice/Gestures in the future)
    - Identify and handle basic system commands (Start, Exit, Developer info, etc.)
    - Maintain the long-term interaction loop
    - Forward complex dialogue content to the core brain (core/agent.py)
    - Provide graceful shutdown and error handling mechanisms

Author: Easy-to-understand version designed for Interdisciplinary Arts Researchers
Based on Legacy Code Refactoring: Retains the core intent of 'check_system_status' and upgrades it to an OOP architecture.
"""

from typing import Callable, Optional, Dict, Any
import sys
import logging
from datetime import datetime

# Configure logging to observe the system operation process
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | [DialogueManager] %(message)s'
)
logger = logging.getLogger(__name__)


class DialogueManager:
    """
    Aura Dialogue Manager - Core Interaction Class

    Acts like a professional receptionist:
    - Handles simple commands personally (Start, Exit, Who is the developer?)
    - Forwards complex content to the "Brain" (core/agent.py)
    - Responsible for starting, maintaining, and gracefully ending the dialogue.
    """

    def __init__(self, agent_processor: Optional[Callable[[str], str]] = None):
        """
        Initialize the Dialogue Manager

        Args:
            agent_processor: Processing function from the core brain (from core/agent.py)
                             If None, a Mock version is used for independent testing.
        """
        self.is_running: bool = False
        self.current_session_id: str = self._generate_session_id()
        self.conversation_history: list[Dict[str, str]] = []

        # Core Brain Interface (Key for Decoupling)
        self.agent_processor = agent_processor or self._mock_agent_processor

        logger.info(f"DialogueManager 初始化完成 | 会话ID: {self.current_session_id}")

    def _generate_session_id(self) -> str:
        """Generate a unique Session ID to track each interaction"""
        return f"aura_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # ====================== Legacy Code Upgrade Section ======================

    def check_system_status(self, user_input: str) -> bool:
        """
        [Upgraded] System Command Processor

        Refactored directly from the previous 'check_system_status',
        retaining the same command intent while adding friendly prompts and logs.
        Returns True to continue running, False to exit.
        """
        cmd = user_input.strip()

        if cmd == "启动系统":
            print(" 系统已就绪，全息投影模块待命。")
            logger.info("系统启动指令已执行")
            return True

        elif cmd == "开发者是谁":
            print(">> [Aura]: 我的缔造者是了不起的 SHEN 女士。")
            logger.info("开发者信息查询")
            return True

        elif cmd in ["退出", "exit", "bye", "再见"]:
            print(">> [Aura]: 再见，Selene 女士。期待下次与您共创艺术。🌌")
            logger.info("收到退出指令")
            return False

        # Newly added common commands (Recommended for extension)
        elif cmd in ["帮助", "help", "?"]:
            print(">> [Aura]: 可用指令：启动系统、开发者是谁、帮助、退出")
            return True

        elif cmd in ["状态", "status"]:
            print(f">> [Aura]: 当前会话ID: {self.current_session_id} | 运行中: {self.is_running}")
            return True

        else:
            # Not a system command, pass to core Agent
            return True

    def _mock_agent_processor(self, user_input: str) -> str:
        """Mock Core Brain (Used during development phase)"""
        logger.info(f"[MOCK Agent] 收到复杂输入: {user_input[:60]}...")
        return f"Aura 正在思考中...（已收到：{user_input}）\n接下来见证全息粒子生命韵动为您呈现更丰富的回应。"

    def process_user_input(self, user_input: str) -> Optional[str]:
        """
        Core method to process a single user input

        Process:
        1. Hand over to check_system_status to determine if it's a system command.
        2. If System Command -> Decide whether to continue based on return value.
        3. If Not System Command -> Forward to core Agent and return the response.
        """
        if not user_input or not user_input.strip():
            return "💫 我在这里，请告诉我你的想法～"

        # Step 1: Handle system commands (Retaining original logic intent)
        should_continue = self.check_system_status(user_input)

        # If system command requests exit, return None (Outer loop will stop)
        if not should_continue:
            return None

        # Step 2: Non-system command -> Log history and forward to core brain
        self.conversation_history.append({"role": "user", "content": user_input})

        try:
            # Call core Agent to process complex semantics
            response = self.agent_processor(user_input)
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            logger.error(f"Agent 处理异常: {e}", exc_info=True)
            return "⚠️ 大脑在思考时遇到了一点小问题... 请再试一次。"

    def run_interactive_loop(self) -> None:
        """
        Main Interaction Loop (Upgraded from the original main() function)

        Features:
        - Long-term operation
        - Supports Ctrl+C for graceful exit
        - Exceptions will not crash the entire program
        """
        self.is_running = True
        print("\n" + "=" * 70)
        print("🌟 Aura 全息数字生命韵动平台 - 对话系统已启动")
        print("    请输入指令开始交互（例如：启动系统、开发者是谁、退出）")
        print("=" * 70)

        try:
            while self.is_running:
                try:
                    user_input = input("\n💬 你： ").strip()

                    if not user_input:
                        continue

                    response = self.process_user_input(user_input)

                    # If response is None, it indicates an exit request
                    if response is None:
                        self.is_running = False
                        break

                    # Display Aura's response
                    if response:
                        print(f"✨ Aura：{response}")

                except KeyboardInterrupt:
                    print("\n\n👋 检测到键盘中断，正在优雅关闭 Aura...")
                    break

                except Exception as e:
                    logger.warning(f"交互循环发生非致命错误: {e}")
                    print("⚠️ 处理输入时出现问题，请重试。")

        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """Graceful shutdown, resource cleanup"""
        if not self.is_running:
            return

        self.is_running = False
        logger.info("DialogueManager 正在进行优雅停机...")

        if self.conversation_history:
            logger.info(f"本次会话共记录 {len(self.conversation_history)} 条对话")

        print("\n🛠️ Aura 系统资源清理完成。感谢你的陪伴！")

    def get_status(self) -> Dict[str, Any]:
        """Returns current system status (for external monitoring)"""
        return {
            "is_running": self.is_running,
            "session_id": self.current_session_id,
            "history_count": len(self.conversation_history),
            "has_real_agent": self.agent_processor is not self._mock_agent_processor
        }


# ====================== Independent Module Entry Point ======================

def main():
    """
    Facilitates direct testing of dialogue_manager.py
    In actual projects, import the DialogueManager class from the main program.
    """
    print("🚀 正在启动 Aura 对话管理模块独立测试模式...\n")

    # Create Dialogue Manager (Temporary Mock, replace with real Agent later)
    dialogue_manager = DialogueManager()

    # Start the interaction loop
    dialogue_manager.run_interactive_loop()


if __name__ == "__main__":
    main()
