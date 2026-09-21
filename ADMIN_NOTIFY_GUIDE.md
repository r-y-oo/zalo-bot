# 🤖 Hướng Dẫn Hệ Thống Thông Báo Admin

## 📋 Tổng Quan

Hệ thống thông báo admin giúp admin theo dõi hoạt động của bot một cách tự động và hiệu quả. Mỗi khi có user sử dụng bot, admin sẽ nhận được thông báo riêng. Ngoài ra, admin cũng nhận thông báo khi bot khởi động/tắt.

## ⚡ Tính Năng Chính

### 1. **🚀 Thông Báo Khởi Động**
- Gửi tin nhắn đến admin khi bot khởi động thành công
- Hiển thị thông tin hệ thống: CPU, RAM, Disk
- Thống kê modules đã load
- Kiểm tra dependencies và báo cáo vấn đề
- Ghi log thời gian khởi động

### 2. **🛑 Thông Báo Tắt Bot**
- Gửi tin nhắn khi bot tắt
- Thống kê session vừa kết thúc
- Xác nhận bot đã tắt an toàn

### 3. **🚨 Thông Báo Lỗi**
- Gửi tin nhắn khi bot gặp lỗi khởi động
- Chi tiết lỗi và gợi ý khắc phục
- Hướng dẫn troubleshooting

### 4. **📊 Thông Báo Hoạt Động**
- Gửi tin nhắn riêng đến admin khi có user dùng bot
- Hiển thị thông tin chi tiết: tên user, ID, lệnh được dùng, thời gian
- Phân biệt hoạt động trong group vs chat riêng
- Chống spam: chỉ thông báo mỗi user/lệnh sau 30 phút

### 5. **⚙️ Quản Lý Thông Báo**
```
-notify on     # Bật thông báo admin
-notify off    # Tắt thông báo admin
```

### 6. **📈 Thống Kê Hoạt Động**
```
-stats         # Xem thống kê chi tiết
-clearstats    # Xóa toàn bộ thống kê
```

### 7. **💬 Liên Hệ Admin**
```
-toadmin [tin nhắn]    # User gửi tin nhắn đến admin
```

## 🚀 Ví Dụ Thông Báo Khởi Động

```
🚀 BOT KHỞI ĐỘNG THÀNH CÔNG 🚀

🕐 Thời gian: 05/06/2025 02:10:00
🤖 Bot Name: Bot by Duy Khanh
📱 Version: 1.1
🆔 Bot ID: 1234567890123456789

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 THÔNG TIN HỆ THỐNG:

💻 OS: Windows
🔧 CPU: 8 cores (25.5%)
🧠 RAM: 4.2GB/16.0GB (26.3%)
💾 Disk: 150.5GB free / 500.0GB total

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 THÔNG TIN MODULES:

📦 Modules loaded: 45
🔄 Prefix commands: 38
🚫 Noprefix commands: 7

━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 THỐNG KÊ BOT:

📊 Tổng lượt sử dụng: 1,250
👥 Users đã dùng: 85
🔧 Commands tracked: 342

━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Bot đã sẵn sàng nhận lệnh!

📝 Dùng -stats để xem thống kê chi tiết
🔔 Dùng -notify off để tắt thông báo
🆘 Dùng -toadmin để liên hệ admin
```

## 🛑 Ví Dụ Thông Báo Tắt Bot

```
🛑 BOT ĐANG TẮT 🛑

🕐 Thời gian: 05/06/2025 15:30:00
🤖 Bot ID: 1234567890123456789

📊 Thống kê session:
• Tổng lượt sử dụng: 1,267
• Users hoạt động: 92

✅ Session đã hoàn thành an toàn!
```

## 🚨 Ví Dụ Thông Báo Lỗi

```
🚨 LỖI KHỞI ĐỘNG BOT 🚨

🕐 Thời gian: 05/06/2025 08:00:00

❌ Lỗi:
Connection timeout: Failed to connect to Zalo API

🔧 Vui lòng kiểm tra và khắc phục!

📝 Có thể do:
• Mất kết nối internet
• API key/session cookies hết hạn
• Thiếu thư viện cần thiết
• Lỗi cấu hình
```

## 📊 Thống Kê Bao Gồm

- **Tổng lượt sử dụng**: Số lần bot được sử dụng
- **Số users hoạt động**: Số user đã từng dùng bot
- **Top 5 users**: Users sử dụng bot nhiều nhất
- **Top 5 commands**: Lệnh được dùng phổ biến nhất
- **Thời gian thống kê**: Cập nhật realtime

