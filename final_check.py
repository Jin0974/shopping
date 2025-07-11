#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内购系统启动验证脚本
"""

def final_verification():
    """最终验证"""
    print("🔧 内购系统 - 最终验证")
    print("=" * 40)
    
    try:
        # 1. 语法检查
        print("1. Python语法检查...")
        import py_compile
        py_compile.compile('app.py', doraise=True)
        print("   ✅ 语法正确")
        
        # 2. 模块导入
        print("2. 模块导入测试...")
        import app
        print("   ✅ 导入成功")
        
        # 3. 关键函数检查
        print("3. 关键函数检查...")
        key_functions = ['main', 'admin_page', 'user_page', 'load_data', 'save_data']
        for func in key_functions:
            if hasattr(app, func):
                print(f"   ✅ {func}")
            else:
                print(f"   ❌ {func} 缺失")
        
        # 4. 数据文件检查
        print("4. 数据文件检查...")
        import os
        files = ['inventory.json', 'orders.json', 'users.json']
        for file in files:
            if os.path.exists(file):
                print(f"   ✅ {file} 存在")
            else:
                print(f"   ℹ️ {file} 将自动创建")
        
        print("\n🎉 验证完成！系统已准备就绪。")
        print("\n📱 启动命令:")
        print("   streamlit run app.py")
        print("\n🌐 访问地址:")
        print("   http://localhost:8501")
        print("\n👤 登录说明:")
        print("   管理员: 输入'管理员'")
        print("   用户: 输入任意姓名")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    final_verification()
