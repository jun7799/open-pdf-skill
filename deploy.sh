#!/bin/bash

echo "=== PDF Cloud Service 部署脚本 ==="
echo ""

# 检查是否已登录 Railway
if ! railway whoami > /dev/null 2>&1; then
    echo "请先登录 Railway:"
    echo "  railway login"
    exit 1
fi

# 部署后端到 Railway
echo "1. 部署后端到 Railway..."
cd backend
railway init --yes
railway up

# 获取后端 URL
BACKEND_URL=$(railway domain | head -1)
echo "   后端 URL: $BACKEND_URL"

# 返回根目录
cd ..

# 更新前端环境变量
echo ""
echo "2. 配置前端环境变量..."
cd frontend
echo "   VITE_API_URL=$BACKEND_URL/api"

# 部署前端到 Vercel
echo ""
echo "3. 部署前端到 Vercel..."
cd ..
vercel --prod

echo ""
echo "=== 部署完成! ==="
