@echo off
echo 🚀 Streamlit 部署助手
echo ==================

echo 正在检查文件...
python 部署检查.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ 所有文件检查通过！
    echo.
    echo 📋 GitHub 部署步骤:
    echo 1. 在GitHub创建新仓库
    echo 2. 将这个文件夹的内容推送到仓库
    echo 3. 访问 https://share.streamlit.io/
    echo 4. 使用GitHub账号登录
    echo 5. 选择你的仓库，主文件设为 app.py
    echo 6. 点击部署！
    echo.
    echo 🌐 本地测试:
    echo streamlit run app.py
    echo.
) else (
    echo.
    echo ❌ 检查发现问题，请修复后重试
)

pause
