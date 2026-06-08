# 🎮 Gomoku AI - Cờ Caro Tích Hợp Trí Tuệ Nhân Tạo

Chào mừng bạn đến với dự án **Gomoku AI**! Đây là một ứng dụng web chơi cờ Caro (Gomoku) trực tuyến với bàn cờ tiêu chuẩn 15x15. Điểm nhấn của dự án là một hệ thống Trí Tuệ Nhân Tạo (AI) cực kỳ thông minh được xây dựng bằng thuật toán **Minimax** kết hợp với **Alpha-Beta Pruning** (Cắt tỉa Alpha-Beta) và **Iterative Deepening** (Tìm kiếm sâu dần).

Giao diện ứng dụng được thiết kế theo phong cách hiện đại (Glassmorphism, Dark Theme) mang lại cảm giác mượt mà và cao cấp.

---

## 🌟 Các Tính Năng Nổi Bật

- **AI Thông Minh Kế Thừa Chiến Thuật Caro Thực Tế**: Hàm đánh giá (Heuristic Evaluation) được hiệu chỉnh chi tiết dựa trên cấp độ đe dọa thực tế của cờ Caro (VD: chặn chuỗi 4 bịt 1 đầu được ưu tiên cao hơn việc tự tạo chuỗi 4 hở 2 đầu).
- **Thuật Toán Tối Ưu Cao**: AI sử dụng **Alpha-Beta Pruning** kết hợp đánh giá cục bộ (Local Evaluation) để loại bỏ hàng triệu trường hợp thừa, giúp AI nghĩ nhanh nhưng vẫn nhìn xa.
- **3 Cấp Độ Khó**:
  - **Dễ (Easy)**: AI đánh giá ở độ sâu 1 (chỉ nhìn trước 1 bước). Thích hợp cho người mới làm quen.
  - **Trung Bình (Medium)**: AI đánh giá ở độ sâu 2 (nhìn trước 2 bước). Cân bằng giữa phòng thủ và tấn công.
  - **Khó (Hard)**: AI tìm kiếm sâu tới 6 bước (Depth 6) trong giới hạn 3 giây. AI sẽ phòng thủ chặt chẽ và giăng bẫy cực kỳ nguy hiểm.
- **Hoàn Tác (Undo)**: Cho phép người chơi rút lại nước đi sai lầm.
- **Tùy Chọn Lượt Đi**: Người chơi có thể chọn đi trước (X) hoặc nhường AI đi trước (O).
- **Thông Báo Trực Quan**: Modal thông báo kết quả thắng/thua rõ ràng, hiện đại.

---

## 🛠️ Công Nghệ Sử Dụng

- **Backend**: Python 3, Flask (Xử lý logic game và API phân tích nước đi cho AI).
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 thuần (Tối ưu hóa tốc độ load, giao diện Glassmorphism).
- **AI Core**: Thuật toán Minimax nguyên bản được tinh chỉnh sâu.

---

## 🚀 Hướng Dẫn Cài Đặt Và Khởi Chạy

Để chạy dự án này trên máy tính của bạn, hãy làm theo các bước chi tiết dưới đây:

### 1. Yêu cầu hệ thống
- Máy tính đã cài đặt sẵn **Python 3.8** trở lên.
- Trình duyệt web hiện đại (Chrome, Edge, Firefox, Safari...).

### 2. Tải mã nguồn dự án
- Clone dự án từ GitHub (nếu có) hoặc giải nén file ZIP chứa mã nguồn vào một thư mục trên máy tính của bạn.
- Mở Terminal (Command Prompt / PowerShell trên Windows) và di chuyển vào thư mục dự án:
  ```bash
  cd duong_dan_den_thu_muc/Gomoku_MinMax
  ```

### 3. Tạo môi trường ảo (Khuyến nghị)
Việc tạo môi trường ảo (Virtual Environment) giúp các thư viện của dự án không bị xung đột với các dự án Python khác trên máy của bạn.
- Chạy lệnh tạo môi trường ảo (tên là `.venv`):
  ```bash
  python -m venv .venv
  ```
- **Kích hoạt môi trường ảo**:
  - Trên **Windows** (Command Prompt / PowerShell):
    ```bash
    .\.venv\Scripts\activate
    ```
  - Trên **macOS / Linux**:
    ```bash
    source .venv/bin/activate
    ```

### 4. Cài đặt các thư viện cần thiết
- Sau khi kích hoạt môi trường ảo, bạn chạy lệnh sau để cài đặt Flask và các thư viện liên quan:
  ```bash
  pip install -r requirements.txt
  ```

