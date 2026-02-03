FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends     postgresql-client     && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 依賴
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用代碼
COPY backend/ .

# 暴露端口
EXPOSE 10000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3     CMD python -c "import requests; requests.get('http://localhost:10000/health')"

# 啟動命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
