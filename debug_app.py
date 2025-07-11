import streamlit as st
import pandas as pd
import json
import os
import time
import contextlib
import io
from datetime import datetime
import uuid

# 设置页面配置
st.set_page_config(
    page_title="内购系统-调试版",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 调试模式：不隐藏错误
st.markdown("""
<style>
.debug-info {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# 数据文件路径
INVENTORY_FILE = "inventory.json"
ORDERS_FILE = "orders.json"
USERS_FILE = "users.json"

# 简化的数据加载函数
@st.cache_data
def load_data(file_path):
    """加载JSON数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"加载数据失败: {file_path} - {e}")
        return []

# 简化的库存管理函数
def inventory_management():
    """库存管理-调试版"""
    st.subheader("📦 库存管理")
    
    # 加载库存数据
    inventory = load_data(INVENTORY_FILE)
    st.write(f"🔍 调试信息: 加载了 {len(inventory)} 个商品")
    
    if inventory:
        # 加载订单数据计算销售
        orders = load_data(ORDERS_FILE)
        st.write(f"🔍 调试信息: 加载了 {len(orders)} 个订单")
        
        # 计算销售数据
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
        
        try:
            df = pd.DataFrame(inventory)
            st.write(f"🔍 调试信息: DataFrame形状 {df.shape}")
            st.write(f"🔍 调试信息: 列名 {df.columns.tolist()}")
            
            # 检查必要的列
            required_columns = ['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ 缺少必要的列: {missing_columns}")
                st.write("现有列：", df.columns.tolist())
                return
            
            # 重新排列列的顺序
            df = df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']]
            df.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
            
            # 格式化价格列
            df['价格'] = df['价格'].apply(lambda x: f"¥{float(x):.2f}" if pd.notna(x) and x != '' else "¥0.00")
            
            # 格式化添加时间
            df['添加时间'] = pd.to_datetime(df['添加时间'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
            df['添加时间'] = df['添加时间'].fillna('未知时间')
            
            st.write("✅ 数据格式化完成")
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ 数据处理失败: {e}")
            st.write("错误详情:", str(e))
            
            # 显示原始数据
            st.write("### 原始数据（前10行）")
            try:
                raw_df = pd.DataFrame(inventory[:10])
                st.dataframe(raw_df, use_container_width=True)
            except Exception as e2:
                st.error(f"连原始数据也无法显示: {e2}")
    else:
        st.info("📦 暂无商品库存")

# 主函数
def main():
    st.title("🛒 内购系统调试版")
    st.markdown('<div class="debug-info">🔍 调试模式已启用，显示详细错误信息</div>', unsafe_allow_html=True)
    
    # 直接显示库存管理
    inventory_management()

if __name__ == "__main__":
    main()
