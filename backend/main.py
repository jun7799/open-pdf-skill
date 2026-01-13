"""
PDF Cloud Service - FastAPI Backend
提供 PDF 合并、拆分等功能的云端 API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# 创建临时目录
TEMP_DIR = Path("/tmp/pdf-service")
TEMP_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="PDF Cloud Service API",
    description="PDF 合并、拆分等功能的云端服务",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API 健康检查"""
    return {
        "service": "PDF Cloud Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """健康检查端点"""
    return {"status": "healthy"}


# 导入路由
from api.merge import router as merge_router
from api.split import router as split_router

# 注册路由
app.include_router(merge_router, prefix="/api")
app.include_router(split_router, prefix="/api")
