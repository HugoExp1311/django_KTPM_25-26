# Dùng image Python chính thức
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy toàn bộ project vào container
COPY . /app

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port Django
EXPOSE 8000

# Chạy server khi container khởi động
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