## 🔧 Cấu Hình

### Thư Mục Cache
```
modules/cache/
├── user_activity.json     # Lưu hoạt động users
├── admin_settings.json    # Cài đặt thông báo
├── admindata.json        # Trạng thái admin mode
└── startup_log.txt       # Log thời gian khởi động
```

### Cài Đặt Admin
Trong file `config.py`:
```python
ADMIN = 'your_admin_id_here'
```

## 🎯 Lệnh Admin

| Lệnh | Mô Tả | Quyền |
|------|-------|-------|
| `-notify on/off` | Bật/tắt thông báo hoạt động | Admin Only |
| `-stats` | Xem thống kê hoạt động | Admin Only |
| `-clearstats` | Xóa thống kê | Admin Only |
| `-admin on/off` | Bật/tắt admin mode | Admin Only |

## 🎭 Lệnh User

| Lệnh | Mô Tả | Quyền |
|------|-------|-------|
| `-toadmin [message]` | Gửi tin nhắn đến admin | All Users |

## 🚀 Cách Hoạt Động

### Quy Trình Khởi Động:
1. **Bot khởi tạo** → Load modules và cấu hình
2. **Nhận tin nhắn đầu tiên** → Trigger thông báo khởi động
3. **Thu thập thông tin** → Hệ thống, modules, thống kê
4. **Gửi thông báo** → Admin nhận tin nhắn chi tiết
5. **Kiểm tra vấn đề** → Báo cáo warnings/errors

### Quy Trình Hoạt Động:
1. **User gửi lệnh** → Bot xử lý lệnh
2. **Kiểm tra spam** → Đã thông báo trong 30 phút chưa?
3. **Thu thập thông tin** → Tên user, group, thời gian
4. **Gửi thông báo** → Admin nhận tin nhắn riêng
5. **Lưu thống kê** → Cập nhật database hoạt động

## ⚙️ Cấu Hình Nâng Cao

### Tùy Chỉnh Thời Gian Chống Spam
Trong `mitaizl.py`, dòng 154:
```python
if (current_time - last_notify).total_seconds() < 1800:  # 30 phút
```

### Tùy Chỉnh Dependencies Check
Trong `startup_notify.py`, hàm `check_dependencies()`:
```python
required_packages = [
    'psutil', 'pytz', 'colorama', 'pillow', 'pystyle'
]
```

### Bật/Tắt Thông Báo Khởi Động
Trong `bot.py`, dòng 58:
```python
# client.force_startup_notification()  # Uncomment để gửi ngay
```

## 🛡️ Bảo Mật

- ✅ Chỉ admin mới nhận thông báo
- ✅ Admin không bị thông báo khi tự dùng bot
- ✅ Chống spam với cooldown 30 phút
- ✅ Dữ liệu được lưu local, không public
- ✅ Auto-cleanup khi cần thiết
- ✅ Error handling toàn diện

## 🧪 Testing

### Chạy Test Tổng Quát:
```bash
python test_noprefix.py      # Test noprefix system
python test_startup.py       # Test startup notification
```

### Test Thủ Công:
```python
# Trong Python console
from modules.startup_notify import notify_bot_startup
from bot import Client

client = Client(API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES)
notify_bot_startup(client)  # Test thông báo khởi động
```

## 🔄 Backup & Restore

### Backup Dữ Liệu
```bash
cp -r modules/cache/ backup_$(date +%Y%m%d)/
```

### Restore Dữ Liệu
```bash
cp -r backup_20250605/ modules/cache/
```

## 🔧 Troubleshooting

### Bot Không Gửi Thông Báo Khởi Động:
1. Kiểm tra ADMIN ID trong config.py
2. Kiểm tra kết nối internet
3. Kiểm tra session cookies còn hạn
4. Xem log console có lỗi không

### Thông Báo Hoạt Động Không Hoạt Động:
1. Kiểm tra `-notify on` đã bật chưa
2. Kiểm tra cooldown 30 phút
3. Xem file user_activity.json

### Lỗi Dependencies:
```bash
pip install -r requirements.txt
```

## 📞 Hỗ Trợ

Nếu có vấn đề, hãy:
1. Chạy `python test_startup.py`
2. Kiểm tra log console
3. Xem các file trong `modules/cache/`
4. Restart bot nếu cần thiết
5. Liên hệ developer

---

**Phiên Bản:** 2.0.0  
**Tác Giả:** Nguyễn Đức Tài  
**Cập Nhật:** 05/06/2025  
**Tính Năng Mới:** Thông báo khởi động, tắt bot, và error handling