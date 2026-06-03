# Hướng dẫn khởi chạy dự án cục bộ (Local)

Dự án này đã được đóng gói bằng Docker. Để chạy dự án, vui lòng thực hiện các bước sau:

**Bước 1: Chuẩn bị môi trường**
Đảm bảo máy tính của bạn đã cài đặt [Docker](https://www.docker.com/products/docker-desktop/).

**Bước 2: Build Docker Image**
Tại thư mục gốc của dự án, mở terminal và chạy lệnh:
`docker build -t fit4110/iot-ingestion:lab04 .`

**Bước 3: Khởi chạy Container**
Chạy container từ image vừa build với môi trường giả lập:
`docker run --rm --name fit4110-iot-lab04 -p 8000:8000 --env-file .env.example fit4110/iot-ingestion:lab04`

**Bước 4: Kiểm tra trạng thái (Healthcheck)**
Mở trình duyệt hoặc terminal và truy cập:
`curl http://localhost:8000/health`
(Nếu trả về Status 200 / "OK", ứng dụng đã chạy thành công).

**Bước 5: Chạy tự động kiểm thử (Tuỳ chọn)**
Mở một terminal mới và chạy Postman/Newman test:
`npm run test:local`