@echo off
echo 启动简单测试版本...
cd /d "%~dp0"
python -m streamlit run simple_test.py --server.port 8504
pause
