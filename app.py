import streamlit as st
import pandas as pd
import os
import time
import contextlib
import io
from datetime import datetime
import uuid
from database import get_database_manager

# 设置页面配置
st.set_page_config(
    page_title="内购系统",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 清理完成 - 所有JavaScript残留代码已移除

# 初始化数据库管理器
db = get_database_manager()

# 获取数据库管理器
@st.cache_resource
def get_db():
    return get_database_manager()

db = get_db()

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

# 数据操作函数（直接使用数据库）
def get_users():
    """获取用户数据"""
    return db.load_users()

def get_orders():
    """获取订单数据"""
    return db.load_orders()

def get_inventory():
    """获取库存数据"""
    return db.load_inventory()

def save_inventory(inventory_data):
    """保存库存数据 - 增强版本"""
    try:
        # 显示保存前的状态
        st.info(f"🔄 正在保存 {len(inventory_data)} 条商品数据...")
        
        # 检查数据库环境
        import os
        if 'DATABASE_URL' in os.environ:
            st.write("📊 生产环境: PostgreSQL")
        else:
            st.write("📊 开发环境: SQLite")
        
        # 保存前先读取当前数据
        before_count = len(db.load_inventory())
        st.write(f"保存前商品数量: {before_count}")
        
        # 执行保存
        db.save_inventory(inventory_data)
        st.write("✅ 数据库保存操作已执行")
        
        # 立即验证保存结果
        import time
        time.sleep(0.5)  # 等待数据库写入完成
        
        saved_data = db.load_inventory()
        after_count = len(saved_data)
        st.write(f"保存后商品数量: {after_count}")
        
        if after_count == len(inventory_data):
            st.success(f"✅ 数据库保存验证成功: {after_count} 条商品")
        else:
            st.error(f"❌ 数据保存验证失败!")
            st.write(f"   期望保存: {len(inventory_data)} 条")
            st.write(f"   实际保存: {after_count} 条")
            st.write(f"   差异: {len(inventory_data) - after_count} 条")
            
    except Exception as e:
        st.error(f"❌ 数据库保存异常: {str(e)}")
        st.write("🔍 错误详情:")
        st.code(str(e))
        import traceback
        st.write("🐛 完整错误堆栈:")
        st.code(traceback.format_exc())

def add_order(order_data):
    """添加订单 - 增强版本"""
    try:
        # 显示保存前状态
        before_count = len(db.load_orders())
        st.info(f"🔄 正在保存订单 {order_data.get('order_id', 'N/A')}...")
        st.write(f"保存前订单数量: {before_count}")
        
        # 执行保存
        db.add_order(order_data)
        st.write("✅ 订单保存操作已执行")
        
        # 验证保存结果
        import time
        time.sleep(0.5)
        
        saved_orders = db.load_orders()
        after_count = len(saved_orders)
        st.write(f"保存后订单数量: {after_count}")
        
        if after_count == before_count + 1:
            st.success(f"✅ 订单保存验证成功")
        else:
            st.error(f"❌ 订单保存验证失败!")
            
    except Exception as e:
        st.error(f"❌ 订单保存异常: {str(e)}")
        st.code(str(e))

def add_user(user_data):
    """添加用户"""
    db.add_user(user_data)

def save_users(users_data):
    """保存用户数据"""
    for user in users_data:
        db.add_user(user)

def clear_orders():
    """清空订单"""
    db.clear_orders()

def clear_users():
    """清空用户"""
    db.clear_users()

def clear_inventory():
    """清空库存"""
    db.save_inventory([])

# 文件常量（兼容性）
USERS_FILE = "users.json"
ORDERS_FILE = "orders.json"
INVENTORY_FILE = "inventory.json"

# 兼容性函数（将文件操作转换为数据库操作）
def load_data(file_path):
    """加载数据（兼容性函数）"""
    if file_path == USERS_FILE:
        return get_users()
    elif file_path == ORDERS_FILE:
        return get_orders()
    elif file_path == INVENTORY_FILE:
        return get_inventory()
    else:
        return []

def save_data(file_path, data):
    """保存数据（兼容性函数）"""
    if file_path == USERS_FILE:
        save_users(data)
    elif file_path == ORDERS_FILE:
        # 订单数据需要逐个添加
        clear_orders()
        for order in data:
            add_order(order)
    elif file_path == INVENTORY_FILE:
        save_inventory(data)

# 初始化数据（数据库已自动初始化）
def initialize_data():
    """初始化数据（数据库版本）"""
    pass  # 数据库会自动初始化

# 用户认证
def authenticate_user(name):
    """用户认证"""
    users = get_users()
    # 只有输入“管理员666”才允许进入管理员界面
    if name == "管理员666":
        # 检查是否已存在管理员666
        for user in users:
            if user["name"] == "管理员666" and user["role"] == "admin":
                return user
        # 不存在则创建
        admin_user = {
            "username": "admin666",
            "password": "admin123",
            "name": "管理员666",
            "role": "admin"
        }
        add_user(admin_user)
        return admin_user
    # 其它任何姓名都只能是普通用户
    for user in users:
        if user["name"] == name and user["role"] == "user":
            return user
    new_user = {
        "username": f"user_{len(users)}",
        "password": "default123",
        "name": name,
        "role": "user"
    }
    add_user(new_user)
    return new_user

# 检查用户历史购买数量
def get_user_purchase_history(user_name, product_id):
    """获取用户对特定商品的历史购买数量"""
    orders = load_data(ORDERS_FILE)
    total_purchased = 0
    
    for order in orders:
        if order.get('user_name') == user_name:
            for item in order.get('items', []):
                if item.get('product_id') == product_id:
                    total_purchased += item.get('quantity', 0)
    
    return total_purchased

# 检查限购限制（包含历史购买记录）
def check_purchase_limit(user_name, product_id, current_cart_quantity, new_quantity, purchase_limit):
    """
    检查限购限制，包含用户历史购买记录
    返回 (是否允许购买, 错误信息)
    """
    if purchase_limit <= 0:
        return True, ""  # 不限购
    
    # 获取历史购买数量
    historical_quantity = get_user_purchase_history(user_name, product_id)
    
    # 计算总数量：历史购买 + 购物车中已有 + 本次要添加
    total_quantity = historical_quantity + current_cart_quantity + new_quantity
    
    if total_quantity > purchase_limit:
        error_msg = f"⚠️ 该商品限购{purchase_limit}件\n"
        error_msg += f"您已购买：{historical_quantity}件\n"
        error_msg += f"购物车中：{current_cart_quantity}件\n"
        error_msg += f"本次添加：{new_quantity}件\n"
        error_msg += f"总计：{total_quantity}件，超出限购数量！"
        return False, error_msg
    
    return True, ""

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
    
    # 不再显示管理员登录提示

# 管理员页面
def admin_page():
    """管理员页面"""
    st.title("📊 管理员控制面板")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["库存管理", "订单管理", "用户管理", "数据统计", "🔍 数据库检查"])
    
    with tab1:
        inventory_management()
    
    with tab2:
        order_management()
    
    with tab3:
        user_management()
    
    with tab4:
        data_statistics()
    
    with tab5:
        database_status_check()

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
        
        # 商品筛选功能
        with st.expander("🔍 商品筛选", expanded=False):
            filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1])
            with filter_col1:
                name_filter = st.text_input(
                    "🔍 搜索商品名称",
                    placeholder="输入商品名称关键词",
                    key="admin_name_filter",
                    value=st.session_state.get('admin_name_filter', '')
                )
                stock_filter = st.selectbox(
                    "📦 库存状态",
                    ["全部", "有库存", "库存充足(>10)", "库存紧张(1-10)", "缺货"],
                    key="admin_stock_filter"
                )
            with filter_col2:
                st.write("💰 价格范围")
                prices = [item['price'] for item in inventory]
                min_price = min(prices) if prices else 0
                max_price = max(prices) if prices else 1000
                price_range = st.slider(
                    "选择价格范围",
                    min_value=float(min_price),
                    max_value=float(max_price),
                    value=(float(min_price), float(max_price)),
                    step=0.01,
                    format="¥%.2f",
                    key="admin_price_range"
                )
            with filter_col3:
                limit_filter = st.selectbox(
                    "🚫 限购状态",
                    ["全部", "限购商品", "不限购商品"],
                    key="admin_limit_filter"
                )
                barcode_filter = st.text_input(
                    "📊 搜索条码",
                    placeholder="输入条码",
                    key="admin_barcode_filter",
                    value=st.session_state.get('admin_barcode_filter', '')
                )
            # 不再提供重置按钮，管理员可手动清空筛选条件

        # 应用筛选条件
        filtered_inventory = inventory.copy()
        if 'admin_name_filter' in st.session_state and st.session_state['admin_name_filter']:
            filtered_inventory = [item for item in filtered_inventory if st.session_state['admin_name_filter'].lower() in item['name'].lower()]
        if 'admin_barcode_filter' in st.session_state and st.session_state['admin_barcode_filter']:
            filtered_inventory = [item for item in filtered_inventory if st.session_state['admin_barcode_filter'] in item.get('barcode', '')]
        if 'admin_price_range' in st.session_state:
            price_min, price_max = st.session_state['admin_price_range']
            filtered_inventory = [item for item in filtered_inventory if price_min <= item['price'] <= price_max]
        if 'admin_stock_filter' in st.session_state:
            stock_filter = st.session_state['admin_stock_filter']
            if stock_filter == "有库存":
                filtered_inventory = [item for item in filtered_inventory if item['stock'] > 0]
            elif stock_filter == "库存充足(>10)":
                filtered_inventory = [item for item in filtered_inventory if item['stock'] > 10]
            elif stock_filter == "库存紧张(1-10)":
                filtered_inventory = [item for item in filtered_inventory if 1 <= item['stock'] <= 10]
            elif stock_filter == "缺货":
                filtered_inventory = [item for item in filtered_inventory if item['stock'] == 0]
        if 'admin_limit_filter' in st.session_state:
            limit_filter = st.session_state['admin_limit_filter']
            if limit_filter == "限购商品":
                filtered_inventory = [item for item in filtered_inventory if item.get('purchase_limit', 0) > 0]
            elif limit_filter == "不限购商品":
                filtered_inventory = [item for item in filtered_inventory if item.get('purchase_limit', 0) == 0]

        # 商品列表
        df = pd.DataFrame(filtered_inventory)

        # 调试信息 - 检查数据是否正确加载
        if df.empty:
            st.error("❌ 数据框为空，无法显示商品信息")
            return

        # 确保所有商品都有 sold 和 purchase_limit 字段
        if 'sold' not in df.columns:
            df['sold'] = 0
        if 'purchase_limit' not in df.columns:
            df['purchase_limit'] = 0  # 0表示不限购

        # 为旧数据添加限购字段
        for product in filtered_inventory:
            if 'purchase_limit' not in product:
                product['purchase_limit'] = 0  # 0表示不限购

        # 重新排列列的顺序，添加限购数量列
        try:
            df = df[['barcode', 'name', 'price', 'stock', 'sold', 'purchase_limit', 'description', 'created_at']]
            df.columns = ['条码', '商品名称', '价格', '库存', '已售', '限购数量', '描述', '添加时间']
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

        st.write(f"### 📊 商品库存管理  (共 {len(df)} 条)")

        # 创建用于编辑的数据框，保持原始数值格式以便编辑（赋值用filtered_inventory，保证行数一致）
        edit_df = df.copy()
        try:
            edit_df['限购数量'] = [product.get('purchase_limit', 0) for product in filtered_inventory]
            edit_df['价格'] = [product.get('price', 0) for product in filtered_inventory]
            edit_df['库存'] = [product.get('stock', 0) for product in filtered_inventory]
        except Exception as e:
            st.warning(f"数据处理失败: {e}")
            edit_df['限购数量'] = 0
            edit_df['价格'] = 0
            edit_df['库存'] = 0
        # 只允许编辑价格、库存、限购数量，无删除列
        disabled_cols = ["条码", "商品名称", "已售", "描述", "添加时间"]
        try:
            edited_df = st.data_editor(
                edit_df,
                use_container_width=True,
                num_rows="fixed",
                disabled=disabled_cols,
                column_config={
                    "限购数量": st.column_config.NumberColumn(
                        "限购数量",
                        help="设置商品限购数量，0表示不限购",
                        min_value=0,
                        max_value=9999,
                        step=1,
                        format="%d"
                    ),
                    "价格": st.column_config.NumberColumn(
                        "价格",
                        help="商品单价",
                        min_value=0.0,
                        max_value=999999.0,
                        step=0.01,
                        format="%.2f"
                    ),
                    "库存": st.column_config.NumberColumn(
                        "库存",
                        help="商品库存数量",
                        min_value=0,
                        max_value=999999,
                        step=1,
                        format="%d"
                    ),
                },
                key="inventory_editor"
            )
            changed = False
            for i, row in edited_df.iterrows():
                if i < len(inventory):
                    new_limit = int(row['限购数量']) if pd.notna(row['限购数量']) else 0
                    try:
                        new_price = float(row['价格']) if pd.notna(row['价格']) else 0
                    except:
                        new_price = 0
                    try:
                        new_stock = int(row['库存']) if pd.notna(row['库存']) else 0
                    except:
                        new_stock = 0
                    if (inventory[i]['purchase_limit'] != new_limit or
                        inventory[i]['price'] != new_price or
                        inventory[i]['stock'] != new_stock):
                        inventory[i]['purchase_limit'] = new_limit
                        inventory[i]['price'] = new_price
                        inventory[i]['stock'] = new_stock
                        changed = True
            if changed:
                save_data(INVENTORY_FILE, inventory)
                st.success("✅ 商品信息已更新！")
                st.rerun()
        except Exception as e:
            st.error(f"可编辑表格显示异常: {e}")
        
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
                            # 处理限购数量字段（支持多种表头名称）
                            purchase_limit = row.get("限购数量", row.get("limit", row.get("purchase_limit", 0)))
                            
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
                            
                            # 处理限购数量数据
                            if pd.isna(purchase_limit) or purchase_limit == "":
                                purchase_limit = 0  # 0表示不限购
                            else:
                                purchase_limit = int(purchase_limit)
                            
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
                                "purchase_limit": purchase_limit,
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
            # 确保所有商品都有purchase_limit字段
            for product in inventory:
                if 'purchase_limit' not in product:
                    product['purchase_limit'] = 0
            export_df = pd.DataFrame(inventory)
            export_df = export_df[['barcode', 'name', 'price', 'stock', 'sold', 'purchase_limit', 'description', 'created_at']]
            export_df.columns = ['条码', '商品名称', '价格', '库存', '已售', '限购数量', '描述', '添加时间']
            
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
                        # 处理限购数量字段（支持多种表头名称）
                        purchase_limit = row.get("限购数量", row.get("limit", row.get("purchase_limit", 0)))
                        
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
                        
                        # 处理限购数量数据
                        if pd.isna(purchase_limit) or purchase_limit == "":
                            purchase_limit = 0  # 0表示不限购
                        else:
                            purchase_limit = int(purchase_limit)
                        
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
                            "purchase_limit": purchase_limit,
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
        # 计算统计数据 - 兼容新旧订单格式
        total_cash = sum(order.get('cash_amount', 0) for order in orders)
        total_voucher = sum(order.get('voucher_amount', 0) for order in orders)
        total_original = sum(order.get('original_amount', order.get('total_amount', 0)) for order in orders)
        total_final = sum(order.get('total_amount', 0) for order in orders)
        total_savings = sum(order.get('discount_savings', 0) for order in orders)
        
        # 订单统计
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("总订单数", len(orders))
        with col2:
            st.metric("商品原价总额", f"¥{total_original:.2f}")
        with col3:
            st.metric("折扣优惠总额", f"¥{total_savings:.2f}")
        with col4:
            st.metric("现金收款", f"¥{total_cash:.2f}")
        with col5:
            st.metric("内购券收款", f"¥{total_voucher:.2f}")
        
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
                
                # 获取订单折扣信息（兼容新旧订单）
                order_original = order.get('original_amount', order.get('total_amount', 0))
                order_discount = order.get('discount_savings', 0)
                order_discount_text = order.get('discount_text', '无折扣')
                order_final = order.get('total_amount', 0)
                order_cash = order.get('cash_amount', 0)
                order_voucher = order.get('voucher_amount', 0)
                
                # 处理多付显示（无找零）
                total_paid = order_cash + order_voucher
                if total_paid > order_final:
                    overpay = total_paid - order_final
                    overpay_display = f"¥{overpay:.2f} (不设找零)"
                else:
                    overpay_display = "¥0.00"
                
                order_detail = {
                    '订单ID': order.get('order_id', 'N/A'),
                    '用户姓名': order.get('user_name', 'N/A'),
                    '条码': barcode,
                    '商品名称': product_name,
                    '单价': f"¥{item.get('price', 0):.2f}",
                    '数量': item.get('quantity', 0),
                    '小计': f"¥{item.get('price', 0) * item.get('quantity', 0):.2f}",
                    '折扣优惠': order_discount_text,
                    '优惠金额': f"¥{order_discount:.2f}",
                    '应付金额': f"¥{order_final:.2f}",
                    '现金支付': f"¥{order_cash:.2f}",
                    '内购券支付': f"¥{order_voucher:.2f}",
                    '多付金额': overpay_display,
                    '支付方式': order.get('payment_method', '现金支付'),
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
            st.write("### 💰 支付方式统计")
            # 计算现金和内购券支付金额（兼容新旧订单）
            total_cash = sum(order.get('cash_amount', 0) for order in orders)
            total_voucher = sum(order.get('voucher_amount', 0) for order in orders)
            total_original = sum(order.get('original_amount', order.get('total_amount', 0)) for order in orders)
            total_discount = sum(order.get('discount_savings', 0) for order in orders)
            
            # 统计图表数据
            payment_data = pd.DataFrame({
                '支付方式': ['现金支付', '内购券支付'],
                '金额': [total_cash, total_voucher]
            })
            st.bar_chart(payment_data.set_index('支付方式'))
            
            # 显示具体数值
            st.write(f"**现金支付总额:** ¥{total_cash:.2f}")
            st.write(f"**内购券支付总额:** ¥{total_voucher:.2f}")
            st.write(f"**商品原价总额:** ¥{total_original:.2f}")
            st.write(f"**折扣优惠总额:** ¥{total_discount:.2f}")
            
            # 计算平均折扣率（仅针对现金支付订单）
            cash_orders = [order for order in orders if order.get('voucher_amount', 0) == 0]
            if cash_orders:
                cash_original = sum(order.get('original_amount', order.get('total_amount', 0)) for order in cash_orders)
                cash_discount = sum(order.get('discount_savings', 0) for order in cash_orders)
                if cash_original > 0:
                    avg_discount_rate = (cash_discount / cash_original) * 100
                    st.write(f"**现金支付平均折扣率:** {avg_discount_rate:.1f}%")
        
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
    
    # 创建选项卡，新增购物车页面
    tab1, tab2, tab3 = st.tabs(["🛍️ 商品购买", "� 购物车", "�📋 订单历史"])
    
    with tab1:
        shopping_page()
    with tab2:
        cart_page()
    with tab3:
        user_order_history()

def shopping_page():
    """商品购买页面"""
    inventory = load_data(INVENTORY_FILE)
    
    if not inventory:
        st.info("暂无商品可购买")
        return
    
    # 购物车初始化（仅初始化，不展示）
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # 商品筛选功能
    st.subheader("🛍️ 商品列表")
    
    # 筛选器
    with st.expander("🔍 商品筛选", expanded=False):
        prices = [item['price'] for item in inventory]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 1000

        # 初始化 session_state
        if 'name_filter' not in st.session_state:
            st.session_state['name_filter'] = ''
        if 'stock_filter' not in st.session_state:
            st.session_state['stock_filter'] = '全部'
        if 'price_range' not in st.session_state:
            st.session_state['price_range'] = (float(min_price), float(max_price))
        if 'limit_filter' not in st.session_state:
            st.session_state['limit_filter'] = '全部'
        if 'barcode_filter' not in st.session_state:
            st.session_state['barcode_filter'] = ''

        filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1])
        with filter_col1:
            st.text_input(
                "🔍 搜索商品名称",
                placeholder="输入商品名称关键词",
                key="name_filter",
                value=st.session_state['name_filter']
            )
            st.selectbox(
                "📦 库存状态",
                ["全部", "有库存", "库存充足(>10)", "库存紧张(1-10)", "缺货"],
                key="stock_filter",
                index=["全部", "有库存", "库存充足(>10)", "库存紧张(1-10)", "缺货"].index(st.session_state['stock_filter'])
            )
        with filter_col2:
            st.write("💰 价格范围")
            st.slider(
                "选择价格范围",
                min_value=float(min_price),
                max_value=float(max_price),
                value=st.session_state['price_range'],
                step=0.01,
                format="¥%.2f",
                key="price_range"
            )
        with filter_col3:
            st.selectbox(
                "🚫 限购状态",
                ["全部", "限购商品", "不限购商品"],
                key="limit_filter",
                index=["全部", "限购商品", "不限购商品"].index(st.session_state['limit_filter'])
            )
            st.text_input(
                "📊 搜索条码",
                placeholder="输入条码",
                key="barcode_filter",
                value=st.session_state['barcode_filter']
            )
        # 不再提供重置按钮，用户可手动清空筛选条件
    
    # 应用筛选条件
    filtered_inventory = inventory.copy()
    # 名称筛选
    name_filter = st.session_state.get('name_filter', '')
    if name_filter:
        filtered_inventory = [
            item for item in filtered_inventory 
            if name_filter.lower() in item['name'].lower()
        ]
    # 条码筛选
    barcode_filter = st.session_state.get('barcode_filter', '')
    if barcode_filter:
        filtered_inventory = [
            item for item in filtered_inventory 
            if barcode_filter in item.get('barcode', '')
        ]
    # 价格范围筛选
    price_range = st.session_state.get('price_range', (float(min_price), float(max_price)))
    filtered_inventory = [
        item for item in filtered_inventory 
        if price_range[0] <= item['price'] <= price_range[1]
    ]
    # 库存状态筛选
    stock_filter = st.session_state.get('stock_filter', '全部')
    if stock_filter == "有库存":
        filtered_inventory = [item for item in filtered_inventory if item['stock'] > 0]
    elif stock_filter == "库存充足(>10)":
        filtered_inventory = [item for item in filtered_inventory if item['stock'] > 10]
    elif stock_filter == "库存紧张(1-10)":
        filtered_inventory = [item for item in filtered_inventory if 1 <= item['stock'] <= 10]
    elif stock_filter == "缺货":
        filtered_inventory = [item for item in filtered_inventory if item['stock'] == 0]
    # 限购状态筛选
    limit_filter = st.session_state.get('limit_filter', '全部')
    if limit_filter == "限购商品":
        filtered_inventory = [
            item for item in filtered_inventory 
            if item.get('purchase_limit', 0) > 0
        ]
    elif limit_filter == "不限购商品":
        filtered_inventory = [
            item for item in filtered_inventory 
            if item.get('purchase_limit', 0) == 0
        ]
    
    # 显示筛选结果统计
    total_count = len(inventory)
    filtered_count = len(filtered_inventory)
    
    if filtered_count != total_count:
        st.info(f"📊 筛选结果：显示 {filtered_count} 件商品（共 {total_count} 件）")
    
    if not filtered_inventory:
        st.warning("😔 没有找到符合筛选条件的商品，请调整筛选条件")
        return
    
    # 分页参数
    PAGE_SIZE = 100
    total_items = len(filtered_inventory)
    total_pages = (total_items + PAGE_SIZE - 1) // PAGE_SIZE
    if 'user_goods_page' not in st.session_state:
        st.session_state['user_goods_page'] = 1
    page = st.session_state['user_goods_page']
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    st.session_state['user_goods_page'] = page
    start_idx = (page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    current_page_items = filtered_inventory[start_idx:end_idx]

    st.write(f"### 🛍️ 商品列表  (第 {page} / {total_pages} 页，共 {total_items} 条)")

    # 表格表头（带排序功能）
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2.5, 1, 1, 1, 1, 1])
    with col1:
        st.write("**条码**")
    with col2:
        st.write("**产品名称**")
    with col3:
        st.write("**库存**")
    with col4:
        st.write("**价格**")
    with col5:
        st.write("**限购数量**")
    with col6:
        st.write("**数量**")
    with col7:
        st.write("**加入购物车**")
    st.divider()

    # 为每个商品添加数量选择和加入购物车按钮
    for i, product in enumerate(current_page_items):
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 2.5, 1, 1, 1, 1, 1])
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
            purchase_limit = product.get('purchase_limit', 0)
            if purchase_limit > 0:
                user_name = st.session_state.user['name']
                historical_quantity = get_user_purchase_history(user_name, product['id'])
                if historical_quantity > 0:
                    remaining = max(0, purchase_limit - historical_quantity)
                    if remaining > 0:
                        st.write(f":orange[限购{purchase_limit}件]\n:blue[已购{historical_quantity}件]\n:green[可购{remaining}件]")
                    else:
                        st.write(f":orange[限购{purchase_limit}件]\n:red[已购{historical_quantity}件]\n:red[已达上限]")
                else:
                    st.write(f":orange[{purchase_limit}件]")
            else:
                st.write(":green[不限购]")
        with col6:
            if product['stock'] > 0:
                max_qty = product['stock']
                if purchase_limit > 0:
                    user_name = st.session_state.user['name']
                    historical_quantity = get_user_purchase_history(user_name, product['id'])
                    remaining = max(0, purchase_limit - historical_quantity)
                    max_qty = min(max_qty, remaining)
                if max_qty > 0:
                    quantity = st.number_input(
                        "",
                        min_value=1,
                        max_value=max_qty,
                        value=1,
                        key=f"qty_{product['id']}",
                        label_visibility="collapsed"
                    )
                else:
                    st.write(":red[已达上限]")
            else:
                st.write("-")
        with col7:
            if product['stock'] > 0:
                purchase_limit = product.get('purchase_limit', 0)
                can_add_to_cart = True
                if purchase_limit > 0:
                    user_name = st.session_state.user['name']
                    historical_quantity = get_user_purchase_history(user_name, product['id'])
                    remaining = max(0, purchase_limit - historical_quantity)
                    if remaining <= 0:
                        can_add_to_cart = False
                if can_add_to_cart:
                    if st.button("加入购物车", key=f"add_{product['id']}"):
                        quantity = st.session_state.get(f"qty_{product['id']}", 1)
                        existing_item = None
                        current_cart_quantity = 0
                        for item in st.session_state.cart:
                            if item['product_id'] == product['id']:
                                existing_item = item
                                current_cart_quantity = item['quantity']
                                break
                        purchase_limit = product.get('purchase_limit', 0)
                        user_name = st.session_state.user['name']
                        can_purchase, error_msg = check_purchase_limit(
                            user_name,
                            product['id'],
                            current_cart_quantity,
                            quantity,
                            purchase_limit
                        )
                        if not can_purchase:
                            st.error(error_msg)
                        else:
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
                    st.button("已达上限", disabled=True, key=f"limit_{product['id']}")
            else:
                st.button("库存不足", key=f"out_of_stock_{product['id']}", disabled=True)

    # 分页控件（底部）
    st.divider()
    col_prev, col_page, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.button("上一页", disabled=(page <= 1), key="user_goods_prev_page"):
            st.session_state['user_goods_page'] = page - 1
            st.rerun()
    with col_page:
        st.markdown(f"<div style='text-align:center;'>第 <b>{page}</b> / <b>{total_pages}</b> 页</div>", unsafe_allow_html=True)
    with col_next:
        if st.button("下一页", disabled=(page >= total_pages), key="user_goods_next_page"):
            st.session_state['user_goods_page'] = page + 1
            st.rerun()
    # 购物车展示和结算功能已移至 cart_page()
