# 济外国际智能钥匙柜管理系统

基于 Flask + Vue 3 的智能钥匙柜管理系统，覆盖钥匙借用/归还、用户与钥匙管理、借用记录追踪，并提供管理后台。

## 功能亮点
- 借钥匙、还钥匙全流程
- 借用理由必填与借用记录追踪
- 用户与钥匙信息管理
- 实时借用状态展示
- 管理后台（Flask-Admin）

## 技术栈
- 后端：Flask、SQLAlchemy、Flask-Admin、SQLite（默认）
- 前端：Vue 3、Element Plus、Vue Router、Vite

## 目录结构
```
智能钥匙柜管理系统/
├── backend/                    # 后端服务 (Flask)
│   ├── app.py                  # 完整版API服务（SQLite/MySQL）
│   ├── simple_app.py           # 简化版API服务（内存数据）
│   ├── models.py               # 数据模型
│   ├── requirements.txt        # Python依赖
│   └── README.md               # 后端说明文档
├── frontend/                   # 前端应用 (Vue3)
│   ├── src/                    # 源代码
│   ├── package.json            # 前端依赖
│   ├── vite.config.js          # 构建与代理配置
│   └── README.md               # 前端说明文档
├── legacy-html/                # 原始HTML版本（已停止维护）
├── start-dev.sh                # 简化版启动脚本
├── start-new.sh                # 完整版启动脚本
├── QUICK_START.md              # 快速启动指南
├── NEW_FEATURES.md             # 新功能说明
└── README.md                   # 项目说明
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+

### 一键启动（推荐）

#### 完整版（SQLite 默认）
```bash
./start-new.sh
```
默认端口：
- 前端：http://localhost:3001
- 后端：http://localhost:5001
- 管理后台：http://localhost:5001/admin

#### 简化版（内存数据）
```bash
./start-dev.sh
```
端口以脚本输出为准。如需调整，请设置 `PORT` 环境变量并同步修改 `frontend/vite.config.js` 代理地址。

### 手动启动

#### 1) 后端（完整版）
```bash
cd backend
pip3 install -r requirements.txt
PORT=5001 python3 app.py
```

#### 2) 后端（简化版）
```bash
cd backend
pip3 install flask flask-cors
PORT=5002 python3 simple_app.py
```

#### 3) 前端
```bash
cd frontend
npm install
npm run dev
```

## 数据库与配置

`backend/app.py` 默认使用 SQLite 数据库（`backend/school.db`）。如需切换到 MySQL，设置环境变量：
```
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/数据库名?charset=utf8mb4
```

## API 概览

### 用户相关
- `GET /api/user/` - 获取所有用户
- `POST /api/user/` - 创建用户
- `POST /api/user/:id/borrow` - 借钥匙
- `POST /api/user/:id/return` - 还钥匙
- `GET /api/user/borrow-records` - 借用记录

### 钥匙相关
- `GET /api/key/` - 获取所有钥匙
- `POST /api/key/` - 创建钥匙
- `PUT /api/key/:id` - 更新钥匙
- `DELETE /api/key/:id` - 删除钥匙

## 文档与测试数据
- `QUICK_START.md`：启动与功能速览
- `NEW_FEATURES.md`：借用记录、借用理由等新功能说明
- `test_setup.py`：生成测试数据

## 开发说明
前后端分离，推荐保持 `frontend/vite.config.js` 的代理端口与后端一致。若修改端口，请同步调整：
- 前端启动端口
- 后端 `PORT`
- Vite 代理 `target`

## 许可证
本项目仅用于教育目的，版权归济外国际所有。
