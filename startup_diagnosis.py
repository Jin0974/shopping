import streamlit as st
import pandas as pd
import json
import os
import sys
from datetime import datetime

print("=== 内购系统启动诊断 ===")
print(f"当前时间: {datetime.now()}")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

# 检查必要文件
required_files = ["inventory.json", "orders.json", "users.json"]
print("\n检查必要文件:")
for file in required_files:
    if os.path.exists(file):
        print(f"✓ {file} 存在")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"  - 包含 {len(data)} 条记录")
        except Exception as e:
            print(f"  - 读取错误: {e}")
    else:
        print(f"✗ {file} 不存在")

# 检查Streamlit
print("\n检查Streamlit:")
try:
    import streamlit
    print(f"✓ Streamlit版本: {streamlit.__version__}")
except ImportError:
    print("✗ Streamlit未安装")

# 检查pandas
print("\n检查Pandas:")
try:
    import pandas
    print(f"✓ Pandas版本: {pandas.__version__}")
except ImportError:
    print("✗ Pandas未安装")

print("\n=== 诊断完成 ===")
print("如果所有检查都通过，应用应该能正常启动")
print("请运行: streamlit run app.py")
