import threading
import random
from zlapi.models import Message

# Module metadata
des = {
    'version': "1.0.0",
    'credits': "Trung Trí",
    'description': "Tự động thả biểu cảm ngẫu nhiên vào tin nhắn."
}

# Hàm xử lý lệnh icon
def handle_icon_command(message, message_object, thread_id, thread_type, author_id, client):
    # Danh sách các biểu cảm
    reaction_all = [
        "💐", "🌸", "❄️", "🍀", "🪵", "🌲", "🌅", "🌄", "🏖️", "🏞️", 
        "⛈️", "🌩️", "🌨️", "☁️", "💧", "☔", "⚡", "🌪️", "🌌", 
        "🐷", "🐮", "💟", "🦊", "🐼", "🎃", "🐳", "🐟", "🐠", 
        "🐋", "🐬", "♨️", "💢", "🔆"
    ]

    def send_reaction():
        try:
            # Chọn biểu cảm ngẫu nhiên từ danh sách
            reaction_icon = random.choice(reaction_all)
            # Gửi biểu cảm đến tin nhắn
            client.sendReaction(message_object, reaction_icon, thread_id, thread_type)
            print(f"🌟 Đã thả biểu cảm '{reaction_icon}' vào tin nhắn.")
        except Exception as e:
            print(f"🚦 Lỗi khi thả biểu cảm: {e}")

    # Chạy việc gửi biểu cảm trong một thread
    threading.Thread(target=send_reaction).start()

# Đăng ký lệnh vào module
def get_mitaizl():
    return {
        'icon': handle_icon_command  # Tên lệnh là 'icon'
    }
