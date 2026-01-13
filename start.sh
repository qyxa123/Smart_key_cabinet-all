#!/bin/bash

echo "🔑 济外国际智能钥匙柜管理系统启动脚本"
echo "============================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

echo "✅ 环境检查通过"

# 启动后端
echo "🚀 启动后端Flask应用..."
cd myflask
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

echo "🔧 启动Flask后端服务器 (端口: 5000)..."
python app.py &
FLASK_PID=$!

cd ..

# 启动前端
echo "🎨 启动Vue3前端应用..."
cd 智能钥匙柜-vue

if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

echo "🔧 启动Vue3前端服务器 (端口: 3000)..."
npm run dev &
VUE_PID=$!

echo ""
echo "🎉 系统启动完成！"
echo "============================================"
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端API: http://localhost:5000"
echo "⚙️  管理后台: http://localhost:5000/admin"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo ''; echo '🛑 正在停止服务...'; kill $FLASK_PID $VUE_PID 2>/dev/null; exit 0" INT

wait