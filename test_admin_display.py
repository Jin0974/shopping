import streamlit as st
import pandas as pd
import json
import os

# 设置页面配置
st.set_page_config(
    page_title="管理员页面测试",
    page_icon="🛒",
    layout="wide"
)

# 文件路径
INVENTORY_FILE = "inventory.json"

def load_data(filename):
    """加载JSON数据"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"加载数据失败: {e}")
        return []

def main():
    st.title("🧪 管理员页面显示测试")
    
    # 测试数据加载
    st.write("### 1. 测试数据加载")
    inventory = load_data(INVENTORY_FILE)
    st.write(f"库存数据加载结果: {len(inventory)} 个商品")
    
    if not inventory:
        st.warning("⚠️ 没有库存数据，请先添加商品")
        # 创建测试数据
        if st.button("创建测试数据"):
            test_data = [
                {
                    "id": "test001",
                    "barcode": "1234567890",
                    "name": "测试商品1",
                    "price": 10.5,
                    "stock": 100,
                    "description": "这是一个测试商品",
                    "created_at": "2024-01-01 10:00:00"
                },
                {
                    "id": "test002", 
                    "barcode": "1234567891",
                    "name": "测试商品2",
                    "price": 25.8,
                    "stock": 50,
                    "description": "这是另一个测试商品",
                    "created_at": "2024-01-01 11:00:00"
                }
            ]
            
            with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, ensure_ascii=False, indent=2)
            st.success("✅ 测试数据创建成功")
            st.rerun()
        return
    
    # 测试DataFrame转换
    st.write("### 2. 测试DataFrame转换")
    try:
        df = pd.DataFrame(inventory)
        st.write(f"DataFrame创建成功，行数: {len(df)}, 列数: {len(df.columns)}")
        st.write(f"列名: {df.columns.tolist()}")
        
        # 添加销售数量（测试用）
        df['sold'] = [5, 3, 8, 2, 1][:len(df)] if len(df) <= 5 else [1] * len(df)
        
        # 重新排列列
        if all(col in df.columns for col in ['barcode', 'name', 'price', 'stock']):
            df = df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']]
            df.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
            
            # 格式化价格
            df['价格'] = df['价格'].apply(lambda x: f"¥{float(x):.2f}")
            
            st.write("✅ DataFrame格式化成功")
        else:
            st.error("❌ 数据列不完整")
            st.write("现有列:", df.columns.tolist())
            return
            
    except Exception as e:
        st.error(f"❌ DataFrame转换失败: {e}")
        return
    
    # 测试表格显示
    st.write("### 3. 测试表格显示")
    
    # 方法1: st.dataframe
    st.write("**方法1: st.dataframe**")
    try:
        st.dataframe(df, use_container_width=True)
        st.success("✅ st.dataframe 显示成功")
    except Exception as e:
        st.error(f"❌ st.dataframe 显示失败: {e}")
    
    # 方法2: st.table
    st.write("**方法2: st.table (前5行)**")
    try:
        st.table(df.head(5))
        st.success("✅ st.table 显示成功")
    except Exception as e:
        st.error(f"❌ st.table 显示失败: {e}")
    
    # 方法3: st.write
    st.write("**方法3: st.write**")
    try:
        st.write(df)
        st.success("✅ st.write 显示成功")
    except Exception as e:
        st.error(f"❌ st.write 显示失败: {e}")

if __name__ == "__main__":
    main()
