import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import streamlit as st

# 数据库配置
Base = declarative_base()

# 数据库模型定义
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    role = Column(String(20), default='user')
    created_at = Column(DateTime, default=datetime.now)

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    barcode = Column(String(50), unique=True)
    category = Column(String(100))
    description = Column(Text)
    max_purchase = Column(Integer, default=999999)  # 限购数量
    created_at = Column(DateTime, default=datetime.now)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    items = Column(Text)  # JSON格式存储商品列表
    total_amount = Column(Float, nullable=False)
    original_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    payment_method = Column(String(50))
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

# 数据库连接类
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
            if not database_url:
                # 开发环境使用SQLite
                database_url = 'sqlite:///purchase_system.db'
            
            self.engine = create_engine(database_url)
            self.Session = sessionmaker(bind=self.engine)
            
            # 创建表
            Base.metadata.create_all(self.engine)
            
        except Exception as e:
            st.error(f"数据库连接失败: {e}")
            raise e
    
    def get_session(self):
        """获取数据库会话"""
        return self.Session()
    
    def migrate_json_data(self):
        """从JSON文件迁移数据到数据库"""
        session = self.get_session()
        
        try:
            # 迁移用户数据
            if os.path.exists('users.json'):
                with open('users.json', 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                
                for username, user_info in users_data.items():
                    existing_user = session.query(User).filter_by(username=username).first()
                    if not existing_user:
                        user = User(
                            username=username,
                            role=user_info.get('role', 'user')
                        )
                        session.add(user)
            
            # 迁移商品数据
            if os.path.exists('inventory.json'):
                with open('inventory.json', 'r', encoding='utf-8') as f:
                    inventory_data = json.load(f)
                
                for item_name, item_info in inventory_data.items():
                    existing_product = session.query(Product).filter_by(name=item_name).first()
                    if not existing_product:
                        product = Product(
                            name=item_name,
                            price=item_info.get('price', 0),
                            stock=item_info.get('stock', 0),
                            barcode=item_info.get('barcode', ''),
                            category=item_info.get('category', ''),
                            description=item_info.get('description', ''),
                            max_purchase=item_info.get('max_purchase', 999999)
                        )
                        session.add(product)
            
            # 迁移订单数据
            if os.path.exists('orders.json'):
                with open('orders.json', 'r', encoding='utf-8') as f:
                    orders_data = json.load(f)
                
                for order_id, order_info in orders_data.items():
                    existing_order = session.query(Order).filter_by(order_id=order_id).first()
                    if not existing_order:
                        order = Order(
                            order_id=order_id,
                            username=order_info.get('username', ''),
                            items=json.dumps(order_info.get('items', [])),
                            total_amount=order_info.get('total_amount', 0),
                            original_amount=order_info.get('original_amount', 0),
                            discount_amount=order_info.get('discount_amount', 0),
                            payment_method=order_info.get('payment_method', ''),
                            status=order_info.get('status', 'completed'),
                            created_at=datetime.fromisoformat(order_info.get('timestamp', datetime.now().isoformat()))
                        )
                        session.add(order)
            
            session.commit()
            st.success("数据迁移完成！")
            
        except Exception as e:
            session.rollback()
            st.error(f"数据迁移失败: {e}")
        finally:
            session.close()

# 全局数据库管理器
@st.cache_resource
def get_database_manager():
    return DatabaseManager()
