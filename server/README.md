## Hạ tầng Cloud & Xử lý AI

#### ☁️ Thành phần chính

**\*1. MediaMTX (rtsp server):** Nhận luồng từ Raspberry và forward đến Model Server.

**2. EMQX Broker:** Giao tiếp dữ liệu IoT từ Pi và trả về kết quả từ model.

**3. Model Server:**

- Nhận luồng video từ MediaMTX.
- Chạy YOLO + DeepSORT để tracking.
- Nhận dữ liệu từ cảm biến qua EMQX để xác định khoảng cách trái/phải, hoặc trạng thái té ngã.
- So sánh dữ liệu trong 30s để xác định người dùng có bất tỉnh hay không.

#### 🧠 Luồng xử lý AI

- ** Input:** Stream video từ RTSP + Dữ liệu cảm biến MQTT.

- **Processing:**

  - YOLOv8: Object Detection.
  - DeepSORT: Tracking các object theo thời gian.
  - Gộp kết quả với dữ liệu khoảng cách và gia tốc.

- **Output:**

  - Publish kết quả phân tích nguy hiểm về EMQX.

  - Nếu nghi ngờ ngã bất tỉnh: gửi tín hiệu cảnh báo.

#### ⚙️ Công nghệ

- Python
- OpenCV
- paho-mqtt
- MediaMTX
- YOLOv8, DeepSORT
