@echo off
echo 正在重启内购系统...
cd /d "c:\Users\huishi00\Desktop\内购系统"

echo 检查Python和Streamlit安装...
python --version
python -m pip list | findstr streamlit

echo.
echo 启动Streamlit应用...
streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8501

pause
