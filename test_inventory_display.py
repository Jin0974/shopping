import streamlit as st
import pandas as pd
import json
import os

# 简化的测试页面
st.title("📦 库存数据测试")

# 检查文件是否存在
if os.path.exists('inventory.json'):
    st.success("✅ inventory.json 文件存在")
    
    # 加载数据
    try:
        with open('inventory.json', 'r', encoding='utf-8') as f:
            inventory = json.load(f)
        
        st.success(f"✅ 数据加载成功，共 {len(inventory)} 个商品")
        
        if inventory:
            # 显示原始数据
            st.subheader("原始数据（前3个商品）")
            st.json(inventory[:3])
            
            # 转换为DataFrame
            df = pd.DataFrame(inventory)
            st.subheader("DataFrame信息")
            st.write(f"形状: {df.shape}")
            st.write(f"列名: {df.columns.tolist()}")
            
            # 检查必要的列
            required_columns = ['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ 缺少必要的列: {missing_columns}")
            else:
                st.success("✅ 所有必要的列都存在")
                
                # 显示数据
                st.subheader("商品数据表")
                
                # 安全地重新排列列
                try:
                    df_display = df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']].copy()
                    df_display.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
                    
                    # 格式化价格
                    df_display['价格'] = df_display['价格'].apply(lambda x: f"¥{float(x):.2f}" if pd.notna(x) and x != '' else "¥0.00")
                    
                    # 格式化时间
                    df_display['添加时间'] = pd.to_datetime(df_display['添加时间'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
                    df_display['添加时间'] = df_display['添加时间'].fillna('未知时间')
                    
                    st.dataframe(df_display, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ 数据格式化失败: {e}")
                    st.write("错误详情:", str(e))
                    
                    # 显示未格式化的数据
                    st.subheader("未格式化的数据")
                    st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ 库存数据为空")
            
    except Exception as e:
        st.error(f"❌ 数据加载失败: {e}")
        st.write("错误详情:", str(e))
else:
    st.error("❌ inventory.json 文件不存在")
