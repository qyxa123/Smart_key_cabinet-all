# 济外国际智能钥匙柜管理系统

一个基于Flask + Vue3的现代化智能钥匙柜管理系统，支持钥匙的借用、归还以及用户和钥匙的管理。

## 🎯 项目概述

本系统为济外国际学校设计，用于管理学校的智能钥匙柜。系统支持学生和老师借用钥匙，提供完整的借用记录管理，以及直观的Web界面进行操作。

## ✨ 主要功能

### 🔑 钥匙管理
- 钥匙信息的增删改查
- 钥匙使用状态实时监控
- 房间号管理

### 👥 用户管理
- 支持学生和老师两种身份
- 用户信息管理（姓名、学号/工号、年级、班级、办公室）
- 用户借用记录查看

### 📤 借用功能
- 在线钥匙借用申请
- 身份验证和信息填写
- 可用钥匙列表选择

### 📥 归还功能
- 便捷的钥匙归还流程
- 使用情况反馈
- 服务满意度评价

### 📊 系统监控
- 实时显示可用钥匙数量
- 已借出钥匙统计
- 系统运行状态监控

## 🏗️ 技术架构

### 后端 (Flask)
- **Flask** - Python Web框架
- **SQLAlchemy** - ORM数据库操作
- **MySQL** - 数据库
- **Flask-Admin** - 管理后台
- **Flask-CORS** - 跨域支持
- **Marshmallow** - 数据序列化

### 前端 (Vue3)
- **Vue 3** - 渐进式JavaScript框架
- **Vue Router 4** - 路由管理
- **Element Plus** - UI组件库
- **Axios** - HTTP客户端
- **Vite** - 构建工具

## 📁 项目结构

```
智能钥匙柜/
├── myflask/                    # 后端Flask应用
│   ├── app.py                  # 主应用文件
│   ├── models.py               # 数据模型
│   ├── user.py                 # 用户相关API
│   ├── key.py                  # 钥匙相关API
│   ├── schemas.py              # 数据序列化
│   ├── extensions.py           # 扩展配置
│   └── requirements.txt        # Python依赖
├── 智能钥匙柜-vue/              # 前端Vue3应用
│   ├── src/
│   │   ├── views/              # 页面组件
│   │   ├── api/                # API接口
│   │   ├── router/             # 路由配置
│   │   └── style.css           # 全局样式
│   ├── package.json            # 前端依赖
│   └── vite.config.js          # Vite配置
├── 智能钥匙柜/                  # 原始HTML版本（参考）
├── start.sh                    # Linux/Mac启动脚本
├── start.bat                   # Windows启动脚本
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 方式一：使用启动脚本（推荐）

#### Linux/Mac
```bash
./start.sh
```

#### Windows
```cmd
start.bat
```

### 方式二：手动启动

#### 1. 启动后端

```bash
cd myflask

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动Flask应用
python app.py
```

#### 2. 启动前端

```bash
cd 智能钥匙柜-vue

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 3. 访问系统

- 🌐 **前端界面**: http://localhost:3000
- 🔧 **后端API**: http://localhost:5000
- ⚙️ **管理后台**: http://localhost:5000/admin

## 📊 数据库配置

### MySQL配置

1. 创建数据库：
```sql
CREATE DATABASE school CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改 `myflask/app.py` 中的数据库连接配置：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://用户名:密码@localhost:3306/school?charset=utf8mb4'
```

### 数据表结构

系统会自动创建以下数据表：
- `user` - 用户表
- `key` - 钥匙表  
- `jnflsic_keys` - 用户钥匙关联表（多对多）

## 🔌 API接口

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

## 🎨 界面预览

### 主页
- 现代化的科技风格设计
- 实时系统状态显示
- 快速功能导航

### 借钥匙页面
- 用户身份选择（学生/老师）
- 个人信息填写
- 可用钥匙选择

### 还钥匙页面
- 身份验证
- 借用记录显示
- 使用反馈收集

### 管理页面
- 用户管理（增删改查）
- 钥匙管理（增删改查）
- 借用状态监控

## 🔧 开发说明

### 添加新功能
1. 后端：在相应的蓝图文件中添加API接口
2. 前端：在 `src/api/index.js` 中添加API调用
3. 创建或修改Vue组件
4. 更新路由配置

### 数据库迁移
系统使用SQLAlchemy自动创建表结构，如需修改：
1. 更新 `models.py` 中的模型定义
2. 重启应用自动应用更改

### 样式定制
- 全局样式：`智能钥匙柜-vue/src/style.css`
- 组件样式：各Vue组件的 `<style scoped>` 部分
- Element Plus主题：通过CSS变量定制

## 📝 更新日志

### v1.0.0 (2025-01-13)
- ✨ 完整的钥匙借用和归还功能
- 👥 用户管理系统
- 🗝️ 钥匙管理系统
- 📊 实时状态监控
- 🎨 现代化UI设计
- 📱 响应式布局支持

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目仅用于教育目的，版权归济外国际所有。

## 📞 联系方式

如有问题或建议，请联系开发团队。

---

**济外国际智能钥匙柜管理系统** - 让钥匙管理更智能、更便捷！