import matplotlib.pyplot as plt
import os
from pythonosc.udp_client import SimpleUDPClient

# 假设这是你的 OSC 发送端 (基于你现有的代码扩展)
client = SimpleUDPClient("127.0.0.1", 5005)


def generate_and_send_chart(intent_data):
    """
    1. 生成数据图表 (模拟 LLM 经过分析后给出的数据)
    """
    labels = ['Top 2% Target', 'General Applicant', 'Tier-2 Applicant']
    
    probabilities = [0.08, 0.04, 0.0001]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, probabilities, color=['#4fc3f7', '#81c784', '#e57373'])
    plt.title('MIT Full-Ride Admission Probability Model', color='white')

    # 统一样式，配合 Aura 的科幻感
    plt.gca().set_facecolor('black')
    plt.gcf().patch.set_facecolor('black')
    plt.gca().tick_params(colors='white')
    plt.gca().spines['bottom'].set_color('white')
    plt.gca().spines['left'].set_color('white')

    # 2. 保存到绝对路径
    chart_path = os.path.abspath("current_chart.png")
    plt.savefig(chart_path)
    plt.close()

    # 3. 通过 OSC 告诉 TouchDesigner 发生了状态变化
    # 发送图片路径 (字符串类型)
    client.send_message("/aura/chart_path", chart_path)
    # 发送显示图表的触发指令 (1代表显示图表，0代表显示粒子)
    client.send_message("/aura/show_chart", 1.0)

    print(f"Chart generated and OSC sent: {chart_path}")
