# 济外国际智能钥匙柜管理系统

一个基于Flask + Vue3的现代化智能钥匙柜管理系统，支持钥匙的借用、归还以及用户和钥匙的管理。

## 🎯 项目概述

本系统为济外国际学校设计，用于管理学校的智能钥匙柜。系统支持学生和老师借用钥匙，提供完整的借用记录管理，以及直观的Web界面进行操作。

## 📁 项目结构

```
智能钥匙柜管理系统/
├── backend/                    # 🔧 后端服务 (Flask)
│   ├── simple_app.py           # 简化版API服务
│   ├── app.py                  # 完整版API服务
│   ├── models.py               # 数据模型
│   ├── requirements.txt        # Python依赖
│   └── README.md               # 后端说明文档
├── frontend/                   # 🎨 前端应用 (Vue3)
│   ├── src/                    # 源代码
│   ├── package.json            # 前端依赖
│   ├── vite.config.js          # 构建配置
│   └── README.md               # 前端说明文档
├── legacy-html/                # � 原始HTML版本 (已停止维护)
│   ├── index.html              # 原始主页
│   ├── styles.css              # 原始样式
│   └── README.md               # 说明文档
├── start-dev.sh                # � 开发环境启动脚本 (Linux/Mac)
├── start-dev.bat               # 🚀 开发环境启动脚本 (Windows)
└── README.md                   # 项目总体说明
```

## ✨ 主要功能

### � 钥匙管理
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

### 后端 (backend/)
- **Flask** - Python Web框架
- **SQLAlchemy** - ORM数据库操作 (完整版)
- **MySQL** - 数据库 (完整版)
- **Flask-CORS** - 跨域支持
- **内存存储** - 简化版数据存储

### 前端 (frontend/)
- **Vue 3** - 渐进式JavaScript框架
- **Vue Router 4** - 路由管理
- **Element Plus** - UI组件库
- **Axios** - HTTP客户端
- **Vite** - 构建工具

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 5.7+ (仅完整版需要)

### 一键启动 (推荐)

#### Linux/Mac
```bash
./start-dev.sh
```

#### Windows
```cmd
start-dev.bat
```

### 手动启动

#### 1. 启动后端
```bash
cd backend
pip3 install flask flask-cors
python3 simple_app.py
```

#### 2. 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 3. 访问系统
- 🌐 **前端界面**: http://localhost:3000
- 🔧 **后端API**: http://localhost:8000

## 📖 详细文档

- **后端文档**: [backend/README.md](backend/README.md)
- **前端文档**: [frontend/README.md](frontend/README.md)
- **原始版本**: [legacy-html/README.md](legacy-html/README.md)

## 🔧 项目维护说明

### 目录结构优化
项目已采用英文目录命名规范，避免在CI/CD、Docker、跨平台脚本等环境中可能出现的编码和路径问题：

- ✅ **backend/** - 后端Flask应用
- ✅ **frontend/** - 前端Vue3应用  
- ✅ **legacy-html/** - 原始HTML版本

### Git管理优化
- 添加了完整的 `.gitignore` 文件，排除系统文件（如 `.DS_Store`）和依赖目录
- 避免提交不必要的系统垃圾文件，保持仓库整洁

## 🔌 API接口

### 用户相关
- `GET /api/user/` - 获取所有用户
- `POST /api/user/` - 创建用户
- `POST /api/user/:id/borrow` - 借钥匙
- `POST /api/user/:id/return` - 还钥匙

### 钥匙相关
- `GET /api/key/` - 获取所有钥匙
- `POST /api/key/` - 创建钥匙
- `PUT /api/key/:id` - 更新钥匙
- `DELETE /api/key/:id` - 删除钥匙

## 🎨 界面预览

### 主页
- 现代化的科技风格设计
- 实时系统状态显示
- 快速功能导航

### 功能页面
- **借钥匙** - 用户身份验证，钥匙选择
- **还钥匙** - 借用记录查看，使用反馈
- **用户管理** - 用户信息的增删改查
- **钥匙管理** - 钥匙状态监控和管理

## 🔧 开发说明

### 目录说明
- **`backend/`** - 后端API服务，负责数据处理和业务逻辑
- **`frontend/`** - 前端Vue应用，负责用户界面和交互
- **`legacy-html/`** - 原始HTML版本，仅作参考，已停止维护

### 开发流程
1. 后端开发：在 `backend/` 目录下开发API接口
2. 前端开发：在 `frontend/` 目录下开发Vue组件
3. 联调测试：使用启动脚本同时运行前后端

### 部署建议
- **开发环境**：使用提供的启动脚本
- **生产环境**：
  - 后端：使用gunicorn等WSGI服务器
  - 前端：构建后部署到nginx等静态服务器

## 📝 更新日志

### v2.0.0 (2025-01-13)
- 🔄 **重构项目结构**：采用清晰的前后端分离结构
- 📁 **目录重组**：backend/ frontend/ legacy-html/
- 📚 **文档完善**：各目录独立的README文档
- 🚀 **启动脚本**：一键启动开发环境

### v1.0.0 (2025-01-13)
- ✨ 完整的钥匙借用和归还功能
- 👥 用户管理系统
- 🗝️ 钥匙管理系统
- 📊 实时状态监控
- 🎨 现代化UI设计

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目仅用于教育目的，版权归济外国际所有。

---

**济外国际智能钥匙柜管理系统** - 让钥匙管理更智能、更便捷！