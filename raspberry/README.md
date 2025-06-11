## Thiết bị và Raspberry Pi

#### 🔧 Phần cứng sử dụng

- **Cảm biến khoảng cách Ultrasonic (2 cái):** gắn hai bên kính đo khoảng cách trái và phải.

- **Camera**: Gắn trước kính, stream thông qua giao thức RTSP.

- **Cảm biến ADXL345:** Phát hiện té ngã qua gia tốc bất thường.

- **Loa + Mạch khuếch đại:** Phát âm thanh cảnh báo khi gần vật thể hoặc té ngã.

- **Nút nhấn:** Khởi động hệ thống và gửi cảnh báo khẩn cấp.

- **Pin:** Cấp nguồn cho Raspberry Pi.

#### 🧪 Phần mềm

- **Python Script:**

  - Đọc giá trị từ cảm biến (Ultrasonic, ADXL345).

  - Gửi dữ liệu cảm biến đến EMQX (MQTT).

  - Phát cảnh báo bằng âm thanh.

  - Gửi tín hiệu SOS khi nhấn nút.

- **Camera Streaming:**

  - Sử dụng ffmpeg để stream qua RTSP đến MediaMTX.
