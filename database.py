import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import streamlit as st
import uuid

# 数据库配置
Base = declarative_base()

# 用户模型
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), default='user')

# 商品模型
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(String(50), primary_key=True)  # 使用字符串ID以兼容现有数据
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    barcode = Column(String(50))
    description = Column(Text)
    purchase_limit = Column(Integer, default=0)  # 限购数量，0表示不限购
    created_at = Column(String(50))  # 存储ISO格式时间字符串

# 订单模型
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(String(50), unique=True, nullable=False)
    user_name = Column(String(100), nullable=False)
    items_json = Column(Text, nullable=False)  # JSON格式存储商品列表
    original_amount = Column(Float, nullable=False)
    total_items = Column(Integer, nullable=False)
    discount_rate = Column(Float, nullable=False)
    discount_text = Column(String(200), nullable=False)
    discount_savings = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    cash_amount = Column(Float, nullable=False)
    voucher_amount = Column(Float, nullable=False)
    order_time = Column(String(50), nullable=False)  # 存储ISO格式时间字符串

# 数据库连接和操作类
class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.connect()
    
    def connect(self):
        """连接数据库"""
        try:
            # 从环境变量获取数据库URL
            database_url = os.getenv('DATABASE_URL')
            print(f"🔍 环境变量检查:")
            print(f"   DATABASE_URL存在: {'是' if database_url else '否'}")
            
            if not database_url:
                # 开发环境使用SQLite
                database_url = 'sqlite:///purchase_system.db'
                print("⚠️  使用本地SQLite数据库")
            else:
                # Render PostgreSQL URL 格式修正
                if database_url.startswith('postgres://'):
                    print("⚠️  检测到老版本postgres://URL，自动修正为postgresql://")
                    database_url = database_url.replace('postgres://', 'postgresql://', 1)
                print("✅ 使用PostgreSQL数据库")
                if '@' in database_url:
                    try:
                        host_info = database_url.split('@')[1].split('/')[0]
                        print(f"数据库主机: {host_info}")
                    except:
                        print("数据库主机: 解析失败")
            
            # 根据数据库类型配置连接参数
            if database_url.startswith('sqlite://'):
                # SQLite配置
                self.engine = create_engine(
                    database_url,
                    echo=False,  # SQLite不需要详细日志
                    connect_args={'check_same_thread': False}
                )
            else:
                # PostgreSQL配置
                self.engine = create_engine(
                    database_url,
                    pool_pre_ping=True,
                    pool_recycle=300,  # 连接回收时间5分钟
                    pool_size=5,  # 连接池大小
                    max_overflow=10,  # 最大溢出连接
                    echo=False,  # 生产环境关闭详细日志
                    connect_args={
                        'sslmode': 'require',  # 要求SSL连接
                        'connect_timeout': 30,  # 连接超时30秒
                    }
                )
            
            self.Session = sessionmaker(bind=self.engine)
            
            # 测试数据库连接
            print("🔍 测试数据库连接...")
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("✅ 数据库连接测试成功")
            
            # 创建表
            print("🔍 创建/验证数据库表...")
            Base.metadata.create_all(self.engine)
            print("✅ 数据库表创建/验证完成")
            
            # 初始化管理员用户
            print("🔍 初始化管理员用户...")
            self.init_admin_user()
            print("✅ 管理员用户初始化完成")
            
            # 显示连接成功信息
            db_type = "SQLite" if database_url.startswith('sqlite://') else "PostgreSQL"
            print(f"🎉 {db_type}数据库连接成功！")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ 数据库连接失败: {error_msg}")
            
            # 提供具体的错误诊断
            if "password authentication failed" in error_msg:
                print("🔑 诊断: 数据库密码认证失败")
                print("   解决方案: 检查DATABASE_URL中的用户名和密码")
            elif "could not connect to server" in error_msg:
                print("🌐 诊断: 无法连接到数据库服务器")
                print("   解决方案: 检查网络连接和数据库服务器状态")
            elif "does not exist" in error_msg:
                print("🗄️ 诊断: 数据库不存在")
                print("   解决方案: 检查DATABASE_URL中的数据库名称")
            elif "SSL connection has been closed unexpectedly" in error_msg:
                print("🔒 诊断: SSL连接问题")
                print("   解决方案: 检查SSL配置")
            
            # 在Streamlit中也显示错误
            if hasattr(st, 'error'):
                st.error(f"数据库连接失败: {error_msg}")
            
            raise e
    
    def get_session(self):
        """获取数据库会话"""
        return self.Session()
    
    def init_admin_user(self):
        """初始化管理员用户"""
        session = self.get_session()
        try:
            admin_user = session.query(User).filter_by(name="管理员666").first()
            if not admin_user:
                admin_user = User(
                    username="admin666",
                    password="admin123",
                    name="管理员666",
                    role="admin"
                )
                session.add(admin_user)
                session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()
    
    # 数据操作方法
    def load_inventory(self):
        """加载商品数据"""
        session = self.get_session()
        try:
            products = session.query(Product).all()
            return [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "stock": p.stock,
                    "description": p.description or "",
                    "barcode": p.barcode or "",
                    "purchase_limit": p.purchase_limit or 0,
                    "created_at": p.created_at or datetime.now().isoformat()
                }
                for p in products
            ]
        finally:
            session.close()
    
    def save_inventory(self, inventory_data):
        """保存商品数据"""
        session = self.get_session()
        try:
            # 更新现有商品或添加新商品
            for item in inventory_data:
                product = session.query(Product).filter_by(id=item["id"]).first()
                if product:
                    # 更新现有商品
                    product.name = item["name"]
                    product.price = item["price"]
                    product.stock = item["stock"]
                    product.description = item.get("description", "")
                    product.barcode = item.get("barcode", "")
                    product.purchase_limit = item.get("purchase_limit", 0)
                    product.created_at = item.get("created_at", datetime.now().isoformat())
                else:
                    # 添加新商品
                    product = Product(
                        id=item.get("id", str(uuid.uuid4())[:8]),
                        name=item["name"],
                        price=item["price"],
                        stock=item["stock"],
                        description=item.get("description", ""),
                        barcode=item.get("barcode", ""),
                        purchase_limit=item.get("purchase_limit", 0),
                        created_at=item.get("created_at", datetime.now().isoformat())
                    )
                    session.add(product)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def load_orders(self):
        """加载订单数据"""
        session = self.get_session()
        try:
            orders = session.query(Order).all()
            return [
                {
                    "order_id": o.order_id,
                    "user_name": o.user_name,
                    "items": json.loads(o.items_json),
                    "original_amount": o.original_amount,
                    "total_items": o.total_items,
                    "discount_rate": o.discount_rate,
                    "discount_text": o.discount_text,
                    "discount_savings": o.discount_savings,
                    "total_amount": o.total_amount,
                    "payment_method": o.payment_method,
                    "cash_amount": o.cash_amount,
                    "voucher_amount": o.voucher_amount,
                    "order_time": o.order_time
                }
                for o in orders
            ]
        finally:
            session.close()
    
    def add_order(self, order_data):
        """添加订单"""
        session = self.get_session()
        try:
            print(f"🔄 开始保存订单: {order_data['order_id']}")
            order = Order(
                order_id=order_data["order_id"],
                user_name=order_data["user_name"],
                items_json=json.dumps(order_data["items"]),
                original_amount=order_data["original_amount"],
                total_items=order_data["total_items"],
                discount_rate=order_data["discount_rate"],
                discount_text=order_data["discount_text"],
                discount_savings=order_data["discount_savings"],
                total_amount=order_data["total_amount"],
                payment_method=order_data["payment_method"],
                cash_amount=order_data["cash_amount"],
                voucher_amount=order_data["voucher_amount"],
                order_time=order_data["order_time"]
            )
            session.add(order)
            session.commit()
            print(f"✅ 订单保存成功: {order_data['order_id']}")
            
            # 验证保存
            saved_order = session.query(Order).filter_by(order_id=order_data['order_id']).first()
            if saved_order:
                print(f"✅ 验证成功: 订单 {order_data['order_id']} 已存在于数据库")
            else:
                print(f"❌ 验证失败: 订单 {order_data['order_id']} 未找到")
                
        except Exception as e:
            session.rollback()
            print(f"❌ 订单保存失败: {e}")
            raise e
        finally:
            session.close()
    
    def load_users(self):
        """加载用户数据"""
        session = self.get_session()
        try:
            users = session.query(User).all()
            return [
                {
                    "username": u.username,
                    "password": u.password,
                    "name": u.name,
                    "role": u.role
                }
                for u in users
            ]
        finally:
            session.close()
    
    def add_user(self, user_data):
        """添加用户"""
        session = self.get_session()
        try:
            user = User(
                username=user_data["username"],
                password=user_data["password"],
                name=user_data["name"],
                role=user_data["role"]
            )
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def clear_orders(self):
        """清空所有订单"""
        session = self.get_session()
        try:
            session.query(Order).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def clear_inventory(self):
        """清空所有商品"""
        session = self.get_session()
        try:
            session.query(Product).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def clear_users(self):
        """清空所有用户"""
        session = self.get_session()
        try:
            session.query(User).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# 全局数据库管理器（移除缓存，确保连接正常）
def get_database_manager():
    return DatabaseManager()
