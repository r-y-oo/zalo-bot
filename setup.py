#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script setup tự động cho Bot Zalo
Kiểm tra và cài đặt dependencies cần thiết
"""

import subprocess
import sys
import os
from colorama import Fore, Style, init

init(autoreset=True)

def install_package(package):
    """Cài đặt package qua pip"""
    try:
        print(f"{Fore.YELLOW}📦 Đang cài đặt {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{Fore.GREEN}✅ Đã cài đặt {package} thành công!")
        return True
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}❌ Lỗi khi cài đặt {package}")
        return False

def check_package(package):
    """Kiểm tra package đã được cài đặt chưa"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("=" * 60)
    print("🚀 SETUP BOT ZALO - KIỂM TRA DEPENDENCIES")
    print("=" * 60)
    print(f"{Style.RESET_ALL}")
    
    # Đọc requirements.txt
    if not os.path.exists('requirements.txt'):
        print(f"{Fore.RED}❌ Không tìm thấy file requirements.txt!")
        return
    
    with open('requirements.txt', 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"{Fore.BLUE}📋 Danh sách packages cần kiểm tra: {len(packages)}")
    print()
    
    missing_packages = []
    installed_packages = []
    
    # Map tên package trong requirements với tên import
    package_mapping = {
        'pillow': 'PIL',
        'beautifulsoup4': 'bs4',
        'bs4': 'bs4',
        'pycryptodome': 'Crypto',
        'fake_useragent': 'fake_useragent'
    }
    
    # Kiểm tra từng package
    for package in packages:
        import_name = package_mapping.get(package, package)
        
        print(f"{Fore.YELLOW}🔍 Kiểm tra {package}...", end=" ")
        
        if check_package(import_name):
            print(f"{Fore.GREEN}✅ Đã có")
            installed_packages.append(package)
        else:
            print(f"{Fore.RED}❌ Thiếu")
            missing_packages.append(package)
    
    print()
    print(f"{Fore.GREEN}✅ Packages đã có: {len(installed_packages)}")
    print(f"{Fore.RED}❌ Packages thiếu: {len(missing_packages)}")
    
    if missing_packages:
        print()
        print(f"{Fore.YELLOW}📦 ĐANG CÀI ĐẶT PACKAGES THIẾU...")
        print("-" * 40)
        
        success_count = 0
        for package in missing_packages:
            if install_package(package):
                success_count += 1
        
        print()
        print(f"{Fore.BLUE}📊 KẾT QUẢ CÀI ĐẶT:")
        print(f"   ✅ Thành công: {success_count}/{len(missing_packages)}")
        print(f"   ❌ Thất bại: {len(missing_packages) - success_count}/{len(missing_packages)}")
        
        if success_count == len(missing_packages):
            print(f"{Fore.GREEN}{Style.BRIGHT}")
            print("🎉 TẤT CẢ DEPENDENCIES ĐÃ ĐƯỢC CÀI ĐẶT!")
        else:
            print(f"{Fore.YELLOW}{Style.BRIGHT}")
            print("⚠️  MỘT SỐ PACKAGES CHƯA ĐƯỢC CÀI ĐẶT!")
            print("   Vui lòng cài đặt thủ công:")
            for package in missing_packages[success_count:]:
                print(f"   pip install {package}")
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}")
        print("🎉 TẤT CẢ DEPENDENCIES ĐÃ SẴN SÀNG!")
    
    print()
    print(f"{Fore.CYAN}🚀 Setup hoàn tất! Bây giờ có thể chạy bot:")
    print(f"{Fore.WHITE}   python bot.py")
    print()
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Setup đã bị hủy bởi người dùng")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Lỗi setup: {e}")