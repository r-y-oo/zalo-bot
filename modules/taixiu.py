from zlapi.models import Message
from PIL import Image
import os
import random
import time

users = {}
command_last_used = {}
command_usage_count = {}
# received_messages = []

des = {
    'version': "1.0.2",
    'credits': "dzi",
    'description': "txiu dangky/dangnhap"
}
def load_users():
    if os.path.exists('tt.txt'):
        try:
            with open('tt.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        user_id, username, password, balance, wins, losses, used_codes = parts
                        users[user_id] = {
                            "username": username,
                            "password": password,
                            "balance": int(balance),
                            "wins": int(wins),
                            "losses": int(losses),
                            "used_codes": set(used_codes.split(',')) if used_codes else set()
                        }
        except Exception as e:
            print(f"Error loading tt.txt: {e}")

def save_users():
    with open('tt.txt', 'w') as f:
        for user_id, user_info in users.items():
            used_codes = ','.join(user_info["used_codes"])
            f.write(f"{user_id}|{user_info['username']}|{user_info['password']}|{user_info['balance']}|{user_info['wins']}|{user_info['losses']}|{used_codes}\n")

def format_currency(amount):
    return '{:,.0f} VNĐ'.format(amount).replace(',', '.')

def get_user_name(user_id):
    if user_id in users:
        return users[user_id]["username"]
    else:
        return f"Người dùng {user_id}"
    
def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

def determine_result(total):
    if total <= 10:
        return 'Xỉu'
    elif total >= 11:
        return 'Tài'

def check_cooldown(command, author_id, cooldown_period=10):
    current_time = time.time()
    if author_id in command_last_used and command in command_last_used[author_id]:
        last_used_time = command_last_used[author_id][command]
        if current_time - last_used_time < cooldown_period:
            return True, cooldown_period - (current_time - last_used_time)
    return False, 0

def update_command_usage(command, author_id):
    current_time = time.time()
    if author_id not in command_last_used:
        command_last_used[author_id] = {}
    command_last_used[author_id][command] = current_time
    
    if author_id not in command_usage_count:
        command_usage_count[author_id] = {}
    if command not in command_usage_count[author_id]:
        command_usage_count[author_id][command] = 0
    command_usage_count[author_id][command] += 1

# def send_dice_images(dice, thread_id, thread_type, client):
#     # Lấy đường dẫn đến thư mục chứa file hiện tại
#     current_dir = os.path.dirname(__file__)
#     image_paths = []
    
#     for die in dice:
#         # Tạo đường dẫn tới ảnh xí ngầu
#         image_path = os.path.join(current_dir, 'dice_images', f'{die}.png')
        
#         if os.path.exists(image_path):
#             image_paths.append(image_path)
#         else:
#             print(f"Image not found: {image_path}")

#     if image_paths:
#         client.sendMultiLocalImage(
#             imagePathList=image_paths,
#             thread_id=thread_id,
#             thread_type=thread_type
#             # width=1200,
#             # height=1600
#         )
def create_dice_image(dice):
    # Lấy đường dẫn đến thư mục chứa file hiện tại
    current_dir = os.path.dirname(__file__)
    
    dice_images = []
    for die in dice:
        image_path = os.path.join(current_dir, 'dice_images', f'{die}.png')
        if os.path.exists(image_path):
            dice_images.append(Image.open(image_path))
        else:
            print(f"Image not found: {image_path}")
            return None
    
    if len(dice_images) == 3:
        # Giả sử các ảnh có kích thước giống nhau
        width, height = 480, 480
        total_width = width * 3  # Ảnh cuối sẽ có chiều rộng bằng ba lần chiều rộng một ảnh
        combined_image = Image.new('RGB', (total_width, height))
        
        # Dán ba ảnh xí ngầu vào ảnh mới
        for i, dice_img in enumerate(dice_images):
            combined_image.paste(dice_img, (i * width, 0))
        
        # Lưu ảnh gộp này vào một tệp tạm
        output_image_path = os.path.join(current_dir, 'combined_dice.png')
        combined_image.save(output_image_path)
        
        return output_image_path
    else:
        print("Không đủ ảnh xí ngầu để gộp.")
        return None


def handle_taixiu_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        # group_name = fetchGroupName(thread_id)
        # if group_name != client.allowed_group_name:
        #     return
        load_users()
        user_name = get_user_name(author_id)
        if not isinstance(message, str):
            print(f"Loại tin nhắn không mong đợi: {type(message)}")
            return
        query = message.strip().split()
        help_text = (
                f"📜 **Danh sách lệnh:**\n"
                f"➟ `!txiu dangky (tên) (mật khẩu)`: Đăng ký người dùng và nhận 100.000 VNĐ 🎉\n"
                f"➟ `!txiu dangnhap (tên) (mật khẩu)`: Đăng nhập người dùng 🔐\n"
                # f"➟ `-taixiu play (số tiền) (T/X)`: Chơi tài xỉu 🎲\n"
                f"➟ `!txiu (t/x/tài/xỉu) (số tiền)`: Chơi tài xỉu 🎲\n"
                f"➟ `!txiu sodu`: Kiểm tra số dư hiện có 💵\n"
                f"➟ `!txiu doipass (mật khẩu mới)`: Thay đổi mật khẩu của bạn 🔑\n"               
                f"➟ `!txiu bxh`: Hiển thị bảng xếp hạng 10 người giàu nhất 🏆\n"
                f"➟ `!txiu ct (tên người nhận) (số tiền)`: Chuyển tiền cho người khác 💸\n"
                f"➟ `!txiu code (mã)`: Nhập mã để nhận tiền thưởng 🎁\n"
        )
        if len(query) < 2:
            client.sendMessage(Message(text=help_text), thread_id, thread_type)
            return
        command = query[1].lower()
        if command == 'dangky':
            if len(query) != 4:
                client.sendMessage(Message(text=f"{user_name} ❌ Cú pháp không hợp lệ. Vui lòng dùng lệnh `-taixiu dangky (tên) (mật khẩu)`."), thread_id, thread_type)
                return
            username = query[2]
            password = query[3]
            if username and password:
                if author_id not in users:
                    users[author_id] = {"username": username, "balance": 100000, "password": password, "wins": 0, "losses": 0, "used_codes": set()}
                    formatted_balance = format_currency(users[author_id]["balance"])
                    client.sendMessage(Message(text=f"{user_name} 🎉 Đăng ký thành công! {username} đã nhận {formatted_balance}."), thread_id, thread_type)
                    save_users()
                else:
                    client.sendMessage(Message(text=f"{user_name} ⚠️ Bạn đã đăng ký rồi."), thread_id, thread_type)
            else:
                client.sendMessage(Message(text=f"{user_name} ⚠️ Vui lòng cung cấp tên và mật khẩu."), thread_id, thread_type)
        elif command == 'dangnhap':
            if len(query) != 4:
                client.sendMessage(Message(text=f"{user_name} ❌ Cú pháp không hợp lệ. Vui lòng dùng lệnh `-taixiu dangnhap (tên) (mật khẩu)`."), thread_id, thread_type)
                return
            username = query[2]
            password = query[3]
            user_id = next((uid for uid, data in users.items() if data["username"] == username), None)
            if user_id and users[user_id]["password"] == password:
                client.sendMessage(Message(text=f"{user_name} 🎉 Đăng nhập thành công! Chào mừng trở lại, {username}."), thread_id, thread_type)
            else:
                client.sendMessage(Message(text=f"{user_name} ❌ Tên hoặc mật khẩu không đúng."), thread_id, thread_type)
            
        elif command == 'doipass':
            if len(query) != 3:
                client.sendMessage(Message(text=f"{user_name} ❌ Cú pháp không hợp lệ. Vui lòng dùng lệnh `-taixiu doipass (mật khẩu mới)`."), thread_id, thread_type)
                return

            new_password = query[2]
            
            if author_id not in users:
                client.sendMessage(Message(text=f"{user_name} ⚠️ Bạn cần đăng ký và đăng nhập để thay đổi mật khẩu."), thread_id, thread_type)
                return

            # Update the password
            users[author_id]["password"] = new_password
            save_users()
            client.sendMessage(Message(text=f"{user_name} 🔑 Bạn đã thay đổi mật khẩu thành công."), thread_id, thread_type)

        elif command == 'sodu':
            if author_id not in users:
                client.sendMessage(Message(text=f"{user_name} ⚠️ Bạn cần đăng ký và đăng nhập để kiểm tra số dư."), thread_id, thread_type)
                return

            formatted_balance = format_currency(users[author_id]["balance"])
            client.sendMessage(Message(text=f"{user_name} 💰 Số dư hiện tại của bạn: {formatted_balance}."), thread_id, thread_type)

        # elif command == 'play':
        elif command in ['t', 'x', 'tài', 'xỉu']:
            cooldown_period = 5  # Đặt thời gian đợi khi bị cooldown
            cooldown_required, time_left = check_cooldown("-taixiu", author_id, cooldown_period)
            if cooldown_required:
                client.sendMessage(Message(text=f"{user_name} ⏳ Bạn đã sử dụng lệnh `-taixiu` quá 2 lần. Vui lòng đợi {int(time_left)} giây để dùng lại."), thread_id, thread_type)
                return
            # if len(query) != 4:
            if len(query) != 3:
                client.sendMessage(Message(text=f"{user_name} ❌ Cú pháp không hợp lệ. Vui lòng dùng lệnh `-taixiu (t/x/tài/xỉu) (số tiền)`."), thread_id, thread_type)
                return
            try:
                bet_amount = int(query[2])
                # bet_choice = query[3].upper()
                bet_choice = query[1].upper()
            except ValueError:
                client.sendMessage(Message(text=f"{user_name} ❌ Số tiền không hợp lệ."), thread_id, thread_type)
                return
            # if bet_choice not in ['T', 'X']:
            #     client.sendMessage(Message(text=f"{user_name} ❌ Lựa chọn không hợp lệ. Sử dụng `T` cho Tài, `X` cho Xỉu, `H` cho Hoà."), thread_id, thread_type)
            #     return
            if author_id not in users:
                client.sendMessage(Message(text=f"{user_name} ⚠️ Bạn cần đăng ký và đăng nhập để chơi tài xỉu."), thread_id, thread_type)
                return
            if users[author_id]["balance"] < bet_amount:
                client.sendMessage(Message(text=f"{user_name} ❌ Số dư không đủ để cược {format_currency(bet_amount)}."), thread_id, thread_type)
                return
            update_command_usage("-taixiu", author_id)
            dice = roll_dice()
            total = sum(dice)
            result = determine_result(total)
            formatted_dice = ' + '.join(map(str, dice))
            formatted_total = format_currency(total)

            current_dir = os.path.dirname(__file__)
            gif_path = os.path.join(current_dir, 'dice_images', f'xingau.gif')

            client.sendMessage(Message(text=f"Đang lăc..."), thread_id, thread_type, ttl=5000)
            gif_response = client.sendLocalGif(
                gifPath=gif_path,
                thumbnailUrl="https://i.imgur.com/lV7QJp9.jpeg",
                thread_id=thread_id,
                thread_type=thread_type,
                width=800,
                height=466,
                ttl=5000
            )
            time.sleep(5)
            # Đợi 3 giây
            # time.sleep(3)

            # Lấy msgId từ gif_response
            # gif_msg_id = gif_response.msgId

            # Giả sử messages là danh sách các message_object đã lưu
            # received_messages = []
            # messages = [
            #     # Thêm các message_object đã lưu ở đây
            #     Message(msgId='5854648152499', cliMsgId='1726940888459', ...),
            #     Message(msgId='123456789', cliMsgId='987654321', ...),
            #     # ...
            # ]
            # received_messages.append(message_object)

            # # Dò tìm message_object với msgId trùng khớp
            # matching_message = None
            # for message_object2 in received_messages:
            #     print(f"ABCD: {message_object2.msgId}")
            #     print(f"EAAA: {gif_msg_id}")
            #     if message_object2.msgId == gif_msg_id:
            #         matching_message = message_object2
            #         break

            # # Kiểm tra và thu hồi
            # if matching_message:
            #     cli_msg_id = matching_message.cliMsgId

            #     # Thu hồi GIF
            #     undo_response = client.undoMessage(
            #         msgId=gif_msg_id,
            #         cliMsgId=cli_msg_id,
            #         thread_id=thread_id,
            #         thread_type=thread_type
            #     )

            #     # Kiểm tra kết quả thu hồi
            #     if undo_response.get("error_code") != 0:
            #         print(f"Error while undoing GIF: {undo_response.get('error_message')}")
            # else:
            #     print("Không tìm thấy message_object nào trùng khớp với msgId của GIF.")
            # Dò tìm message_object với msgId trùng khớp
            # Đợi 3 giây
            # time.sleep(10)

            # # Lấy msgId từ gif_response
            # gif_msg_id = gif_response.msgId

            # # Dò tìm message_object với msgId trùng khớp
            # matching_message = next((msg for msg in received_messages if msg.msgId == gif_msg_id), None)

            # # Kiểm tra và thu hồi
            # if matching_message:
            #     cli_msg_id = matching_message.cliMsgId

            #     # Thu hồi GIF
            #     undo_response = client.undoMessage(
            #         msgId=gif_msg_id,
            #         cliMsgId=cli_msg_id,
            #         thread_id=thread_id,
            #         thread_type=thread_type
            #     )

            #     # Kiểm tra kết quả thu hồi
            #     if undo_response.get("error_code") != 0:
            #         print(f"Error while undoing GIF: {undo_response.get('error_message')}")
            # else:
            #     print("Không tìm thấy message_object nào trùng khớp với msgId của GIF.")

            if bet_choice == 'T' and result == 'Tài' or bet_choice == 'X' and result == 'Xỉu' or bet_choice == 'H' and result == 'Hoà':
                winnings = bet_amount * 2
                users[author_id]["balance"] += winnings
                users[author_id]["wins"] += 1
                formatted_winnings = format_currency(winnings)
                response=Message(text=f"{user_name} 🎉 Bạn thắng! Kết quả xúc xắc: {formatted_dice} = {formatted_total}. Kết quả: {result}. Bạn nhận được {formatted_winnings}.")
            else:
                users[author_id]["balance"] -= bet_amount
                users[author_id]["losses"] += 1
                formatted_loss = format_currency(bet_amount)
                response=Message(text=f"{user_name} 😞 Bạn thua! Kết quả xúc xắc: {formatted_dice} = {formatted_total}. Kết quả: {result}. Bạn mất {formatted_loss}.")
            # Send dice images
            # send_dice_images(dice, thread_id, thread_type, client)
            # Tạo ảnh gộp từ ba ảnh xí ngầu
            combined_image_path = create_dice_image(dice)
            if combined_image_path:
                # Gửi ảnh gộp xí ngầu
                client.sendLocalImage(
                    imagePath=combined_image_path,
                    message=response,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=480*3,
                    height=480
                )
            else:
                print("Không thể tạo ảnh gộp.")

            save_users()

        elif command == 'ct':
            if len(query) != 4:
                client.sendMessage(Message(text=f"{user_name} ❌ Cú pháp không hợp lệ. Vui lòng dùng lệnh `-taixiu ct (tên người nhận) (số tiền)`."), thread_id, thread_type)
                return

            recipient_name = query[2]
            try:
                transfer_amount = int(query[3])
            except ValueError:
                client.sendMessage(Message(text=f"{user_name} ❌ Số tiền không hợp lệ."), thread_id, thread_type)
                return

            if author_id not in users:
                client.sendMessage(Message(text=f"{user_name} ⚠️ Bạn cần đăng ký và đăng nhập để chuyển tiền."), thread_id, thread_type)
                return

            if users[author_id]["balance"] < transfer_amount:
                client.sendMessage(Message(text=f"{user_name} ❌ Số dư không đủ để chuyển {format_currency(transfer_amount)}."), thread_id, thread_type)
                return

            recipient_id = next((uid for uid, data in users.items() if data["username"] == recipient_name), None)
            if recipient_id:
                users[author_id]["balance"] -= transfer_amount
                users[recipient_id]["balance"] += transfer_amount
                save_users()
                formatted_transfer_amount = format_currency(transfer_amount)
                client.sendMessage(Message(text=f"{user_name} 💸 Đã chuyển {formatted_transfer_amount} cho {recipient_name} thành công!"), thread_id, thread_type)
                client.sendMessage(Message(text=f"{recipient_name} 💰 Bạn đã nhận được {formatted_transfer_amount} từ {user_name}."), thread_id, thread_type)
            else:
                client.sendMessage(Message(text=f"{user_name} ❌ Không tìm thấy người nhận với tên {recipient_name}."), thread_id, thread_type)

        elif command == 'code':
            if len(query) != 3:
                client.sendMessage(Message(text=f"{user_name} ❌ Cú pháp không hợp lệ. Vui lòng dùng lệnh `-taixiu code (mã)`."), thread_id, thread_type)
                return

            code = query[2]
            reward = 0

            if code == "KHAITRUONGNHACAI":
                reward = 5000000000000000
            	

            if reward > 0:
                if author_id not in users:
                    client.sendMessage(Message(text=f"{user_name} ⚠️ Bạn cần đăng ký và đăng nhập để nhận thưởng."), thread_id, thread_type)
                    return

                if code in users[author_id]["used_codes"]:
                    client.sendMessage(Message(text=f"{user_name} ❌ Bạn đã sử dụng mã này rồi."), thread_id, thread_type)
                    return

                users[author_id]["balance"] += reward
                users[author_id]["used_codes"].add(code)
                formatted_reward = format_currency(reward)
                client.sendMessage(Message(text=f"{user_name} 🎁 Chúc mừng! Bạn đã nhận {formatted_reward} với mã {code}."), thread_id, thread_type)
                save_users()
            else:
                client.sendMessage(Message(text=f"{user_name} ❌ Mã không hợp lệ."), thread_id, thread_type)
        
        elif command == 'bxh':
            top_users = sorted(users.items(), key=lambda item: item[1]["balance"], reverse=True)[:10]
            if not top_users:
                client.sendMessage(Message(text=f"{user_name} 📉 Hiện tại không có dữ liệu bảng xếp hạng."), thread_id, thread_type)
                return

            leaderboard = "🏆 **Bảng Xếp Hạng Top 10**\n"
            for rank, (uid, user_info) in enumerate(top_users, start=1):
                formatted_balance = format_currency(user_info["balance"])
                leaderboard += f"{rank}. {user_info['username']} - {formatted_balance}\n"

            client.sendMessage(Message(text=leaderboard), thread_id, thread_type)

    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def fetchGroupName(thread_id):
        
        return "Xb"

def get_mitaizl():
    return {
        'txiu': handle_taixiu_command
    }