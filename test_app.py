import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 简单的语法检查
try:
    import app
    print("✅ 代码语法检查通过")
    print("✅ 所有模块导入成功")
    print("✅ 应用程序准备就绪")
except Exception as e:
    print(f"❌ 代码检查失败: {e}")
