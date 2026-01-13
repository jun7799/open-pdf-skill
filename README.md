# PDF Cloud Service

> 免费的在线 PDF 工具 - 支持合并、拆分 PDF 文件

## 功能特性

- **合并 PDF** - 将多个 PDF 文件合并为一个
- **拆分 PDF** - 将 PDF 按页拆分（单页拆分/按范围拆分）
- **云端处理** - 所有操作在云端完成，无需本地安装
- **隐私保护** - 文件处理后自动删除，不存储用户数据

## 技术栈

### 后端
- FastAPI - Python Web 框架
- pypdf - PDF 处理库
- Vercel - Serverless 部署平台

### 前端
- React 18 - UI 框架
- Tailwind CSS - 样式框架
- Vite - 构建工具
- Lucide React - 图标库

## 本地开发

### 后端开发

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn main:app --reload --port 8000
```

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 部署到 Vercel

### 1. 准备工作

确保你已经安装了 Vercel CLI：

```bash
npm install -g vercel
```

### 2. 部署后端

```bash
cd backend
vercel
```

### 3. 部署前端

```bash
cd frontend

# 设置后端 API 地址
vercel env add VITE_API_URL

# 构建并部署
vercel
```

## API 文档

### 合并 PDF

```
POST /api/merge
Content-Type: multipart/form-data

files: File[]  # 要合并的 PDF 文件列表
```

### 拆分 PDF

```
POST /api/split
Content-Type: multipart/form-data

file: File        # 要拆分的 PDF 文件
mode: string      # single | range
ranges: string    # 页面范围，如 "1-3,5-7"（可选）
```

## 项目结构

```
pdf-cloud-service/
├── backend/                 # 后端服务
│   ├── api/                # API 路由
│   │   ├── merge.py        # 合并接口
│   │   └── split.py        # 拆分接口
│   ├── main.py             # FastAPI 入口
│   ├── requirements.txt    # Python 依赖
│   └── vercel.json         # Vercel 配置
│
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── components/     # React 组件
│   │   │   ├── FileUploader.jsx
│   │   │   ├── MergePanel.jsx
│   │   │   └── SplitPanel.jsx
│   │   ├── api/            # API 调用
│   │   ├── App.jsx         # 主应用
│   │   └── main.jsx        # 入口文件
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

## 许可证

MIT License
