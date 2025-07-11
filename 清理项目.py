#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理项目文件，只保留部署需要的文件
"""

import os
import shutil

def clean_project():
    """清理项目，只保留部署必要文件"""
    print("🧹 清理项目文件...")
    
    # 要删除的文件列表
    files_to_delete = [
        "clean_test.py",
        "debug_app.py", 
        "debug_inventory.py",
        "final_check.py",
        "simple_test.py",
        "test_admin_display.py",
        "test_app.py",
        "test_data_loading.py", 
        "test_inventory_display.py",
        "test_stability.py",
        "test_startup.py",
        "verify_cleanup.py",
        "app_backup.py",
        "start.bat",
        "start_clean.bat", 
        "start_debug.bat",
        "start_simple_test.bat",
        "启动系统.bat"
    ]
    
    # 要删除的文件夹
    folders_to_delete = [
        "__pycache__"
    ]
    
    deleted_count = 0
    
    # 删除文件
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"   ✅ 删除文件: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ 删除失败: {file} - {e}")
    
    # 删除文件夹
    for folder in folders_to_delete:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"   ✅ 删除文件夹: {folder}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ 删除失败: {folder} - {e}")
    
    print(f"\n🎉 清理完成！删除了 {deleted_count} 个文件/文件夹")
    
    # 显示保留的文件
    print("\n📁 保留的核心文件:")
    keep_files = [
        "app.py",
        "requirements.txt", 
        ".streamlit/config.toml",
        ".gitignore",
        "README_部署版.md",
        "部署指南.md",
        "商品导入模板.csv",
        "测试导入.csv"
    ]
    
    for file in keep_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (缺失)")

if __name__ == "__main__":
    clean_project()
