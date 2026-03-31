"""
interaction/dialogue_manager.py

Aura 全息数字生命与交互平台 - 对话管理模块（前台接待员）

模块职责（单一职责原则 SRP）：
    - 接收用户输入（文字、未来可扩展为语音/手势）
    - 识别并处理基础系统指令（启动、退出、开发者信息等）
    - 维持长效交互循环
    - 将复杂对话内容转发给核心大脑 core/agent.py 处理
    - 提供优雅停机和错误处理机制

作者：为美术跨学科研究者设计的通俗易懂版
基于 Legacy Code 重构：保留了 check_system_status 的核心意图，并升级为 OOP 架构
"""

from typing import Callable, Optional, Dict, Any
import sys
import logging
from datetime import datetime

# 配置日志，方便观察系统运行过程
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | [DialogueManager] %(message)s'
)
logger = logging.getLogger(__name__)


class DialogueManager:
    """
    Aura 对话管理器 - 前台交互核心类

    像一位专业的接待员：
    - 听到简单指令（启动、退出、开发者是谁）就自己处理
    - 听到复杂内容就转交给「大脑」（core/agent.py）
    - 负责整个对话的开始、维持和优雅结束
    """

    def __init__(self, agent_processor: Optional[Callable[[str], str]] = None):
        """
        初始化对话管理器

        Args:
            agent_processor: 核心大脑的处理函数（来自 core/agent.py）
                             如果不传，则使用 Mock 版本，方便单独测试这个模块
        """
        self.is_running: bool = False
        self.current_session_id: str = self._generate_session_id()
        self.conversation_history: list[Dict[str, str]] = []

        # 核心大脑接口（解耦关键）
        self.agent_processor = agent_processor or self._mock_agent_processor

        logger.info(f"DialogueManager 初始化完成 | 会话ID: {self.current_session_id}")

    def _generate_session_id(self) -> str:
        """生成唯一会话ID，用于追踪每次交互"""
        return f"aura_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # ====================== Legacy Code 升级部分 ======================

    def check_system_status(self, user_input: str) -> bool:
        """
        【升级版】系统指令处理函数

        直接基于你之前写的 check_system_status 进行重构，
        保留了相同的指令意图，同时增加了更多友好提示和日志。
        返回 True 表示继续运行，False 表示应该退出。
        """
        cmd = user_input.strip()

        if cmd == "启动系统":
            print(" 系统已就绪，全息投影模块待命。")
            logger.info("系统启动指令已执行")
            return True

        elif cmd == "开发者是谁":
            print(">> [Aura]: 我的造物主是了不起的 SHEN 女士。")
            logger.info("开发者信息查询")
            return True

        elif cmd in ["退出", "exit", "bye", "再见"]:
            print(">> [Aura]: 再见，Selene 女士。期待下次与您共创艺术。🌌")
            logger.info("收到退出指令")
            return False

        # 新增常用指令（推荐扩展）
        elif cmd in ["帮助", "help", "?"]:
            print(">> [Aura]: 可用指令：启动系统、开发者是谁、帮助、退出")
            return True

        elif cmd in ["状态", "status"]:
            print(f">> [Aura]: 当前会话ID: {self.current_session_id} | 运行中: {self.is_running}")
            return True

        else:
            # 非系统指令，交给核心 Agent 处理
            return True

    def _mock_agent_processor(self, user_input: str) -> str:
        """Mock 核心大脑（开发阶段使用）"""
        logger.info(f"[MOCK Agent] 收到复杂输入: {user_input[:60]}...")
        return f"Aura 正在思考中...（已收到：{user_input}）\n接下来见证全息粒子生命韵动为您呈现更丰富的回应。"

    def process_user_input(self, user_input: str) -> Optional[str]:
        """
        处理单条用户输入的核心方法

        流程：
        1. 先交给 check_system_status 判断是否为系统指令
        2. 如果是系统指令 → 根据返回值决定是否继续运行
        3. 如果不是系统指令 → 转发给核心 Agent 处理，并返回回复内容
        """
        if not user_input or not user_input.strip():
            return "💫 我在这里，请告诉我你的想法～"

        # 第一步：处理系统指令（保留你原来的逻辑意图）
        should_continue = self.check_system_status(user_input)

        # 如果系统指令要求退出，则直接返回 None（上层循环会停止）
        if not should_continue:
            return None

        # 第二步：非系统指令 → 记录历史并交给核心大脑
        self.conversation_history.append({"role": "user", "content": user_input})

        try:
            # 调用核心 Agent 处理复杂语义
            response = self.agent_processor(user_input)
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            logger.error(f"Agent 处理异常: {e}", exc_info=True)
            return "⚠️ 大脑在思考时遇到了一点小问题... 请再试一次。"

    def run_interactive_loop(self) -> None:
        """
        主交互循环（升级自原来的 main() 函数）

        特点：
        - 长效运行
        - 支持 Ctrl+C 优雅退出
        - 异常不会导致整个程序崩溃
        """
        self.is_running = True
        print("\n" + "=" * 70)
        print("🌟 Aura 全息数字生命律动平台 - 对话系统已启动")
        print("   请输入指令开始交互（例如：启动系统、开发者是谁、退出）")
        print("=" * 70)

        try:
            while self.is_running:
                try:
                    user_input = input("\n💬 你： ").strip()

                    if not user_input:
                        continue

                    response = self.process_user_input(user_input)

                    # 如果返回 None，说明需要退出
                    if response is None:
                        self.is_running = False
                        break

                    # 显示 Aura 的回复
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
        """优雅停机，清理资源"""
        if not self.is_running:
            return

        self.is_running = False
        logger.info("DialogueManager 正在进行优雅停机...")

        if self.conversation_history:
            logger.info(f"本次会话共记录 {len(self.conversation_history)} 条对话")

        print("\n🛠️ Aura 系统资源清理完成。感谢你的陪伴！")

    def get_status(self) -> Dict[str, Any]:
        """返回当前系统状态（便于外部监控）"""
        return {
            "is_running": self.is_running,
            "session_id": self.current_session_id,
            "history_count": len(self.conversation_history),
            "has_real_agent": self.agent_processor is not self._mock_agent_processor
        }


# ====================== 模块独立运行入口 ======================

def main():
    """
    方便你直接运行测试 dialogue_manager.py
    实际项目中，你可以从主程序导入 DialogueManager 类使用
    """
    print("🚀 正在启动 Aura 对话管理模块独立测试模式...\n")

    # 创建对话管理器（暂时使用 Mock，后续替换为真实 Agent）
    dialogue_manager = DialogueManager()

    # 启动交互循环
    dialogue_manager.run_interactive_loop()


if __name__ == "__main__":
    main()
