@echo off
chcp 65001 >nul
echo 🔑 济外国际智能钥匙柜管理系统启动脚本
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
echo 🚀 启动后端Flask应用...
cd myflask

if not exist venv (
    echo 📦 创建Python虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

echo 🔧 启动Flask后端服务器 (端口: 5000)...
start "Flask Backend" cmd /k "python app.py"

cd ..

REM 启动前端
echo 🎨 启动Vue3前端应用...
cd 智能钥匙柜-vue

if not exist node_modules (
    echo 📦 安装前端依赖...
    npm install
)

echo 🔧 启动Vue3前端服务器 (端口: 3000)...
start "Vue Frontend" cmd /k "npm run dev"

echo.
echo 🎉 系统启动完成！
echo ============================================
echo 📱 前端地址: http://localhost:3000
echo 🔧 后端API: http://localhost:5000
echo ⚙️  管理后台: http://localhost:5000/admin
echo.
echo 按任意键退出...
pause >nul