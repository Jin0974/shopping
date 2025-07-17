#!/bin/bash
# Streamlit 高并发部署脚本

# 设置环境变量优化性能
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false
export STREAMLIT_CLIENT_TOOLBAR_MODE=minimal

# 启动应用
streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.maxUploadSize 200 \
  --server.enableCORS false \
  --browser.gatherUsageStats false \
  --client.showErrorDetails false \
  --client.toolbarMode minimal