### 5. Khởi chạy ứng dụng
- Tại thư mục gốc của dự án, chạy lệnh:
  ```bash
  python app.py
  ```
- Terminal sẽ hiển thị dòng chữ: `* Running on http://127.0.0.1:5000`. Điều này có nghĩa là Server đã hoạt động.

### 6. Chơi Game
- Mở trình duyệt web của bạn và truy cập vào địa chỉ:
  👉 **http://127.0.0.1:5000**
- Chọn cấp độ, chọn lượt đi (Đi trước / Đi sau) và tận hưởng trò chơi!

---

## 🧠 Sơ Đồ Cấu Trúc & Vai Trò Các File Code

Dưới đây là sơ đồ thư mục của dự án và giải thích chi tiết chức năng của từng tệp:

```text
Gomoku_MinMax/
├── .venv/                      # Thư mục môi trường ảo chứa thư viện Python (sinh ra khi setup)
├── static/                     # Thư mục chứa tài nguyên tĩnh (Frontend)
│   ├── css/
│   │   └── style.css           # Mã thiết kế UI/UX (Glassmorphism, Dark Theme, Animations)
│   └── js/
│       └── game.js             # Logic Frontend: vẽ bàn cờ X/O, gửi API requests (fetch)
├── templates/                  # Thư mục chứa giao diện web (HTML)
│   └── index.html              # Trang chủ giao diện trò chơi (được Flask render)
├── app.py                      # (Backend) File server chính, định nghĩa API và Game State
├── minmax.py                   # (AI Core) "Bộ não" Trí tuệ Nhân tạo xử lý nước cờ
└── requirements.txt            # Danh sách các gói thư viện Python cần cài đặt
```

### 📝 Chi Tiết Vai Trò Từng File:

1. **`app.py` (Backend Gateway)**: 
   Sử dụng framework Flask để khởi chạy Server cục bộ. Nơi này duy trì trạng thái ván cờ hiện tại (mảng `board` 2D, danh sách `move_history`) và cung cấp các RESTful API endpoints: 
   - `/start`: Cấu hình độ khó và chọn người đi trước.
   - `/move`: Tiếp nhận nước đi của người chơi, gọi AI tính toán và trả về nước đi đáp trả.
   - `/undo`: Cập nhật lại mảng dữ liệu khi người dùng muốn hoàn tác.
   - `/reset`: Dọn dẹp dữ liệu để bắt đầu ván mới.

2. **`minmax.py` (Bộ Não AI)**:
   Xử lý toàn bộ logic thông minh nhất của hệ thống, bao gồm các thành phần:
   - **Đánh giá Thế cờ (`evaluate`, `_evaluate_line`)**: Quét bàn cờ và chấm điểm mức độ nguy hiểm, phòng thủ và tấn công dựa trên Hệ số đe dọa thực tế của Caro (Gomoku Initiative Hierarchy).
   - **Khoanh vùng Nước đi (`get_possible_moves`)**: Tìm kiếm thông minh các nước đi ở bán kính gần các khu vực giao tranh, giảm thiểu vùng tìm kiếm vô nghĩa.
   - **Thuật toán (`minimax`, `iterative_deepening`)**: Ứng dụng Minimax với kỹ thuật Alpha-Beta Pruning và quản lý thời gian (Timeout). AI sẽ tự đưa ra quyết định tốt nhất trong giới hạn 3 giây thay vì suy nghĩ mãi mãi.

3. **`static/js/game.js` (Frontend Controller)**:
   Quản lý tương tác với người chơi ở trình duyệt. Lắng nghe các sự kiện click chuột trên lưới Caro, vẽ quân `X`/`O` lên màn hình, khóa bàn cờ trong lúc đợi AI phản hồi để tránh lỗi click đúp, đồng thời điều khiển bật/tắt Modal thông báo khi có người chiến thắng.

4. **`static/css/style.css` (UI/UX Styling)**:
   Đảm nhận phần nhìn của game. Tạo nên thiết kế kính mờ (Glassmorphism) sắc sảo, nền đen (Dark theme) huyền bí, đổ bóng nổi 3D và các hiệu ứng chuyển động vi mô (micro-animations) khi người chơi đưa chuột qua các ô cờ.

5. **`templates/index.html` (Markup Structure)**:
   Cung cấp bộ khung xương của trang web, nơi bố trí Layout cho lưới bàn cờ 15x15, các cụm nút bấm điều khiển trò chơi (Dễ/Trung Bình/Khó, Đi trước/Đi sau) và cấu trúc cho các thông báo.

---
*Chúc bạn có những giờ phút đấu trí thú vị cùng Gomoku AI!*
