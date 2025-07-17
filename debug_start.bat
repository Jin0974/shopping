@echo off
echo === 内购系统调试启动 ===
cd /d "c:\Users\huishi00\Desktop\内购系统"

echo 1. 检查数据文件...
if exist inventory.json (
    echo ✓ inventory.json 存在
) else (
    echo ✗ inventory.json 不存在
)

if exist orders.json (
    echo ✓ orders.json 存在
) else (
    echo ✗ orders.json 不存在
)

if exist users.json (
    echo ✓ users.json 存在
) else (
    echo ✗ users.json 不存在
)

echo.
echo 2. 运行数据加载测试...
python test_product_loading.py
pause

echo.
echo 3. 启动应用（调试模式）...
streamlit run app.py --logger.level debug

pause
