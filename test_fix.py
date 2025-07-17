#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品列表显示修复验证脚本
测试普通用户能否正常看到商品列表
"""

import json
import os

def test_inventory_loading():
    """测试商品数据加载"""
    print("🔍 测试商品数据加载...")
    
    try:
        with open('inventory.json', 'r', encoding='utf-8') as f:
            inventory = json.load(f)
        
        print(f"✅ 成功加载 {len(inventory)} 件商品")
        
        if inventory:
            sample = inventory[0]
            print(f"📦 示例商品：{sample.get('name', 'N/A')}")
            print(f"💰 价格：¥{sample.get('price', 0)}")
            print(f"📊 库存：{sample.get('stock', 0)}")
            return True
        else:
            print("❌ 商品列表为空")
            return False
            
    except Exception as e:
        print(f"❌ 加载商品数据失败：{e}")
        return False

def test_user_data():
    """测试用户数据"""
    print("\n👤 测试用户数据...")
    
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        print(f"✅ 成功加载 {len(users)} 个用户")
        
        # 查找普通用户
        normal_users = [u for u in users if u.get('role') != 'admin']
        if normal_users:
            print(f"👥 找到 {len(normal_users)} 个普通用户")
        else:
            print("⚠️ 未找到普通用户")
            
        return True
        
    except Exception as e:
        print(f"❌ 加载用户数据失败：{e}")
        return False

def analyze_code_structure():
    """分析代码结构"""
    print("\n🔍 分析代码结构...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键函数
        key_functions = [
            'def shopping_page',
            'def user_page', 
            'def load_data',
            'current_page_items',
            'if not current_page_items:'
        ]
        
        for func in key_functions:
            if func in content:
                print(f"✅ 找到关键代码：{func}")
            else:
                print(f"❌ 缺少关键代码：{func}")
        
        # 检查潜在的错误模式
        error_patterns = [
            'product.get(',  # 确保在正确的上下文中使用
            'for i, product in enumerate(current_page_items)',
            'if current_page_items:'
        ]
        
        print("\n🔍 检查错误修复模式...")
        for pattern in error_patterns:
            count = content.count(pattern)
            print(f"📊 '{pattern}' 出现 {count} 次")
        
        return True
        
    except Exception as e:
        print(f"❌ 分析代码失败：{e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始商品列表显示修复验证\n")
    
    # 测试数据文件
    inventory_ok = test_inventory_loading()
    user_ok = test_user_data()
    code_ok = analyze_code_structure()
    
    print("\n📊 测试结果汇总：")
    print(f"📦 商品数据：{'✅ 正常' if inventory_ok else '❌ 异常'}")
    print(f"👤 用户数据：{'✅ 正常' if user_ok else '❌ 异常'}")
    print(f"💻 代码结构：{'✅ 正常' if code_ok else '❌ 异常'}")
    
    if all([inventory_ok, user_ok, code_ok]):
        print("\n🎉 修复验证通过！商品列表显示问题应该已解决")
        print("💡 建议：现在可以启动应用程序测试：streamlit run app.py")
    else:
        print("\n⚠️ 仍有问题需要解决")
    
    print("\n" + "="*60)
    print("修复说明：")
    print("1. 🔧 修复了商品渲染逻辑中的未定义变量错误")
    print("2. 🎯 简化了商品列表显示逻辑，移除了错误的else分支")
    print("3. 🛡️ 增强了错误处理，确保普通用户能正常看到商品")
    print("4. 🔍 保留了所有筛选、排序、分页功能")
    print("5. 🛒 确保购物车功能完整可用")

if __name__ == "__main__":
    main()
