import json
from datetime import datetime
from database import get_database_manager, User, Product, Order
import streamlit as st

class DataService:
    def __init__(self):
        self.db = get_database_manager()
    
    # 用户相关操作
    def get_user(self, username):
        """获取用户信息"""
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user:
                return {
                    'username': user.username,
                    'role': user.role
                }
            return None
        finally:
            session.close()
    
    def create_user(self, username, role='user'):
        """创建新用户"""
        session = self.db.get_session()
        try:
            user = User(username=username, role=role)
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            st.error(f"创建用户失败: {e}")
            return False
        finally:
            session.close()
    
    def get_all_users(self):
        """获取所有用户"""
        session = self.db.get_session()
        try:
            users = session.query(User).all()
            return {user.username: {'role': user.role} for user in users}
        finally:
            session.close()
    
    # 商品相关操作
    def get_all_products(self):
        """获取所有商品"""
        session = self.db.get_session()
        try:
            products = session.query(Product).all()
            result = {}
            for product in products:
                result[product.name] = {
                    'price': product.price,
                    'stock': product.stock,
                    'barcode': product.barcode or '',
                    'category': product.category or '',
                    'description': product.description or '',
                    'max_purchase': product.max_purchase
                }
            return result
        finally:
            session.close()
    
    def update_product(self, name, product_data):
        """更新商品信息"""
        session = self.db.get_session()
        try:
            product = session.query(Product).filter_by(name=name).first()
            if product:
                product.price = product_data.get('price', product.price)
                product.stock = product_data.get('stock', product.stock)
                product.barcode = product_data.get('barcode', product.barcode)
                product.category = product_data.get('category', product.category)
                product.description = product_data.get('description', product.description)
                product.max_purchase = product_data.get('max_purchase', product.max_purchase)
            else:
                product = Product(
                    name=name,
                    price=product_data.get('price', 0),
                    stock=product_data.get('stock', 0),
                    barcode=product_data.get('barcode', ''),
                    category=product_data.get('category', ''),
                    description=product_data.get('description', ''),
                    max_purchase=product_data.get('max_purchase', 999999)
                )
                session.add(product)
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            st.error(f"更新商品失败: {e}")
            return False
        finally:
            session.close()
    
    def delete_product(self, name):
        """删除商品"""
        session = self.db.get_session()
        try:
            product = session.query(Product).filter_by(name=name).first()
            if product:
                session.delete(product)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            st.error(f"删除商品失败: {e}")
            return False
        finally:
            session.close()
    
    # 订单相关操作
    def get_all_orders(self):
        """获取所有订单"""
        session = self.db.get_session()
        try:
            orders = session.query(Order).all()
            result = {}
            for order in orders:
                result[order.order_id] = {
                    'username': order.username,
                    'items': json.loads(order.items),
                    'total_amount': order.total_amount,
                    'original_amount': order.original_amount,
                    'discount_amount': order.discount_amount,
                    'payment_method': order.payment_method,
                    'status': order.status,
                    'timestamp': order.created_at.isoformat()
                }
            return result
        finally:
            session.close()
    
    def create_order(self, order_id, order_data):
        """创建新订单"""
        session = self.db.get_session()
        try:
            order = Order(
                order_id=order_id,
                username=order_data.get('username', ''),
                items=json.dumps(order_data.get('items', [])),
                total_amount=order_data.get('total_amount', 0),
                original_amount=order_data.get('original_amount', 0),
                discount_amount=order_data.get('discount_amount', 0),
                payment_method=order_data.get('payment_method', ''),
                status=order_data.get('status', 'completed')
            )
            session.add(order)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            st.error(f"创建订单失败: {e}")
            return False
        finally:
            session.close()
    
    def update_order(self, order_id, order_data):
        """更新订单"""
        session = self.db.get_session()
        try:
            order = session.query(Order).filter_by(order_id=order_id).first()
            if order:
                order.username = order_data.get('username', order.username)
                order.items = json.dumps(order_data.get('items', json.loads(order.items)))
                order.total_amount = order_data.get('total_amount', order.total_amount)
                order.original_amount = order_data.get('original_amount', order.original_amount)
                order.discount_amount = order_data.get('discount_amount', order.discount_amount)
                order.payment_method = order_data.get('payment_method', order.payment_method)
                order.status = order_data.get('status', order.status)
                order.updated_at = datetime.now()
                
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            st.error(f"更新订单失败: {e}")
            return False
        finally:
            session.close()
    
    def delete_order(self, order_id):
        """删除订单"""
        session = self.db.get_session()
        try:
            order = session.query(Order).filter_by(order_id=order_id).first()
            if order:
                session.delete(order)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            st.error(f"删除订单失败: {e}")
            return False
        finally:
            session.close()

# 全局数据服务实例
@st.cache_resource
def get_data_service():
    return DataService()
