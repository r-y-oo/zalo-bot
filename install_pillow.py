#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cài đặt thư viện Pillow cho Bot Zalo
"""

import subprocess
import sys

def install_pillow():
    """Cài đặt thư viện Pillow"""
    print("🔄 Đang tải xuống và cài đặt thư viện Pillow...")
    print("-" * 50)
    
    try:
        # Cài đặt pillow
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("\n✅ Đã cài đặt Pillow thành công!")
        
        # Kiểm tra cài đặt
        print("🔍 Đang kiểm tra cài đặt...")
        try:
            import PIL
            print(f"✅ Pillow version: {PIL.__version__}")
            print("🎉 Pillow đã sẵn sàng sử dụng!")
        except ImportError:
            print("❌ Có lỗi khi import Pillow")
            return False
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt Pillow: {e}")
        print("\n🔧 Thử các giải pháp sau:")
        print("1. Chạy lại với quyền admin/sudo")
        print("2. Cập nhật pip: python -m pip install --upgrade pip")
        print("3. Cài thủ công: pip install pillow")
        return False

if __name__ == "__main__":
    print("🚀 CÀI ĐẶT THỦ VIỆN PILLOW")
    print("=" * 50)
    
    # Kiểm tra xem đã có Pillow chưa
    try:
        import PIL
        print(f"✅ Pillow đã được cài đặt (version: {PIL.__version__})")
        print("🎉 Không cần cài đặt thêm!")
    except ImportError:
        print("📦 Pillow chưa được cài đặt")
        success = install_pillow()
        
        if success:
            print("\n🎯 Bây giờ có thể chạy bot:")
            print("   python bot.py")
        else:
            print("\n⚠️  Vui lòng cài đặt Pillow thủ công:")
            print("   pip install pillow")
    
    print("\n" + "=" * 50)
    print("✅ Hoàn tất!")