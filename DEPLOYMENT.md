# 部署指南

## 方案：前后端分离部署

### 后端部署到 Railway

#### 方式一：通过 GitHub（推荐）

1. **推送代码到 GitHub**
   ```bash
   cd pdf-cloud-service
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **在 Railway 上创建项目**
   - 访问 https://railway.app/new
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库
   - Railway 会自动检测 Python 项目并部署

3. **配置项目**
   - Railway 会自动识别 `railway.toml` 配置
   - 部署完成后，获取后端 URL（如：https://xxx.up.railway.app）

#### 方式二：通过 Railway CLI

1. **安装 CLI**（已完成）
   ```bash
   npm install -g @railway/cli
   ```

2. **登录**
   ```bash
   railway login
   ```

3. **初始化项目**
   ```bash
   cd backend
   railway init
   railway up
   ```

4. **获取域名**
   ```bash
   railway domain
   ```

### 前端部署到 Vercel

1. **设置环境变量**
   ```bash
   cd frontend
   vercel env add VITE_API_URL production
   # 输入你的 Railway 后端 URL，例如：
   # https://xxx.up.railway.app/api
   ```

2. **重新部署**
   ```bash
   cd ..
   vercel --prod
   ```

## 部署后的完整架构

```
用户浏览器
    │
    ▼
┌─────────────────┐
│  Vercel (前端)  │ ← https://pdf-cloud-service.vercel.app
│   React + Vite  │
└────────┬────────┘
         │ API 请求
         ▼
┌─────────────────┐
│  Railway (后端) │ ← https://xxx.up.railway.app
│  FastAPI + PDF  │
└─────────────────┘
```

## 本地开发

### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# 访问 http://localhost:8000
```

### 前端
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000
```
