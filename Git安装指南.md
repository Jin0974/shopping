# Git 安装指南 (Windows)

## 🎯 Git 是什么？
Git 是一个版本控制系统，用来管理代码的版本和上传到GitHub。

## 📥 安装步骤

### 方法一：官网下载（推荐）

#### 1. 下载Git
- 访问官网：https://git-scm.com/download/win
- 点击"Download for Windows"
- 会自动下载最新版本的Git安装包

#### 2. 运行安装程序
- 双击下载的 `.exe` 文件
- 如果出现安全提示，点击"运行"

#### 3. 安装配置（推荐设置）

**选择安装位置**：
- 保持默认路径即可：`C:\Program Files\Git`

**选择组件**：
- ✅ 勾选所有默认选项
- ✅ 特别确保勾选"Git Bash Here"和"Git GUI Here"

**选择默认编辑器**：
- 推荐选择"Use Notepad as Git's default editor"（使用记事本）

**调整PATH环境**：
- ⭐ **重要**：选择"Git from the command line and also from 3rd-party software"
- 这样可以在命令提示符中使用git命令

**选择HTTPS传输后端**：
- 选择"Use the OpenSSL library"

**配置行尾转换**：
- 选择"Checkout Windows-style, commit Unix-style line endings"

**配置终端模拟器**：
- 选择"Use MinTTY (the default terminal of MSYS2)"

**其他选项**：
- 保持所有默认设置
- 点击"Install"开始安装

#### 4. 完成安装
- 安装完成后，勾选"Launch Git Bash"
- 点击"Finish"

### 方法二：通过Chocolatey（高级用户）

如果您已安装Chocolatey包管理器：
```powershell
# 以管理员身份运行PowerShell
choco install git
```

### 方法三：通过winget（Windows 10/11）

```powershell
# 在PowerShell中运行
winget install --id Git.Git -e --source winget
```

## ⚙️ 安装后配置

### 1. 验证安装
打开命令提示符（cmd）或PowerShell，输入：
```bash
git --version
```
如果显示版本号，说明安装成功。

### 2. 配置用户信息
```bash
# 设置用户名（使用您的GitHub用户名）
git config --global user.name "您的GitHub用户名"

# 设置邮箱（使用您的GitHub邮箱）
git config --global user.email "您的GitHub邮箱"
```

### 3. 配置GitHub认证（如需要）

#### 如果是第一次使用GitHub：
```bash
# 生成SSH密钥（可选，推荐）
ssh-keygen -t rsa -b 4096 -C "您的GitHub邮箱"
```

#### 或者使用Personal Access Token：
1. 访问GitHub Settings → Developer settings → Personal access tokens
2. 生成新token，权限选择repo相关权限
3. 保存token，在推送时用作密码

## 🚀 安装后使用

### 1. 在项目目录中初始化Git（如果之前没有）
```bash
cd "c:\Users\huishi00\Desktop\内购系统"
git init
git remote add origin https://github.com/您的用户名/您的仓库名.git
```

### 2. 运行更新脚本
安装Git后，您就可以双击运行 `更新到Streamlit.bat` 了！

## 📱 快速安装（一键式）

如果您想要最简单的安装方式：

1. **点击下载**：https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe
2. **双击运行**，一路点击"Next"使用默认设置
3. **完成安装**

## ❓ 常见问题

### Q: 安装后命令提示符不识别git命令？
**A**: 重启电脑或重新打开命令提示符

### Q: 推送时要求输入用户名密码？
**A**: 
- 用户名：您的GitHub用户名
- 密码：您的GitHub Personal Access Token（不是登录密码）

### Q: 如何生成Personal Access Token？
**A**: 
1. 登录GitHub
2. 点击头像 → Settings
3. Developer settings → Personal access tokens → Tokens (classic)
4. Generate new token → 选择repo权限 → Generate token
5. 复制token，在git推送时用作密码

## 🎯 安装完成后

1. ✅ 重启命令提示符
2. ✅ 运行 `git --version` 验证安装
3. ✅ 配置用户名和邮箱
4. ✅ 双击运行 `更新到Streamlit.bat`

现在您就可以使用Git来更新您的Streamlit应用了！
