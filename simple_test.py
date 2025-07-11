import streamlit as st
import pandas as pd
import json

# 最简单的测试版本
st.title("📦 数据显示测试")

# 加载数据
try:
    with open('inventory.json', 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    st.success(f"✅ 加载了 {len(inventory)} 个商品")
    
    if inventory:
        # 显示前几个商品的原始数据
        st.write("### 原始数据（前3个商品）")
        for i, item in enumerate(inventory[:3]):
            st.write(f"**商品 {i+1}:**")
            st.json(item)
        
        # 转换为DataFrame
        df = pd.DataFrame(inventory)
        st.write(f"### DataFrame信息")
        st.write(f"形状: {df.shape}")
        st.write(f"列名: {df.columns.tolist()}")
        
        # 显示原始DataFrame
        st.write("### 原始DataFrame（前10行）")
        st.dataframe(df.head(10))
        
        # 尝试格式化显示
        st.write("### 格式化后的数据")
        try:
            # 确保有sold字段
            if 'sold' not in df.columns:
                df['sold'] = 0
            
            # 选择需要的列
            display_df = df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']].copy()
            display_df.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
            
            # 格式化价格
            display_df['价格'] = display_df['价格'].apply(lambda x: f"¥{float(x):.2f}")
            
            # 格式化时间
            display_df['添加时间'] = pd.to_datetime(display_df['添加时间'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
            display_df['添加时间'] = display_df['添加时间'].fillna('未知时间')
            
            st.dataframe(display_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"格式化失败: {e}")
            st.write("错误详情:", str(e))
            
    else:
        st.warning("数据为空")
        
except Exception as e:
    st.error(f"加载数据失败: {e}")
    st.write("错误详情:", str(e))
