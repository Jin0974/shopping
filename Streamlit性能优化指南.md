# Streamlit性能优化指南

## 🚀 提升并发用户数的方法

### 当前问题分析
- **Streamlit Cloud免费版限制**：同时只支持3-5个用户
- **资源限制**：CPU、内存、网络带宽都有限制
- **会话管理**：每个用户都会创建独立的Python进程

## 💡 优化方案

### 1. 代码优化（立即可行）

#### A. 添加数据缓存
在app.py顶部添加：
```python
# 性能优化配置
@st.cache_data(ttl=300)  # 缓存5分钟
def load_cached_data(file_path, default_data):
    """缓存数据加载，减少重复文件读取"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default_data

# 使用缓存加载数据
inventory = load_cached_data(INVENTORY_FILE, {})
orders = load_cached_data(ORDERS_FILE, [])
users = load_cached_data(USERS_FILE, [])
```

#### B. 减少页面重新渲染
```python
# 在页面顶部添加
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    # 只在首次加载时执行重要操作
```

#### C. 优化CSS减少资源占用
```python
st.markdown("""
<style>
    /* 禁用动画节省CPU */
    * { transition: none !important; animation: none !important; }
    
    /* 隐藏不必要元素 */
    .stDeployButton, footer { display: none; }
    
    /* 限制表格高度减少内存 */
    .stDataFrame { max-height: 300px; overflow-y: auto; }
</style>
""", unsafe_allow_html=True)
```

### 2. 数据库优化（中期方案）

#### 使用轻量级数据库
考虑将JSON文件替换为SQLite：
```python
import sqlite3

# 比JSON文件更高效的数据库操作
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    return conn
```

### 3. 部署升级方案

#### A. Streamlit Cloud Pro（推荐）
- **费用**：约$20/月
- **并发用户**：50-100人
- **资源**：更多CPU和内存
- **升级方法**：在Streamlit Cloud设置中升级

#### B. 自建服务器部署
- **阿里云/腾讯云**：最低配置约￥100/月
- **并发能力**：几百人同时在线
- **完全控制权**：无任何限制

#### C. 其他云平台
- **Heroku**：类似Streamlit Cloud
- **Railway**：更便宜的选择
- **DigitalOcean**：性价比较高

## 🛠️ 立即优化步骤

### 第1步：修改requirements.txt
```txt
streamlit==1.28.0
pandas==1.5.0
openpyxl==3.0.0
python-dateutil==2.8.0
```
（固定版本，减少依赖冲突）

### 第2步：添加.streamlit/config.toml
创建配置文件优化性能：
```toml
[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

### 第3步：优化数据处理
- 减少实时数据刷新频率
- 使用分页显示大量数据
- 缓存计算结果

## 📊 不同方案对比

| 方案 | 费用 | 并发用户 | 实施难度 | 推荐度 |
|------|------|----------|----------|--------|
| 代码优化 | 免费 | 8-10人 | 简单 | ⭐⭐⭐ |
| Streamlit Pro | $20/月 | 50-100人 | 极简单 | ⭐⭐⭐⭐⭐ |
| 自建服务器 | ￥100/月 | 500+人 | 复杂 | ⭐⭐⭐⭐ |

## 🎯 建议方案

### 短期（立即）：
1. 应用代码优化
2. 限制同时使用人数
3. 错峰使用

### 长期（推荐）：
1. **升级到Streamlit Cloud Pro**
   - 最简单的解决方案
   - 官方支持，稳定可靠
   - 性价比最高

## 🔄 临时解决方案

### 用户管理策略：
1. **分批使用**：安排不同时间段使用
2. **轮换制**：每次最多3人同时使用
3. **提前通知**：告知用户高峰期可能需要等待

### 监控用户数：
```python
# 在app.py中添加简单的用户计数
if "user_count" not in st.session_state:
    st.session_state.user_count = len(st.session_state)
    
if st.session_state.user_count > 3:
    st.warning("⚠️ 当前用户较多，系统可能运行缓慢，请稍后再试")
```

## 💰 成本效益分析

对于经常有多人使用的内购系统，建议直接升级到 **Streamlit Cloud Pro**：
- 月费用：$20（约￥140）
- 解决所有并发问题
- 无需修改代码
- 官方技术支持

这比花时间优化代码更经济高效！

---

**总结**：如果预算允许，直接升级到Pro版是最佳选择。如果暂时不升级，先应用代码优化，能从3人提升到8-10人同时使用。
