"""
Vercel Serverless Function 入口
代理所有 API 请求到 FastAPI 应用
"""

from main import app

# Vercel 会使用这个 app 对象来处理请求
