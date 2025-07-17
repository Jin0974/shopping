import streamlit as st
import json

st.title("🛒 商品显示测试")

# 加载数据函数
def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"加载失败: {e}")
        return []

# 加载商品数据
inventory = load_data("inventory.json")

st.write(f"**数据加载结果:** 共 {len(inventory)} 件商品")

if not inventory:
    st.error("没有加载到商品数据！请检查 inventory.json 文件")
    st.stop()

# 显示前几个商品的原始数据
st.write("**原始数据样例:**")
for i, product in enumerate(inventory[:3]):
    st.json(product)

# 筛选有库存的商品
in_stock_products = [p for p in inventory if p.get('stock', 0) > 0]
st.write(f"**有库存的商品:** {len(in_stock_products)} 件")

# 简单的商品列表显示
st.write("**商品列表:**")

if in_stock_products:
    # 创建表格表头
    col1, col2, col3, col4 = st.columns([2, 3, 1, 1])
    with col1:
        st.write("**条码**")
    with col2:
        st.write("**商品名称**")
    with col3:
        st.write("**库存**")
    with col4:
        st.write("**价格**")
    
    st.divider()
    
    # 显示商品
    for product in in_stock_products[:10]:  # 只显示前10个
        col1, col2, col3, col4 = st.columns([2, 3, 1, 1])
        
        with col1:
            st.write(product.get('barcode', 'N/A'))
        
        with col2:
            st.write(product.get('name', 'N/A'))
        
        with col3:
            stock = product.get('stock', 0)
            if stock > 10:
                st.write(f":green[{stock}]")
            elif stock > 0:
                st.write(f":orange[{stock}]")
            else:
                st.write(f":red[{stock}]")
        
        with col4:
            st.write(f"¥{product.get('price', 0):.2f}")
else:
    st.warning("没有找到有库存的商品")

# 调试信息
st.write("---")
st.write("**调试信息:**")
st.write(f"- 总商品数: {len(inventory)}")
st.write(f"- 有库存商品数: {len(in_stock_products)}")

if inventory:
    stock_counts = {}
    for product in inventory:
        stock = product.get('stock', 0)
        if stock == 0:
            stock_counts['缺货'] = stock_counts.get('缺货', 0) + 1
        elif stock <= 10:
            stock_counts['库存紧张'] = stock_counts.get('库存紧张', 0) + 1
        else:
            stock_counts['库存充足'] = stock_counts.get('库存充足', 0) + 1
    
    st.write("**库存统计:**")
    for status, count in stock_counts.items():
        st.write(f"- {status}: {count} 件")
