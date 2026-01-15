#!/bin/bash

echo "🔑 济外国际智能钥匙柜管理系统 - 开发环境启动"
echo "============================================"

# 检查环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

echo "✅ 环境检查通过"

# 启动后端
echo "🚀 启动后端服务..."
cd backend
echo "🔧 启动Flask后端服务器 (端口: 5002)..."
PORT=5002 python3 app.py &
BACKEND_PID=$!

cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端服务..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

echo "🔧 启动Vue3前端服务器 (端口: 3000)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 开发环境启动完成！"
echo "============================================"
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端API: http://localhost:5002"
echo "🔐 管理后台: http://localhost:5002/admin"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

wait
