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

        # Initialize message styles with better font size
        default_style = MessageStyle(offset=0, length=5000, style='font', size='16', auto_format=False)

        if event_type == GroupEventType.JOIN:
            group_name = event_data.groupName
            for i, member in enumerate(event_data.updateMembers):
                member_id = member['id']
                member_name = member['dName']
                
                # Beautiful welcome message with enhanced design
                text = f'╭─────────────────────╮\n'
                text += f'│  🎉 CHÀO MỪNG! 🎉   │\n'
                text += f'╰─────────────────────╯\n\n'
                text += f'🌟 Xin chào @{member_name}! 🌟\n\n'
                text += f'🏠 Chào mừng bạn đến với:\n'
                text += f'📝 {group_name}\n\n'
                text += f'─────────────────────\n'
                text += f'🎯 Bạn là thành viên thứ {total_members + i} của nhóm!\n'
                text += f'👥 Tổng cộng: {total_members + i} thành viên\n'
                text += f'⏰ Thời gian: {formatted_time}\n'
                text += f'─────────────────────\n\n'
                text += f'🤖 Bot được phát triển bởi: Duy Khanh\n'
                text += f'💝 Chúc bạn có những trải nghiệm tuyệt vời!\n\n'
                text += f'🎊 Hãy tham gia và thỏa sức vui chơi! 🎊'

                # Enhanced message styles for better visual appeal
                message_styles = [
                    default_style,
                    # Header box styling
                    MessageStyle(offset=0, length=70, style='color', color='00d4ff', auto_format=False),
                    MessageStyle(offset=0, length=70, style='bold', auto_format=False),
                    
                    # Welcome message styling
                    MessageStyle(offset=72, length=25, style='color', color='ffb347', auto_format=False),
                    MessageStyle(offset=72, length=25, style='bold', auto_format=False),
                    
                    # Group name styling
                    MessageStyle(offset=120, length=len(group_name), style='color', color='87ceeb', auto_format=False),
                    MessageStyle(offset=120, length=len(group_name), style='italic', auto_format=False),
                    
                    # Member count styling
                    MessageStyle(offset=text.find('Bạn là thành viên'), length=50, style='color', color='98fb98', auto_format=False),
                    
                    # Bot info styling
                    MessageStyle(offset=text.find('Bot được phát triển'), length=40, style='color', color='dda0dd', auto_format=False),
                    
                    # Final message styling
                    MessageStyle(offset=text.find('Hãy tham gia'), length=35, style='color', color='ffd700', auto_format=False),
                    MessageStyle(offset=text.find('Hãy tham gia'), length=35, style='bold', auto_format=False)
                ]

                msg = Message(text=text, style=MultiMsgStyle(message_styles))
                self.send(msg, thread_id, ThreadType.GROUP, ttl=30000)

        elif event_type in {GroupEventType.LEAVE, GroupEventType.REMOVE_MEMBER}:
            group_name = event_data.groupName
            for member in event_data.updateMembers:
                member_id = member['id']
                member_name = member['dName']
                
                # Beautiful goodbye message
                text = f'╭─────────────────────╮\n'
                text += f'│  👋 TẠM BIỆT! 😢    │\n'
                text += f'╰─────────────────────╯\n\n'
                text += f'💔 @{member_name} đã rời khỏi nhóm\n\n'
                text += f'🏠 Nhóm: {group_name}\n'
                text += f'⏰ Thời gian: {formatted_time}\n'
                text += f'👥 Còn lại: {total_members - 1} thành viên\n\n'
                text += f'─────────────────────\n'
                text += f'🌟 Cảm ơn bạn đã tham gia cùng chúng tôi!\n'
                text += f'💝 Chúc bạn luôn vui vẻ và hạnh phúc!\n'
                text += f'🚪 Cửa nhóm luôn mở chào đón bạn trở lại!\n\n'
                text += f'🤖 Bot By: Duy Khanh'

                # Enhanced goodbye message styles
                message_styles = [
                    default_style,
                    # Header box styling
                    MessageStyle(offset=0, length=70, style='color', color='ff6b6b', auto_format=False),
                    MessageStyle(offset=0, length=70, style='bold', auto_format=False),
                    
                    # Member name styling
                    MessageStyle(offset=text.find('@'), length=len(member_name), style='color', color='ffa07a', auto_format=False),
                    MessageStyle(offset=text.find('@'), length=len(member_name), style='bold', auto_format=False),
                    
                    # Group info styling
                    MessageStyle(offset=text.find('Nhóm:'), length=len(group_name) + 10, style='color', color='87ceeb', auto_format=False),
                    
                    # Farewell message styling
                    MessageStyle(offset=text.find('Cảm ơn bạn'), length=80, style='color', color='dda0dd', auto_format=False),
                    
                    # Bot signature styling
                    MessageStyle(offset=text.find('Bot By:'), length=20, style='color', color='98fb98', auto_format=False)
                ]

                msg = Message(text=text, style=MultiMsgStyle(message_styles))
                self.send(msg, thread_id, ThreadType.GROUP, ttl=30000)

    thread = Thread(target=send)
    thread.start()

def get_mitaizl():
    return {
        'welcome': welcome  # Ensure the welcome function is correctly assigned
    }