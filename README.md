# 济外国际智能钥匙柜管理系统 (Smart Key Cabinet System)

> 一个基于 Flask + Vue 3 的现代化智能钥匙柜管理系统，专为济外国际学校设计。支持扫码借还、实时状态追踪、用户权限管理以及可视化的数据后台。

---

## 🎯 项目概述

本系统旨在解决传统钥匙管理中“记录难、查找难、追踪难”的痛点。通过软硬件结合（可选）的方式，实现钥匙借用、归还的全流程数字化管理。无论是学生还是老师，都能通过简洁的 Web 界面快速完成操作，管理员则可以通过后台实时监控每一把钥匙的去向。

## ✨ 核心功能

### 🔑 智能借还
- **极速借用**：支持输入学号/工号或扫码快速借用，强制填写借用理由，确保责任到人。
- **简化归还**：一键查询名下未归还钥匙，点选即可归还，无需重复输入繁琐信息。
- **状态追踪**：借出时间、归还时间、经手人全记录，历史数据可追溯。

### 👥 用户与权限
- **多角色支持**：区分学生与教师身份，支持不同的业务逻辑。
- **信息管理**：完整的用户增删改查（CRUD），支持批量导入（需扩展）。

### 📊 实时监控与管理
- **可视化看板**：首页实时显示在库钥匙数量、借出数量。
- **后台管理系统**：集成 Flask-Admin，提供强大的数据库底层管理能力。
- **设备管理**：支持钥匙与房间号的绑定与解绑。

## 🏗️ 技术架构

### 后端 (Backend)
- **核心框架**: Flask (Python)
- **数据库**: SQLAlchemy (ORM), SQLite (默认) / MySQL (生产环境支持)
- **管理后台**: Flask-Admin
- **接口服务**: RESTful API

### 前端 (Frontend)
- **核心框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **UI 组件库**: Element Plus
- **路由管理**: Vue Router 4
- **HTTP 客户端**: Axios

## 📁 目录结构

```text
智能钥匙柜管理系统/
├── backend/                    # 🔧 后端服务 (Flask)
│   ├── app.py                  # 完整版 API 服务 (SQLite/MySQL)
│   ├── simple_app.py           # 简化版 API 服务 (内存数据)
│   ├── models.py               # 数据库模型定义
│   ├── requirements.txt        # Python 依赖清单
│   └── school.db               # 默认 SQLite 数据库文件
├── frontend/                   # 🎨 前端应用 (Vue 3)
│   ├── src/                    # 源代码目录
│   │   ├── api/                # API 接口封装
│   │   ├── views/              # 页面组件 (借还、管理等)
│   │   └── App.vue             # 根组件
│   ├── vite.config.js          # Vite 构建与代理配置
│   └── package.json            # NPM 依赖配置
├── legacy-html/                # 📜 历史版本 (纯 HTML/jQuery，已归档)
├── start-new.sh                # 🚀 [推荐] 一键启动脚本 (完整版)
├── start-dev.sh                # 🛠 开发启动脚本 (简化版)
└── README.md                   # 项目说明文档
```

## 🚀 快速开始 (Quick Start)

### 环境要求
- **Python**: 3.8+
- **Node.js**: 16+

### 方式一：一键启动（推荐）

我们在根目录下提供了便捷的启动脚本，会自动处理端口和依赖检查。

#### 启动完整版 (SQLite 数据库)
```bash
./start-new.sh
```
此命令将启动：
- **前端页面**: http://localhost:3000
- **后端 API**: http://localhost:5002
- **管理后台**: http://localhost:5002/admin

#### 启动简化版 (内存数据，无需数据库)
```bash
./start-dev.sh
```

### 方式二：手动分步启动

如果您需要更精细的控制，可以分别启动前后端。

#### 1. 启动后端
```bash
cd backend
pip3 install -r requirements.txt
# 设置端口为 5002 以匹配前端代理
export PORT=5002 
python3 app.py
```

#### 2. 启动前端
```bash
cd frontend
npm install
npm run dev
```

## 🔌 API 接口概览

系统采用标准 RESTful 风格设计。

| 模块 | 方法 | 路径 | 描述 |
|------|------|------|------|
| **用户** | GET | `/api/user/` | 获取所有用户列表 |
| | POST | `/api/user/` | 创建新用户 |
| | POST | `/api/user/<id>/borrow` | 用户借用钥匙 |
| | GET | `/api/user/borrow-records/active` | 获取所有未归还记录 |
| | POST | `/api/user/<id>/return` | 用户归还钥匙 |
| **钥匙** | GET | `/api/key/` | 获取所有钥匙状态 |
| | POST | `/api/key/` | 新增钥匙 |

## ⚙️ 配置说明

### 数据库切换
默认使用 SQLite (`backend/school.db`)，开箱即用。如需切换到 MySQL，请设置环境变量：
```bash
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/dbname?charset=utf8mb4"
```

### 端口配置
- **前端代理**: 修改 `frontend/vite.config.js` 中的 `server.proxy`。
- **后端端口**: 修改启动脚本或环境变量 `PORT`。

## 📦 版本控制与协作

本项目已托管在 GitHub：

- 仓库地址：https://github.com/qyxa123/Smart_key_cabinet-all

一般使用者只需要：
- 直接 `git clone` 本仓库；
- 按“快速开始”章节启动前后端；
- 无需再次执行 `git init`、`git remote add` 等初始化命令。

协作方式：
- 团队成员：在该仓库创建分支、提交代码并合并。
- 外部贡献者：Fork 仓库后，通过 Pull Request 提交修改。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

---
**Designed with ❤️ for JFLSIC**
