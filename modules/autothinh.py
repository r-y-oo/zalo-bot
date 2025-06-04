import time
from zlapi.models import Message, ThreadType
from datetime import datetime, timedelta
import pytz
import threading

# Mô tả của bot
des = {
    'version': "1.0.0",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Dzi x Shin Team"
}

# Các câu thả thính sẽ được gửi vào thời gian định sẵn
time_messages = {
    "01:00": "Em có biết không? Ánh trăng này chỉ đẹp khi có em ở đây cùng anh.",
    "01:30": "Nếu có thể, anh muốn được là người duy nhất em nghĩ đến khi thức dậy.",
    "02:00": "Em là điều tuyệt vời nhất mà anh đã tìm thấy trong cuộc đời này.",
    "02:30": "Mỗi lần nhìn vào mắt em, anh lại quên hết những lo toan trong cuộc sống.",
    "03:00": "Nụ cười của em có thể xua tan mọi ưu phiền trong anh.",
    "03:30": "Nếu em là một ngôi sao, anh sẽ là bầu trời để em luôn tỏa sáng.",
    "04:00": "Cuộc sống của anh sẽ hoàn hảo nếu có em ở bên cạnh.",
    "04:30": "Em là lý do duy nhất khiến anh muốn thức dậy mỗi sáng.",
    "05:00": "Dù ngày có dài đến đâu, chỉ cần có em bên cạnh, mọi thứ sẽ trở nên ngắn lại.",
    "05:30": "Anh sẽ không bao giờ mệt mỏi khi được yêu em.",
    "06:00": "Em chính là lý do mà anh luôn muốn làm người tốt hơn mỗi ngày.",
    "06:30": "Nếu em là một giấc mơ, anh sẽ chẳng bao giờ muốn tỉnh dậy.",
    "07:00": "Chỉ cần có em, thế giới này sẽ trở thành thiên đường của anh.",
    "07:30": "Không gì đẹp bằng ánh sáng trong mắt em, đó là ngọn lửa của tình yêu.",
    "08:00": "Em luôn là người anh tìm kiếm, dù cho bầu trời có thay đổi thế nào đi nữa.",
    "08:30": "Anh không biết lúc nào mình bắt đầu yêu em, chỉ biết là mỗi giây phút bên em đều quý giá.",
    "09:00": "Mỗi lần em cười, trái tim anh lại lỡ nhịp một nhịp.",
    "09:30": "Anh thích cách em làm cho thế giới này trở nên tươi đẹp hơn mỗi ngày.",
    "10:00": "Em là nguồn cảm hứng giúp anh vượt qua mọi khó khăn trong cuộc sống.",
    "10:30": "Tình yêu anh dành cho em giống như một cơn gió, chẳng thể nắm bắt nhưng luôn ở đây.",
    "11:00": "Anh yêu em nhiều hơn cả việc yêu chính mình.",
    "11:30": "Chỉ cần em yêu anh, anh sẽ không sợ gì cả, kể cả những khó khăn phía trước.",
    "12:00": "Em là người duy nhất có thể khiến anh quên đi mọi lo lắng trong cuộc sống này.",
    "12:30": "Anh luôn mong mỗi khoảnh khắc bên em sẽ kéo dài mãi mãi.",
    "13:00": "Nếu em là cơn mưa, anh sẽ là đất để em tưới mát mỗi ngày.",
    "13:30": "Anh chẳng cần gì cả, chỉ cần em ở đây là đủ.", "14:00": "Chắc chắn rằng trái tim anh đã thuộc về em từ lâu rồi, em có biết không?",
    "14:30": "Em làm cho trái tim anh nhảy múa mỗi khi em cười.",
}

# Cấu hình múi giờ Việt Nam
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

def start_auto(client):
    try:
        all_group = client.fetchAllGroups()
        allowed_thread_ids = [gid for gid in all_group.gridVerMap.keys() if gid != '9034032228046851908']

        last_sent_time = None

        while True:
            now = datetime.now(vn_tz)
            current_time_str = now.strftime("%H:%M")

            if current_time_str in time_messages and (last_sent_time is None or now - last_sent_time >= timedelta(minutes=1)):
                message = time_messages[current_time_str]
                for thread_id in allowed_thread_ids:
                    gui = Message(text=f"🌠 [BOT DEXRY PROJECT - AUTOSEND] 🌠\n> {message} 💬")
                    try:
                        # Gửi câu thính dưới dạng văn bản mà không kèm video
                        client.sendMessage(
                            gui,
                            thread_id=thread_id,
                            thread_type=ThreadType.GROUP
                        )
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"Error sending message to {thread_id}: {e}")
                last_sent_time = now

            time.sleep(30)

    except Exception as e:
        print(f"Error: {e}")
        return

def handle_autosend_start(message, message_object, thread_id, thread_type, author_id, client):
    threading.Thread(target=start_auto, args=(client,), daemon=True).start()
    response_message = Message(text="🔱 Hệ thống tự động đã được khởi chạy. Chúc bạn một hành trình vũ trụ tuyệt vời! 🚀")
    client.replyMessage(response_message, message_object, thread_id, thread_type, ttl=12000)

def handle_autosend_off(message, message_object, thread_id, thread_type, author_id, client):
    response_message = Message(text="🛑 Hệ thống tự động đã tạm dừng. Đợi khi bạn sẵn sàng, vũ trụ sẽ tiếp tục trao gửi thông điệp!")
    client.replyMessage(response_message, message_object, thread_id, thread_type, ttl=12000)

def get_mitaizl():
    return {
        'auto_on': handle_autosend_start,
        'auto_off': handle_autosend_off
    }