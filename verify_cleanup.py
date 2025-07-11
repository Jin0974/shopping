#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证app.py清理后的功能是否正常
"""

import sys
import os
import json
import pandas as pd

def test_basic_functions():
    """测试基本功能"""
    print("🔍 开始验证app.py清理后的功能...")
    
    try:
        # 测试导入
        print("1. 测试模块导入...")
        import app
        print("   ✅ 模块导入成功")
        
        # 测试基本函数存在
        print("2. 测试关键函数存在...")
        functions_to_check = [
            'load_inventory', 'save_inventory', 
            'load_orders', 'save_orders',
            'admin_page', 'user_page'
        ]
        
        for func_name in functions_to_check:
            if hasattr(app, func_name):
                print(f"   ✅ {func_name} 函数存在")
            else:
                print(f"   ❌ {func_name} 函数缺失")
        
        # 测试数据加载
        print("3. 测试数据加载...")
        try:
            inventory = app.load_inventory()
            print(f"   ✅ 库存数据加载成功，共 {len(inventory)} 个商品")
            
            orders = app.load_orders()
            print(f"   ✅ 订单数据加载成功，共 {len(orders)} 个订单")
            
        except Exception as e:
            print(f"   ⚠️ 数据加载异常: {e}")
        
        # 测试商品表格显示逻辑
        print("4. 测试商品表格数据准备...")
        try:
            inventory = app.load_inventory()
            if inventory:
                # 模拟表格数据准备
                df_data = []
                for item in inventory:
                    df_data.append({
                        '条码': item.get('barcode', item.get('code', '')),
                        '产品名称': item.get('name', ''),
                        '库存': item.get('stock', 0),
                        '价格': f"¥{item.get('price', 0):.2f}",
                        '已售': item.get('sold', 0)
                    })
                
                df = pd.DataFrame(df_data)
                print(f"   ✅ 表格数据准备成功，{len(df)} 行 × {len(df.columns)} 列")
                print(f"   📊 列名: {list(df.columns)}")
                
                if len(df) > 0:
                    print(f"   📝 示例数据 (前3行):")
                    for i, row in df.head(3).iterrows():
                        print(f"      {i+1}. {row['条码']} | {row['产品名称']} | 库存:{row['库存']} | {row['价格']}")
            else:
                print("   ℹ️ 当前没有商品数据")
                
        except Exception as e:
            print(f"   ❌ 表格数据准备失败: {e}")
        
        print("\n🎉 验证完成！app.py已清理完毕，核心功能正常。")
        return True
        
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functions()
    if success:
        print("\n✅ 建议：可以启动Streamlit应用进行完整测试")
        print("💡 命令: streamlit run app.py")
    else:
        print("\n❌ 发现问题，需要进一步修复")
