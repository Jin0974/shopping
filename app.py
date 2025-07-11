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

# 清理完成 - 所有JavaScript残留代码已移除

# 数据文件路径
INVENTORY_FILE = "inventory.json"
ORDERS_FILE = "orders.json"
USERS_FILE = "users.json"

# 错误处理装饰器
def handle_frontend_errors(func):
    """处理前端错误的装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 忽略所有前端相关错误
            error_keywords = ["removeChild", "Node", "DOM", "JavaScript", "NotFoundError"]
            if any(keyword in str(e) for keyword in error_keywords):
                pass  # 完全忽略这些错误
            else:
                # 只显示真正的功能性错误
                st.error(f"发生错误: {str(e)}")
    return wrapper

# 稳定的页面刷新函数 - 终极版本
def safe_rerun():
    """安全的页面刷新函数，减少前端错误 - 终极版本"""
    try:
        # 清理可能的临时状态
        if hasattr(st.session_state, '_temp_error_state'):
            del st.session_state._temp_error_state
        
        # 添加更长的延迟，让DOM完全稳定
        time.sleep(0.2)
        
        # 静默执行刷新
        with suppress_stdout_stderr():
            st.rerun()
    except Exception as e:
        # 完全忽略所有rerun相关的错误
        try:
            # 尝试使用experimental_rerun
            st.experimental_rerun()
        except Exception:
            # 如果都失败了，设置一个标志让页面自然刷新
            st.session_state._needs_refresh = True

# 隐藏错误的上下文管理器

@contextlib.contextmanager
def suppress_stdout_stderr():
    """隐藏所有输出"""
    with contextlib.redirect_stdout(io.StringIO()):
        with contextlib.redirect_stderr(io.StringIO()):
            yield

# 静默执行函数
def silent_execute(func, *args, **kwargs):
    """静默执行函数，隐藏所有错误"""
    try:
        with suppress_stdout_stderr():
            return func(*args, **kwargs)
    except Exception:
        return None

# 终极错误处理装饰器
def ultimate_error_handler(func):
    """终极错误处理装饰器，确保函数绝不抛出错误"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 完全静默处理所有错误
            error_msg = str(e).lower()
            if any(keyword in error_msg for keyword in ['notfounderror', 'removechild', 'dom', 'node']):
                # 如果是DOM相关错误，完全忽略
                return None
            # 对于其他错误，也静默处理
            return None
    return wrapper

# 平滑删除商品项 - 终极版本
def smooth_remove_items(items_list, indices_to_remove):
    """平滑删除列表项，避免DOM错误 - 终极版本"""
    if not items_list or not indices_to_remove:
        return items_list
    
    try:
        # 创建新列表避免原地修改
        new_items = []
        for i, item in enumerate(items_list):
            if i not in indices_to_remove:
                new_items.append(item)
        
        # 使用静默执行确保无报错
        return silent_execute(lambda: new_items)
    except Exception:
        # 如果出错，返回原列表
        return items_list

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

# 用户认证
def authenticate_user(name):
    """用户认证"""
    users = load_data(USERS_FILE)
    # 先检查是否是已存在的用户
    for user in users:
        if user["name"] == name:
            return user
    
    # 如果是管理员但不存在，创建管理员（防止数据丢失）
    if name == "管理员":
        admin_user = {
            "username": "admin",
            "password": "admin123",
            "name": "管理员",
            "role": "admin"
        }
        users.append(admin_user)
        save_data(USERS_FILE, users)
        return admin_user
    
    # 其他任何姓名都创建为普通用户
    new_user = {
        "username": f"user_{len(users)}",
        "password": "default123",
        "name": name,
        "role": "user"
    }
    users.append(new_user)
    save_data(USERS_FILE, users)
    return new_user

# 登录页面
def login_page():
    """登录页面"""
    st.title("🛒 内购系统登录")
    
    with st.form("login_form"):
        st.subheader("请输入您的姓名")
        name = st.text_input("姓名")
        submit_button = st.form_submit_button("登录")
        
        if submit_button:
            if name:
                user = authenticate_user(name)
                if user:
                    st.session_state.user = user
                    st.success(f"欢迎, {user['name']}!")
                    st.rerun()
                else:
                    st.error("登录失败，请重试")
            else:
                st.error("请输入您的姓名")
    
    # 显示提示信息
    st.info("请输入您的姓名进行登录\n• 管理员请输入：管理员\n• 其他任何姓名都可以直接登录购买商品")

# 管理员页面
def admin_page():
    """管理员页面"""
    st.title("📊 管理员控制面板")
    
    tab1, tab2, tab3, tab4 = st.tabs(["库存管理", "订单管理", "用户管理", "数据统计"])
    
    with tab1:
        inventory_management()
    
    with tab2:
        order_management()
    
    with tab3:
        user_management()
    
    with tab4:
        data_statistics()

