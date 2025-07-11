import streamlit as st
import pandas as pd
import json

# 无任何错误隐藏的纯净版本
st.set_page_config(page_title="库存测试", layout="wide")

st.title("📦 库存数据测试 - 无错误隐藏版本")

# 加载库存数据
try:
    with open('inventory.json', 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    st.success(f"✅ 成功加载 {len(inventory)} 个商品")
    
    if inventory:
        # 添加sold字段
        for product in inventory:
            if 'sold' not in product:
                product['sold'] = 0
        
        # 创建DataFrame
        df = pd.DataFrame(inventory)
        st.write(f"DataFrame形状: {df.shape}")
        st.write(f"列名: {df.columns.tolist()}")
        
        # 重新排列列
        df = df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']]
        df.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
        
        # 格式化
        df['价格'] = df['价格'].apply(lambda x: f"¥{float(x):.2f}")
        df['添加时间'] = pd.to_datetime(df['添加时间'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        df['添加时间'] = df['添加时间'].fillna('未知时间')
        
        st.write("### 方法1: st.dataframe")
        st.dataframe(df, use_container_width=True)
        
        st.write("### 方法2: st.table (前10行)")
        st.table(df.head(10))
        
        st.write("### 方法3: st.write")
        st.write(df.head(5))
        
    else:
        st.warning("库存数据为空")
        
except Exception as e:
    st.error(f"加载失败: {e}")
    import traceback
    st.text(traceback.format_exc())
