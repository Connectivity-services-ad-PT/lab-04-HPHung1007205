FROM python:3.11

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set PYTHONPATH để đảm bảo từ thư mục /app có thể import được 'src'
ENV PYTHONPATH=/app

# Dùng CMD trực tiếp và đầy đủ
CMD ["uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]