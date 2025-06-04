from zlapi import ZaloAPIException
from zlapi.models import *
from datetime import datetime
from config import PREFIX

def handle_infouser_command(message, message_object, thread_id, thread_type, author_id, client):
    msg_error = f"🔴 Something went wrong\n| Không thể lấy thông tin tài khoản Zalo!"
    try:
        if message_object.mentions:
            author_id = message_object.mentions[0]['uid']
        elif message[9:].strip().isnumeric():
            author_id = message[9:].strip()
        elif message.strip() == f"{PREFIX}infouser":
            author_id = author_id
        else:
            client.send(Message(text=msg_error), thread_id, thread_type)
            return
                
        msg = ""
        multistyle = []
        try:
            info = client.fetchUserInfo(author_id)
            info = info.unchanged_profiles or info.changed_profiles
        

            info = info[str(author_id)]
            userId = info.userId or "Undefined"
            msg += f"• User ID: {userId}\n"
            userName = info.zaloName[:30] + "..." if len(info.zaloName) > 30 else info.zaloName
            userName = userName
            msg += f"• User Name: {userName}\n"
            gender = "Male" if info.gender == 0 else "Female" if info.gender == 1 else "Undefined"
            msg += f"• Gender: {gender}\n"
            status = info.status or "Default"
            msg += f"• Bio: {status}\n" 
            business = info.bizPkg.label
            business = "Yes" if business else "No"
            msg += f"• Business: {business}\n" 
            dob = info.dob or info.sdob or "Hidden"
            if isinstance(dob, int):
                dob = datetime.fromtimestamp(dob).strftime("%d/%m/%Y")
            msg += f"• Date Of Birth: {dob}\n" 
            phoneNumber = info.phoneNumber or "Hidden"
            if author_id == self.uid:
                phoneNumber = 'Hidden'
            msg += f"• Phone Number: {phoneNumber}\n" 
                    # Adding Last Action Time
            lastAction = info.lastActionTime
            if isinstance(lastAction, int):
                lastAction = lastAction / 1000
                timeAction = datetime.fromtimestamp(lastAction)
                lastAction = timeAction.strftime("%H:%M %d/%m/%Y")
            else:
                lastAction = "Undefined"
            msg += f"• Last Action At: {lastAction}\n" 
                    
                    # Adding Created Time
            createTime = info.createdTs
            if isinstance(createTime, int):
                createTime = datetime.fromtimestamp(createTime).strftime("%H:%M %d/%m/%Y")
            else:
                createTime = "Undefined"
            msg += f"• Created Time: {createTime}\n"
                    
            msg += f"• Tình trạng: {'✅ Hoạt động' if info.isBlocked == 0 else '🔒 Đã bị khóa'}\n"
                    
            msg += f"• Windows: {'🟢 Kích hoạt' if info.isActivePC == 1 else '🔴 Không kích hoạt'}\n"
                    
            msg += f"• Web: {'🟢 Kích hoạt' if info.isActiveWeb == 1 else '🔴 Không kích hoạt'}\n"
                    
            msg += f"• Avatar: {info.avatar}\n"
                    
            msg += f"• Background: {info.cover}\n"
                    
            msg_to_send = Message(text=msg, style=MultiMsgStyle(multistyle))
            client.replyMessage(msg_to_send, message_object, thread_id, thread_type)
        except ZaloAPIException as e:
            print(f"Error fetching user info: {e}")
    except ZaloAPIException as e:
        error_message = Message(text="Đã xảy ra lỗi")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text="Đã xảy ra lỗi")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'infouser': handle_infouser_command
    }
