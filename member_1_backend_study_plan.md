# Hướng Dẫn Học Tập & Vấn Đáp: Thành viên 1 - Kiến trúc Backend & Game State

Tài liệu này được biên soạn dành riêng cho **Thành viên 1** để chuẩn bị cho buổi bảo vệ đồ án Gomoku AI. Nội dung tập trung giải thích chi tiết hoạt động của file [app.py](file:///d:/Gomoku_MinMax/app.py) và được tối ưu hóa đặc biệt theo **Tiêu chí đánh giá đồ án** để giúp bạn đạt điểm tối đa (**Mức =** và **Mức +**).

---

## 🎯 TIÊU CHÍ ĐÁNH GIÁ CỦA GIẢNG VIÊN & ĐỊNH HƯỚNG ÔN TẬP
*   **Mức 0 (Liệt):** Không hiểu hệ thống, code của chính project của mình, ko tham gia project.
    *   *Cách tránh:* Phải nắm rõ cấu trúc [app.py](file:///d:/Gomoku_MinMax/app.py), giải thích được từng dòng code và cách nó gọi module [minmax.py](file:///d:/Gomoku_MinMax/minmax.py).
*   **Mức - (Yếu):** Không hiểu rõ phương pháp, hệ thống không minh họa được phương pháp lựa chọn.
    *   *Cách tránh:* Hiểu rõ thuật toán Minimax, Alpha-Beta, Iterative Deepening là gì và hệ thống chạy chúng ra sao.
*   **Mức = (Đạt):** Hiểu phương pháp; kết quả và phân tích minh họa được phương pháp TTNT lựa chọn.
    *   *Cách đạt:* Chỉ ra được cách Backend cấu hình độ khó (`depth`, `time_limit`) ảnh hưởng trực tiếp đến độ sâu tìm kiếm và chất lượng nước đi của AI.
*   **Mức + (Xuất sắc):** Phân tích, so sánh, làm rõ các tính chất phương pháp TTNT lựa chọn, ý nghĩa thực tế.
    *   *Cách đạt:* Phân tích sự bùng nổ tổ hợp (combinatorial explosion) khi tăng độ sâu, so sánh kiến trúc lưu trữ trạng thái cờ (In-memory vs Database), và phân tích các trade-off giữa độ trễ API (latency) với độ thông minh của AI.

---

## I. Giải Thích Chi Tiết Phần Việc (app.py)

File [app.py](file:///d:/Gomoku_MinMax/app.py) đóng vai trò là **API Gateway & Controller** của hệ thống, quản lý vòng đời của trò chơi và thiết lập các giới hạn vật lý cho AI.

### 1. Quản lý trạng thái (Game State Variables)
Trạng thái trò chơi được lưu trữ trên RAM của server bằng các biến toàn cục:
*   `board`: Mảng hai chiều 15x15. Giá trị: `0` (Trống), `1` (Human - O), `2` (AI - X).
*   `game_over`: Khóa Boolean (`True`/`False`) ngăn chặn người chơi gửi nước đi khi game đã kết thúc.
*   `current_turn`: Xác định ai có quyền đi tiếp.
*   `move_history`: Ngăn xếp (Stack) lưu các tuple `(x, y, player)` phục vụ logic Hoàn tác (Undo).
*   `DIFFICULTY_SETTINGS`: Cấu hình ràng buộc cho AI:
    *   **Easy:** `depth = 1`, `time_limit = 0.5s`
    *   **Medium:** `depth = 2`, `time_limit = 1.0s`
    *   **Hard:** `depth = 6`, `time_limit = 3.0s`

> [!NOTE]
> **Minh họa phương pháp AI (Mức =):** Bảng cấu hình này minh họa trực quan tính chất cốt lõi của cây trò chơi (Game Tree). Độ sâu càng lớn thì số nút phải duyệt càng nhiều theo hàm mũ. Giới hạn thời gian (`time_limit`) là điều kiện dừng thực tế cho thuật toán Iterative Deepening.

---

## II. Kế Hoạch Học Tập Chi Tiết (5 Ngày)

```mermaid
gantt
    title Kế hoạch học tập cho Thành viên 1 (Mức điểm = và +)
    dateFormat  YYYY-MM-DD
    section Học tập lý thuyết & thực hành
    Ngày 1: Nắm vững Flask & Kết nối hệ thống (Tránh điểm 0)      :active, day1, 2026-06-11, 1d
    Ngày 2: Quản lý Game State & Cơ chế Undo (Tránh điểm -)      :day2, after day1, 1d
    Ngày 3: Minh họa phương pháp AI qua tham số (Mức điểm =)    :day3, after day2, 1d
    Ngày 4: Phân tích sâu kiến trúc & Trade-off hiệu năng (Mức +) :day4, after day3, 1d
    Ngày 5: Mô phỏng vấn đáp & Phản biện giảng viên (Chốt điểm +) :day5, after day4, 1d
```

*   **Ngày 1:** Đọc hiểu cách Flask nhận POST request chứa tọa độ `x`, `y` dưới dạng JSON và trả về kết quả qua `jsonify()`.
*   **Ngày 2:** Tìm hiểu cơ chế quản lý danh sách `move_history` và cách hoạt động của hàm `undo()` (tại sao phải xóa 2 phần tử).
*   **Ngày 3:** Nghiên cứu mối liên hệ giữa `DIFFICULTY_SETTINGS` và thuật toán `minimax`. Quan sát sự thay đổi tốc độ phản hồi của AI khi chơi ở các chế độ Easy, Medium, Hard.
*   **Ngày 4:** Phân tích các giới hạn vật lý của server khi chạy AI (CPU, RAM, HTTP Timeout) và đề xuất phương án tối ưu kiến trúc.
*   **Ngày 5:** Tự trả lời bộ câu hỏi vấn đáp Mức + dưới đây mà không cần nhìn tài liệu.

---

## III. Bộ Câu Hỏi Vấn Đáp Thường Gặp (Phân loại theo Mức Điểm)

### 📌 NHÓM CÂU HỎI ĐẠT ĐIỂM KHÁ (Mức =)
*Giảng viên kiểm tra xem hệ thống của bạn có thực sự minh họa được phương pháp AI đã lựa chọn hay không.*

#### ❓ Câu 1: Làm thế nào để Backend thể hiện được sự khác biệt giữa các độ khó của thuật toán Minimax?
*   **Trả lời (Mức =):**
    *   Sự khác biệt nằm ở cấu hình `DIFFICULTY_SETTINGS`. Ở mức **Easy** (`depth=1`), AI chỉ nhìn trước đúng 1 nước (chỉ duyệt các nước đi trực tiếp trên bàn cờ hiện tại). Ở mức **Medium** (`depth=2`), AI duyệt trước 2 nước (nước của AI và phản ứng của đối thủ). Ở mức **Hard** (`depth=6`), AI tính toán trước tới 6 nước đi tiếp theo của cả hai bên.
    *   Khi gọi bộ não AI, Backend truyền tham số này vào: `iterative_deepening(board, max_depth=max_depth, time_limit=time_limit)`. Điều này trực tiếp giới hạn độ sâu của cây trò chơi mà Minimax sẽ xây dựng, từ đó quyết định độ thông minh và thời gian tính toán của AI.

#### ❓ Câu 2: Thuật toán Iterative Deepening hoạt động dựa trên thời gian thực. Backend làm thế nào để đảm bảo AI không chạy quá thời gian quy định ở mỗi nước đi?
*   **Trả lời (Mức =):**
    *   Backend đóng vai trò là bên áp đặt luật chơi và giới hạn tài nguyên. Khi gọi bộ não AI trong route `/move`, Backend truyền tham số `time_limit` (0.5s / 1.0s / 3.0s).
    *   Hàm tìm kiếm trong `minmax.py` sẽ liên tục kiểm tra thời gian trôi qua. Nếu vượt quá `time_limit`, một `TimeoutException` sẽ được ném ra. Backend sẽ bắt lấy ngoại lệ này (hoặc module AI tự xử lý) và trả về nước đi tốt nhất tìm được ở độ sâu hoàn chỉnh gần nhất trước đó. Đây gọi là tính chất **Anytime Algorithm** của thuật toán Iterative Deepening.

#### ❓ Câu 3: Tại sao trong route `/move`, sau khi nhận nước đi của người chơi, Backend phải gọi hàm `check_winner` ngay lập tức trước khi gọi AI?
*   **Trả lời (Mức =):**
    *   Để minh họa đúng trạng thái của Game Tree: nếu nước đi của người chơi dẫn đến trạng thái thắng (terminal state), cây trò chơi kết thúc tại đó.
    *   Nếu không kiểm tra và lập tức gọi AI, AI sẽ cố gắng tính toán nước đi tiếp theo trên một bàn cờ đã kết thúc, gây lỗi logic (chơi tiếp sau khi thắng) và lãng phí tài nguyên tính toán (CPU phải duyệt cây vô nghĩa).

---

### 🏆 NHÓM CÂU HỎI ĐẠT ĐIỂM TỐI ĐA (Mức +)
*Giảng viên yêu cầu phân tích sâu, so sánh, làm rõ tính chất của phương pháp AI và ý nghĩa thực tế.*

#### ❓ Câu 4: Hãy phân tích sự bùng nổ tổ hợp (Combinatorial Explosion) trên bàn cờ Gomoku 15x15 và cách cấu hình độ khó của Backend giải quyết bài toán này?
*   **Trả lời (Mức +):**
    *   **Phân tích bùng nổ tổ hợp:** Bàn cờ Gomoku 15x15 có tổng cộng 225 ô. Ở nước đi đầu tiên, hệ số nhánh (branching factor) $b = 225$. Độ phức tạp của Minimax thuần túy là $O(b^d)$, trong đó $d$ là độ sâu tìm kiếm. Nếu không tối ưu, ở độ sâu $d = 6$, số nút phải duyệt là $225^6 \approx 1.29 \times 10^{14}$ nút, một con số khổng lồ không thể tính toán trong vài giây.
    *   **Cách giải quyết:** Hệ thống đã áp dụng các kỹ thuật cắt giảm không gian tìm kiếm cực kỳ hiệu quả mà Backend trực tiếp tham gia điều phối:
        1.  **Neighborhood-based Move Generation:** Trong `minmax.py`, thay vì duyệt cả 225 ô, ta chỉ sinh nước đi trong bán kính 2 ô xung quanh các quân cờ hiện tại. Số lượng nước đi ứng viên giảm từ 225 xuống trung bình $b \approx 20$ đến $40$.
        2.  **Move Ordering & Alpha-Beta Pruning:** Các nước đi được sắp xếp nhanh bằng thuật toán Delta Evaluation. Việc duyệt các nước đi tốt nhất lên đầu giúp Alpha-Beta Pruning cắt bỏ tới 70-90% nhánh phụ.
        3.  **Hard Setting Limitation:** Backend giới hạn `depth=6` và `time_limit=3.0s` cho mức Hard. Ở độ sâu 6 với $b \approx 20$, số nút lý thuyết tối đa là $20^6 \approx 64,000,000$ nút. Nhờ Alpha-Beta và Move Ordering, số nút thực tế cần duyệt chỉ khoảng vài trăm nghìn đến hơn 1 triệu nút, hoàn toàn chạy mượt mà dưới 3 giây trên CPU thông thường.

#### ❓ Câu 5: Hiện tại game đang dùng biến toàn cục (`board`, `game_over`,...) lưu trên RAM. Hãy so sánh kiến trúc này với kiến trúc thực tế chạy môi trường Production (nhiều người chơi cùng lúc)?
*   **Trả lời (Mức +):**
    *   **Kiến trúc hiện tại (In-Memory Global Variables):**
        *   *Ưu điểm:* Cực kỳ đơn giản, dễ triển khai, truy xuất trạng thái bàn cờ với độ trễ gần như bằng 0 ($O(1)$ truy cập bộ nhớ).
        *   *Nhược điểm:* **Single-session** (chỉ chơi được 1 game duy nhất tại một thời điểm). Nếu có người chơi thứ 2 truy cập, họ sẽ ghi đè lên trạng thái bàn cờ của người thứ nhất. Tiến trình server bị restart sẽ làm mất toàn bộ trạng thái game.
    *   **So sánh với kiến trúc Production (Multi-session & Scalability):**
        *   Để chạy thực tế cho hàng ngàn người chơi, ta phải chuyển sang kiến trúc **Stateful API** hoặc **Stateless API kết hợp Session Store**:
            1.  *Giải pháp Session-based:* Sử dụng cookie session để lưu `game_id` riêng biệt cho mỗi người chơi.
            2.  *Giải pháp External State Store (Redis):* Thay vì lưu bàn cờ trong biến toàn cục của Flask, ta lưu bàn cờ vào **Redis Cache** với key là `game_id` (ví dụ: `game:1002:board`). Redis là in-memory database nên tốc độ truy xuất cực nhanh, hỗ trợ đọc ghi song song (concurrency) tốt và giải quyết triệt để bài toán Race Condition khi nhiều người chơi gửi request `/move` cùng lúc.
            3.  *Giải pháp Database lâu dài:* Lưu lịch sử các trận đấu vào cơ sở dữ liệu quan hệ (SQLite/PostgreSQL) để phân tích dữ liệu nước đi hoặc phục vụ chức năng xem lại trận đấu (replay).

#### ❓ Câu 6: Hãy phân tích Trade-off (sự đánh đổi) giữa độ thông minh của AI và độ trễ (latency) của HTTP API. Nếu muốn nâng độ sâu tìm kiếm lên `depth=10`, hệ thống sẽ gặp vấn đề gì và em đề xuất giải pháp kiến trúc nào để khắc phục?
*   **Trả lời (Mức +):**
    *   **Phân tích Trade-off:** AI càng thông minh (depth càng sâu) thì độ chính xác nước đi càng cao, nhưng thời gian xử lý của thuật toán tìm kiếm đệ quy tăng theo hàm mũ, dẫn đến thời gian phản hồi HTTP request (API Latency) tăng mạnh. Trải nghiệm người dùng sẽ bị ảnh hưởng nếu họ phải chờ quá 3-5 giây cho một nước đi của AI.
    *   **Vấn đề khi tăng lên `depth=10`:**
        1.  **HTTP Timeout:** Nếu AI tính toán mất trên 30 giây, trình duyệt hoặc các proxy/web server (như Nginx, Gunicorn) sẽ tự động ngắt kết nối và trả về lỗi `504 Gateway Timeout`.
        2.  **Blocking CPU:** Flask hoạt động đơn luồng (hoặc đa luồng giới hạn). Việc chạy một thuật toán tốn CPU như Minimax ở depth 10 sẽ làm nghẽn tiến trình server, khiến mọi người chơi khác không thể kết nối hoặc thực hiện nước đi.
    *   **Đề xuất giải pháp kiến trúc khắc phục (Mức +):**
        *   Để chạy các tác vụ AI tốn thời gian mà không làm nghẽn API, ta phải chuyển từ kiến trúc đồng bộ (Synchronous) sang **Kiến trúc bất đồng bộ (Asynchronous Event-driven Architecture)**:
            1.  **Message Queue & Worker (Celery + RabbitMQ/Redis):** Khi nhận request `/move`, thay vì tính toán trực tiếp, Backend chỉ đẩy tác vụ tính toán vào hàng đợi Celery và trả về ngay HTTP `202 Accepted` kèm theo một `task_id`. Một tiến trình Worker riêng biệt sẽ đảm nhận việc tính toán nước đi AI ở background.
            2.  **WebSockets (Flask-SocketIO):** Thay vì dùng HTTP REST API ngắn hạn, Client và Server sẽ duy trì kết nối Socket song hướng lâu dài. Khi Worker tính xong nước đi AI, Server sẽ chủ động gửi (push) kết quả về cho Client qua kênh Socket. Điều này giúp giao diện web hiển thị trạng thái "AI đang suy nghĩ..." mà không bao giờ bị timeout kết nối.