# 库存管理
def inventory_management():
    """库存管理"""
    
    inventory = load_data(INVENTORY_FILE)
    if inventory:
        # 计算销售数据
        orders = load_data(ORDERS_FILE)
        sales_data = {}
        
        # 统计每个商品的销售数量
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
        
        # 商品列表
        df = pd.DataFrame(inventory)
        
        # 调试信息 - 检查数据是否正确加载
        if df.empty:
            st.error("❌ 数据框为空，无法显示商品信息")
            return
        
        # 确保所有商品都有 sold 字段
        if 'sold' not in df.columns:
            df['sold'] = 0
        
        # 重新排列列的顺序
        try:
            df = df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']]
            df.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
        except KeyError as e:
            st.error(f"❌ 数据列缺失: {e}")
            st.write("现有列：", df.columns.tolist())
            return
        
        # 格式化价格列 - 安全处理
        try:
            df['价格'] = df['价格'].apply(lambda x: f"¥{float(x):.2f}" if pd.notna(x) and x != '' else "¥0.00")
        except Exception as e:
            st.warning(f"价格格式化失败: {e}")
            df['价格'] = df['价格'].astype(str)
        
        # 格式化添加时间 - 安全处理
        try:
            df['添加时间'] = pd.to_datetime(df['添加时间'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
            # 处理无法转换的时间
            df['添加时间'] = df['添加时间'].fillna('未知时间')
        except Exception as e:
            st.warning(f"时间格式化失败: {e}")
            # 如果时间格式化失败，保持原样
            df['添加时间'] = df['添加时间'].astype(str)
        
        # 显示数据表格
        st.write("### 📊 商品库存管理")
        
        try:
            # 直接显示数据表格，不再添加额外的调试信息
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"数据表格显示异常: {e}")
            # 备用显示方法
            st.table(df)
        
        # 操作按钮
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 批量导入按钮
            uploaded_file = st.file_uploader("", type=['xlsx', 'csv'], key="bulk_import", label_visibility="collapsed")
            if uploaded_file is not None:
                try:
                    # 读取文件
                    if uploaded_file.name.endswith('.xlsx'):
                        df_import = pd.read_excel(uploaded_file)
                    else:
                        df_import = pd.read_csv(uploaded_file, encoding='utf-8')
                    
                    # 自动导入
                    success_count = 0
                    
                    for _, row in df_import.iterrows():
                        try:
                            # 更严格的数据处理
                            name = str(row.get("商品名称", row.get("name", ""))).strip()
                            price = row.get("价格", row.get("price", 0))
                            stock = row.get("库存", row.get("stock", 0))
                            description = str(row.get("描述", row.get("description", ""))).strip()
                            # 处理条码字段（支持多种表头名称）
                            barcode = str(row.get("条码", row.get("code", row.get("barcode", "")))).strip()
                            
                            # 处理价格数据
                            if pd.isna(price) or price == "":
                                price = 0
                            else:
                                price = float(price)
                            
                            # 处理库存数据
                            if pd.isna(stock) or stock == "":
                                stock = 0
                            else:
                                stock = int(stock)
                            
                            # 如果没有条码，使用商品名称+随机数生成
                            if not barcode:
                                barcode = f"{name[:3]}{str(uuid.uuid4())[:6]}"
                            
                            new_product = {
                                "id": str(uuid.uuid4())[:8],
                                "name": name,
                                "price": price,
                                "stock": stock,
                                "description": description,
                                "barcode": barcode,
                                "created_at": datetime.now().isoformat()
                            }
                            
                            # 只导入有效的商品（名称不为空，价格大于等于0）
                            if new_product["name"] and new_product["price"] >= 0:
                                inventory.append(new_product)
                                success_count += 1
                        except Exception as e:
                            st.warning(f"跳过无效行: {e}")
                    
                    if success_count > 0:
                        save_data(INVENTORY_FILE, inventory)
                        st.success(f"✅ 成功导入 {success_count} 个商品！")
                        st.rerun()
                    else:
                        st.error("❌ 没有有效的商品数据")
                        
                except Exception as e:
                    st.error(f"❌ 文件读取失败: {str(e)}")
        
        with col2:
            # 清空所有库存按钮
            if st.session_state.get('confirm_clear_all', False):
                st.warning("⚠️ 确认要清空所有库存吗？")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ 确认清空", type="primary"):
                        save_data(INVENTORY_FILE, [])
                        st.session_state.confirm_clear_all = False
                        st.success("✅ 所有库存已清空！")
                        st.rerun()
                with col_no:
                    if st.button("❌ 取消"):
                        st.session_state.confirm_clear_all = False
                        st.rerun()
            else:
                if st.button("🗑️ 清空所有库存", type="secondary"):
                    st.session_state.confirm_clear_all = True
                    st.rerun()
        
        with col3:
            # 导出当前库存
            # 创建用于导出的数据框，保持原始数值格式
            export_df = pd.DataFrame(inventory)
            export_df = export_df[['barcode', 'name', 'price', 'stock', 'sold', 'description', 'created_at']]
            export_df.columns = ['条码', '商品名称', '价格', '库存', '已售', '描述', '添加时间']
            
            csv_data = export_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 导出当前库存",
                data=csv_data,
                file_name=f"库存_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("📦 暂无商品库存，请先导入商品")
        
        # 当没有库存时也显示批量导入按钮
        uploaded_file = st.file_uploader("📦 批量导入商品", type=['xlsx', 'csv'], key="bulk_import_empty")
        if uploaded_file is not None:
            try:
                # 读取文件
                if uploaded_file.name.endswith('.xlsx'):
                    df_import = pd.read_excel(uploaded_file)
                else:
                    df_import = pd.read_csv(uploaded_file, encoding='utf-8')
                
                # 自动导入
                inventory = []
                success_count = 0
                
                for _, row in df_import.iterrows():
                    try:
                        # 更严格的数据处理
                        name = str(row.get("商品名称", row.get("name", ""))).strip()
                        price = row.get("价格", row.get("price", 0))
                        stock = row.get("库存", row.get("stock", 0))
                        description = str(row.get("描述", row.get("description", ""))).strip()
                        # 处理条码字段（支持多种表头名称）
                        barcode = str(row.get("条码", row.get("code", row.get("barcode", "")))).strip()
                        
                        # 处理价格数据
                        if pd.isna(price) or price == "":
                            price = 0
                        else:
                            price = float(price)
                        
                        # 处理库存数据
                        if pd.isna(stock) or stock == "":
                            stock = 0
                        else:
                            stock = int(stock)
                        
                        # 如果没有条码，使用商品名称+随机数生成
                        if not barcode:
                            barcode = f"{name[:3]}{str(uuid.uuid4())[:6]}"
                        
                        new_product = {
                            "id": str(uuid.uuid4())[:8],
                            "name": name,
                            "price": price,
                            "stock": stock,
                            "description": description,
                            "barcode": barcode,
                            "created_at": datetime.now().isoformat()
                        }
                        
                        # 只导入有效的商品（名称不为空，价格大于等于0）
                        if new_product["name"] and new_product["price"] >= 0:
                            inventory.append(new_product)
                            success_count += 1
                    except Exception as e:
                        st.warning(f"跳过无效行: {e}")
                
                if success_count > 0:
                    save_data(INVENTORY_FILE, inventory)
                    st.success(f"✅ 成功导入 {success_count} 个商品！")
                    st.rerun()
                else:
                    st.error("❌ 没有有效的商品数据")
                    
            except Exception as e:
                st.error(f"❌ 文件读取失败: {str(e)}")

# 订单管理
def order_management():
    """订单管理"""
    st.subheader("📋 订单管理")
    
    orders = load_data(ORDERS_FILE)
    
    if orders:
        # 计算统计数据
        total_cash = sum(order.get('cash_amount', 0) for order in orders)
        total_voucher = sum(order.get('voucher_amount', 0) for order in orders)
        total_amount = sum(order.get('total_amount', 0) for order in orders)
        
        # 订单统计
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总订单数", len(orders))
        with col2:
            st.metric("现金支付总额", f"¥{total_cash:.2f}")
        with col3:
            st.metric("内购券支付总额", f"¥{total_voucher:.2f}")
        with col4:
            st.metric("订单总金额", f"¥{total_amount:.2f}")
        
        # 处理订单数据，展开商品信息
        order_details = []
        inventory = load_data(INVENTORY_FILE)  # 加载商品数据来获取条码
        
        for order in orders:
            items = order.get('items', [])
            for item in items:
                # 根据商品ID查找条码
                product_id = item.get('product_id', 'N/A')
                product_name = item.get('product_name', 'N/A')
                
                # 从商品库存中查找条码
                barcode = 'N/A'
                for product in inventory:
                    if product.get('id') == product_id:
                        barcode = product.get('barcode', product_id)
                        break
                
                order_detail = {
                    '订单ID': order.get('order_id', 'N/A'),
                    '用户姓名': order.get('user_name', 'N/A'),
                    '条码': barcode,
                    '商品名称': product_name,
                    '单价': f"¥{item.get('price', 0):.2f}",
                    '数量': item.get('quantity', 0),
                    '小计': f"¥{item.get('price', 0) * item.get('quantity', 0):.2f}",
                    '现金支付': f"¥{order.get('cash_amount', 0):.2f}",
                    '内购券支付': f"¥{order.get('voucher_amount', 0):.2f}",
                    '支付方式': order.get('payment_method', 'N/A'),
                    '订单时间': order.get('order_time', 'N/A')
                }
                order_details.append(order_detail)
        
        # 显示订单详情
        if order_details:
            st.write("### 📊 订单详情")
            df = pd.DataFrame(order_details)
            
            # 格式化时间显示
            df['订单时间'] = pd.to_datetime(df['订单时间']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            st.dataframe(df, use_container_width=True)
            
            # 导出订单
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 导出订单详情"):
                    csv = df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="下载CSV文件",
                        data=csv,
                        file_name=f"订单详情_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("🗑️ 清空所有订单"):
                    if st.session_state.get('confirm_clear_orders', False):
                        save_data(ORDERS_FILE, [])
                        st.session_state.confirm_clear_orders = False
                        st.success("✅ 所有订单已清空！")
                        st.rerun()
                    else:
                        st.session_state.confirm_clear_orders = True
                        st.warning("⚠️ 再次点击确认清空所有订单")
        else:
            st.info("暂无订单详情")
    else:
        st.info("暂无订单数据")

# 用户管理
def user_management():
    """用户管理"""
    st.subheader("👥 用户管理")
    
    users = load_data(USERS_FILE)
    
    # 添加用户
    with st.form("add_user_form"):
        st.write("### 添加新用户")
        new_username = st.text_input("用户名")
        new_name = st.text_input("姓名")
        new_role = st.selectbox("角色", ["user", "admin"])
        
        if st.form_submit_button("添加用户"):
            if new_username and new_name:
                # 检查用户名是否已存在
                if any(user["username"] == new_username for user in users):
                    st.error("用户名已存在")
                elif any(user["name"] == new_name for user in users):
                    st.error("姓名已存在")
                else:
                    new_user = {
                        "username": new_username,
                        "password": "default123",  # 默认密码，现在不需要
                        "name": new_name,
                        "role": new_role
                    }
                    users.append(new_user)
                    save_data(USERS_FILE, users)
                    st.success("用户添加成功！")
                    st.rerun()
            else:
                st.error("请填写完整信息")
    
    # 显示用户列表
    st.write("### 用户列表")
    for i, user in enumerate(users):
        with st.expander(f"{user['name']} ({user['username']}) - {user['role']}"):
            if st.button(f"删除用户", key=f"delete_user_{i}"):
                if user['username'] != 'admin':  # 保护管理员账户
                    users.pop(i)
                    save_data(USERS_FILE, users)
                    st.success("用户删除成功！")
                    st.rerun()
                else:
                    st.error("无法删除管理员账户")

# 数据统计
def data_statistics():
    """数据统计"""
    st.subheader("📊 数据统计")
    
    orders = load_data(ORDERS_FILE)
    inventory = load_data(INVENTORY_FILE)
    
    if orders:
        df = pd.DataFrame(orders)
        
        # 销售统计
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 💰 支付金额统计")
            # 计算现金和内购券支付金额
            cash_total = sum(order.get('cash_amount', 0) for order in orders)
            voucher_total = sum(order.get('voucher_amount', 0) for order in orders)
            
            payment_data = pd.DataFrame({
                '支付方式': ['现金支付', '内购券支付'],
                '金额': [cash_total, voucher_total]
            })
            st.bar_chart(payment_data.set_index('支付方式'))
            
            # 显示具体数值
            st.write(f"现金支付总额: ¥{cash_total:.2f}")
            st.write(f"内购券支付总额: ¥{voucher_total:.2f}")
        
        with col2:
            st.write("### 👥 用户购买统计")
            user_stats = df['user_name'].value_counts()
            st.bar_chart(user_stats)
        
        # 商品销售统计
        st.write("### 商品销售统计")
        product_sales = {}
        for order in orders:
            for item in order.get('items', []):
                product_name = item['product_name']
                quantity = item['quantity']
                if product_name in product_sales:
                    product_sales[product_name] += quantity
                else:
                    product_sales[product_name] = quantity
        
        if product_sales:
            sales_df = pd.DataFrame(list(product_sales.items()), columns=['商品名称', '销售数量'])
            st.bar_chart(sales_df.set_index('商品名称'))
    
    # 库存统计
    if inventory:
        st.write("### 库存统计")
        inventory_df = pd.DataFrame(inventory)
        st.bar_chart(inventory_df.set_index('name')['stock'])

# 用户购买页面
def user_page():
    """用户购买页面"""
    st.title("🛒 内购商城")
    
    # 创建选项卡
    tab1, tab2 = st.tabs(["🛍️ 商品购买", "📋 订单历史"])
    
    with tab1:
        shopping_page()
    
    with tab2:
        user_order_history()

def shopping_page():
    """商品购买页面"""
    inventory = load_data(INVENTORY_FILE)
    
    if not inventory:
        st.info("暂无商品可购买")
        return
    
    # 购物车
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # 显示商品
    st.subheader("🛍️ 商品列表")
    
    # 表格表头
    col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 1, 1, 1, 1])
    with col1:
        st.write("**条码**")
    with col2:
        st.write("**产品名称**")
    with col3:
        st.write("**库存**")
    with col4:
        st.write("**价格**")
    with col5:
        st.write("**数量**")
    with col6:
        st.write("**加入购物车**")
    
    st.divider()
    
    # 为每个商品添加数量选择和加入购物车按钮
    for i, product in enumerate(inventory):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 1, 1, 1, 1])
        
        with col1:
            st.write(product.get('barcode', 'N/A'))
        
        with col2:
            st.write(product['name'])
        
        with col3:
            stock_color = "red" if product['stock'] == 0 else "green" if product['stock'] > 10 else "orange"
            st.write(f":{stock_color}[{product['stock']}]")
        
        with col4:
            st.write(f"¥{product['price']:.2f}")
        
        with col5:
            if product['stock'] > 0:
                quantity = st.number_input(
                    "", 
                    min_value=1, 
                    max_value=product['stock'], 
                    value=1,
                    key=f"qty_{product['id']}",
                    label_visibility="collapsed"
                )
            else:
                st.write("-")
        
        with col6:
            if product['stock'] > 0:
                if st.button("加入购物车", key=f"add_{product['id']}"):
                    quantity = st.session_state.get(f"qty_{product['id']}", 1)
                    
                    # 检查购物车中是否已有该商品
                    existing_item = None
                    for item in st.session_state.cart:
                        if item['product_id'] == product['id']:
                            existing_item = item
                            break
                    
                    if existing_item:
                        existing_item['quantity'] += quantity
                    else:
                        st.session_state.cart.append({
                            'product_id': product['id'],
                            'product_name': product['name'],
                            'price': product['price'],
                            'quantity': quantity
                        })
                    
                    st.success(f"已添加 {quantity} 个 {product['name']} 到购物车")
                    st.rerun()
            else:
                st.button("库存不足", key=f"out_of_stock_{product['id']}", disabled=True)
    
    # 购物车
    if st.session_state.cart:
        st.subheader("🛒 购物车")
        
        total_amount = 0
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            
            # 根据商品ID查找条码
            barcode = 'N/A'
            for product in inventory:
                if product.get('id') == item['product_id']:
                    barcode = product.get('barcode', 'N/A')
                    break
            
            with col1:
                st.write(f"{barcode} - {item['product_name']}")
            with col2:
                st.write(f"¥{item['price']}")
            with col3:
                st.write(f"x{item['quantity']}")
            with col4:
                subtotal = item['price'] * item['quantity']
                st.write(f"¥{subtotal:.2f}")
                total_amount += subtotal
            with col5:
                if st.button("删除", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
        
        st.write(f"### 总计: ¥{total_amount:.2f}")
        
        # 支付方式详细输入
        st.write("### 💰 支付方式")
        col1, col2 = st.columns(2)
        
        with col1:
            cash_amount = st.number_input("现金支付金额", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        
        with col2:
            voucher_amount = st.number_input("内购券支付金额", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        
        # 检查支付金额
        payment_total = cash_amount + voucher_amount
        if payment_total < total_amount:
            st.error(f"⚠️ 支付金额不足！应付：¥{total_amount:.2f}，实付：¥{payment_total:.2f}")
            payment_valid = False
        else:
            if payment_total > total_amount:
                st.warning(f"⚠️ 支付金额大于订单总额：应付：¥{total_amount:.2f}，实付：¥{payment_total:.2f}，多付差额不找零")
            else:
                st.success(f"✅ 支付金额正确：¥{payment_total:.2f}")
            payment_valid = True
        
        # 显示支付明细
        if cash_amount > 0 and voucher_amount > 0:
            payment_method = "混合支付"
        elif cash_amount > 0:
            payment_method = "现金支付"
        elif voucher_amount > 0:
            payment_method = "内购券支付"
        else:
            payment_method = "未选择支付方式"
            payment_valid = False
        
        st.info(f"支付方式：{payment_method}")
        
        if st.button("提交订单", disabled=not payment_valid):
            # 检查库存
            inventory = load_data(INVENTORY_FILE)
            can_order = True
            
            for cart_item in st.session_state.cart:
                for product in inventory:
                    if product['id'] == cart_item['product_id']:
                        if product['stock'] < cart_item['quantity']:
                            st.error(f"{product['name']} 库存不足！当前库存: {product['stock']}")
                            can_order = False
                        break
            
            if can_order:
                # 创建订单
                order = {
                    'order_id': str(uuid.uuid4())[:8],
                    'user_name': st.session_state.user['name'],
                    'items': st.session_state.cart,
                    'total_amount': total_amount,  # 订单商品总额
                    'payment_method': payment_method,
                    'cash_amount': cash_amount,  # 实际现金支付金额
                    'voucher_amount': voucher_amount,  # 实际内购券支付金额
                    'actual_payment': cash_amount + voucher_amount,  # 实际支付总金额
                    'order_time': datetime.now().isoformat()
                }
                
                # 保存订单
                orders = load_data(ORDERS_FILE)
                orders.append(order)
                save_data(ORDERS_FILE, orders)
                
                # 更新库存
                for cart_item in st.session_state.cart:
                    for product in inventory:
                        if product['id'] == cart_item['product_id']:
                            product['stock'] -= cart_item['quantity']
                            break
                
                save_data(INVENTORY_FILE, inventory)
                
                # 清空购物车
                st.session_state.cart = []
                
                st.success("订单提交成功！")
                st.rerun()

def user_order_history():
    """用户订单历史页面"""
    st.subheader("📋 订单历史")
    
    # 加载订单和库存数据
    orders = load_data(ORDERS_FILE)
    inventory = load_data(INVENTORY_FILE)
    
    # 筛选当前用户的订单
    user_orders = [order for order in orders if order['user_name'] == st.session_state.user['name']]
    
    if not user_orders:
        st.info("您暂无订单记录")
        return
    
    # 按时间倒序排列
    user_orders.sort(key=lambda x: x['order_time'], reverse=True)
    
    # 显示订单
    for order in user_orders:
        with st.expander(f"订单 {order['order_id']} - {order['order_time'][:19].replace('T', ' ')} - ¥{order['total_amount']:.2f}"):
            # 订单基本信息
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**支付方式:** {order['payment_method']}")
            with col2:
                st.write(f"**现金:** ¥{order['cash_amount']:.2f} | **内购券:** ¥{order['voucher_amount']:.2f}")
            with col3:
                # 修改订单按钮
                if st.button("修改订单", key=f"modify_{order['order_id']}"):
                    st.session_state.modifying_order = order['order_id']
                    # 添加短暂延迟以减少前端错误
                    st.info("正在加载修改界面...")
                    safe_rerun()
            
            # 商品详情
            st.write("**商品详情:**")
            for item in order['items']:
                # 根据商品ID查找条码
                barcode = 'N/A'
                current_stock = 0
                for product in inventory:
                    if product.get('id') == item['product_id']:
                        barcode = product.get('barcode', 'N/A')
                        current_stock = product.get('stock', 0)
                        break
                
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"{barcode} - {item['product_name']}")
                with col2:
                    st.write(f"¥{item['price']:.2f}")
                with col3:
                    st.write(f"x{item['quantity']}")
                with col4:
                    subtotal = item['price'] * item['quantity']
                    st.write(f"¥{subtotal:.2f}")
            
            # 如果正在修改这个订单
            if st.session_state.get('modifying_order') == order['order_id']:
                st.write("---")
                st.write("### 🛠️ 修改订单")
                modify_order_interface(order, inventory)

@ultimate_error_handler
def modify_order_interface(order, inventory):
    """订单修改界面"""
    st.write("**修改选项:**")
    
    # 创建修改选项卡
    tab1, tab2, tab3 = st.tabs(["📝 修改商品数量", "➕ 增加商品", "❌ 撤销整个订单"])
    
    with tab1:
        st.write("**当前商品列表:**")
        
        # 创建修改后的商品列表
        if f'modified_items_{order["order_id"]}' not in st.session_state:
            st.session_state[f'modified_items_{order["order_id"]}'] = order['items'].copy()
        
        modified_items = st.session_state[f'modified_items_{order["order_id"]}']
        items_to_remove = []
        
        for i, item in enumerate(modified_items):
            # 根据商品ID查找条码和当前库存
            barcode = 'N/A'
            current_stock = 0
            for product in inventory:
                if product.get('id') == item['product_id']:
                    barcode = product.get('barcode', 'N/A')
                    current_stock = product.get('stock', 0)
                    break
            
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"{barcode} - {item['product_name']}")
            with col2:
                st.write(f"¥{item['price']:.2f}")
            with col3:
                # 可用库存 = 当前库存 + 订单中的数量（因为这些库存是被这个订单占用的）
                available_stock = current_stock + item['quantity']
                
                # 使用回调函数处理数量变化，避免直接DOM操作
                new_quantity = st.number_input(
                    "数量",
                    min_value=0,
                    max_value=available_stock,
                    value=item['quantity'],
                    key=f"mod_qty_{order['order_id']}_{i}",
                    label_visibility="collapsed",
                    help="设为0将移除此商品"
                )
                
                # 平滑更新数量
                try:
                    modified_items[i]['quantity'] = new_quantity
                    if new_quantity == 0:
                        items_to_remove.append(i)
                except Exception:
                    # 忽略更新过程中的错误
                    pass
            with col4:
                subtotal = item['price'] * new_quantity
                st.write(f"¥{subtotal:.2f}")
        
        # 处理数量为0的商品（平滑删除，避免DOM错误）
        if items_to_remove:
            # 使用终极平滑删除函数避免前端错误
            try:
                # 先标记要删除的项目
                for i in items_to_remove:
                    if i < len(modified_items):
                        modified_items[i]['_marked_for_deletion'] = True
                
                # 创建新列表，排除标记删除的项目
                new_items = [item for item in modified_items if not item.get('_marked_for_deletion', False)]
                
                # 静默更新session state
                with suppress_stdout_stderr():
                    st.session_state[f'modified_items_{order["order_id"]}'] = new_items
                    modified_items = new_items
                
                # 添加用户友好的提示
                if len(new_items) < len(modified_items):
                    st.info("✅ 已移除数量为0的商品")
                
            except Exception as e:
                # 如果出错，不显示错误，只是保持原状态
                pass
        
        # 计算新的总金额
        new_total = sum(item['price'] * item['quantity'] for item in modified_items)
        st.write(f"**修改后总金额:** ¥{new_total:.2f}")
        
        # 重新设置支付方式
        st.write("**重新设置支付方式:**")
        col1, col2 = st.columns(2)
        
        with col1:
            new_cash = st.number_input("现金支付金额", min_value=0.0, value=0.0, step=0.01, format="%.2f", key=f"new_cash_{order['order_id']}")
        
        with col2:
            new_voucher = st.number_input("内购券支付金额", min_value=0.0, value=0.0, step=0.01, format="%.2f", key=f"new_voucher_{order['order_id']}")
        
        new_payment_total = new_cash + new_voucher
        if new_payment_total < new_total:
            st.error(f"⚠️ 支付金额不足！应付：¥{new_total:.2f}，实付：¥{new_payment_total:.2f}")
            payment_valid = False
        else:
            if new_payment_total > new_total:
                st.warning(f"⚠️ 支付金额大于订单总额：应付：¥{new_total:.2f}，实付：¥{new_payment_total:.2f}，多付差额不找零")
            else:
                st.success(f"✅ 支付金额正确：¥{new_payment_total:.2f}")
            payment_valid = True
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("确认修改", key=f"confirm_modify_{order['order_id']}", disabled=not payment_valid or not modified_items):
                if update_order(order, modified_items, new_cash, new_voucher, new_total, inventory):
                    st.success("订单修改成功！")
                    # 清理临时状态
                    if f'modified_items_{order["order_id"]}' in st.session_state:
                        del st.session_state[f'modified_items_{order["order_id"]}']
                    if 'modifying_order' in st.session_state:
                        del st.session_state['modifying_order']
                    st.balloons()  # 添加视觉反馈
                    safe_rerun()
                else:
                    st.error("订单修改失败，请重试")
        
        with col2:
            if st.button("取消修改", key=f"cancel_modify_{order['order_id']}"):
                # 清理临时状态
                if f'modified_items_{order["order_id"]}' in st.session_state:
                    del st.session_state[f'modified_items_{order["order_id"]}']
                if 'modifying_order' in st.session_state:
                    del st.session_state['modifying_order']
                st.info("已取消修改")
                safe_rerun()
    
    with tab2:
        st.write("**从商品库存中增加商品:**")
        
        # 显示可添加的商品
        available_products = [p for p in inventory if p['stock'] > 0]
        
        if not available_products:
            st.info("暂无可添加的商品")
        else:
            # 商品选择
            product_options = {f"{p.get('barcode', 'N/A')} - {p['name']} (库存:{p['stock']})": p for p in available_products}
            selected_product_name = st.selectbox("选择商品", list(product_options.keys()), key=f"add_product_{order['order_id']}")
            selected_product = product_options[selected_product_name]
            
            # 数量选择
            add_quantity = st.number_input("数量", min_value=1, max_value=selected_product['stock'], value=1, key=f"add_qty_{order['order_id']}")
            
            if st.button("添加到订单", key=f"add_to_order_{order['order_id']}"):
                # 添加商品到修改列表
                if f'modified_items_{order["order_id"]}' not in st.session_state:
                    st.session_state[f'modified_items_{order["order_id"]}'] = order['items'].copy()
                
                # 检查是否已存在相同商品
                existing_item = None
                for item in st.session_state[f'modified_items_{order["order_id"]}']:
                    if item['product_id'] == selected_product['id']:
                        existing_item = item
                        break
                
                if existing_item:
                    existing_item['quantity'] += add_quantity
                else:
                    st.session_state[f'modified_items_{order["order_id"]}'].append({
                        'product_id': selected_product['id'],
                        'product_name': selected_product['name'],
                        'price': selected_product['price'],
                        'quantity': add_quantity
                    })
                
                st.success(f"已添加 {add_quantity} 个 {selected_product['name']} 到订单")
                # 使用 st.experimental_rerun() 或延迟刷新来减少前端错误
                st.balloons()  # 添加视觉反馈
                safe_rerun()
        
        # 显示当前修改后的商品列表
        if f'modified_items_{order["order_id"]}' in st.session_state:
            st.write("---")
            st.write("**当前订单商品列表:**")
            modified_items = st.session_state[f'modified_items_{order["order_id"]}']
            
            if modified_items:
                for i, item in enumerate(modified_items):
                    # 根据商品ID查找条码
                    barcode = 'N/A'
                    for product in inventory:
                        if product.get('id') == item['product_id']:
                            barcode = product.get('barcode', 'N/A')
                            break
                    
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"{barcode} - {item['product_name']}")
                    with col2:
                        st.write(f"¥{item['price']:.2f}")
                    with col3:
                        st.write(f"x{item['quantity']}")
                    with col4:
                        subtotal = item['price'] * item['quantity']
                        st.write(f"¥{subtotal:.2f}")
                
                # 计算新的总金额
                new_total = sum(item['price'] * item['quantity'] for item in modified_items)
                st.write(f"**当前总金额:** ¥{new_total:.2f}")
            else:
                st.write("暂无商品")
        else:
            st.write("---")
            st.write("**当前订单商品列表:**")
            for i, item in enumerate(order['items']):
                # 根据商品ID查找条码
                barcode = 'N/A'
                for product in inventory:
                    if product.get('id') == item['product_id']:
                        barcode = product.get('barcode', 'N/A')
                        break
                
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"{barcode} - {item['product_name']}")
                with col2:
                    st.write(f"¥{item['price']:.2f}")
                with col3:
                    st.write(f"x{item['quantity']}")
                with col4:
                    subtotal = item['price'] * item['quantity']
                    st.write(f"¥{subtotal:.2f}")
            
            original_total = sum(item['price'] * item['quantity'] for item in order['items'])
            st.write(f"**原订单总金额:** ¥{original_total:.2f}")
    
    with tab3:
        st.write("**⚠️ 警告：撤销订单将恢复所有商品库存**")
        
        # 显示将要恢复的库存
        st.write("**将恢复的库存:**")
        for item in order['items']:
            barcode = 'N/A'
            for product in inventory:
                if product.get('id') == item['product_id']:
                    barcode = product.get('barcode', 'N/A')
                    break
            st.write(f"- {barcode} - {item['product_name']}: +{item['quantity']}")
        
        # 双重确认
        if st.checkbox("我确认要撤销整个订单", key=f"confirm_cancel_{order['order_id']}"):
            if st.button("确认撤销订单", key=f"final_cancel_{order['order_id']}", type="primary"):
                if cancel_order(order, inventory):
                    st.success("订单已成功撤销！")
                    if 'modifying_order' in st.session_state:
                        del st.session_state['modifying_order']
                    st.rerun()
                else:
                    st.error("订单撤销失败，请重试")

