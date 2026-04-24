import logging
import os
import matplotlib.pyplot as plt
from pythonosc.udp_client import SimpleUDPClient

logger = logging.getLogger(__name__)


class Stereopsis:
    """负责 Aura 的空间深度感知、外部状态(TouchDesigner)投影与多模态数据生成"""

    def __init__(self, ip="127.0.0.1", port=5005):
        self.client = SimpleUDPClient(ip, port)
        # logging setup might need basic config if not done globally
        logging.basicConfig(level=logging.INFO)
        logger.info(f"Stereopsis 立体视觉神经已连接 -> {ip}:{port}")

    def transmit(self, address, value):
        """核心封装：发射 OSC 信号"""
        self.client.send_message(address, value)

    def generate_and_send_chart(self, intent_data=None):
        """生成数据图表并通知 TouchDesigner 切换渲染模式"""
        labels = ['Top 2% Target', 'General Applicant', 'Tier-2 Applicant']
        probabilities = [0.08, 0.04, 0.0001]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, probabilities, color=['#4fc3f7', '#81c784', '#e57373'])
        plt.title('MIT Full-Ride Admission Probability Model', color='white')

        plt.gca().set_facecolor('black')
        plt.gcf().patch.set_facecolor('black')
        plt.gca().tick_params(colors='white')
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')

        # 确保图片保存在当前工作目录下
        chart_path = os.path.abspath("current_chart.png")
        # 转换路径格式，避免 Windows 反斜杠在 OSC 传输中被转义
        chart_path = chart_path.replace('\\', '/')

        plt.savefig(chart_path)
        plt.close()

        # 使用类内部的 transmit 方法发送
        self.transmit("/aura/chart_path", chart_path)
        self.transmit("/aura/show_chart", 1.0)

        logger.info(f"Chart generated and OSC sent: {chart_path}")
