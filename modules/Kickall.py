import random
import threading
import time
import json
import re
from zlapi import *
from zlapi.models import *
from config import ADMIN  # Thêm import ADMIN từ config.py
#DzixMode
#Cút Nhé
author = (
    "👨‍💻 Tác giả: Dminh ☠️\n"
    "🔄 Cập nhật: 02-12-24\n"
    "🚀 Tính năng: Tính năng đi var\n"
)

def kick_all_member_group(message, message_object, thread_id, thread_type, author_id, bot):
    # Kiểm tra xem người dùng có phải là admin không
    if author_id not in ADMIN:
        return  # Không thông báo khi người dùng không có quyền

    # Lấy thông tin nhóm
    group = bot.fetchGroupInfo(thread_id).gridInfoMap[thread_id]
    
    # Lấy danh sách admin (bao gồm cả creatorId)
    admin_ids = group.adminIds.copy()
    if group.creatorId not in admin_ids:
        admin_ids.append(group.creatorId)
    
    # Lấy danh sách thành viên nhóm
    list_mem_group = set([member.split('_')[0] for member in group["memVerList"]])

    # Loại trừ các admin và creator khỏi danh sách bị kick
    list_mem_group_to_kick = list_mem_group - set(admin_ids)

    # Thực hiện kick các thành viên không phải admin
    for uid in list_mem_group_to_kick:
        bot.blockUsersInGroup(uid, thread_id)
        bot.kickUsersInGroup(uid, thread_id)
     # Hàm gọi lệnh
def get_mitaizl():
    return {
        'lungu': kick_all_member_group
    }