#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test để kiểm tra hệ thống thông báo khởi động
"""

import sys
import os
sys.path.append('.')

def test_startup_notification():
    print("=" * 60)
    print("🚀 KIỂM TRA THÔNG BÁO KHỞI ĐỘNG")
    print("=" * 60)
    
    try:
        from modules.startup_notify import (
            get_system_info, 
            get_bot_stats, 
            count_loaded_modules,
            check_dependencies
        )
        
        print("\n📊 Test lấy thông tin hệ thống:")
        sys_info = get_system_info()
        if sys_info:
            print(f"   ✅ CPU: {sys_info['cpu_cores']} cores ({sys_info['cpu_percent']:.1f}%)")
            print(f"   ✅ RAM: {sys_info['ram_used']:.1f}GB/{sys_info['ram_total']:.1f}GB")
            print(f"   ✅ OS: {sys_info['os_name']}")
        else:
            print("   ❌ Không thể lấy thông tin hệ thống")
        
        print("\n📈 Test lấy thống kê bot:")
        bot_stats = get_bot_stats()
        print(f"   📊 Tổng lượt sử dụng: {bot_stats['total_usage']}")
        print(f"   👥 Users đã dùng: {bot_stats['unique_users']}")
        print(f"   🔧 Commands tracked: {bot_stats['commands_tracked']}")
        
        print("\n🔧 Test đếm modules:")
        modules = count_loaded_modules()
        print(f"   📦 Tổng modules: {modules['total']}")
        print(f"   🔄 Prefix modules: {modules['prefix']}")
        print(f"   🚫 Noprefix modules: {modules['noprefix']}")
        
        print("\n📋 Test kiểm tra dependencies:")
        missing_deps = check_dependencies()
        if missing_deps:
            print(f"   ⚠️  Thiếu thư viện: {', '.join(missing_deps)}")
        else:
            print("   ✅ Tất cả dependencies đều có sẵn")
        
        print("\n📁 Test kiểm tra folders:")
        folders_to_check = [
            'modules',
            'modules/cache',
            'modules/noprefix'
        ]
        
        for folder in folders_to_check:
            if os.path.exists(folder):
                print(f"   ✅ {folder} - Tồn tại")
            else:
                print(f"   ❌ {folder} - Không tồn tại")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test: {e}")
        return False

def test_notification_format():
    print("\n" + "=" * 60)
    print("📝 KIỂM TRA FORMAT THÔNG BÁO")
    print("=" * 60)
    
    try:
        from modules.startup_notify import get_system_info, get_bot_stats, count_loaded_modules
        import datetime
        import pytz
        
        # Tạo mock client
        class MockClient:
            def __init__(self):
                self.uid = "test_bot_12345678"
                self.me_name = "Test Bot"
                self.version = "1.1"
        
        mock_client = MockClient()
        
        # Tạo thông báo mẫu
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        startup_time = datetime.datetime.now(vn_tz).strftime('%d/%m/%Y %H:%M:%S')
        
        sys_info = get_system_info()
        bot_stats = get_bot_stats()
        modules_count = count_loaded_modules()
        
        startup_message = f"""
🚀 BOT KHỞI ĐỘNG THÀNH CÔNG 🚀

🕐 Thời gian: {startup_time}
🤖 Bot Name: {mock_client.me_name}
📱 Version: {mock_client.version}
🆔 Bot ID: {mock_client.uid}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 THÔNG TIN HỆ THỐNG:
"""
        
        if sys_info:
            startup_message += f"""
💻 OS: {sys_info['os_name']}
🔧 CPU: {sys_info['cpu_cores']} cores ({sys_info['cpu_percent']:.1f}%)
🧠 RAM: {sys_info['ram_used']:.1f}GB/{sys_info['ram_total']:.1f}GB ({sys_info['ram_percent']:.1f}%)
💾 Disk: {sys_info['disk_free']:.1f}GB free / {sys_info['disk_total']:.1f}GB total
"""
        
        startup_message += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 THÔNG TIN MODULES:

📦 Modules loaded: {modules_count['total']}
🔄 Prefix commands: {modules_count['prefix']}
🚫 Noprefix commands: {modules_count['noprefix']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 THỐNG KÊ BOT:

📊 Tổng lượt sử dụng: {bot_stats['total_usage']}
👥 Users đã dùng: {bot_stats['unique_users']}
🔧 Commands tracked: {bot_stats['commands_tracked']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Bot đã sẵn sàng nhận lệnh!

📝 Dùng -stats để xem thống kê chi tiết
🔔 Dùng -notify off để tắt thông báo
🆘 Dùng -toadmin để liên hệ admin
"""
        
        print("📧 Preview thông báo khởi động:")
        print("-" * 50)
        print(startup_message.strip())
        print("-" * 50)
        
        print(f"\n📏 Độ dài thông báo: {len(startup_message)} ký tự")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test format: {e}")
        return False

def test_file_operations():
    print("\n" + "=" * 60)
    print("📁 KIỂM TRA THAO TÁC FILE")
    print("=" * 60)
    
    try:
        # Test tạo cache folder
        cache_folder = 'modules/cache'
        os.makedirs(cache_folder, exist_ok=True)
        print(f"   ✅ Tạo folder cache: {cache_folder}")
        
        # Test ghi file log
        log_file = 'modules/cache/test_startup_log.txt'
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Test startup at: {datetime.datetime.now()}\n")
        print(f"   ✅ Ghi file log: {log_file}")
        
        # Test đọc file log
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"   ✅ Đọc file log: {len(content)} ký tự")
        
        # Test xóa file test
        os.remove(log_file)
        print(f"   ✅ Xóa file test: {log_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test file operations: {e}")
        return False

def main():
    print("🎯 BẮT ĐẦU TEST STARTUP NOTIFICATION SYSTEM")
    
    results = []
    
    # Test các components
    results.append(test_startup_notification())
    results.append(test_notification_format())
    results.append(test_file_operations())
    
    print("\n" + "=" * 60)
    print("📊 KẾT QUẢ TỔNG HỢP")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests passed: {passed}/{total}")
    print(f"📈 Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 TẤT CẢ TESTS THÀNH CÔNG!")
        print("🚀 Hệ thống startup notification đã sẵn sàng!")
    else:
        print("\n⚠️  CÓ MỘT SỐ TESTS THẤT BẠI!")
        print("🔧 Vui lòng kiểm tra và sửa lỗi!")
    
    print("=" * 60)

if __name__ == "__main__":
    import datetime
    main()