#!/usr/bin/env python3
"""
PostgreSQL连接测试和验证脚本
"""

import os
from sqlalchemy import create_engine, text

def test_postgresql_connection():
    """测试PostgreSQL连接"""
    # 你的数据库URL
    db_url = 'postgresql://nei_gou_xi_tong_user:J6kAunCyE9oUXJ3IOZwilouz6nDxc25P@dpg-d1rgl8euk2gs738i6dt0-a.oregon-postgres.render.com/nei_gou_xi_tong'
    
    print('=' * 60)
    print('🔍 PostgreSQL数据库连接测试')
    print('=' * 60)
    print(f'主机: dpg-d1rgl8euk2gs738i6dt0-a.oregon-postgres.render.com')
    print(f'数据库: nei_gou_xi_tong')
    print(f'用户: nei_gou_xi_tong_user')
    print('-' * 60)
    
    try:
        # 第1步: 创建数据库引擎
        print('1️⃣ 创建数据库引擎...')
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            connect_args={
                'sslmode': 'require',
                'connect_timeout': 30,
            }
        )
        print('   ✅ 引擎创建成功')
        
        # 第2步: 测试基本连接
        print('2️⃣ 测试数据库连接...')
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f'   ✅ 连接成功! 测试查询结果: {row[0]}')
        
        # 第3步: 检查数据库版本
        print('3️⃣ 检查PostgreSQL版本...')
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f'   ✅ PostgreSQL版本: {version[:50]}...')
        
        # 第4步: 创建/验证表结构
        print('4️⃣ 创建/验证表结构...')
        from database import Base
        Base.metadata.create_all(engine)
        print('   ✅ 表结构创建/验证成功')
        
        # 第5步: 检查已存在的表
        print('5️⃣ 检查数据库表...')
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f'   ✅ 发现表: {", ".join(tables)}')
        
        # 第6步: 测试数据操作
        print('6️⃣ 测试数据库操作...')
        from database import DatabaseManager
        
        # 设置环境变量以便测试
        os.environ['DATABASE_URL'] = db_url
        
        db_manager = DatabaseManager()
        
        # 测试读取操作
        users = db_manager.load_users()
        products = db_manager.load_inventory()
        orders = db_manager.load_orders()
        
        print(f'   ✅ 数据读取成功:')
        print(f'      用户数量: {len(users)}')
        print(f'      商品数量: {len(products)}')
        print(f'      订单数量: {len(orders)}')
        
        print('\n' + '=' * 60)
        print('🎉 所有测试通过! PostgreSQL数据库连接正常!')
        print('✅ 可以在Render中设置这个DATABASE_URL')
        print('=' * 60)
        return True
        
    except Exception as e:
        print(f'\n❌ 测试失败: {str(e)}')
        
        # 详细错误分析
        error_msg = str(e).lower()
        print('\n🔍 错误分析:')
        
        if 'could not connect to server' in error_msg:
            print('   原因: 无法连接到数据库服务器')
            print('   可能解决方案:')
            print('   1. 检查网络连接是否正常')
            print('   2. 确认Render数据库服务是否运行中')
            print('   3. 检查防火墙或网络限制')
            
        elif 'password authentication failed' in error_msg:
            print('   原因: 密码认证失败')
            print('   可能解决方案:')
            print('   1. 检查用户名和密码是否正确')
            print('   2. 确认数据库用户是否存在且有权限')
            
        elif 'database' in error_msg and 'does not exist' in error_msg:
            print('   原因: 数据库不存在')
            print('   可能解决方案:')
            print('   1. 检查数据库名称是否正确')
            print('   2. 确认在Render中创建了该数据库')
            
        elif 'ssl' in error_msg or 'connection' in error_msg:
            print('   原因: SSL或连接配置问题')
            print('   可能解决方案:')
            print('   1. 检查SSL配置')
            print('   2. 尝试调整连接参数')
            
        elif 'timeout' in error_msg:
            print('   原因: 连接超时')
            print('   可能解决方案:')
            print('   1. 检查网络延迟')
            print('   2. 增加连接超时时间')
            print('   3. 检查数据库服务器负载')
            
        else:
            print(f'   其他错误详情: {error_msg}')
        
        print('\n📋 下一步建议:')
        print('1. 登录Render控制台检查PostgreSQL数据库状态')
        print('2. 确认数据库服务正在运行')
        print('3. 检查网络连接是否稳定')
        print('4. 如果本地测试失败，可以直接在Render环境中设置')
        
        return False

if __name__ == "__main__":
    test_postgresql_connection()
