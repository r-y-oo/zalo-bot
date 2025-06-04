# 🤖 Bot Zalo by Ha Huy Hoang

Bot Zalo tự động với nhiều tính năng hữu ích, hệ thống thông báo admin toàn diện và menu phân loại có tổ chức.

## 🚀 Cài Đặt Nhanh (Quick Setup)

### Bước 1: Cài đặt thư viện
```bash
python install.py
```

### Bước 2: Cấu hình Admin ID
Sửa file `config.py`:
```python
ADMIN = 'your_admin_id_here'  # Thay bằng ID của bạn
```

### Bước 3: Chạy bot
```bash
python bot.py
```

**Xong! Bot đã sẵn sàng hoạt động! 🎉**

---

## 📂 Hệ Thống Menu Mới (v2.1.0)

### 🎯 Menu Chính:
```
-menu          # Menu chính với tất cả danh mục
-help          # Hướng dẫn sử dụng chi tiết
```

### 📋 Các Danh Mục:
```
🔧 -menua      # Lệnh admin (chỉ admin)
👥 -menug      # Quản lý group
🎮 -menuf      # Giải trí & game  
🎵 -menum      # Âm nhạc & media
🖼️ -menuv      # Ảnh & video
🔞 -menu18     # Content 18+
🛠️ -menut      # Công cụ tiện ích
🌐 -menus      # Mạng xã hội
💬 -menuc      # Chat AI
📊 -stats      # Thống kê (admin)
```

### 🚫 Lệnh Không Cần Prefix:
```
hello, hi, chào    # Chào hỏi
bot, bót           # Gọi bot
system            # Thông tin hệ thống
```

---

## 📋 Tính Năng

### 🔧 Lệnh Admin (chỉ admin)
- `-admin on/off` - Bật/tắt admin mode
- `-notify on/off` - Bật/tắt thông báo  
- `-stats` - Thống kê chi tiết
- `-clearstats` - Xóa thống kê

### 👥 Quản Lý Group
- `-tagall` - Gọi tất cả thành viên
- `-war` - Lệnh war
- `-meid @user` - Lấy ID user

### 🎮 Giải Trí & Game
- `-txiu` - Game tài xỉu
- `-tangai` - Thả thính
- `-boibai` - Xem bói

### 🎵 Âm Nhạc & Media  
- `-nhac` - Chọn nhạc
- `-voice` - Tạo voice
- `-chill` - Video chill

### 🖼️ Ảnh & Video
- `-girl` - Ảnh gái xinh
- `-meme` - Ảnh meme
- `-taoanh` - Vẽ ảnh AI

### 🛠️ Công Cụ
- `-qrcode` - Tạo mã QR
- `-toadmin [tin nhắn]` - Gửi tin nhắn cho admin

### 📊 Thông Báo Admin Tự Động
- 🚀 **Khi khởi động**: Thông tin hệ thống chi tiết
- 📱 **Khi có người dùng**: Thông báo realtime
- 🛑 **Khi tắt bot**: Thống kê session

---

## 💡 Cách Sử Dụng Menu

### Bước 1: Xem menu chính
```
-menu
```

### Bước 2: Chọn danh mục
```
-menug          # Xem lệnh group
-menuf          # Xem lệnh giải trí
-menuv          # Xem lệnh ảnh/video
```

### Bước 3: Sử dụng lệnh
```
-girl           # Xem ảnh gái
-txiu           # Chơi game
hello           # Chào bot (không cần -)
```

### 💭 Cần Hỗ Trợ:
```
-help           # Hướng dẫn chi tiết
-commands       # Danh sách lệnh tóm tắt
-noprefix       # Hướng dẫn lệnh không prefix
-toadmin        # Liên hệ admin
```

---

## ⚠️ Nếu Gặp Lỗi

