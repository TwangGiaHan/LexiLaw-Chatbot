# Dùng bản python slim để tối ưu dung lượng
FROM python:3.10-slim

# Cập nhật OS và cài đặt thư viện build cần thiết
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Chuyển vào thư mục làm việc /app
WORKDIR /app

# Copy requirements vào và install trước để docker tối ưu hóa layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy phần lớn mã nguồn dự án vào
COPY . .

# Bật port 8000
EXPOSE 8000

# Chạy server FastAPI bằng uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]