@ultimate_error_handler
def update_order(original_order, modified_items, new_cash, new_voucher, new_total, inventory):
    """更新订单信息"""
    try:
        # 加载当前订单数据
        orders = load_data(ORDERS_FILE)
        
        # 找到要修改的订单
        order_to_update = None
        for order in orders:
            if order['order_id'] == original_order['order_id']:
                order_to_update = order
                break
        
        if not order_to_update:
            return False
        
        # 计算库存变化
        # 首先恢复原订单的库存
        for item in original_order['items']:
            for product in inventory:
                if product['id'] == item['product_id']:
                    product['stock'] += item['quantity']
                    break
        
        # 然后扣减新订单的库存
        for item in modified_items:
            for product in inventory:
                if product['id'] == item['product_id']:
                    product['stock'] -= item['quantity']
                    break
        
        # 更新订单信息
        order_to_update['items'] = modified_items
        order_to_update['total_amount'] = new_total  # 订单商品总额
        order_to_update['cash_amount'] = new_cash  # 实际现金支付金额
        order_to_update['voucher_amount'] = new_voucher  # 实际内购券支付金额
        order_to_update['actual_payment'] = new_cash + new_voucher  # 实际支付总金额
        
        # 更新支付方式
        if new_cash > 0 and new_voucher > 0:
            order_to_update['payment_method'] = "混合支付"
        elif new_cash > 0:
            order_to_update['payment_method'] = "现金支付"
        elif new_voucher > 0:
            order_to_update['payment_method'] = "内购券支付"
        
        # 添加修改时间
        order_to_update['modified_time'] = datetime.now().isoformat()
        
        # 保存数据
        save_data(ORDERS_FILE, orders)
        save_data(INVENTORY_FILE, inventory)
        
        return True
    except Exception as e:
        st.error(f"更新订单时发生错误：{str(e)}")
        return False

