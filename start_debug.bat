@echo off
echo 启动内购系统调试版本...
cd /d "%~dp0"
python -m streamlit run app.py --server.port 8502 --server.address 0.0.0.0
pause
