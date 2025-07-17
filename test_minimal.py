import streamlit as st
import json

# 极简商品显示测试
st.title("🔍 极简商品显示测试")

# 模拟用户登录状态
if 'user' not in st.session_state:
    st.session_state.user = {'name': 'test_user', 'role': 'user'}

# 加载商品数据
try:
    with open('inventory.json', 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    st.success(f"✅ 成功加载 {len(inventory)} 件商品")
    
    # 极简显示
    st.subheader("📦 商品列表")
    
    for i, product in enumerate(inventory):
        st.write(f"**{i+1}. {product.get('name', 'N/A')}**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"价格: ¥{product.get('price', 0)}")
        with col2:
            st.write(f"库存: {product.get('stock', 0)}")
        with col3:
            st.write(f"条码: {product.get('barcode', 'N/A')}")
        
        st.write("---")
    
except Exception as e:
    st.error(f"❌ 加载失败：{e}")
