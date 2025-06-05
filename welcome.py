import time
import os
import json
import requests
from colorama import Fore
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from threading import Thread
from datetime import datetime

def welcome(self, event_data, event_type):
    def send():
        if event_type == GroupEventType.UNKNOWN:
            return

        print(event_data)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d/%m/%Y [%H:%M:%S]")
        thread_id = event_data['groupId']
        group_info = self.fetchGroupInfo(thread_id)

        # Get total members in the group
        total_members = group_info.gridInfoMap.get(thread_id, {}).get('totalMember', 0)

        # Initialize message styles
        default_style = MessageStyle(offset=0, length=3000, style='font', size='15', auto_format=False)

        if event_type == GroupEventType.JOIN:
            group_name = event_data.groupName
            for i, member in enumerate(event_data.updateMembers):
                member_id = member['id']
                member_name = member['dName']
                text = f'🪂 Hello! \n'
                text += 'Bot By Duy Khanh! \n'
                text += f'• Xin Chào @{member_name} đến với {group_name}, Group💤.\n\n'
                text += f'| ☃️Member thứ {total_members + i + 0} của nhóm.'  # Adjust the count

                # Message styles
                message_styles = [
                    default_style,
                    MessageStyle(offset=0, length=19, style='bold', auto_format=False),
                    MessageStyle(offset=20, length=len(text) - 20, style='color', color='ced6f0', auto_format=False)
                ]

                msg = Message(text=text, style=MultiMsgStyle(message_styles))
                self.send(msg, thread_id, ThreadType.GROUP, ttl=30000)

        elif event_type in {GroupEventType.LEAVE, GroupEventType.REMOVE_MEMBER}:
            group_name = event_data.groupName
            for member in event_data.updateMembers:
                member_id = member['id']
                member_name = member['dName']
                text = f'bai 👋🏻 Tạm biệt\n'
                text += 'Bot By Duy Khanh \n'
                text += f'• @{member_name}Out Group{group_name} '

                # Message styles
                message_styles = [
                    default_style,
                    MessageStyle(offset=0, length=12, style='bold', auto_format=False),
                    MessageStyle(offset=13, length=len(member_name), style='color', color='f9b387', auto_format=False),
                    MessageStyle(offset=22, length=len(text) - 22, style='color', color='ced6f0', auto_format=False)
                ]

                msg = Message(text=text, style=MultiMsgStyle(message_styles))
                self.send(msg, thread_id, ThreadType.GROUP, ttl=30000)

    thread = Thread(target=send)
    thread.start()

def get_mitaizl():
    return {
        'welcome': welcome  # Ensure the welcome function is correctly assigned
    }