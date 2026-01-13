@echo off
chcp 65001 >nul
echo 🔑 济外国际智能钥匙柜管理系统 - 开发环境启动
echo ============================================

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装，请先安装Python
    pause
    exit /b 1
)

REM 检查Node.js环境
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js 未安装，请先安装Node.js
    pause
    exit /b 1
)

echo ✅ 环境检查通过

REM 启动后端
echo 🚀 启动后端服务...
cd backend
echo 🔧 启动Flask后端服务器 (端口: 8000)...
start "Backend API" cmd /k "python simple_app.py"

cd ..

REM 启动前端
echo 🎨 启动前端服务...
cd frontend

if not exist node_modules (
    echo 📦 安装前端依赖...
    npm install
)

echo 🔧 启动Vue3前端服务器 (端口: 3000)...
start "Frontend Dev Server" cmd /k "npm run dev"

echo.
echo 🎉 开发环境启动完成！
echo ============================================
echo 📱 前端地址: http://localhost:3000
echo 🔧 后端API: http://localhost:8000
echo.
echo 按任意键退出...
pause >nul