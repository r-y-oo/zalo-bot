from zlapi.models import *
import datetime
import os
import subprocess
import time

last_sms_times = {}
admin_ids = ['771784369546632493']

des = {
    'version': "1.0.2",
    'credits': "Duy Khanh",
    'description': "Spam SMS một cách an toàn."
}

def handle_sms_command(message, message_object, thread_id, thread_type, author_id, client):
    if not hasattr(client, "last_sms_times"):
        client.last_sms_times = {}

    parts = message.split()
    if len(parts) < 2:
        client.replyMessage(Message(text='🚫Vui lòng nhập số điện thoại sau lệnh.'), message_object, thread_id=thread_id, thread_type=thread_type)
        return

    attack_phone_number = parts[1]
    if not attack_phone_number.isnumeric() or len(attack_phone_number) != 10:
        client.replyMessage(Message(text='❌Số điện thoại không hợp lệ!'), message_object, thread_id=thread_id, thread_type=thread_type)
        return

    if attack_phone_number in ['113', '911', '114', '115','0789305260' ]:
        client.replyMessage(Message(text="⛔Số này không thể spam.⛔"), message_object, thread_id=thread_id, thread_type=thread_type)
        return

    current_time = datetime.datetime.now()
    last_sent_time = client.last_sms_times.get(author_id)
    if last_sent_time:
        elapsed_time = (current_time - last_sent_time).total_seconds()
        if elapsed_time < 120:
            client.replyMessage(Message(text="⏳Vui lòng chờ 120s và thử lại."), message_object, thread_id=thread_id, thread_type=thread_type)
            return

    client.last_sms_times[author_id] = current_time
    file_path1 = os.path.join(os.getcwd(), "smsv2.py")
    subprocess.Popen(["python", file_path1, attack_phone_number, "120"])
    
    time_str = current_time.strftime("%d/%m/%Y %H:%M:%S")
    masked_phone_number = f"{attack_phone_number[:3]}***{attack_phone_number[-3:]}"
    msg_content = f"""@Member

Bot SMS By Hà Huy Hoàng

ᴘʜᴏɴᴇ 📞:
   ├─> {masked_phone_number} 
   ├─────────────⭔
 ᴛɪᴍᴇ ⏰:
   ├─> {time_str} 
   ├─────────────⭔
 ᴄᴏᴏʟᴅᴏᴡɴ 👾:
   ├─> 120
   ├─────────────⭔
 ᴀᴅᴍɪɴ:
   ├─> Hà Huy Hoàng
   └─────────────⭔
"""
    mention = Mention(author_id, length=len("@Member"), offset=0)
    color_green = MessageStyle(style="color", color="#4caf50", length=300, offset=0, auto_format=False)
    style = MultiMsgStyle([color_green])
    client.replyMessage(Message(text=msg_content.strip(), style=style, mention=mention), message_object, thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {'spamsms': handle_sms_command}