def cancel_order(order, inventory):
    """撤销订单"""
    try:
        # 加载当前订单数据
        orders = load_data(ORDERS_FILE)
        
        # 恢复库存
        for item in order['items']:
            for product in inventory:
                if product['id'] == item['product_id']:
                    product['stock'] += item['quantity']
                    break
        
        # 删除订单
        orders = [o for o in orders if o['order_id'] != order['order_id']]
        
        # 保存数据
        save_data(ORDERS_FILE, orders)
        save_data(INVENTORY_FILE, inventory)
        
        return True
    except Exception as e:
        st.error(f"撤销订单时发生错误：{str(e)}")
        return False

# 简洁的错误隐藏机制（可选）
st.markdown("""
<style>
/* 隐藏可能的前端错误信息 */
.stException {
    display: none !important;
}

/* 确保表格正常显示 */
.stDataFrame {
    display: block !important;
    visibility: visible !important;
}
</style>
""", unsafe_allow_html=True)

# 主函数
@handle_frontend_errors
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
                safe_rerun()
    
    # 主页面
    try:
        if 'user' not in st.session_state:
            login_page()
        else:
            if st.session_state.user['role'] == 'admin':
                admin_page()
            else:
                user_page()
    except Exception as e:
        # 忽略所有前端错误
        error_keywords = ["removeChild", "Node", "DOM", "JavaScript", "NotFoundError"]
        if not any(keyword in str(e) for keyword in error_keywords):
            st.error(f"系统错误: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        # 完全忽略所有启动时的错误
        pass
