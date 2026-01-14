FROM python:3.11-slim

WORKDIR /app

# 复制后端代码
COPY backend/ ./backend/

# 安装依赖
RUN pip install --no-cache-dir -r backend/requirements.txt

# 暴露端口
EXPOSE 8080

# 启动应用
CMD ["python", "backend/main.py"]
