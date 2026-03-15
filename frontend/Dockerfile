# Sử dụng Node.js để build ứng dụng
FROM node:18-alpine AS builder

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy các file lock và package
COPY package.json package-lock.json* ./

# Cài đặt dependencies
RUN npm install

# Copy toàn bộ mã nguồn
COPY . .

# Build Vite app thành static files
RUN npm run build

# Sử dụng Nginx để serve static files
FROM nginx:alpine

# Copy kết quả build từ stage trước sang thư mục html của Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy file cấu hình (nếu cần đổi port hoặc rule), mặc định Nginx chạy cổng 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
