# 智能钥匙柜管理系统 - 后端

基于Flask的RESTful API后端服务。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip

### 安装依赖
```bash
# 使用简化版本（推荐）
pip3 install flask flask-cors

# 或使用完整版本（需要MySQL）
pip install -r requirements.txt
```

### 启动服务

#### 简化版本（内存数据库）
```bash
python3 simple_app.py
```

#### 完整版本（MySQL数据库）
```bash
# 配置数据库连接
# 编辑 app.py 中的数据库配置
python3 app.py
```

## 📡 API接口

### 用户相关
- `GET /api/user/` - 获取所有用户
- `POST /api/user/` - 创建用户
- `GET /api/user/:id` - 获取单个用户
- `PUT /api/user/:id` - 更新用户
- `DELETE /api/user/:id` - 删除用户
- `POST /api/user/:id/borrow` - 借钥匙
- `POST /api/user/:id/return` - 还钥匙

### 钥匙相关
- `GET /api/key/` - 获取所有钥匙
- `POST /api/key/` - 创建钥匙
- `GET /api/key/:id` - 获取单个钥匙
- `PUT /api/key/:id` - 更新钥匙
- `DELETE /api/key/:id` - 删除钥匙

## 📁 文件说明

- `simple_app.py` - 简化版本，使用内存数据存储
- `app.py` - 完整版本，使用MySQL数据库
- `models.py` - 数据模型定义
- `user.py` - 用户相关API
- `key.py` - 钥匙相关API
- `schemas.py` - 数据序列化
- `extensions.py` - Flask扩展配置
- `requirements.txt` - Python依赖

## 🔧 开发说明

### 数据模型
- User: 用户表（姓名、身份、年级、班级、办公室）
- Key: 钥匙表（房间号）
- 多对多关系：用户可以借用多把钥匙

### 数据库配置
修改 `app.py` 中的数据库连接字符串：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://用户名:密码@localhost:3306/数据库名?charset=utf8mb4'
```

## 🌐 部署

### 开发环境
```bash
python3 simple_app.py
```

### 生产环境
```bash
# 使用gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 simple_app:app
```