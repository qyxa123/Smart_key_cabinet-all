# 济外国际智能钥匙柜管理系统 - Vue3前端

基于Vue3 + Element Plus开发的智能钥匙柜管理系统前端应用。

## 功能特性

- 🔑 **钥匙借用** - 支持学生和老师借用钥匙
- 📥 **钥匙归还** - 便捷的钥匙归还流程
- 👥 **用户管理** - 用户信息的增删改查
- 🗝️ **钥匙管理** - 钥匙信息的管理和状态监控
- 📊 **实时状态** - 系统状态和钥匙使用情况的实时显示
- 🎨 **现代UI** - 基于Element Plus的现代化界面设计
- 📱 **响应式** - 支持移动端和桌面端

## 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **Vue Router 4** - 官方路由管理器
- **Element Plus** - Vue 3组件库
- **Axios** - HTTP客户端
- **Vite** - 现代化构建工具

## 项目结构

```
智能钥匙柜-vue/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API接口
│   │   └── index.js       # API配置和接口定义
│   ├── router/            # 路由配置
│   │   └── index.js       # 路由定义
│   ├── views/             # 页面组件
│   │   ├── Home.vue       # 首页
│   │   ├── BorrowKey.vue  # 借钥匙页面
│   │   ├── ReturnKey.vue  # 还钥匙页面
│   │   ├── UserManagement.vue    # 用户管理
│   │   └── KeyManagement.vue     # 钥匙管理
│   ├── App.vue            # 根组件
│   ├── main.js            # 入口文件
│   └── style.css          # 全局样式
├── index.html             # HTML模板
├── package.json           # 项目配置
├── vite.config.js         # Vite配置
└── README.md              # 项目说明
```

## 安装和运行

### 前提条件

- Node.js >= 16.0.0
- npm 或 yarn

### 安装依赖

```bash
cd 智能钥匙柜-vue
npm install
```

### 启动开发服务器

```bash
npm run dev
```

应用将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 后端API配置

确保后端Flask应用正在运行在 http://localhost:5000

后端API接口：
- `GET /api/user/` - 获取所有用户
- `POST /api/user/` - 创建用户
- `GET /api/user/:id` - 获取单个用户
- `PUT /api/user/:id` - 更新用户
- `DELETE /api/user/:id` - 删除用户
- `POST /api/user/:id/borrow` - 借钥匙
- `POST /api/user/:id/return` - 还钥匙
- `GET /api/key/` - 获取所有钥匙
- `POST /api/key/` - 创建钥匙
- `GET /api/key/:id` - 获取单个钥匙
- `PUT /api/key/:id` - 更新钥匙
- `DELETE /api/key/:id` - 删除钥匙

## 页面说明

### 首页 (/)
- 系统概览和导航
- 实时显示可用钥匙数量和借用状态
- 快速访问各功能模块

### 借钥匙 (/borrow)
- 用户身份验证（学生/老师）
- 钥匙选择和借用申请
- 表单验证和提交

### 还钥匙 (/return)
- 用户身份验证
- 显示用户当前借用的钥匙
- 钥匙归还和使用反馈

### 用户管理 (/users)
- 用户列表查看
- 添加、编辑、删除用户
- 查看用户借用记录

### 钥匙管理 (/keys)
- 钥匙列表查看
- 添加、编辑、删除钥匙
- 查看钥匙使用状态

## 特色功能

### 响应式设计
- 适配移动端和桌面端
- 流畅的用户体验

### 实时状态更新
- 自动刷新系统状态
- 实时显示钥匙使用情况

### 表单验证
- 完整的前端表单验证
- 用户友好的错误提示

### 现代化UI
- 基于Element Plus的组件库
- 科技感十足的视觉设计
- 流畅的动画效果

## 开发说明

### 添加新页面
1. 在 `src/views/` 目录下创建新的Vue组件
2. 在 `src/router/index.js` 中添加路由配置
3. 在相应页面添加导航链接

### 添加新API
1. 在 `src/api/index.js` 中添加API接口定义
2. 在组件中导入并使用API

### 样式定制
- 全局样式在 `src/style.css` 中定义
- 组件样式使用scoped CSS
- 支持Element Plus主题定制

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 许可证

本项目仅用于教育目的，版权归济外国际所有。