### Lỗi "No module named 'pillow'" hoặc thiếu thư viện:
```bash
# Giải pháp 1: Chạy lại install
python install.py

# Giải pháp 2: Cài thủ công
pip install pillow psutil pytz colorama beautifulsoup4

# Giải pháp 3: Nếu vẫn lỗi
pip install --upgrade pip
python install.py
```

### Lỗi "can't open file":
- Kiểm tra đang ở đúng thư mục bot chưa
- Đảm bảo file `install.py` có trong thư mục
- Thử: `dir` (Windows) hoặc `ls` (Linux) để xem files

### Bot không khởi động:
1. Kiểm tra `config.py` có đúng ADMIN ID
2. Chạy `python install.py` để cài thư viện
3. Kiểm tra session cookies còn hạn

### Không nhận thông báo:
1. Kiểm tra ADMIN ID trong config
2. Gửi `-notify on` để bật thông báo
3. Thử gửi `hello` để test

---

## 📁 Cấu Trúc Files

```
bothoang/
├── bot.py              # File chính
├── config.py           # Cấu hình
├── install.py          # Script cài đặt
├── requirements.txt    # Danh sách thư viện
├── modules/           # Các modules
│   ├── menu_v2.py         # Menu system mới
│   ├── help.py            # Hướng dẫn sử dụng
│   ├── startup_notify.py  # Thông báo khởi động
│   ├── admin_notify.py    # Quản lý admin
│   └── noprefix/         # Lệnh không prefix
└── README.md          # File này
```

---

## 🧪 Test Hệ Thống

```bash
# Test lệnh noprefix
python test_noprefix.py

# Test thông báo khởi động
python test_startup.py
```

---

## 💡 Tips Sử Dụng

### Để xem ADMIN ID của bạn:
1. Gửi tin nhắn bất kỳ cho bot
2. Xem console, sẽ hiện `Author ID: xxxxx`
3. Copy số đó vào `config.py`

### Để bot chỉ admin sử dụng:
- Gửi `-admin on` (chỉ admin có thể dùng bot)
- Gửi `-admin off` (mọi người có thể dùng)

### Để tắt thông báo spam:
- Gửi `-notify off` (tắt thông báo hoạt động)
- Gửi `-notify on` (bật lại thông báo)

### Sử dụng menu hiệu quả:
- Gõ `-menu` để xem tổng quan
- Gõ `-menug` để xem lệnh group cụ thể
- Gõ `-help` khi cần hướng dẫn chi tiết

---

## 📞 Hỗ Trợ

**Nếu vẫn gặp vấn đề:**

1. **Chạy lại setup**: `python install.py`
2. **Xem hướng dẫn**: `-help`
3. **Liên hệ admin**: `-toadmin [tin nhắn của bạn]`
4. **Test riêng**: Chạy `python -c "import pillow"` để test

**Các lỗi thường gặp:**
- ❌ `No such file`: Đang ở sai thư mục
- ❌ `No module named`: Thiếu thư viện → chạy `install.py`  
- ❌ `Permission denied`: Chạy với quyền admin
- ❌ `Connection error`: Kiểm tra internet

---

## 🆕 Cập Nhật v2.1.0

### ✨ Tính Năng Mới:
- **Menu System v2**: Phân loại lệnh theo danh mục
- **Help System**: Hướng dẫn chi tiết từng bước  
- **Auto Setup**: Script cài đặt siêu đơn giản
- **Admin Notification**: Thông báo tự động toàn diện

### 🔧 Cải Thiện:
- Menu được tổ chức theo danh mục rõ ràng
- Hướng dẫn sử dụng chi tiết hơn
- Error handling tốt hơn
- User experience được cải thiện

---

## 📝 Credits

- **Developer**: Ha Huy Hoang
- **Version**: 2.1.0
- **Last Update**: 05/06/2025
- **Features**: Menu System v2, Auto Setup, Admin Notification, Help System

**🎯 Mục tiêu: Setup trong 3 lệnh, sử dụng trực quan với menu phân loại!**