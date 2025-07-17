# Railway部署指南

## 🚀 Railway部署步骤（$5/月，无限用户）

### 1. 注册Railway
- 访问：https://railway.app
- 用GitHub账户登录

### 2. 创建新项目
- 点击"New Project"
- 选择"Deploy from GitHub repo"
- 选择您的内购系统仓库

### 3. 配置环境
Railway会自动：
- 检测Python项目
- 安装requirements.txt中的依赖
- 使用Dockerfile部署

### 4. 设置端口
- 在Variables中添加：
  - PORT: 8501
  - STREAMLIT_SERVER_PORT: 8501

### 5. 部署完成
- 获得免费域名：yourapp.railway.app
- 可绑定自定义域名

## 费用说明
- 免费额度：每月$5使用额度
- 超出后：$0.000463/GB-小时
- 对于30人使用，月费用约$5-10

## 优势
✅ 支持无限并发用户
✅ 自动扩展资源
✅ 全球部署
✅ 简单易用
