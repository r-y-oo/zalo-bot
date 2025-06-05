from config import PREFIX
from zlapi.models import Message

des = {
    'version': "1.0.5",
    'credits': "Nguyễn Đức Tài",
    'description': "check prefix"
}

def prf():
    return PREFIX

def checkprefix(message, message_object, thread_id, thread_type, author_id, client):
    gui = Message(text=f"Prefix của bot là: {prf()}")
    client.replyMessage(gui, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'prefix': checkprefix
    }
    