# ⬡ Project Aura: Holographic AI & HCI Research Platform
> **基于跨学科视角的全息数字生命与人机交互框架**

## 🧬 项目愿景 (Project Vision)
**Aura** 不仅仅是一个 AI 助手，它是一个探索**具身智能 (Embodied AI)**、**生成式艺术 (Generative Art)** 与**空间计算 (Spatial Computing)** 融合边界的实验性平台。

作为一名拥有美术学与心理学背景的开发者，本项目试图打破传统 GUI（图形用户界面）的冰冷感，利用传统的“佩珀尔幻象 (Pepper's Ghost)”光学原理，结合现代计算机视觉与大语言模型，赋予数字代码以“情绪感知”与“物理形态”。

## 🏗️ 系统架构 (System Architecture)
本平台采用高度解耦的模块化设计，以支持未来多模态交互的无缝接入：

* 🧠 **`core/` (认知中枢)**：AI 的大脑模块。包含决策系统 (`agent.py`) 与长短期记忆网络，负责处理复杂逻辑与意图生成。
* 👁️ **`perception/` (感知系统)**：AI 的五官。预留多模态传感器接口，包括计算机视觉（手势/人脸追踪）与音频环境识别。
* 🗣️ **`interaction/` (交互层)**：连接人与 AI 的桥梁。处理对话管理 (`dialogue_manager.py`) 与多模态控制逻辑。
* 🎨 **`rendering/` (显示与渲染)**：Aura 的视觉表现层。通过 Python 驱动 Blender API (`particles.py`)，实现从静态网格到高密度动态粒子云（星尘形态）的程序化视觉生成。
* 🌌 **`spatial/` & `hardware/` (空间与物理映射)**：负责全息投影设备的校准、深度估计与虚拟锚点追踪。

## 🛠 开发方法论 (AI-Augmented Methodology)
本项目实践了前瞻性的 **AI 协同开发 (AI-Augmented Development)** 范式。
面对艺术与代码的跨学科壁垒，本人专注于**系统架构设计**、**心理学动机建模**与 **CMF（色彩/材质/细节）视觉调优**，并利用大语言模型辅助完成复杂的代码封装与底层调试，实现从艺术构思到工程落地的全流程闭环。

## 🚀 当前进展与研发日志 (Milestones & DevLog)
* **[Phase 1] 视觉协议确立 (Visual Protocol)**：成功在 `rendering/particles.py` 中实现了基于 Blender API 的粒子转换协议。将几何体转化为 8000+ 粒子的能量场，并完成了辉光 (Bloom) 参数的极客级调优。
* **[Phase 1] 核心交互雏形 (Interaction Logic)**：在 `interaction/` 模块下构建了基础的状态机与对话解析引擎。
* **[Phase 1] 智能中枢集成 (Brain Integration) —— *NEW!***：
    * **架构升级**：成功接入 **OpenRouter API**，重构了核心大脑 `core/agent.py`。
    * **人格塑造**：确立了 Aura “极简、温暖、深邃”的智者人格，支持自然语言的高级共情与逻辑穿透。

## 🔮 未来演进 (Roadmap)
- [ ] 接入视觉感知 (`perception/vision`)，实现基于手势的全息粒子互动。
- [ ] 结合心理学认知模型，优化 `core/` 中的性格模拟与情绪反馈机制。
- [ ] 搭建线下 Pepper's Ghost 物理倒金字塔投影装置，完成“虚实融合”。

---
> *"Art defines the soul, HCI designs the behavior, and Code builds the nervous system."*