# 新增购物车页面
def cart_page():
    """购物车页面"""
    st.title("🛒 我的购物车")
    inventory = load_data(INVENTORY_FILE)
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    cart = st.session_state.cart
    if not cart:
        st.info("购物车为空，请先添加商品！")
        return

    total_amount = 0
    quantity_changed = False
    for i, item in enumerate(cart):
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        barcode = 'N/A'
        purchase_limit = 0
        current_stock = 0
        for product in inventory:
            if product.get('id') == item['product_id']:
                barcode = product.get('barcode', 'N/A')
                purchase_limit = product.get('purchase_limit', 0)
                current_stock = product.get('stock', 0)
                break
        with col1:
            product_display = f"{barcode} - {item['product_name']}"
            if purchase_limit > 0:
                user_name = st.session_state.user['name']
                historical_quantity = get_user_purchase_history(user_name, item['product_id'])
                total_with_history = historical_quantity + item['quantity']
                if total_with_history > purchase_limit:
                    product_display += f" ⚠️ (限购{purchase_limit}件，已购{historical_quantity}件，总计{total_with_history}件，超限)"
                elif historical_quantity > 0:
                    product_display += f" (限购{purchase_limit}件，已购{historical_quantity}件)"
                else:
                    product_display += f" (限购{purchase_limit}件)"
            st.write(product_display)
        with col2:
            st.write(f"¥{item['price']}")
        with col3:
            max_quantity = current_stock + item['quantity']
            if purchase_limit > 0:
                user_name = st.session_state.user['name']
                historical_quantity = get_user_purchase_history(user_name, item['product_id'])
                other_cart_quantity = 0
                for j, other_item in enumerate(cart):
                    if j != i and other_item['product_id'] == item['product_id']:
                        other_cart_quantity += other_item['quantity']
                remaining_limit = max(0, purchase_limit - historical_quantity - other_cart_quantity)
                max_quantity = min(max_quantity, remaining_limit)
            if max_quantity > 0:
                new_quantity = st.number_input(
                    "数量",
                    min_value=1,
                    max_value=max_quantity,
                    value=item['quantity'],
                    key=f"cart_qty_{i}",
                    label_visibility="collapsed",
                    help=f"最大可选: {max_quantity}"
                )
                if new_quantity != item['quantity']:
                    if purchase_limit > 0:
                        user_name = st.session_state.user['name']
                        current_cart_quantity = sum(cart_item['quantity'] for j, cart_item in enumerate(cart) if j != i and cart_item['product_id'] == item['product_id'])
                        can_purchase, error_msg = check_purchase_limit(
                            user_name,
                            item['product_id'],
                            current_cart_quantity,
                            new_quantity,
                            purchase_limit
                        )
                        if can_purchase:
                            cart[i]['quantity'] = new_quantity
                            quantity_changed = True
                        else:
                            st.error(error_msg)
                            cart[i]['quantity'] = item['quantity']
                    else:
                        cart[i]['quantity'] = new_quantity
                        quantity_changed = True
            else:
                st.write("无库存")
                cart[i]['_to_remove'] = True
        with col4:
            subtotal = item['price'] * item['quantity']
            st.write(f"¥{subtotal:.2f}")
            total_amount += subtotal
        with col5:
            if st.button("删除", key=f"remove_cart_{i}"):
                cart.pop(i)
                st.rerun()
    st.session_state.cart = [item for item in cart if not item.get('_to_remove', False)]
    if quantity_changed:
        st.rerun()
    st.write(f"### 💰 价格明细")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**商品原价:** ¥{total_amount:.2f}")
        total_items = sum(item['quantity'] for item in cart)
        st.write(f"**商品总件数:** {total_items} 件")
    st.write("### 💳 支付方式")
    st.info("💡 **现金折扣优惠:** 全现金支付享受阶梯折扣！1件85折，2件8折，3件及以上75折")
    col1, col2 = st.columns(2)
    with col1:
        cash_amount = st.number_input("现金支付金额", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    with col2:
        voucher_amount = st.number_input("内购券支付金额", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    if voucher_amount > 0:
        discount_rate = 1.0
        discount_text = "使用内购券，无折扣"
        discount_savings = 0
        final_amount = total_amount
        st.info("🔸 使用内购券支付，按原价结算")
    else:
        if total_items >= 3:
            discount_rate = 0.75
            discount_text = "全现金支付 - 3件及以上75折"
        elif total_items == 2:
            discount_rate = 0.8
            discount_text = "全现金支付 - 2件8折"
        elif total_items == 1:
            discount_rate = 0.85
            discount_text = "全现金支付 - 1件85折"
        else:
            discount_rate = 1.0
            discount_text = "无商品"
        discount_savings = total_amount * (1 - discount_rate)
        final_amount = total_amount - discount_savings
        if discount_rate < 1.0:
            st.success(f"🎉 {discount_text}，优惠¥{discount_savings:.2f}")
    cash_only_amount = total_amount * (0.75 if total_items >= 3 else 0.8 if total_items == 2 else 0.85 if total_items == 1 else 1.0)
    with col2:
        st.write(f"**折扣说明:** {discount_text}")
        if discount_savings > 0:
            st.write(f"**优惠金额:** -¥{discount_savings:.2f}")
        if voucher_amount > 0:
            st.write(f"### **应付金额:** ¥{final_amount:.2f}")
            st.write(f"**全现金支付金额:** ¥{cash_only_amount:.2f}")
        else:
            st.write(f"### **应付金额:** ¥{total_amount:.2f}")
            st.write(f"**全现金支付金额:** ¥{cash_only_amount:.2f}")
            if discount_rate < 1.0:
                st.write(f"**（当前享受折扣）**")
    total_payment = cash_amount + voucher_amount
    required_amount = final_amount
    if total_payment < required_amount:
        if voucher_amount > 0:
            st.error(f"⚠️ 支付金额不足！应付（原价）：¥{required_amount:.2f}，实付：¥{total_payment:.2f}")
        else:
            st.error(f"⚠️ 支付金额不足！应付（折扣价）：¥{required_amount:.2f}，实付：¥{total_payment:.2f}")
        payment_valid = False
    else:
        if total_payment > required_amount:
            overpay = total_payment - required_amount
            st.info(f"💡 多付金额：¥{overpay:.2f}（不设找零）")
        st.success(f"✅ 支付金额确认：¥{total_payment:.2f}")
        payment_valid = True
    if cash_amount > 0 and voucher_amount > 0:
        payment_method = "混合支付"
    elif cash_amount > 0:
        payment_method = "现金支付"
    elif voucher_amount > 0:
        payment_method = "内购券支付"
    else:
        payment_method = "无支付"
    if st.button("提交订单", disabled=not payment_valid):
        inventory = load_data(INVENTORY_FILE)
        can_order = True
        user_name = st.session_state.user['name']
        # 只统计本次订单的商品和金额
        order_items = [dict(item) for item in cart]
        order_total_items = sum(item['quantity'] for item in order_items)
        order_original_amount = sum(item['price'] * item['quantity'] for item in order_items)
        # 现金折扣逻辑
        if voucher_amount > 0:
            order_discount_rate = 1.0
            order_discount_text = "使用内购券，无折扣"
            order_discount_savings = 0
            order_final_amount = order_original_amount
        else:
            if order_total_items >= 3:
                order_discount_rate = 0.75
                order_discount_text = "全现金支付 - 3件及以上75折"
            elif order_total_items == 2:
                order_discount_rate = 0.8
                order_discount_text = "全现金支付 - 2件8折"
            elif order_total_items == 1:
                order_discount_rate = 0.85
                order_discount_text = "全现金支付 - 1件85折"
            else:
                order_discount_rate = 1.0
                order_discount_text = "无商品"
            order_discount_savings = order_original_amount * (1 - order_discount_rate)
            order_final_amount = order_original_amount - order_discount_savings

        for cart_item in order_items:
            for product in inventory:
                if product['id'] == cart_item['product_id']:
                    if product['stock'] < cart_item['quantity']:
                        st.error(f"{product['name']} 库存不足！当前库存: {product['stock']}")
                        can_order = False
                    purchase_limit = product.get('purchase_limit', 0)
                    if purchase_limit > 0:
                        can_purchase, error_msg = check_purchase_limit(
                            user_name,
                            product['id'],
                            0,
                            cart_item['quantity'],
                            purchase_limit
                        )
                        if not can_purchase:
                            st.error(f"{product['name']} - {error_msg}")
                            can_order = False
                    break
        if can_order:
            order = {
                'order_id': str(uuid.uuid4())[:8],
                'user_name': st.session_state.user['name'],
                'items': order_items,
                'original_amount': order_original_amount,
                'total_items': order_total_items,
                'discount_rate': order_discount_rate,
                'discount_text': order_discount_text,
                'discount_savings': order_discount_savings,
                'total_amount': order_final_amount,
                'payment_method': payment_method,
                'cash_amount': cash_amount,
                'voucher_amount': voucher_amount,
                'order_time': datetime.now().isoformat()
            }
            orders = load_data(ORDERS_FILE)
            orders.append(order)
            save_data(ORDERS_FILE, orders)
            for cart_item in order_items:
                for product in inventory:
                    if product['id'] == cart_item['product_id']:
                        product['stock'] -= cart_item['quantity']
                        break
            save_data(INVENTORY_FILE, inventory)
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
        # 兼容旧订单格式
        original_amount = order.get('original_amount', order.get('total_amount', 0))
        final_amount = order.get('total_amount', 0)
        discount_text = order.get('discount_text', '无折扣')
        discount_savings = order.get('discount_savings', 0)
        
        with st.expander(f"订单 {order['order_id']} - {order['order_time'][:19].replace('T', ' ')} - 应付¥{final_amount:.2f}"):
            # 订单基本信息
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**支付方式:** {order['payment_method']}")
                if discount_savings > 0:
                    st.write(f"**折扣优惠:** {discount_text}")
                elif order.get('voucher_amount', 0) > 0:
                    st.write(f"**说明:** 使用内购券，无折扣")
            with col2:
                st.write(f"**商品原价:** ¥{original_amount:.2f}")
                if discount_savings > 0:
                    st.write(f"**优惠金额:** -¥{discount_savings:.2f}")
                st.write(f"**应付金额:** ¥{final_amount:.2f}")
                
                # 显示支付明细
                cash_paid = order.get('cash_amount', 0)
                voucher_paid = order.get('voucher_amount', 0)
                if cash_paid > 0:
                    st.write(f"**现金支付:** ¥{cash_paid:.2f}")
                if voucher_paid > 0:
                    st.write(f"**内购券支付:** ¥{voucher_paid:.2f}")
                
                # 显示多付情况（无找零）
                total_paid = cash_paid + voucher_paid
                if total_paid > final_amount:
                    overpay = total_paid - final_amount
                    st.write(f"**多付:** ¥{overpay:.2f} (不设找零)")
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
        if f'modified_items_{order["order_id"]}' not in st.session_state:
            st.session_state[f'modified_items_{order["order_id"]}'] = order['items'].copy()
        modified_items = st.session_state[f'modified_items_{order["order_id"]}']
        items_to_remove = []
        user_name = order.get('user_name', '')
        for i, item in enumerate(modified_items):
            barcode = 'N/A'
            current_stock = 0
            purchase_limit = 0
            historical_quantity = 0
            for product in inventory:
                if product.get('id') == item['product_id']:
                    barcode = product.get('barcode', 'N/A')
                    current_stock = product.get('stock', 0)
                    purchase_limit = product.get('purchase_limit', 0)
                    break
            # 限购校验：历史已购（不含本订单本商品）
            historical_quantity = get_user_purchase_history(user_name, item['product_id']) - item['quantity']
            # 最大可选 = min(库存+本订单原数量, 限购-历史已购+本订单原数量)
            available_stock = current_stock + item['quantity']
            if purchase_limit > 0:
                max_limit = max(0, purchase_limit - historical_quantity)
                max_quantity = min(available_stock, max_limit)
            else:
                max_quantity = available_stock
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"{barcode} - {item['product_name']}")
            with col2:
                st.write(f"¥{item['price']:.2f}")
            with col3:
                new_quantity = st.number_input(
                    "数量",
                    min_value=0,
                    max_value=max_quantity,
                    value=item['quantity'],
                    key=f"mod_qty_{order['order_id']}_{i}",
                    label_visibility="collapsed",
                    help=f"限购{purchase_limit}，历史已购{historical_quantity}，最大可选{max_quantity}"
                )
                try:
                    modified_items[i]['quantity'] = new_quantity
                    if new_quantity == 0:
                        items_to_remove.append(i)
                except Exception:
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
        
        # 计算商品总数和价格信息
        total_items = sum(item['quantity'] for item in modified_items)
        original_total = sum(item['price'] * item['quantity'] for item in modified_items)
        
        # 显示修改后的金额信息
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**商品原价:** ¥{original_total:.2f}")
            st.write(f"**商品总件数:** {total_items} 件")
        
        # 重新设置支付方式
        st.write("**重新设置支付方式:**")
        st.info("💡 **现金折扣优惠:** 全现金支付享受阶梯折扣！")
        
        col1, col2 = st.columns(2)
        with col1:
            new_cash = st.number_input(
                "现金支付金额", 
                min_value=0.0, 
                value=0.0, 
                step=0.01, 
                format="%.2f", 
                key=f"new_cash_{order['order_id']}"
            )
        with col2:
            new_voucher = st.number_input(
                "内购券支付金额", 
                min_value=0.0, 
                value=0.0, 
                step=0.01, 
                format="%.2f", 
                key=f"new_voucher_{order['order_id']}"
            )
        
        # 计算折扣逻辑
        if new_voucher > 0:
            # 有内购券支付，不享受折扣
            discount_rate = 1.0
            discount_text = "使用内购券，无折扣"
            discount_amount = 0
            final_total = original_total
            st.info("🔸 使用内购券支付，按原价结算")
        else:
            # 全现金支付，享受阶梯折扣
            if total_items >= 3:
                discount_rate = 0.75  # 75折
                discount_text = "全现金支付 - 3件及以上75折"
            elif total_items == 2:
                discount_rate = 0.8   # 8折
                discount_text = "全现金支付 - 2件8折"
            elif total_items == 1:
                discount_rate = 0.85  # 85折
                discount_text = "全现金支付 - 1件85折"
            else:
                discount_rate = 1.0
                discount_text = "无商品"
            
            discount_amount = original_total * (1 - discount_rate)
            final_total = original_total - discount_amount
            
            if discount_rate < 1.0:
                st.success(f"🎉 {discount_text}，优惠¥{discount_amount:.2f}")
        
        # 计算全现金支付金额（享受折扣后的金额）
        cash_only_amount = original_total * (0.75 if total_items >= 3 else 0.8 if total_items == 2 else 0.85 if total_items == 1 else 1.0)
        
        with col2:
            st.write(f"**折扣说明:** {discount_text}")
            if discount_amount > 0:
                st.write(f"**优惠金额:** -¥{discount_amount:.2f}")
            
            # 区分显示两种金额
            if new_voucher > 0:
                # 有内购券时，应付金额是原价，全现金支付金额是折扣价
                st.write(f"**应付金额:** ¥{final_total:.2f}")
                st.write(f"**全现金支付金额:** ¥{cash_only_amount:.2f}")
            else:
                # 全现金支付时，显示折扣后的金额
                st.write(f"**应付金额:** ¥{original_total:.2f}")
                st.write(f"**全现金支付金额:** ¥{cash_only_amount:.2f}")
                if discount_rate < 1.0:
                    st.write(f"**（当前享受折扣）**")
        
        # 检查支付金额
        total_payment = new_cash + new_voucher
        if total_payment < final_total:
            st.error(f"⚠️ 支付金额不足！应付：¥{final_total:.2f}，实付：¥{total_payment:.2f}")
            payment_valid = False
        else:
            if new_voucher > 0:
                # 有内购券支付的情况
                if total_payment > final_total:
                    overpay = total_payment - final_total
                    st.info(f"💡 多付金额：¥{overpay:.2f}（不设找零）")
            st.success(f"✅ 支付金额确认：¥{total_payment:.2f}")
            payment_valid = True
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("确认修改", key=f"confirm_modify_{order['order_id']}", disabled=not payment_valid or not modified_items):
                # 新增限购校验
                limit_error = False
                for item in modified_items:
                    for product in inventory:
                        if product.get('id') == item['product_id']:
                            purchase_limit = product.get('purchase_limit', 0)
                            if purchase_limit > 0:
                                # 获取历史购买数量（不包含当前订单）
                                all_orders = load_data(ORDERS_FILE)
                                historical_quantity = 0
                                for hist_order in all_orders:
                                    if hist_order['user_name'] == user_name and hist_order['order_id'] != order['order_id']:
                                        for hist_item in hist_order.get('items', []):
                                            if hist_item.get('product_id') == item['product_id']:
                                                historical_quantity += hist_item.get('quantity', 0)
                                
                                if item['quantity'] + historical_quantity > purchase_limit:
                                    st.error(f"商品【{item['product_name']}】限购{purchase_limit}件，您已购{historical_quantity}件，本次修改后共{item['quantity']+historical_quantity}件，超出限购！")
                                    limit_error = True
                            break
                if limit_error:
                    return
                if update_order(order, modified_items, new_cash, new_voucher, final_total, discount_rate, discount_text, discount_amount, inventory):
                    st.success("订单修改成功！")
                    if f'modified_items_{order["order_id"]}' in st.session_state:
                        del st.session_state[f'modified_items_{order["order_id"]}']
                    if 'modifying_order' in st.session_state:
                        del st.session_state['modifying_order']
                    st.balloons()
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
        available_products = [p for p in inventory if p['stock'] > 0]
        
        if not available_products:
            st.info("暂无可添加的商品")
            return
        
        # 商品选择
        product_options = {f"{p.get('barcode', 'N/A')} - {p['name']} (库存:{p['stock']})": p for p in available_products}
        selected_product_name = st.selectbox("选择商品", list(product_options.keys()), key=f"add_product_{order['order_id']}")
        selected_product = product_options[selected_product_name]
        
        # 限购信息显示和数量选择    
        purchase_limit = selected_product.get('purchase_limit', 0)
        user_name = order.get('user_name', '')
        historical_quantity = get_user_purchase_history(user_name, selected_product['id'])
        current_quantity_in_order = 0
        for item in order['items']:
            if item['product_id'] == selected_product['id']:
                current_quantity_in_order = item['quantity']
                break
        remaining_limit = max(0, purchase_limit - historical_quantity - current_quantity_in_order)
        max_add_quantity = min(selected_product['stock'], remaining_limit)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"限购信息：\n- 限购数量：{purchase_limit}件\n- 历史已购：{historical_quantity}件\n- 当前订单：{current_quantity_in_order}件\n- 可添加：{remaining_limit}件")
        with col2:
            if max_add_quantity > 0:
                add_quantity = st.number_input("数量", min_value=1, max_value=max_add_quantity, value=1, key=f"add_qty_{order['order_id']}")
            else:
                st.error("已达限购上限，无法添加")
        
        if st.button("添加到订单", key=f"add_to_order_{order['order_id']}"):
            # 添加商品到修改列表
            if f'modified_items_{order["order_id"]}' not in st.session_state:
                st.session_state[f'modified_items_{order["order_id"]}'] = order['items'].copy()
            modified_items = st.session_state[f'modified_items_{order["order_id"]}']
            
            # 检查是否已存在相同商品
            existing_item = None
            for item in modified_items:
                if item['product_id'] == selected_product['id']:
                    existing_item = item
                    break
            
            # 限购检查
            purchase_limit = selected_product.get('purchase_limit', 0)
            user_name = order.get('user_name', '')
            can_purchase, error_msg = check_purchase_limit(
                user_name,
                selected_product['id'],
                0,
                add_quantity,
                purchase_limit
            )
            
            if not can_purchase:
                st.error(error_msg)
            else:
                if existing_item:
                    existing_item['quantity'] += add_quantity
                else:
                    modified_items.append({
                        'product_id': selected_product['id'],
                        'product_name': selected_product['name'],
                        'price': selected_product['price'],
                        'quantity': add_quantity
                    })
                st.success(f"已添加 {add_quantity} 个 {selected_product['name']} 到订单")
                st.balloons()
                safe_rerun()
    
    with tab3:
        st.write("**⚠️ 警告：撤销订单将恢复所有商品库存**")
        # 显示将要恢复的库存
        inventory = load_data(INVENTORY_FILE)
        user_names = [user['name'] for user in load_data(USERS_FILE)]
        selected_user = st.selectbox("选择用户查看购买历史", user_names, key="check_user_history")
        for item in order['items']:
            barcode = 'N/A'
            for product in inventory:
                if product.get('id') == item['product_id']:
                    barcode = product.get('barcode', 'N/A')
                    break
            st.write(f"- {barcode} - {item['product_name']}: +{item['quantity']}")
        
        if st.button("确认撤销订单", key=f"confirm_cancel_{order['order_id']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**订单商品列表:**")
                for item in order['items']:
                    barcode = 'N/A'
                    for product in inventory:
                        if product.get('id') == item['product_id']:
                            barcode = product.get('barcode', 'N/A')
                            break
                    st.write(f"- {barcode} - {item['product_name']} (库存:{item['quantity']})")
            
            with col2:
                st.write("**订单金额信息:**")
                original_total = sum(item['price'] * item['quantity'] for item in order['items'])
                st.write(f"**原订单总金额:** ¥{original_total:.2f}")
        
        # 撤销订单 - 恢复库存
        if st.button("撤销订单", key=f"final_cancel_{order['order_id']}"):
            if cancel_order(order, inventory):
                st.success("订单已成功撤销！")
                st.balloons()
                safe_rerun()
            else:
                st.error("订单撤销失败，请重试")

