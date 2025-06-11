## 📌 Tên đề tài

## MẮT KÍNH THÔNG MINH SỬ DỤNG TRONG NHÀ DÀNH CHO NGƯỜI KHIẾM THỊ

## 🧠 Mô tả tổng quát

Thiết bị Mắt kính thông minh được sử dụng để hỗ trợ cho người khiếm thị trong việc phát hiện và đo khoảng cách các vật thể thông dụng như bàn, ghế, cửa ra vào… bằng cảm biến siêu âm Ultrasonic ở không gian bên trong nhà. Kết hợp thêm mô hình học máy DeepSORT với YOLO model trong nhiệm vụ phát hiện các vật thể. Thông qua chức năng đó, thực hiện phát cảnh báo bằng loa đến người sử dụng khi tiếp cận gần với vật cản đã được phát hiện. Đồng thời, gửi thông báo và yêu cầu liên lạc đến người thân thông qua ứng dụng trong các trường hợp người sử dụng gặp nguy hiểm như ngã hay ngất xỉu.

## 🏗️ Kiến trúc hệ thống

- **Device layer:** kính thông thường kết hợp 2 cảm biến ultrasonic, một camera ở giữa kính, cảm biến gia tốc, nút khởi động, nút cảnh báo khẩn cấm và loa cảnh báo.

- **Egde Layer (Raspberry Pi):** Đọc dữ liệu từ cảm biến, gửi qua MQTT đến cloud và stream video từ camera thông qua giao thức RTSP.

- **Cloud Layer:**
  - **MediaMTX server:** nhận và chuyển tiếp video stream.
  - **EMQX broker:** publish và subscribe dữ liệu cảm biến và kết quả xử lý AI.
  - **Model server:** xử lý YOLO + DeepSORT để tracking và phân tích sử kiện nguy hiểm.
  - **Realtime Database (Firebase):** lưu trữ thông tin như mã đăng nhập, mã kính; nội dung cảnh báo, token của các app sẽ nhận thông báo.

## 🔁 Luồng hoạt động

#### 1. Trên Raspberry Pi:

- Stream video từ camera qua RTSP → MediaMTX Server.
- Đọc dữ liệu cảm biến và gửi về EMQX Broker.
- Khi người dùng nhấn nút hoặc té ngã → gửi tín hiệu khẩn cấp.

#### 2. Trên Server

- Nhận video stream từ MediaMTX → đưa vào YOLO + DeepSORT → Object tracking.
- Kết hợp dữ liệu cảm biến để xác định vật thể và nguy cơ va chạm.
- Phát hiện té ngã → so sánh dữ liệu để đưa ra cảnh báo khẩn cấp.

#### 3. Trên App

- Nhập thông báo nguy hiểm thông qua Realtime Database của Firebase
- Hiển thị lịch sử thông báo
- Hiên thị trạng thái kính, hiển thị số lần cảnh báo thông qua biểu đồ.
