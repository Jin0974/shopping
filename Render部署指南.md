# Render部署指南

## 🚀 Render部署步骤（免费支持50+用户）

### 1. 准备文件
确保您有以下文件：
- app.py（主程序）
- requirements.txt（依赖包）
- Dockerfile（已创建）

### 2. 注册Render账户
- 访问：https://render.com
- 用GitHub账户注册登录

### 3. 连接GitHub仓库
- 点击"New +" → "Web Service"
- 选择"Build and deploy from a Git repository"
- 连接您的GitHub仓库

### 4. 配置部署设置
- **Name**: 内购系统
- **Region**: Oregon (US West)
- **Branch**: main
- **Runtime**: Docker
- **Build Command**: 自动检测
- **Start Command**: 自动检测

### 5. 部署
- 点击"Create Web Service"
- 等待3-5分钟部署完成
- 获得免费的https网址

## 优势
✅ 免费版支持50+并发用户
✅ 自动HTTPS证书
✅ 全球CDN加速
✅ 24/7运行，不会休眠
