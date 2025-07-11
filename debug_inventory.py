import streamlit as st
import pandas as pd
import json
import os

# 简单的管理员页面测试
st.title("📊 库存管理调试")

# 直接加载和显示数据
if os.path.exists('inventory.json'):
    with open('inventory.json', 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    st.write(f"加载了 {len(inventory)} 个商品")
    
    if inventory:
        # 计算销售数据
        orders = []
        if os.path.exists('orders.json'):
            with open('orders.json', 'r', encoding='utf-8') as f:
                orders = json.load(f)
        
        sales_data = {}
        for order in orders:
            for item in order.get('items', []):
                product_id = item.get('product_id')
                quantity = item.get('quantity', 0)
                if product_id in sales_data:
                    sales_data[product_id] += quantity
                else:
                    sales_data[product_id] = quantity
        
        # 为每个商品添加销售数量
        for product in inventory:
            product['sold'] = sales_data.get(product['id'], 0)
        
        # 统计信息
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("商品总数", len(inventory))
        with col2:
            total_stock = sum(item['stock'] for item in inventory)
            st.metric("总库存", total_stock)
        with col3:
            total_sold = sum(item['sold'] for item in inventory)
            st.metric("总销售量", total_sold)
        with col4:
            total_value = sum(item['price'] * item['stock'] for item in inventory)
            st.metric("总价值", f"¥{total_value:.2f}")
        with col5:
            low_stock = len([item for item in inventory if item['stock'] < 5])
            st.metric("低库存商品", low_stock)
        
        # 显示数据表格
        st.write("### 商品数据表格")
        df = pd.DataFrame(inventory)
        
        # 检查列是否存在
        st.write("数据列:", df.columns.tolist())
        st.write("数据形状:", df.shape)
        
        # 显示前几行原始数据
        st.write("### 原始数据（前5行）")
        st.dataframe(df.head(), use_container_width=True)
        
        # 尝试格式化显示
        try:
            df_display = df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']].copy()
            df_display.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
            
            # 格式化价格
            df_display['价格'] = df_display['价格'].apply(lambda x: f"¥{float(x):.2f}")
            
            # 格式化时间
            df_display['添加时间'] = pd.to_datetime(df_display['添加时间'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
            df_display['添加时间'] = df_display['添加时间'].fillna('未知时间')
            
            st.write("### 格式化后的数据")
            st.dataframe(df_display, use_container_width=True)
            
        except Exception as e:
            st.error(f"格式化失败: {e}")
            st.write("错误详情:", str(e))
    else:
        st.warning("库存数据为空")
else:
    st.error("inventory.json 文件不存在")