# 数据库状态检查        
def database_status_check():   # 根据用户角色显示不同页面
    """数据库状态检查页面"""st.session_state.user['role'] == 'admin':
    st.subheader("🔍 数据库状态检查")dmin_page()
    e:
    col1, col2 = st.columns(2)()
    
    with col1:== "__main__":
        st.write("### 📊 数据统计")
        try:
            # 使用统一的数据库接口t Exception:
            inventory = get_inventory()的错误
            orders = get_orders()
            users = get_users()                        # 显示基本统计            st.metric("商品总数", len(inventory))            st.metric("订单总数", len(orders))            st.metric("用户总数", len(users))                        # 显示有库存的商品数量            in_stock_count = len([item for item in inventory if item.get('stock', 0) > 0])            st.metric("有库存商品", in_stock_count)                        # 显示限购商品数量            limited_count = len([item for item in inventory if item.get('purchase_limit', 0) > 0])            st.metric("限购商品", limited_count)                    except Exception as e:            st.error(f"❌ 数据库查询失败: {str(e)}")        with col2:        st.write("### 🔧 环境信息")                # 检查环境变量        import os        database_url = os.getenv('DATABASE_URL')        if database_url:            st.success("✅ 生产环境: PostgreSQL")
            st.write(f"**数据库URL:** {db_url[:50]}...")
            
            # 解析数据库URL
            if 'postgresql://' in db_url:
                st.write("**数据库类型:** PostgreSQL")
            elif 'sqlite://' in db_url:
                st.write("**数据库类型:** SQLite")
            else:
                st.write("**数据库类型:** 未知")
        else:
            st.warning("⚠️ 开发环境: SQLite")
            st.write("**数据库文件:** 本地 SQLite 文件")
        
        # 检查数据库连接
        try:
            from database import get_database_manager
            db_manager = get_database_manager()
            st.write("**数据库管理器:** 已初始化")
            
            # 尝试简单查询
            users = db_manager.load_users()
            st.write(f"**连接测试:** 成功读取 {len(users)} 个用户")
            
        except Exception as e:
            st.error(f"❌ 数据库连接异常: {str(e)}")
    
    # 详细数据展示
    st.write("### 📝 数据详情")
    
    detail_tab1, detail_tab2, detail_tab3 = st.tabs(["商品数据", "订单数据", "用户数据"])
    
    with detail_tab1:
        try:
            inventory = get_inventory()
            if inventory:
                st.write(f"**商品总数:** {len(inventory)}")
                
                # 显示前5个商品
                st.write("**商品示例 (前5个):**")
                for i, item in enumerate(inventory[:5]):
                    name = item.get('name', '未知商品')
                    stock = item.get('stock', 0)
                    price = item.get('price', 0)
                    barcode = item.get('barcode', 'N/A')
                    st.write(f"{i+1}. [{barcode}] {name} - 库存:{stock} - 价格:¥{price}")
                
                # 库存统计
                total_stock = sum(item.get('stock', 0) for item in inventory)
                avg_price = sum(item.get('price', 0) for item in inventory) / len(inventory) if inventory else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("总库存量", total_stock)
                with col2:
                    st.metric("平均价格", f"¥{avg_price:.2f}")
                with col3:
                    zero_stock = len([item for item in inventory if item.get('stock', 0) == 0])
                    st.metric("零库存商品", zero_stock)
            else:
                st.info("📦 暂无商品数据")
        except Exception as e:
            st.error(f"❌ 商品数据查询失败: {str(e)}")
    
    with detail_tab2:
        try:
            orders = get_orders()
            if orders:
                st.write(f"**订单总数:** {len(orders)}")
                
                # 显示最近5个订单
                st.write("**最近订单 (最新5个):**")
                recent_orders = sorted(orders, key=lambda x: x.get('order_time', ''), reverse=True)[:5]
                
                for i, order in enumerate(recent_orders):
                    order_id = order.get('order_id', '未知')
                    user_name = order.get('user_name', '未知用户')
                    total_amount = order.get('total_amount', 0)
                    order_time = order.get('order_time', '未知时间')[:19].replace('T', ' ')
                    st.write(f"{i+1}. [{order_id}] {user_name} - ¥{total_amount:.2f} - {order_time}")
                
                # 订单统计
                total_sales = sum(order.get('total_amount', 0) for order in orders)
                total_cash = sum(order.get('cash_amount', 0) for order in orders)
                total_voucher = sum(order.get('voucher_amount', 0) for order in orders)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("总销售额", f"¥{total_sales:.2f}")
                with col2:
                    st.metric("现金收入", f"¥{total_cash:.2f}")
                with col3:
                    st.metric("内购券收入", f"¥{total_voucher:.2f}")
            else:
                st.info("📋 暂无订单数据")
        except Exception as e:
            st.error(f"❌ 订单数据查询失败: {str(e)}")
    
    with detail_tab3:
        try:
            users = get_users()
            if users:
                st.write(f"**用户总数:** {len(users)}")
                
                # 显示所有用户
                st.write("**用户列表:**")
                for i, user in enumerate(users):
                    name = user.get('name', '未知')
                    username = user.get('username', '未知')
                    role = user.get('role', 'user')
                    role_icon = "👑" if role == 'admin' else "👤"
                    st.write(f"{i+1}. {role_icon} {name} ({username}) - {role}")
                
                # 用户统计
                admin_count = len([user for user in users if user.get('role') == 'admin'])
                user_count = len([user for user in users if user.get('role') == 'user'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("管理员数量", admin_count)
                with col2:
                    st.metric("普通用户数量", user_count)
            else:
                st.info("👥 暂无用户数据")
        except Exception as e:
            st.error(f"❌ 用户数据查询失败: {str(e)}")
    
    # 数据库操作测试
    st.write("### 🧪 数据库功能测试")
    
    test_col1, test_col2, test_col3 = st.columns(3)
    
    with test_col1:
        if st.button("🔄 刷新数据", help="重新加载所有数据"):
            try:
                # 强制刷新缓存
                st.cache_data.clear()
                st.success("✅ 数据已刷新")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 刷新失败: {str(e)}")
    
    with test_col2:
        if st.button("📥 导出数据", help="导出当前数据库数据"):
            try:
                from datetime import datetime
                import json
                
                inventory = get_inventory()
                orders = get_orders()
                users = get_users()
                
                export_data = {
                    'export_time': datetime.now().isoformat(),
                    'inventory_count': len(inventory),
                    'orders_count': len(orders),
                    'users_count': len(users),
                    'inventory': inventory[:10],  # 只导出前10个商品作为示例
                    'orders': orders[:10],        # 只导出前10个订单作为示例
                    'users': [{'name': u.get('name'), 'role': u.get('role')} for u in users]  # 不导出密码
                }
                
                export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
                st.download_button(
                    label="下载数据文件",
                    data=export_json,
                    file_name=f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                st.success("✅ 数据导出准备完成")
                
            except Exception as e:
                st.error(f"❌ 导出失败: {str(e)}")
    
    with test_col3:
        if st.button("🔍 连接测试", help="测试数据库连接"):
            try:
                from database import get_database_manager
                db = get_database_manager()
                
                # 测试各种操作
                test_results = []
                
                # 测试读取操作
                try:
                    inventory = db.load_inventory()
                    test_results.append("✅ 商品数据读取")
                except Exception as e:
                    test_results.append(f"❌ 商品数据读取失败: {str(e)[:50]}")
                
                try:
                    orders = db.load_orders()
                    test_results.append("✅ 订单数据读取")
                except Exception as e:
                    test_results.append(f"❌ 订单数据读取失败: {str(e)[:50]}")
                
                try:
                    users = db.load_users()
                    test_results.append("✅ 用户数据读取")
                except Exception as e:
                    test_results.append(f"❌ 用户数据读取失败: {str(e)[:50]}")
                
                # 显示测试结果
                for result in test_results:
                    if "✅" in result:
                        st.success(result)
                    else:
                        st.error(result)
                
            except Exception as e:
                st.error(f"❌ 连接测试失败: {str(e)}")
    
    # 新增：数据库写入测试
    st.write("### 🧪 数据库写入测试")
    st.info("💡 这些测试可以帮助诊断生产环境中的数据写入问题")
    
    write_test_col1, write_test_col2, write_test_col3 = st.columns(3)
    
    with write_test_col1:
        if st.button("🧪 测试商品写入", help="测试商品数据是否能正确写入数据库"):
            try:
                # 创建测试商品
                import uuid
                test_product = {
                    "id": f"test_{str(uuid.uuid4())[:8]}",
                    "name": f"测试商品_{datetime.now().strftime('%H%M%S')}",
                    "price": 1.0,
                    "stock": 1,
                    "description": "数据库写入测试商品",
                    "barcode": f"TEST{datetime.now().strftime('%H%M%S')}",
                    "purchase_limit": 0,
                    "created_at": datetime.now().isoformat()
                }
                
                # 获取当前商品数量
                current_inventory = db.load_inventory()
                before_count = len(current_inventory)
                st.info(f"写入前商品数量: {before_count}")
                
                # 添加测试商品
                new_inventory = current_inventory + [test_product]
                db.save_inventory(new_inventory)
                
                # 验证写入
                import time
                time.sleep(0.5)
                after_inventory = db.load_inventory()
                after_count = len(after_inventory)
                
                st.info(f"写入后商品数量: {after_count}")
                
                if after_count > before_count:
                    st.success("✅ 商品写入测试成功！")
                    # 清理测试数据
                    cleaned_inventory = [p for p in after_inventory if not p['id'].startswith('test_')]
                    db.save_inventory(cleaned_inventory)
                    st.info("🧹 测试数据已清理")
                else:
                    st.error("❌ 商品写入测试失败！")
                    
            except Exception as e:
                st.error(f"❌ 商品写入测试异常: {str(e)}")
                st.code(str(e))
    
    with write_test_col2:
        if st.button("🧪 测试用户写入", help="测试用户数据是否能正确写入数据库"):
            try:
                # 创建测试用户
                test_user = {
                    "username": f"test_{datetime.now().strftime('%H%M%S')}",
                    "password": "test123",
                    "name": f"测试用户_{datetime.now().strftime('%H%M%S')}",
                    "role": "user"
                }
                
                # 获取当前用户数量
                before_users = db.load_users()
                before_count = len(before_users)
                st.info(f"写入前用户数量: {before_count}")
                
                # 添加测试用户
                db.add_user(test_user)
                
                # 验证写入
                import time
                time.sleep(0.5)
                after_users = db.load_users()
                after_count = len(after_users)
                
                st.info(f"写入后用户数量: {after_count}")
                
                if after_count > before_count:
                    st.success("✅ 用户写入测试成功！")
                else:
                    st.error("❌ 用户写入测试失败！")
                    
            except Exception as e:
                st.error(f"❌ 用户写入测试异常: {str(e)}")
                st.code(str(e))
    
    with write_test_col3:
        if st.button("🔍 数据库环境检查", help="检查当前数据库环境和配置"):
            try:
                import os
                
                st.write("### 🔧 数据库环境信息")
                
                # 检查环境变量
                if 'DATABASE_URL' in os.environ:
                    db_url = os.environ['DATABASE_URL']
                    st.success("✅ 生产环境: PostgreSQL")
                    st.write(f"**数据库URL:** {db_url[:50]}...")
                    
                    # 解析数据库URL
                    if 'postgresql://' in db_url:
                        st.write("**数据库类型:** PostgreSQL")
                    elif 'sqlite://' in db_url:
                        st.write("**数据库类型:** SQLite")
                    else:
                        st.write("**数据库类型:** 未知")
                else:
                    st.warning("⚠️ 开发环境: SQLite")
                    st.write("**数据库文件:** 本地 SQLite 文件")
                
                # 检查数据库连接
                from database import get_database_manager
                db_manager = get_database_manager()
                st.write("**数据库管理器:** 已初始化")
                
                # 尝试简单查询
                users = db_manager.load_users()
                st.write(f"**连接测试:** 成功读取 {len(users)} 个用户")
                
            except Exception as e:
                st.error(f"❌ 数据库环境检查失败: {str(e)}")
                st.code(str(e))
