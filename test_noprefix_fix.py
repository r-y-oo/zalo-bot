#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test module noprefix sau khi sửa lỗi
import sys
import os
sys.path.append('.')

try:
    # Test import module
    from modules.noprefix.prefix import prf, get_mitaizl
    
    print("✅ Import module thành công")
    
    # Test hàm prf()
    prefix_value = prf()
    print(f"✅ Prefix value: '{prefix_value}'")
    
    # Test get_mitaizl()
    commands = get_mitaizl()
    print(f"✅ Các lệnh noprefix: {list(commands.keys())}")
    
    print("\n🎉 Module noprefix đã hoạt động bình thường!")
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()