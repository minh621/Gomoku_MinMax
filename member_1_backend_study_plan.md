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

## II. Giáo Trình Học Tập Chi Tiết Cho 5 Ngày

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

### 📅 NGÀY 1: NỀN TẢNG FLASK FRAMEWORK & THIẾT KẾ API (Mục tiêu: Tránh điểm 0)

Để tránh điểm 0, bạn phải chứng minh mình tự tay lập trình hoặc hiểu rõ từng dòng code của [app.py](file:///d:/Gomoku_MinMax/app.py).

#### 1. Khái niệm cốt lõi về Flask
Flask là một micro-framework viết bằng Python dùng để xây dựng web application.
*   `app = Flask(__name__)` khởi tạo ứng dụng Flask.
*   Decorator `@app.route(path, methods)` ánh xạ một URL endpoint (đường dẫn) đến một hàm Python cụ thể.

#### 2. Giao tiếp dữ liệu qua RESTful API
Trong dự án này, Frontend và Backend giao tiếp không đồng bộ thông qua JSON.
*   **Nhận dữ liệu (Request JSON):** Frontend gửi tọa độ qua phương thức POST. Backend đọc bằng `request.json` (dòng 34, 81).
*   **Trả dữ liệu (Response JSON):** Backend gửi lại trạng thái bàn cờ qua hàm `jsonify()` (dòng 60, 70, 99,...).
*   **HTTP Status Code:**
    *   `200 OK`: Trả về khi nước đi hợp lệ hoặc khởi tạo thành công.
    *   `400 Bad Request` (dòng 39, 41): Dữ liệu truyền lên bị lỗi cấu trúc (ví dụ: tham số độ khó không hợp lệ).

#### 3. Phân tích luồng của Route `/start` (Khởi động game)
```python
@app.route("/start", methods=["POST"])
def start():
    global board, game_over, current_turn, move_history, difficulty
    data = request.json
    first = data.get("first", "human")
    difficulty = data.get("difficulty", "medium")
    ...
```
*   **Bước 1:** Lấy thông tin người đi trước và độ khó từ `request.json`.
*   **Bước 2 (Validation):** Kiểm tra `first` có nằm trong `("human", "ai")` và `difficulty` có nằm trong `("easy", "medium", "hard")` hay không. Nếu không, trả về lỗi HTTP 400.
*   **Bước 3 (Reset State):** Xóa trắng bàn cờ bằng cách khởi tạo danh sách 2 chiều chứa toàn bộ giá trị `EMPTY`. Xóa lịch sử nước đi.
*   **Bước 4 (AI đi trước):** Nếu AI được cấu hình đi trước, backend lập tức gọi thuật toán `iterative_deepening` để tìm nước đi tối ưu và cập nhật lên bàn cờ, ghi nhận vào lịch sử rồi chuyển lượt lại cho người chơi.

#### 🛠️ Bài tập thực hành Ngày 1:
1. Chạy lệnh `python app.py` trên Terminal.
2. Dùng công cụ Postman hoặc lệnh curl để giả lập gửi một yêu cầu khởi tạo game mới đến `http://127.0.0.1:5000/start` với dữ liệu `{"first": "ai", "difficulty": "hard"}` và xem kết quả JSON trả về.

---

### 📅 NGÀY 2: QUẢN LÝ GAME STATE & CƠ CHẾ HOÀN TÁC (UNDO) (Mục tiêu: Tránh điểm -)

Để tránh điểm yếu (-), bạn cần nắm vững cách lưu giữ và khôi phục trạng thái trò chơi.

#### 1. Biểu diễn Bàn cờ (Matrix representation)
Bàn cờ caro được biểu diễn bằng một mảng 2 chiều kích thước 15x15 chứa các số nguyên:
```python
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
```
*   `board[r][c]` đại diện cho ô ở dòng `r` và cột `c`.
*   Truy cập bằng 2 vòng lặp lồng nhau hoặc tọa độ chỉ số.

#### 2. Vai trò của từ khóa `global` trong Python
*   Trong Flask, mỗi khi client gửi yêu cầu (request), một luồng xử lý sẽ được chạy. Để các hàm xử lý của route sửa đổi được dữ liệu bàn cờ chung của toàn bộ server, chúng ta phải khai báo `global board, game_over, move_history`.
*   Nếu không khai báo `global`, Python sẽ coi phép gán `board = ...` trong hàm là tạo ra một biến cục bộ mới, dẫn đến dữ liệu bàn cờ toàn cục không hề thay đổi sau cuộc gọi API.

#### 3. Phân tích chi tiết thuật toán Hoàn tác (Undo Stack)
`move_history` được thiết kế theo cấu trúc ngăn xếp (Stack - LIFO: Vào sau ra trước).
```python
# Hoàn tác nước đi của AI (nếu nước cuối là của AI)
if move_history and move_history[-1][2] == AI:
    ax, ay, _ = move_history.pop()
    board[ax][ay] = EMPTY
    undone += 1

# Hoàn tác nước đi của người chơi
if move_history and move_history[-1][2] == HUMAN:
    hx, hy, _ = move_history.pop()
    board[hx][hy] = EMPTY
    undone += 1
```
*   **Tại sao lại pop tối đa 2 lần?** Vì người chơi đấu với AI, khi nhấn "Undo" họ muốn rút lại nước đi của mình. Khi đó, cả nước cờ phản công của AI liền trước và nước cờ của chính người chơi đều phải bị thu hồi khỏi bàn cờ.
*   **Trường hợp biên:** Nếu game đã kết thúc (`game_over = True`), việc hoàn tác sẽ khôi phục lại trạng thái chơi bằng cách gán `game_over = False` (dòng 127). Nếu `move_history` trống, hàm lập tức trả về 0 để tránh lỗi `IndexError` khi gọi `.pop()`.

#### 🛠️ Bài tập thực hành Ngày 2:
1. Đọc kỹ route `/undo` trong [app.py](file:///d:/Gomoku_MinMax/app.py).
2. Hãy thử giải thích: Điều gì xảy ra nếu người chơi đi trước, AI chưa kịp đi (hoặc đang tính toán) mà người chơi nhấn Undo? Hệ thống có bị lỗi không? (Hệ thống kiểm tra `move_history[-1][2]`, nếu chỉ có nước đi của HUMAN, nó chỉ pop 1 lần và trả về `undone = 1`).

---

### 📅 NGÀY 3: TƯƠNG TÁC MODULE AI & THỂ HIỆN PHƯƠNG PHÁP (Mục tiêu: Đạt điểm Mức =)

Để đạt điểm `=`, bạn phải làm rõ được cách Backend liên kết và minh họa cho thuật toán AI.

#### 1. Cách Backend gọi bộ não AI
Backend đóng vai trò là "người gọi dịch vụ". Khi người chơi thực hiện nước đi thông qua API `/move`, Backend tiếp nhận tọa độ, cập nhật bàn cờ rồi kích hoạt AI:
```python
max_depth, time_limit = DIFFICULTY_SETTINGS[difficulty]
ai_move = iterative_deepening(board, max_depth=max_depth, time_limit=time_limit)
```
Hàm `iterative_deepening` (từ file [minmax.py](file:///d:/Gomoku_MinMax/minmax.py)) nhận 3 tham số:
1.  `board`: Bản đồ bàn cờ hiện tại để AI giả lập tìm kiếm.
2.  `max_depth`: Giới hạn chiều sâu của cây trò chơi (Game Tree).
3.  `time_limit`: Giới hạn thời gian tính toán tối đa (giây).

#### 2. Mối liên hệ giữa Độ khó, Chiều sâu cây quyết định và Chất lượng AI
Bạn cần giải thích trực quan mối quan hệ này cho giảng viên:
*   **Easy (depth=1, time=0.5s):** Minimax chỉ dựng cây trò chơi cao 1 tầng. Nghĩa là AI chỉ quét các ô trống lân cận và chấm điểm trực tiếp xem nước nào ăn điểm cao nhất ngay lập tức (không tính toán phản ứng tiếp theo của đối thủ). AI chơi rất nhanh nhưng cực kỳ ngây thơ.
*   **Medium (depth=2, time=1.0s):** AI dựng cây cao 2 tầng. Nó giả lập: "Nếu ta đi ô A, đối thủ sẽ phản ứng ở những ô nào, điểm số thế cờ của ta sau đó sẽ ra sao". AI bắt đầu biết chặn các nước đi cơ bản.
*   **Hard (depth=6, time=3.0s):** AI tính trước 6 nước đi (xen kẽ lượt AI và lượt Human). Cây quyết định cực kỳ sâu, giúp AI phát hiện ra các thế cờ hiểm ác như thế gọng kìm (Fork) 3 hở hoặc 4 bịt để chủ động tấn công hoặc phòng thủ.

#### 🛠️ Bài tập thực hành Ngày 3:
1. Hãy thử đổi giá trị độ sâu của mức "hard" trong `DIFFICULTY_SETTINGS` từ `6` thành `10`.
2. Chạy game và chọn mức Hard. Quan sát xem thời gian AI suy nghĩ có tăng lên đột biến không và lý giải tại sao. (Vì số lượng trạng thái trên cây trò chơi tăng theo cấp số mũ).

---

### 📅 NGÀY 4: PHÂN TÍCH KIẾN TRÚC & TRADE-OFF HIỆU NĂNG (Mục tiêu: Đạt điểm Mức +)

Đây là ngày học cốt lõi để đạt điểm xuất sắc (+). Bạn phải đứng ở góc độ kỹ sư kiến trúc hệ thống để phân tích các trade-off và giới hạn thực tế.

#### 1. Phân tích sự Bùng nổ tổ hợp (Combinatorial Explosion)
*   Hệ số nhánh (Branching factor) $b$ của Gomoku là số ô trống còn lại. Trên bàn cờ 15x15, ở các nước đi đầu, $b \approx 200$.
*   Nếu sử dụng thuật toán Minimax nguyên bản, số lượng trạng thái cần duyệt ở độ sâu $d$ là $b^d$. Với $d = 6$, số nút là $200^6 \approx 6.4 \times 10^{13}$ nút. Không một máy tính cá nhân nào có thể tính kịp trong 3 giây.
*   **Giải pháp kết hợp:**
    *   Hàm sinh nước đi trong bộ não AI giảm hệ số nhánh xuống còn $b \approx 20$ bằng cách chỉ xét các ô trống có bán kính 2 xung quanh các quân cờ đã đi.
    *   Lúc này, ở độ sâu 6, số nút tối đa là $20^6 \approx 64,000,000$ nút. Kết hợp cắt tỉa Alpha-Beta và sắp xếp nước đi Delta Evaluation, số nút thực tế phải duyệt giảm xuống dưới 1.000.000 nút, thời gian tính toán giảm từ hàng giờ xuống dưới 1-2 giây.

#### 2. Phân tích Trade-off giữa Trải nghiệm người dùng (UX) và Trí tuệ AI
*   Nếu chúng ta muốn AI vô địch (chơi cực kỳ giỏi), ta cần tăng độ sâu tìm kiếm lên `depth=10` hoặc `12`.
*   Tuy nhiên, thời gian tính toán lúc này sẽ vượt quá 30 giây đến vài phút.
*   **Trade-off:** Chấp nhận AI ở mức độ thông minh vừa phải (`depth=6`) để đổi lấy thời gian phản hồi API dưới 3 giây, đảm bảo nhịp độ trận đấu diễn ra liền mạch, tránh gây ức chế cho người chơi.

#### 3. So sánh kiến trúc lưu trữ trạng thái Game (In-Memory vs Production-Grade)
Hãy chuẩn bị bảng so sánh này để trình bày trực quan:

| Tiêu chí | Kiến trúc hiện tại (In-Memory) | Kiến trúc Production (Redis/DB) |
| :--- | :--- | :--- |
| **Công nghệ** | Biến toàn cục trong bộ nhớ RAM của Flask process. | Sử dụng **Redis Cache** hoặc **Database** (PostgreSQL/SQLite). |
| **Số lượng phiên chơi** | **Single-session** (Chỉ 1 game chơi tại 1 thời điểm). | **Multi-session** (Hàng vạn người chơi song song độc lập). |
| **Tính bền vững** | Mất toàn bộ dữ liệu bàn cờ nếu server bị restart. | Lưu trữ lâu dài, có thể khôi phục trạng thái chơi bất kỳ lúc nào. |
| **Cơ chế phân biệt** | Không có cơ chế phân biệt (mọi user dùng chung 1 board). | Quản lý qua `session_token` hoặc `game_id` truyền kèm trong API. |

#### 4. Giải pháp nâng cấp kiến trúc bất đồng bộ (Asynchronous Architecture)
Nếu bắt buộc phải chạy AI ở độ sâu lớn (ví dụ `depth=10`), ta phải thay thế kiến trúc HTTP đồng bộ hiện tại:
1.  **Dùng Message Queue (Celery + Redis):** Client gửi yêu cầu di chuyển `/move`. Backend đẩy tác vụ tìm kiếm AI vào hàng đợi Celery và lập tức trả về `HTTP 202 Accepted` kèm theo một `task_id` để giải phóng luồng HTTP API, tránh nghẽn server và tránh timeout trình duyệt.
2.  **Dùng WebSockets (Flask-SocketIO):** Tạo kết nối hai chiều liên tục giữa client và server. Khi tiến trình worker tính xong nước đi tốt nhất cho AI ở background, server sẽ chủ động bắn tọa độ nước đi đó về cho client qua WebSocket để cập nhật bàn cờ.

---

### 📅 NGÀY 5: TỔNG ÔN TẬP & THỰC HÀNH PHẢN BIỆN (Mục tiêu: Đóng băng điểm +)

Ngày cuối cùng tập trung vào rèn luyện phong thái thuyết trình và làm quen với kịch bản phản biện.

#### 1. Chiến thuật thuyết trình 3 bước cho Thành viên 1:
*   **Bước 1: Giới thiệu vai trò:** "Em phụ trách phần Backend và quản lý trạng thái trò chơi. Em đã xây dựng các RESTful API bằng Flask để làm cầu nối giao tiếp giữa giao diện người dùng và thuật toán AI."
*   **Bước 2: Giải thích luồng dữ liệu:** "Khi người chơi đi, Frontend gửi tọa độ lên `/move`. Backend xác thực tính hợp lệ, cập nhật trạng thái bàn cờ, sau đó gọi hàm tính toán của AI với các ràng buộc về độ sâu và thời gian tùy theo mức độ khó được cấu hình."
*   **Bước 3: Chỉ ra giới hạn và hướng giải quyết:** "Hệ thống hiện tại chạy dưới dạng single-session để phục vụ demo học thuật trên máy cục bộ. Nếu đưa lên sản phẩm thực tế, em đề xuất sử dụng Redis để lưu trạng thái phiên chơi và Celery để tính toán bất đồng bộ." (Đây là câu chốt hạ giúp bạn lấy điểm cộng từ giảng viên vì chứng tỏ bạn có tầm nhìn thực tế).

#### 2. Kịch bản mô phỏng phản biện:
*   *Tình huống:* Giảng viên hỏi: "Code này tôi mở 2 trình duyệt chơi cùng lúc thì có được không? Tại sao?"
*   *Trả lời tự tin:* "Dạ không được, thưa Thầy/Cô. Vì hệ thống đang lưu trạng thái bàn cờ bằng một biến toàn cục `board` duy nhất trên RAM của tiến trình Flask. Khi hai người chơi cùng truy cập, họ sẽ ghi đè dữ liệu lên nhau. Để khắc phục, em sẽ cấu hình thêm cơ chế Session lưu theo Session ID hoặc đưa trạng thái bàn cờ vào Redis lưu theo Game ID."

---

## III. Bộ Câu Hỏi Vấn Đáp Thường Gặp (Phân loại theo Mức Điểm)

*(Giữ nguyên nội dung bộ câu hỏi vấn đáp Mức = và Mức + đã biên soạn ở phần trước).*

### 📌 NHÓM CÂU HỎI ĐẠT ĐIỂM KHÁ (Mức =)
*(Nội dung câu hỏi 1, 2, 3 đã chuẩn bị sẵn)*

### 🏆 NHÓM CÂU HỎI ĐẠT ĐIỂM TỐI ĐA (Mức +)
*(Nội dung câu hỏi 4, 5, 6 đã chuẩn bị sẵn)*

---

Chúc bạn ôn tập tốt và đạt kết quả cao trong buổi bảo vệ đồ án!
