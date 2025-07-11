@echo off
cd /d "c:\Users\huishi00\Desktop\内购系统"
echo 正在启动内购系统...
echo 注意：如果看到一些技术错误信息，请忽略，这不影响系统正常使用
echo.
streamlit run app.py --server.headless true --server.runOnSave false --browser.gatherUsageStats false 2>nul
pause
