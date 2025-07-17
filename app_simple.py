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
    page_title="内购系统",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 数据文件路径
INVENTORY_FILE = "inventory.json"
ORDERS_FILE = "orders.json"
USERS_FILE = "users.json"

# 初始化数据文件
def initialize_data():
    """初始化数据文件"""
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    
    if not os.path.exists(USERS_FILE):
        # 创建默认管理员
        default_users = [
            {"username": "admin", "password": "admin123", "role": "admin", "name": "管理员"}
        ]
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_users, f, ensure_ascii=False, indent=2)

# 加载数据
def load_data(file_path):
    """加载JSON数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# 保存数据
def save_data(file_path, data):
    """保存JSON数据"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 登录页面
def login_page():
    """登录页面"""
    st.title("🏪 内购系统登录")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 用户登录")
        
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        
        if st.button("登录", use_container_width=True):
            users = load_data(USERS_FILE)
            
            for user in users:
                if user['username'] == username and user['password'] == password:
                    st.session_state.user = user
                    st.success("登录成功！")
                    st.rerun()
                    return
            
            st.error("用户名或密码错误")

# 简化的商品购买页面
def shopping_page():
    """商品购买页面 - 简化版本"""
    inventory = load_data(INVENTORY_FILE)
    
    if not inventory:
        st.info("暂无商品可购买")
        return

    # 购物车
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # 商品列表
    st.subheader("🛍️ 商品列表")
    
    # 简单的表格表头
    col1, col2, col3, col4, col5 = st.columns([2, 3, 1, 1, 1])
    
    with col1:
        st.write("**条码**")
    with col2:
        st.write("**商品名称**")
    with col3:
        st.write("**价格**")
    with col4:
        st.write("**库存**")
    with col5:
        st.write("**操作**")
    
    st.divider()
    
    # 显示所有商品
    for i, product in enumerate(inventory):
        col1, col2, col3, col4, col5 = st.columns([2, 3, 1, 1, 1])
        
        with col1:
            st.write(product.get('barcode', 'N/A'))
        
        with col2:
            st.write(product['name'])
        
        with col3:
            st.write(f"¥{product['price']:.2f}")
        
        with col4:
            if product['stock'] > 0:
                st.write(f"✅ {product['stock']}")
            else:
                st.write("❌ 缺货")
        
        with col5:
            if product['stock'] > 0:
                if st.button("加入购物车", key=f"add_{i}"):
                    # 检查购物车中是否已有该商品
                    existing_item = None
                    for item in st.session_state.cart:
                        if item['product_id'] == product['id']:
                            existing_item = item
                            break
                    
                    if existing_item:
                        existing_item['quantity'] += 1
                    else:
                        st.session_state.cart.append({
                            'product_id': product['id'],
                            'product_name': product['name'],
                            'price': product['price'],
                            'quantity': 1
                        })
                    
                    st.success(f"已添加 {product['name']} 到购物车")
                    st.rerun()
            else:
                st.write("缺货")
    
    # 购物车显示
    if st.session_state.cart:
        st.subheader("🛒 购物车")
        
        total_amount = 0
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(item['product_name'])
            with col2:
                st.write(f"¥{item['price']:.2f}")
            with col3:
                st.write(f"x{item['quantity']}")
            with col4:
                if st.button("删除", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            
            total_amount += item['price'] * item['quantity']
        
        st.write(f"**总计: ¥{total_amount:.2f}**")
        
        if st.button("结算"):
            # 简化的结算流程
            orders = load_data(ORDERS_FILE)
            
            order = {
                'id': str(uuid.uuid4())[:8],
                'user_name': st.session_state.user['name'],
                'items': st.session_state.cart.copy(),
                'total_amount': total_amount,
                'created_at': datetime.now().isoformat(),
                'status': 'completed'
            }
            
            orders.append(order)
            save_data(ORDERS_FILE, orders)
            
            # 更新库存
            inventory = load_data(INVENTORY_FILE)
            for cart_item in st.session_state.cart:
                for product in inventory:
                    if product['id'] == cart_item['product_id']:
                        product['stock'] -= cart_item['quantity']
                        break
            save_data(INVENTORY_FILE, inventory)
            
            st.success("订单已提交！")
            st.session_state.cart = []
            st.rerun()

# 用户页面
def user_page():
    """用户页面"""
    st.title("🛒 内购商城")
    
    # 创建选项卡
    tab1, tab2 = st.tabs(["🛍️ 商品购买", "📋 订单历史"])
    
    with tab1:
        shopping_page()
    
    with tab2:
        st.subheader("📋 我的订单")
        orders = load_data(ORDERS_FILE)
        user_orders = [order for order in orders if order.get('user_name') == st.session_state.user['name']]
        
        if user_orders:
            for order in user_orders:
                with st.expander(f"订单 {order['id']} - {order['created_at'][:10]}"):
                    st.write(f"**总金额**: ¥{order['total_amount']:.2f}")
                    st.write("**商品明细**:")
                    for item in order['items']:
                        st.write(f"- {item['product_name']} x{item['quantity']} = ¥{item['price'] * item['quantity']:.2f}")
        else:
            st.info("暂无订单记录")

# 管理员页面
def admin_page():
    """管理员页面"""
    st.title("📊 管理员控制面板")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["📊 数据统计", "📦 库存管理", "📋 订单管理", "👥 用户管理"])
    
    with tab1:
        inventory = load_data(INVENTORY_FILE)
        orders = load_data(ORDERS_FILE)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("商品总数", len(inventory))
        with col2:
            total_stock = sum(item['stock'] for item in inventory)
            st.metric("总库存", total_stock)
        with col3:
            st.metric("订单总数", len(orders))
        with col4:
            total_sales = sum(order['total_amount'] for order in orders)
            st.metric("总销售额", f"¥{total_sales:.2f}")
    
    with tab2:
        st.subheader("📦 商品库存管理")
        
        # 添加新商品
        with st.expander("➕ 添加新商品"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("商品名称")
                new_price = st.number_input("价格", min_value=0.01, value=1.0, step=0.01)
            
            with col2:
                new_stock = st.number_input("库存数量", min_value=0, value=1, step=1)
                new_barcode = st.text_input("条码")
            
            if st.button("添加商品"):
                if new_name and new_price > 0:
                    inventory = load_data(INVENTORY_FILE)
                    
                    new_product = {
                        'id': str(uuid.uuid4())[:8],
                        'name': new_name,
                        'price': new_price,
                        'stock': new_stock,
                        'barcode': new_barcode,
                        'purchase_limit': 0,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    inventory.append(new_product)
                    save_data(INVENTORY_FILE, inventory)
                    
                    st.success("商品添加成功！")
                    st.rerun()
                else:
                    st.error("请填写必要信息")
        
        # 显示现有商品
        inventory = load_data(INVENTORY_FILE)
        
        if inventory:
            st.write("**当前商品列表:**")
            for i, product in enumerate(inventory):
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                
                with col1:
                    st.write(product['name'])
                with col2:
                    st.write(f"¥{product['price']:.2f}")
                with col3:
                    st.write(product['stock'])
                with col4:
                    st.write(product.get('barcode', 'N/A'))
                with col5:
                    if st.button("删除", key=f"del_{i}"):
                        inventory.pop(i)
                        save_data(INVENTORY_FILE, inventory)
                        st.rerun()
    
    with tab3:
        st.subheader("📋 订单管理")
        orders = load_data(ORDERS_FILE)
        
        if orders:
            for order in orders:
                with st.expander(f"订单 {order['id']} - {order.get('user_name', 'N/A')}"):
                    st.write(f"**时间**: {order['created_at']}")
                    st.write(f"**总金额**: ¥{order['total_amount']:.2f}")
                    st.write("**商品明细**:")
                    for item in order['items']:
                        st.write(f"- {item['product_name']} x{item['quantity']} = ¥{item['price'] * item['quantity']:.2f}")
        else:
            st.info("暂无订单")
    
    with tab4:
        st.subheader("👥 用户管理")
        users = load_data(USERS_FILE)
        
        # 添加新用户
        with st.expander("➕ 添加新用户"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("用户名")
                new_password = st.text_input("密码", type="password")
            
            with col2:
                new_name = st.text_input("姓名")
                new_role = st.selectbox("角色", ["user", "admin"])
            
            if st.button("添加用户"):
                if new_username and new_password and new_name:
                    # 检查用户名是否已存在
                    if any(user['username'] == new_username for user in users):
                        st.error("用户名已存在")
                    else:
                        new_user = {
                            'username': new_username,
                            'password': new_password,
                            'name': new_name,
                            'role': new_role
                        }
                        
                        users.append(new_user)
                        save_data(USERS_FILE, users)
                        
                        st.success("用户添加成功！")
                        st.rerun()
                else:
                    st.error("请填写所有信息")
        
        # 显示现有用户
        if users:
            st.write("**当前用户列表:**")
            for i, user in enumerate(users):
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(user['username'])
                with col2:
                    st.write(user['name'])
                with col3:
                    st.write(user['role'])
                with col4:
                    if user['username'] != 'admin':  # 保护默认管理员
                        if st.button("删除", key=f"del_user_{i}"):
                            users.pop(i)
                            save_data(USERS_FILE, users)
                            st.rerun()

# 主函数
def main():
    # 初始化数据
    initialize_data()
    
    # 侧边栏
    with st.sidebar:
        st.title("🏪 内购系统")
        
        if 'user' not in st.session_state:
            st.write("请先登录")
        else:
            st.write(f"欢迎, {st.session_state.user['name']}")
            if st.button("退出登录"):
                del st.session_state.user
                if 'cart' in st.session_state:
                    del st.session_state.cart
                st.rerun()
    
    # 主页面
    if 'user' not in st.session_state:
        login_page()
    else:
        if st.session_state.user['role'] == 'admin':
            admin_page()
        else:
            user_page()

if __name__ == "__main__":
    main()
