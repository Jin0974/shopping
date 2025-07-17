import streamlit as st
import json

# 简化的商品显示测试
st.title("🔍 商品显示测试")

# 加载商品数据
try:
    with open('inventory.json', 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    st.success(f"✅ 成功加载 {len(inventory)} 件商品")
    
    # 显示前3个商品
    st.subheader("商品列表测试")
    
    for i, product in enumerate(inventory[:3]):
        st.write(f"**商品 {i+1}:**")
        st.write(f"- ID: {product.get('id', 'N/A')}")
        st.write(f"- 名称: {product.get('name', 'N/A')}")
        st.write(f"- 价格: ¥{product.get('price', 0)}")
        st.write(f"- 库存: {product.get('stock', 0)}")
        st.write(f"- 条码: {product.get('barcode', 'N/A')}")
        st.divider()
    
    # 测试列显示
    st.subheader("表格显示测试")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**条码**")
    with col2:
        st.write("**名称**")
    with col3:
        st.write("**价格**")
    with col4:
        st.write("**库存**")
    
    st.divider()
    
    for i, product in enumerate(inventory[:3]):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(product.get('barcode', 'N/A'))
        with col2:
            st.write(product.get('name', 'N/A')[:20] + "...")
        with col3:
            st.write(f"¥{product.get('price', 0)}")
        with col4:
            st.write(product.get('stock', 0))
    
except Exception as e:
    st.error(f"❌ 加载失败：{e}")
