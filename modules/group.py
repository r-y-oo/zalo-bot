from datetime import datetime
from zlapi.models import *




def handle_group(message, message_object, thread_id, thread_type, author_id, bot):
    def get_name(id):
        # print(bot.fetchUserInfo(id))
        return bot.fetchUserInfo(id).changed_profiles[id].zaloName
    msg_error = f"Đã xảy ra lỗi🤧"
    key_translation = {
        'blockName': '\n🚫 Chặn tên nhóm (Không cho phép user đổi tên & ảnh đại diện nhóm)',
        'signAdminMsg': '\n✍️ Ghim (Đánh dấu tin nhắn từ chủ/phó nhóm)',
        'addMemberOnly': '\n👤 Chỉ thêm thành viên (Khi tắt link tham gia nhóm)',
        'setTopicOnly': '\n📝 Cho phép members ghim (tin nhắn, ghi chú, bình chọn)',
        'enableMsgHistory': '\n📜 Bật lịch sử tin nhắn (Cho phép new members đọc tin nhắn gần nhất)',
        'lockCreatePost': '\n🔒 Khóa tạo bài đăng (Không cho phép members tạo ghi chú, nhắc hẹn)',
        'lockCreatePoll': '\n🔒 Khóa tạo cuộc thăm dò (Không cho phép members tạo bình chọn)',
        'joinAppr': '\n✅ Duyệt vào nhóm (Chế độ phê duyệt thành viên)',
        'bannFeature': '\n🚫 Tính năng cấm',
        'dirtyMedia': '\n⚠️ Nội dung nhạy cảm',
        'banDuration': '\n⏳ Thời gian cấm',
        'lockSendMsg': '\n🔒 Khóa gửi tin nhắn',
        'lockViewMember': '\n🔒 Khóa xem thành viên'
    }
    try:
        group = bot.fetchGroupInfo(thread_id).gridInfoMap[thread_id]
        print(group)
        # if not group:
        #     raise ValueError("Thông tin nhóm không tồn tại.")

        # # Check the attributes that could potentially be causing the error
        # print("Debugging group object:", group)
        msg = ""
        msg += f"Thông tin chi tiết nhóm: {group.name}\n"
        msg += f"➡️ Id: {group.groupId}\n"
        msg += f"➡️ Miêu tả: {'Mặc định' if group.desc=='' else group.desc}\n"
        msg += f"➡️ Trưởng nhóm: {get_name(group.creatorId)}\n"
        msg += f"➡️ Phó nhóm: {', '.join([get_name(member) for member in group.adminIds])}\n"
        if group.updateMems:
            update_mems_info = ', '.join([get_name(member) for member in group.updateMems])
        else:
            update_mems_info = ""
        msg += f"➡️ Thanh viên đang chờ duyệt vào nhóm: {update_mems_info}\n"
        memVerList = group.memVerList
        msg += f"➡️ Tổng {group.totalMember} thành viên"
        # print(memVerList)
        # # Tạo danh sách chứa các thông tin thành viên
        # member_info = []
        # for index, member in enumerate(memVerList, start=1):
        #     # Tách ID từ phần tử
        #     id = member.split('_')[0]
        #     print(id)
        #     # Lấy tên dựa trên ID
        #     name = get_name(id)
        #     print(name)
        #     # Thêm thông tin thành viên vào danh sách
        #     member_info.append(f"{index}. {name}")

        # # # Kết hợp tất cả thông tin thành viên thành một chuỗi, phân cách bằng dấu phẩy
        # msg += ', '.join(member_info)#
        createdTime=group.createdTime
        formatted_time = datetime.fromtimestamp(createdTime / 1000).strftime('%H:%M %d/%m/%Y')
        msg += f"\n⏳ Thời gian tạo: {formatted_time}\n"
        setting = group.setting

        #Tạo chuỗi với các thông số cấu hình và dịch sang tiếng Việt
        config_string = ', '.join([f"{key_translation[key]}: {'Bật' if value == 1 else 'Tắt'}" for key, value in setting.items()])
        msg += f"⚙ Cấu hình: {config_string}\n"
        # msg += f"➡️ Ảnh đại diện thu nhỏ: {'Mặc định' if group.avt=='' else group.avt}\n"
        msg += f"➡️ Ảnh đại diện đầy đủ: {'Mặc định' if group.fullAvt=='' else group.fullAvt}\n"

        # Tạo tin nhắn với định dạng
        message = Message(
            text=msg,
            # mention=mention
        )
        bot.replyMessage(message,message_object, thread_id=thread_id, thread_type=thread_type)
        

    except Exception as e:
        print(f"Error: {e}")
        bot.replyMessage(Message(text=msg_error),message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'group': handle_group
    }
