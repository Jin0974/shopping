@echo off
echo 正在启动内购系统...
echo.
echo 请确保已安装 Python 和 Streamlit
echo 如果未安装依赖，请先运行: pip install -r requirements.txt
echo.
echo 系统启动后将自动打开浏览器
echo 默认访问地址: http://localhost:8501
echo.
echo 登录方式：直接输入姓名即可
echo 任何姓名都可以登录，管理员请输入"管理员"
echo.
streamlit run app.py
pause
