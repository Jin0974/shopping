import json
import pandas as pd
from datetime import datetime

# 测试数据加载
def test_data_loading():
    print("=== 测试数据加载 ===")
    
    # 加载库存数据
    try:
        with open('inventory.json', 'r', encoding='utf-8') as f:
            inventory = json.load(f)
        print(f"✅ 库存数据加载成功，共 {len(inventory)} 个商品")
        
        if inventory:
            # 显示前3个商品
            print("\n前3个商品:")
            for i, item in enumerate(inventory[:3]):
                print(f"  {i+1}. {item.get('name', 'N/A')} - 条码: {item.get('barcode', 'N/A')}")
            
            # 测试DataFrame转换
            df = pd.DataFrame(inventory)
            print(f"\n✅ DataFrame创建成功，形状: {df.shape}")
            print(f"✅ 列名: {df.columns.tolist()}")
            
            # 检查必要的列
            required_columns = ['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"❌ 缺少必要的列: {missing_columns}")
            else:
                print("✅ 所有必要的列都存在")
                
                # 测试数据格式化
                try:
                    df = df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']]
                    df.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
                    
                    # 格式化价格
                    df['价格'] = df['价格'].apply(lambda x: f"¥{float(x):.2f}" if pd.notna(x) and x != '' else "¥0.00")
                    
                    # 格式化时间
                    df['添加时间'] = pd.to_datetime(df['添加时间'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
                    df['添加时间'] = df['添加时间'].fillna('未知时间')
                    
                    print("✅ 数据格式化成功")
                    print(f"✅ 格式化后的DataFrame形状: {df.shape}")
                    
                    # 显示前几行
                    print("\n前3行数据:")
                    print(df.head(3).to_string())
                    
                except Exception as e:
                    print(f"❌ 数据格式化失败: {e}")
        
    except Exception as e:
        print(f"❌ 库存数据加载失败: {e}")

if __name__ == "__main__":
    test_data_loading()
