#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('.')

try:
    from modules.noprefix.prefix import prf, get_mitaizl
    
    print("Import module thanh cong")
    
    prefix_value = prf()
    print(f"Prefix value: '{prefix_value}'")
    
    commands = get_mitaizl()
    print(f"Cac lenh noprefix: {list(commands.keys())}")
    
    print("Module noprefix da hoat dong binh thuong!")
    
except Exception as e:
    print(f"Loi: {e}")
    import traceback
    traceback.print_exc()