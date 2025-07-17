#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单数据验证脚本
用于检查订单数据的一致性
"""

import json
import sys

def load_orders():
    """加载订单数据"""
    try:
        with open('orders.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载订单数据失败: {e}")
        return []

def check_order_consistency():
    """检查订单数据一致性"""
    orders = load_orders()
    
    print("=== 订单数据一致性检查 ===")
    print(f"总订单数: {len(orders)}")
    print()
    
    for i, order in enumerate(orders, 1):
        order_id = order.get('order_id', 'N/A')
        user_name = order.get('user_name', 'N/A')
        
        print(f"订单 {i}: {order_id} (用户: {user_name})")
        
        # 计算商品实际原价总额
        items = order.get('items', [])
        calculated_original = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
        stored_original = order.get('original_amount', 0)
        
        # 计算商品总件数
        calculated_items = sum(item.get('quantity', 0) for item in items)
        stored_items = order.get('total_items', 0)
        
        # 其他字段
        total_amount = order.get('total_amount', 0)
        cash_amount = order.get('cash_amount', 0)
        voucher_amount = order.get('voucher_amount', 0)
        discount_savings = order.get('discount_savings', 0)
        
        print(f"  商品详情:")
        for item in items:
            name = item.get('product_name', 'N/A')
            price = item.get('price', 0)
            qty = item.get('quantity', 0)
            subtotal = price * qty
            print(f"    - {name}: ¥{price:.2f} x {qty} = ¥{subtotal:.2f}")
        
        print(f"  计算原价总额: ¥{calculated_original:.2f}")
        print(f"  存储原价总额: ¥{stored_original:.2f}")
        print(f"  一致性检查: {'✅ 一致' if calculated_original == stored_original else '❌ 不一致'}")
        
        print(f"  计算商品件数: {calculated_items}")
        print(f"  存储商品件数: {stored_items}")
        print(f"  件数一致性: {'✅ 一致' if calculated_items == stored_items else '❌ 不一致'}")
        
        print(f"  应付金额: ¥{total_amount:.2f}")
        print(f"  现金支付: ¥{cash_amount:.2f}")
        print(f"  内购券支付: ¥{voucher_amount:.2f}")
        print(f"  总支付: ¥{cash_amount + voucher_amount:.2f}")
        print(f"  优惠金额: ¥{discount_savings:.2f}")
        print(f"  支付方式: {order.get('payment_method', 'N/A')}")
        
        # 检查多付情况
        total_paid = cash_amount + voucher_amount
        if total_paid > total_amount:
            overpay = total_paid - total_amount
            print(f"  多付金额: ¥{overpay:.2f}")
        
        print("-" * 60)
    
    print("=== 检查完成 ===")

if __name__ == "__main__":
    check_order_consistency()
