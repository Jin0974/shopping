import streamlit as st
import pandas as pd
import os
import time
import contextlib
import io
import traceback
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
    
    # 购物车初始化
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # 商品列表显示
    st.subheader("🛍️ 商品列表")
    
    # 简化的商品展示（每页10个商品）
    PAGE_SIZE = 10
    total_items = len(inventory)
    total_pages = (total_items + PAGE_SIZE - 1) // PAGE_SIZE
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    
    # 分页控制
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ 上一页") and st.session_state.current_page > 1:
                st.session_state.current_page -= 1
                st.rerun()
        with col2:
            st.write(f"第 {st.session_state.current_page} 页，共 {total_pages} 页")
        with col3:
            if st.button("➡️ 下一页") and st.session_state.current_page < total_pages:
                st.session_state.current_page += 1
                st.rerun()
    
    # 计算当前页显示的商品
    start_idx = (st.session_state.current_page - 1) * PAGE_SIZE
    end_idx = min(start_idx + PAGE_SIZE, total_items)
    current_products = inventory[start_idx:end_idx]
    
    # 显示商品
    for i in range(0, len(current_products), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(current_products):
                product = current_products[i + j]
                with col:
                    with st.container():
                        st.write(f"**{product['name']}**")
                        st.write(f"💰 价格: ¥{product['price']:.2f}")
                        st.write(f"📦 库存: {product['stock']}")
                        if product.get('purchase_limit', 0) > 0:
                            st.write(f"🚫 限购: {product['purchase_limit']}件")
                        
                        if product['stock'] > 0:
                            quantity = st.number_input(
                                "数量",
                                min_value=1,
                                max_value=min(product['stock'], product.get('purchase_limit', 999) if product.get('purchase_limit', 0) > 0 else 999),
                                value=1,
                                key=f"qty_{product['id']}"
                            )
                            
                            if st.button(f"🛒 加入购物车", key=f"add_{product['id']}"):
                                # 检查限购
                                can_purchase, error_msg = check_purchase_limit(
                                    st.session_state.user['name'],
                                    product['id'],
                                    sum(item['quantity'] for item in st.session_state.cart if item['product_id'] == product['id']),
                                    quantity,
                                    product.get('purchase_limit', 0)
                                )
                                
                                if can_purchase:
                                    # 检查购物车中是否已有此商品
                                    found = False
                                    for cart_item in st.session_state.cart:
                                        if cart_item['product_id'] == product['id']:
                                            cart_item['quantity'] += quantity
                                            found = True
                                            break
                                    
                                    if not found:
                                        st.session_state.cart.append({
                                            'product_id': product['id'],
                                            'quantity': quantity
                                        })
                                    
                                    st.success(f"✅ 已添加 {quantity} 件 {product['name']} 到购物车")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(error_msg)
                        else:
                            st.error("缺货")
                        
                        st.divider()

# 新增购物车页面
def cart_page():
    """购物车页面"""
    st.subheader("🛒 购物车")
    
    if 'cart' not in st.session_state or not st.session_state.cart:
        st.info("购物车为空，去购买一些商品吧！")
        return
    
    cart = st.session_state.cart
    inventory = get_inventory()
    
    # 创建商品ID到库存的映射
    inventory_map = {item['id']: item for item in inventory}
    
    # 显示购物车商品
    total_amount = 0
    cart_items = []
    
    for item in cart:
        product_id = item['product_id']
        quantity = item['quantity']
        
        # 获取最新的商品信息
        if product_id in inventory_map:
            product = inventory_map[product_id]
            item_total = product['price'] * quantity
            total_amount += item_total
            
            cart_items.append({
                'product_id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'total': item_total,
                'stock': product['stock']
            })
    
    if cart_items:
        # 显示购物车内容
        df = pd.DataFrame(cart_items)
        df['价格'] = df['price'].apply(lambda x: f"¥{x:.2f}")
        df['小计'] = df['total'].apply(lambda x: f"¥{x:.2f}")
        df = df[['name', '价格', 'quantity', '小计']]
        df.columns = ['商品名称', '单价', '数量', '小计']
        
        st.dataframe(df, use_container_width=True)
        st.write(f"### 总计: ¥{total_amount:.2f}")
        
        # 结账按钮
        if st.button("💳 立即结账", type="primary"):
            checkout_order(cart_items, total_amount)
    else:
        st.error("购物车中的商品信息有误，请重新添加")

# 订单历史页面
def order_history_page():
    """订单历史页面"""
    st.subheader("📋 我的订单")
    
    user_name = st.session_state.user['name']
    orders = get_orders()
    
    # 筛选当前用户的订单
    user_orders = [order for order in orders if order.get('user_name') == user_name]
    
    if not user_orders:
        st.info("您还没有任何订单")
        return
    
    # 按时间排序，最新的在前
    user_orders.sort(key=lambda x: x.get('order_time', ''), reverse=True)
    
    for order in user_orders:
        with st.expander(f"订单 {order.get('order_id', 'N/A')} - {order.get('order_time', '')[:19].replace('T', ' ')}"):
            st.write(f"**订单时间:** {order.get('order_time', 'N/A')[:19].replace('T', ' ')}")
            st.write(f"**总金额:** ¥{order.get('total_amount', 0):.2f}")
            st.write(f"**现金支付:** ¥{order.get('cash_amount', 0):.2f}")
            st.write(f"**内购券支付:** ¥{order.get('voucher_amount', 0):.2f}")
            
            # 显示商品明细
            items = order.get('items', [])
            if items:
                st.write("**商品明细:**")
                for item in items:
                    st.write(f"- {item.get('product_name', 'N/A')} × {item.get('quantity', 0)} = ¥{item.get('total_price', 0):.2f}")

# 用户订单历史页面（别名）
def user_order_history():
    """用户订单历史页面"""
    order_history_page()

# 结账处理
def checkout_order(cart_items, total_amount):
    """处理结账"""
    try:
        # 显示支付方式选择
        st.write("### 选择支付方式")
        
        payment_method = st.selectbox("支付方式", ["现金", "内购券", "混合支付"])
        
        cash_amount = 0
        voucher_amount = 0
        
        if payment_method == "现金":
            cash_amount = total_amount
            voucher_amount = 0
        elif payment_method == "内购券":
            cash_amount = 0
            voucher_amount = total_amount
        else:  # 混合支付
            col1, col2 = st.columns(2)
            with col1:
                cash_amount = st.number_input("现金金额", min_value=0.0, max_value=total_amount, value=0.0, step=0.01)
            with col2:
                voucher_amount = total_amount - cash_amount
                st.write(f"内购券金额: ¥{voucher_amount:.2f}")
        
        if st.button("确认支付"):
            # 创建订单
            order_id = f"ORD{int(time.time())}"
            order_data = {
                'order_id': order_id,
                'user_name': st.session_state.user['name'],
                'items': [
                    {
                        'product_id': item['product_id'],
                        'product_name': item['name'],
                        'quantity': item['quantity'],
                        'unit_price': item['price'],
                        'total_price': item['total']
                    }
                    for item in cart_items
                ],
                'total_amount': total_amount,
                'cash_amount': cash_amount,
                'voucher_amount': voucher_amount,
                'order_time': datetime.now().isoformat()
            }
            
            # 保存订单
            add_order(order_data)
            
            # 更新库存
            inventory = get_inventory()
            for cart_item in cart_items:
                for product in inventory:
                    if product['id'] == cart_item['product_id']:
                        product['stock'] -= cart_item['quantity']
                        break
            
            save_inventory(inventory)
            
            # 清空购物车
            st.session_state.cart = []
            
            st.success(f"✅ 订单 {order_id} 创建成功！")
            st.balloons()
            time.sleep(2)
            st.rerun()
            
    except Exception as e:
        st.error(f"结账失败: {str(e)}")

# 数据库状态检查
def database_status_check():
    """数据库状态检查页面"""
    st.subheader("🔍 数据库状态检查")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 📊 数据统计")
        try:
            # 使用统一的数据库接口
            inventory = get_inventory()
            orders = get_orders()
            users = get_users()
            
            # 显示基本统计
            st.metric("商品总数", len(inventory))
            st.metric("订单总数", len(orders))
            st.metric("用户总数", len(users))
            
            # 显示有库存的商品数量
            in_stock_count = len([item for item in inventory if item.get('stock', 0) > 0])
            st.metric("有库存商品", in_stock_count)
            
            # 显示限购商品数量
            limited_count = len([item for item in inventory if item.get('purchase_limit', 0) > 0])
            st.metric("限购商品", limited_count)
            
        except Exception as e:
            st.error(f"❌ 数据库查询失败: {str(e)}")
    
    with col2:
        st.write("### 🔧 环境信息")
        
        # 详细的环境变量检查
        import os
        database_url = os.getenv('DATABASE_URL')
        st.write("### 🔍 详细诊断")
        st.write(f"**DATABASE_URL环境变量存在:** {'是' if database_url else '否'}")
        
        if database_url:
            st.success("✅ 检测到DATABASE_URL环境变量")
            # 安全显示URL（隐藏密码）
            if '@' in database_url:
                parts = database_url.split('@')
                if len(parts) >= 2:
                    prefix = parts[0].split('://')[0]
                    suffix = '@' + parts[1]
                    masked_url = f"{prefix}://***:***{suffix}"
                else:
                    masked_url = database_url[:20] + "..."
            else:
                masked_url = database_url[:50] + "..."
            st.write(f"**数据库URL:** {masked_url}")
            
            # 解析数据库类型
            if 'postgresql://' in database_url:
                st.write("**数据库类型:** PostgreSQL")
                st.success("✅ 生产环境: PostgreSQL")
            elif 'sqlite://' in database_url:
                st.write("**数据库类型:** SQLite")
                st.warning("⚠️ 仍在使用SQLite（URL配置错误）")
            else:
                st.write("**数据库类型:** 未知")
                st.error("❌ 数据库URL格式不正确")
                
            # 显示主机信息
            try:
                if '@' in database_url:
                    host_part = database_url.split('@')[1].split('/')[0]
                    st.write(f"**数据库主机:** {host_part}")
            except:
                pass
        else:
            st.error("❌ DATABASE_URL环境变量未设置")
            st.warning("⚠️ 开发环境: SQLite")
            st.write("**数据库文件:** 本地 SQLite 文件")
        
        # 显示关键环境变量（调试用）
        st.write("### 🐛 环境变量调试")
        env_vars = dict(os.environ)
        db_related = {k: v for k, v in env_vars.items() if 'DATABASE' in k.upper()}
        if db_related:
            st.write("**数据库相关环境变量:**")
            for k, v in db_related.items():
                # 隐藏敏感信息
                if len(v) > 20:
                    masked_v = v[:10] + "..." + v[-10:]
                else:
                    masked_v = v[:10] + "..." if len(v) > 10 else v
                st.write(f"- {k}: {masked_v}")
        else:
            st.write("**没有找到DATABASE_URL环境变量**")
        else:
            st.error("❌ 开发环境: SQLite")
            st.write("**数据库文件:** 本地 SQLite 文件")
            
            # 添加解决方案提示
            with st.expander("📋 PostgreSQL配置说明", expanded=True):
                st.write("**您的应用正在使用SQLite，需要配置PostgreSQL：**")
                st.write("1. 在Render仪表板创建PostgreSQL数据库")
                st.write("2. 复制 'External Database URL'")
                st.write("3. 在应用环境变量中添加:")
                st.code("Key: DATABASE_URL\nValue: postgresql://user:pass@host:port/db")
                st.write("4. 重新部署应用")
                
                # 检查是否在Render环境
                if 'RENDER' in os.environ:
                    st.warning("🚨 检测到Render环境但未配置PostgreSQL!")
                else:
                    st.info("ℹ️ 本地开发环境正常使用SQLite")
        
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
    
    # 数据库写入测试
    st.write("### 🧪 数据库写入测试")
    
    write_test_col1, write_test_col2, write_test_col3, write_test_col4 = st.columns(4)
    
    with write_test_col1:
        if st.button("🧪 测试商品写入", help="测试商品数据是否能正确写入数据库"):
            try:
                # 创建测试商品
                test_product = {
                    'id': f'test_{int(time.time())}',
                    'barcode': f'TEST{int(time.time())}',
                    'name': '测试商品',
                    'price': 1.0,
                    'stock': 1,
                    'description': '数据库写入测试商品',
                    'purchase_limit': 0,
                    'created_at': datetime.now().isoformat()
                }
                
                # 获取当前商品数量
                before_inventory = db.load_inventory()
                before_count = len(before_inventory)
                st.info(f"写入前商品数量: {before_count}")
                
                # 添加测试商品
                new_inventory = before_inventory + [test_product]
                db.save_inventory(new_inventory)
                
                # 验证写入
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
                    'username': f'test_user_{int(time.time())}',
                    'password': 'test123',
                    'name': f'测试用户{int(time.time())}',
                    'role': 'user'
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
    
    with write_test_col4:
        if st.button("🗑️ 强制清空数据库", help="强制清空所有数据（商品、订单、用户）"):
            try:
                st.warning("⚠️ 正在清空数据库...")
                
                # 显示清空前状态
                before_inventory = db.load_inventory()
                before_orders = db.load_orders()
                before_users = db.load_users()
                
                st.write(f"清空前 - 商品: {len(before_inventory)}, 订单: {len(before_orders)}, 用户: {len(before_users)}")
                
                # 强制清空
                db.save_inventory([])
                db.clear_orders()
                db.clear_users()
                
                # 验证清空结果
                time.sleep(0.5)
                after_inventory = db.load_inventory()
                after_orders = db.load_orders()
                after_users = db.load_users()
                
                st.write(f"清空后 - 商品: {len(after_inventory)}, 订单: {len(after_orders)}, 用户: {len(after_users)}")
                
                if len(after_inventory) == 0 and len(after_orders) == 0 and len(after_users) == 0:
                    st.success("✅ 数据库清空成功！")
                else:
                    st.error("❌ 数据库清空失败！")
                    
            except Exception as e:
                st.error(f"❌ 数据库清空异常: {str(e)}")
                st.code(str(e))


# 主程序入口
def main():
    """主程序"""
    # 初始化数据
    initialize_data()
    
    # 检查登录状态
    if 'user' not in st.session_state:
        login_page()
    else:
        # 根据用户角色显示不同页面
        if st.session_state.user['role'] == 'admin':
            admin_page()
        else:
            user_page()

# 运行应用
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"应用启动失败: {str(e)}")
        st.code(str(e))
