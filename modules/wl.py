import time
import os
import json
import requests
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from threading import Thread
from datetime import datetime
import random

# General description and version information
des = {
    'version': "1.0.3",
    'credits': "Thịnh",
    'description': "làm cc j"
}

colors = [
    "FF9900", "FFFF33", "33FFFF", "FF99FF", "FF3366", 
    "FFFF66", "FF00FF", "66FF99", "00CCFF", "FF0099", 
    "FF0066", "0033FF", "FF9999", "00FF66", "00FFFF", 
    "CCFFFF", "8F00FF", "FF00CC", "FF0000", "FF1100", 
    "FF3300"
]

# Function to handle welcome messages and member departure notifications
def welcome(self, event_data, event_type):
    def send():
        if event_type == GroupEventType.UNKNOWN:
            return

        print(event_data)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d/%m/%Y [%H:%M:%S]")

        thread_id = event_data.get('groupId')
        if not thread_id:
            print("Lỗi: Không tìm thấy 'groupId' trong event_data")
            return

        group_info = self.fetchGroupInfo(thread_id)
        total_members = group_info.get('gridInfoMap', {}).get(thread_id, {}).get('totalMember', 0)

        if not isinstance(total_members, int):
            print("Lỗi: total_members không phải là số nguyên.")
            return

        if event_type == GroupEventType.JOIN:
            group_name = event_data.get('groupName', "nhóm")
            for member in event_data.get('updateMembers', []):
                member_id = member.get('id')
                member_name = member.get('dName')

                welcome_message = f"[ MITAI PROJECT NOTIFICATION GROUP ]\n> Chào mừng: @{member_name}\n> Bạn là thành viên thứ: {total_members}\n> Đã tham gia nhóm: {group_name}."

                color_styles = []
                start_idx = 0
                colors_random = random.sample(colors, k=min(len(colors), 3))  

                for color in colors_random:
                    length = len(welcome_message) // len(colors_random)
                    color_style = MessageStyle(
                        style="color",
                        color=color,
                        offset=start_idx,
                        length=length,
                        auto_format=False
                    )
                    color_styles.append(color_style)
                    start_idx += length

                font_style = MessageStyle(
                    style="font",
                    size="13",  # Đặt kích thước chữ là 13
                    offset=0,
                    length=len(welcome_message),
                    auto_format=False
                )
                multi_style = MultiMsgStyle(color_styles + [font_style])

                try:
                    self.send(Message(text=welcome_message, style=multi_style), thread_id, ThreadType.GROUP)
                except Exception as e:
                    print(f"Lỗi khi gửi tin nhắn: {e}")

        elif event_type in {GroupEventType.LEAVE, GroupEventType.REMOVE_MEMBER}:
            group_name = event_data.get('groupName', "nhóm")
            member_info = event_data.get('updateMembers', [{}])[0]
            member_name = member_info.get('dName', "thành viên")

            if event_type == GroupEventType.LEAVE:
                farewell_message = (
                    f"[ MITAI PROJECT NOTIFICATION GROUP ]\n"
                    f"> {member_name} đã rời khỏi nhóm\n"
                    f"> Nhóm: {group_name}\n"
                    f"> Vào lúc: {formatted_time}\n"
                    f"> Tổng thành viên còn lại: {total_members}"
                )
            else:  # GroupEventType.REMOVE_MEMBER
                farewell_message = (
                    f"[ MITAI PROJECT NOTIFICATION GROUP ]\n"
                    f"> {member_name} bị xóa khỏi nhóm\n"
                    f"> Nhóm: {group_name}\n"
                    f"> Vào lúc: {formatted_time}\n"
                    f"> Tổng thành viên còn lại: {total_members}"
                )

            color_styles = []
            start_idx = 0
            colors_random = random.sample(colors, k=min(len(colors), 3))  

            for color in colors_random:
                length = len(farewell_message) // len(colors_random)
                color_style = MessageStyle(
                    style="color",
                    color=color,
                    offset=start_idx,
                    length=length,
                    auto_format=False
                )
                color_styles.append(color_style)
                start_idx += length

            font_style = MessageStyle(
                style="font",
                size="13", 
                offset=0,
                length=len(farewell_message),
                auto_format=False
            )
            multi_style = MultiMsgStyle(color_styles + [font_style])

            try:
                self.send(Message(text=farewell_message, style=multi_style), thread_id, ThreadType.GROUP)
            except Exception as e:
                print(f"Lỗi khi gửi tin nhắn: {e}")

    thread = Thread(target=send)
    thread.start()

# Function to get event handlers
def get_mitaizl():
    return {
        'wl2': welcome  
    }