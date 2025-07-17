# 简化版商品页面函数 - 回滚到基本可工作版本

def shopping_page():
    """商品购买页面 - 简化版"""
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
            st.success("订单已提交！")
            st.session_state.cart = []
            st.rerun()
