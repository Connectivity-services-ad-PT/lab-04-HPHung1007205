# Sử dụng base image Python bản slim cho nhẹ
FROM python:3.11-slim

# Cài đặt curl phục vụ cho lệnh HEALTHCHECK
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Tạo non-root user có tên là 'appuser'
RUN useradd -m appuser

# Copy file requirements và cài đặt thư viện trước để tận dụng Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Phân quyền sở hữu thư mục /app cho 'appuser'
RUN chown -R appuser:appuser /app

# Chuyển đổi sang user non-root
USER appuser

# Khai báo port ứng dụng sẽ chạy
EXPOSE 8000

# Thiết lập Healthcheck gọi vào endpoint /health
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Lệnh khởi chạy ứng dụng FastAPI bằng Uvicorn
CMD ["uvicorn", "iot_app.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]