import logging
from pythonosc.udp_client import SimpleUDPClient

logger = logging.getLogger(__name__)

class Stereopsis:
    """负责 Aura 的空间深度感知与外部状态(TouchDesigner)投影"""

    def __init__(self, ip="127.0.0.1", port=5005):
        self.client = SimpleUDPClient(ip, port)
        logger.info(f"Stereopsis 立体视觉神经已连接 -> {ip}:{port}")

    def transmit(self, address, value):
        """核心封装：发射 OSC 信号"""
        self.client.send_message(address, value)
