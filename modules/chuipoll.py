from zlapi.models import *
import os
import time
import threading
from zlapi.models import MessageStyle
from config import ADMIN

is_reo_running = False

des = {
    'version': "1.0.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Chửi chết cụ 1 con chó"
}

def stop_reo(client, message_object, thread_id, thread_type):
    global is_reo_running
    is_reo_running = False

def handle_chuipoll_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_reo_running

    if author_id not in ADMIN:
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_reo_running:
            return
        else:
            stop_reo(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        return

    try:
        with open("name.txt", "r", encoding="utf-8") as file:
            Ngon = file.readlines()
    except FileNotFoundError:
        return

    if not Ngon:
        return

    is_reo_running = True

    def reo_loop():
        while is_reo_running:
            for noidung in Ngon:
                if not is_reo_running:
                    break
                client.createPoll(
                    question=noidung.strip(),
                    options=noidung.strip(),
                    groupId=thread_id,
                    expiredTime=0,
                    pinAct=True,
                    multiChoices=True,
                    allowAddNewOption=True,
                    hideVotePreview=True,
                    isAnonymous=True
                )
                time.sleep(0.1)

    reo_thread = threading.Thread(target=reo_loop)
    reo_thread.start()

def get_mitaizl():
    return {
        'warpoll': handle_chuipoll_command
    }