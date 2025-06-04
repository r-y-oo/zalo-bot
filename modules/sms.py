import datetime,os,subprocess
from zlapi.models import MultiMsgStyle, Mention,MessageStyle
from zlapi.models import Message
import time
des = {
    'version': "1.9.2",
    'credits': "HA HUY HOANG",
    'description': "spam sms"
}
def handle_sms_command(message, message_object, thread_id, thread_type, author_id, client):

        parts = message.split()  

        if len(parts) == 1:
            client.replyMessage(Message(text='🚫Vui lòng nhập số điện thoại sau lệnh .\n'), message_object, thread_id=thread_id, thread_type=thread_type)
            return
        attack_phone_number = parts[1]
        if not attack_phone_number.isnumeric() or len(attack_phone_number) != 10:
            client.replyMessage(Message(text='❌ Số điện thoại không hợp lệ! Vui lòng nhập đúng số.'), message_object, thread_id=thread_id, thread_type=thread_type)
            return
        if attack_phone_number in ['113', '911', '114', '115', '0789305260']:
            client.replyMessage(Message(text="⛔ Số này không thể spam."), message_object, thread_id=thread_id, thread_type=thread_type)
            return
        current_time = datetime.datetime.now()
        if not hasattr(client, "last_sms_times"):
                client.last_sms_times = {}
                last_sent_time = client.last_sms_times[author_id]
                elapsed_time = (current_time - last_sent_time).total_seconds()
                if elapsed_time < 120:
                    client.replyMessage(Message(text="⏳ vui lòng chờ 120s và thử lại!"), message_object, thread_id=thread_id, thread_type=thread_type)
                    return
        client.last_sms_times[author_id] = current_time
        file_path1 = os.path.join(os.getcwd(), "smsv2.py")
        process = subprocess.Popen(["python", file_path1, attack_phone_number, "7"])
        now = datetime.datetime.now()
        time_str = now.strftime("%d/%m/%Y %H:%M:%S")
        masked_phone_number = f"{attack_phone_number[:3]}***{attack_phone_number[-3:]}"
        msg_content = f'''@Member

    bot spam sms và call
 
 ᴘʜᴏɴᴇ :
   ├─> {masked_phone_number} 
   ├─────────────⭔
 ᴛɪᴍᴇ :
   ├─> {time_str} 
   ├─────────────⭔
 ᴄᴏᴏʟᴅᴏᴡɴ :
   ├─> 120
   ├─────────────⭔
 Admin BOT:
   ├─> HA HUY HOANG
   └─────────────⭔

    '''
        mention = Mention(author_id, length=len("@Member"), offset=0)
        color_green = MessageStyle(style="color", color="#4caf50", length=300, offset=0, auto_format=False)
        style = MultiMsgStyle([color_green])
        #sms_img = "sms.png"
        client.replyMessage(Message(text=msg_content, style=style, mention=mention), message_object, thread_id=thread_id, thread_type=thread_type)
def get_mitaizl():
    return {
        'sms': handle_sms_command
    }