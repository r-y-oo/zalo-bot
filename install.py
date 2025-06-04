#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cài đặt nhanh cho Bot Zalo
Cài đặt Pillow và các thư viện cần thiết
"""

import subprocess
import sys

def run_command(command):
    """Chạy command và hiển thị output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Thành công: {command}")
            return True
        else:
            print(f"❌ Lỗi: {command}")
            print(f"   {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    print("🚀 CÀI ĐẶT BOT ZALO")
    print("=" * 40)
    
    # Kiểm tra Python version
    print(f"🐍 Python version: {sys.version}")
    
    print("\n📦 Đang cài đặt thư viện...")
    
    # Danh sách thư viện cần thiết
    packages = [
        "pillow",
        "psutil", 
        "pytz",
        "colorama",
        "beautifulsoup4",
        "pycryptodome"
    ]
    
    success_count = 0
    
    for package in packages:
        print(f"\n🔄 Cài đặt {package}...")
        if run_command(f"pip install {package}"):
            success_count += 1
    
    print("\n" + "=" * 40)
    print(f"📊 KẾT QUẢ: {success_count}/{len(packages)} thành công")
    
    if success_count == len(packages):
        print("🎉 CÀI ĐẶT HOÀN TẤT!")
        print("\n🚀 Bây giờ có thể chạy bot:")
        print("   python bot.py")
    else:
        print("⚠️  MỘT SỐ THỦ VIỆN CHƯA ĐƯỢC CÀI ĐẶT!")
        print("\n🔧 Thử chạy lại hoặc cài thủ công:")
        for package in packages:
            print(f"   pip install {package}")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    main()