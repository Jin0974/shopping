@echo off
chcp 65001
echo ================================
echo    内购系统 Streamlit 自动更新
echo ================================
echo.

echo 正在检查当前目录...
cd /d "c:\Users\huishi00\Desktop\内购系统"
if not exist "app.py" (
    echo 错误：未找到 app.py 文件，请确认当前目录正确
    pause
    exit /b 1
)

echo 当前目录：%cd%
echo.

echo 正在检查 Git 状态...
git status
if %errorlevel% neq 0 (
    echo 错误：Git 未初始化或未安装
    echo 请先安装 Git 或使用 GitHub 网页界面上传文件
    pause
    exit /b 1
)

echo.
echo 正在添加修改的文件...
git add app.py
git add "购物车数量修改功能说明.md"
git add "订单原价修复说明.md"
git add "Streamlit更新部署指南.md"
git add "*.md"

echo.
echo 正在提交更改...
git commit -m "功能更新：购物车数量修改和订单原价修复

- 添加购物车数量修改功能，用户可直接调整商品数量
- 修复订单修改后原价不更新的问题
- 完善限购检查逻辑，防止分批购买绕过限购
- 优化用户体验和数据一致性"

if %errorlevel% neq 0 (
    echo 提交失败，可能没有文件需要提交或存在冲突
    echo 请检查文件状态
    pause
    exit /b 1
)

echo.
echo 正在推送到 GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ================================
    echo      更新成功完成！
    echo ================================
    echo.
    echo ✅ 代码已成功推送到 GitHub
    echo ✅ Streamlit Cloud 将在 2-5 分钟内自动重新部署
    echo ✅ 新功能包括：
    echo    - 购物车数量修改功能
    echo    - 订单原价修复
    echo    - 完善的限购检查
    echo.
    echo 💡 请等待几分钟后访问您的 Streamlit 应用测试新功能
    echo.
) else (
    echo.
    echo ================================
    echo      推送失败
    echo ================================
    echo.
    echo ❌ 可能的原因：
    echo    1. 网络连接问题
    echo    2. GitHub 认证问题
    echo    3. 远程仓库冲突
    echo.
    echo 💡 解决方案：
    echo    1. 检查网络连接
    echo    2. 先执行：git pull origin main
    echo    3. 然后再次运行此脚本
    echo    4. 或使用 GitHub 网页界面手动上传 app.py
    echo.
)

echo 按任意键退出...
pause >nul
