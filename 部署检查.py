#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
部署前检查脚本
确保所有必要文件都已准备就绪
"""

import os
import sys

def check_deployment_readiness():
    """检查部署准备情况"""
    print("🔍 检查Streamlit部署准备情况...")
    print("=" * 50)
    
    # 必要文件检查
    required_files = {
        'app.py': '主应用文件',
        'requirements.txt': 'Python依赖文件',
        '.streamlit/config.toml': 'Streamlit配置文件',
        '.gitignore': 'Git忽略文件',
        '部署指南.md': '部署说明文档'
    }
    
    missing_files = []
    
    print("1. 📁 文件检查:")
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} - {description}")
        else:
            print(f"   ❌ {file_path} - {description} (缺失)")
            missing_files.append(file_path)
    
    # Python语法检查
    print("\n2. 🐍 Python语法检查:")
    try:
        import py_compile
        py_compile.compile('app.py', doraise=True)
        print("   ✅ app.py 语法正确")
    except Exception as e:
        print(f"   ❌ app.py 语法错误: {e}")
        return False
    
    # 依赖包检查
    print("\n3. 📦 依赖包检查:")
    try:
        import streamlit
        import pandas
        import openpyxl
        print("   ✅ 所有必要包已安装")
        print(f"   📊 Streamlit版本: {streamlit.__version__}")
        print(f"   📊 Pandas版本: {pandas.__version__}")
    except ImportError as e:
        print(f"   ❌ 依赖包缺失: {e}")
        print("   💡 请运行: pip install -r requirements.txt")
        return False
    
    # 模块导入检查
    print("\n4. 🔧 模块导入检查:")
    try:
        import app
        print("   ✅ app.py 模块导入成功")
    except Exception as e:
        print(f"   ❌ app.py 导入失败: {e}")
        return False
    
    # 配置文件检查
    print("\n5. ⚙️ 配置文件检查:")
    config_file = '.streamlit/config.toml'
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_content = f.read()
            if '[general]' in config_content and '[server]' in config_content:
                print("   ✅ Streamlit配置文件格式正确")
            else:
                print("   ⚠️ Streamlit配置文件可能格式不完整")
    
    # 总结
    print("\n" + "=" * 50)
    if missing_files:
        print("❌ 部署准备未完成")
        print("缺失文件:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("🎉 部署准备已完成！")
        print("\n📋 下一步操作:")
        print("1. 将代码推送到GitHub仓库")
        print("2. 访问 https://share.streamlit.io/")
        print("3. 选择你的GitHub仓库")
        print("4. 设置主文件为 app.py")
        print("5. 点击Deploy部署")
        print("\n🌐 部署后访问地址格式:")
        print("   https://your-app-name.streamlit.app/")
        return True

if __name__ == "__main__":
    success = check_deployment_readiness()
    if not success:
        sys.exit(1)
