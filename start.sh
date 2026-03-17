#!/bin/bash
# 快速启动脚本

set -e

PROJECT_DIR="/home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api"
cd "$PROJECT_DIR"

echo "🚀 启动 Coze Bilibili API 服务..."

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，使用 Python 直接运行"
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        echo "📦 创建虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 安装依赖
    echo "📦 安装依赖..."
    pip install -q -r requirements.txt
    
    # 启动服务
    echo "🌐 启动服务..."
    python main.py
    
else
    # 使用 Docker
    echo "🐳 使用 Docker 启动..."
    
    # 创建 .env 文件
    if [ ! -f ".env" ]; then
        echo "📝 创建 .env 文件..."
        cat > .env << EOF
API_PORT=8000
DEBUG=false
COOKIES_FILE=/cookies/bilibili_cookies.txt
LOG_LEVEL=INFO
EOF
    fi
    
    # 启动服务
    docker-compose up -d
    
    # 等待服务启动
    echo "⏳ 等待服务启动..."
    sleep 5
    
    # 检查状态
    docker-compose ps
    
    echo ""
    echo "✅ 服务已启动！"
    echo "📍 API 地址：http://localhost:8000"
    echo "📖 查看日志：docker-compose logs -f"
    echo "🧪 测试 API: python test_api.py"
    echo "🛑 停止服务：docker-compose down"
fi
