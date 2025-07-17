import json
import streamlit as st

# 测试数据加载
print("=== 商品数据加载测试 ===")

def load_data(file_path):
    """加载JSON数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载失败: {e}")
        return []

# 测试加载inventory.json
inventory = load_data("inventory.json")
print(f"商品总数: {len(inventory)}")

if inventory:
    print("\n前5个商品:")
    for i, product in enumerate(inventory[:5]):
        print(f"{i+1}. {product.get('name', 'N/A')} - 库存: {product.get('stock', 0)} - 价格: ¥{product.get('price', 0)}")
    
    # 检查有库存的商品
    in_stock = [p for p in inventory if p.get('stock', 0) > 0]
    print(f"\n有库存的商品数量: {len(in_stock)}")
    
    if in_stock:
        print("有库存的商品:")
        for product in in_stock[:5]:
            print(f"- {product.get('name', 'N/A')} (库存: {product.get('stock', 0)})")
else:
    print("没有加载到任何商品数据!")

print("\n=== 测试完成 ===")
