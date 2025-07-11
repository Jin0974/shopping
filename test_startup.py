#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内购系统启动测试脚本
用于验证系统是否可以正常启动
"""

import sys
import os
import importlib.util

def test_import():
    """测试导入系统模块"""
    try:
        # 添加当前目录到Python路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        # 尝试导入app模块
        spec = importlib.util.spec_from_file_location("app", os.path.join(current_dir, "app.py"))
        app = importlib.util.module_from_spec(spec)
        
        print("✅ 成功导入app模块")
        return True
    except Exception as e:
        print(f"❌ 导入app模块失败: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    required_packages = [
        'streamlit',
        'pandas', 
        'json',
        'os',
        'time',
        'contextlib',
        'io',
        'datetime',
        'uuid'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 可用")
        except ImportError:
            print(f"❌ {package} 不可用")
            all_ok = False
    
    return all_ok

def main():
    """主测试函数"""
    print("=== 内购系统启动测试 ===")
    print()
    
    print("1. 测试Python依赖包...")
    deps_ok = test_dependencies()
    print()
    
    print("2. 测试应用模块导入...")
    import_ok = test_import()
    print()
    
    if deps_ok and import_ok:
        print("🎉 所有测试通过！系统可以正常启动。")
        print()
        print("启动命令：")
        print("streamlit run app.py")
        print()
        print("或者：")
        print("python -m streamlit run app.py")
        return True
    else:
        print("⚠️  测试失败，请检查错误信息并修复。")
        return False

if __name__ == "__main__":
    main()
