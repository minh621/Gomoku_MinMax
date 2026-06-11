# Hướng Dẫn Học Tập & Vấn Đáp: Thành viên 1 - Kiến trúc Backend & Game State

Tài liệu này được biên soạn dành riêng cho **Thành viên 1** để chuẩn bị cho buổi bảo vệ đồ án Gomoku AI. Nội dung tập trung giải thích chi tiết hoạt động của file [app.py](file:///d:/Gomoku_MinMax/app.py), thiết lập lộ trình học tập khoa học và chuẩn bị bộ câu hỏi vấn đáp chuyên sâu.

---

## I. Giải Thích Chi Tiết Phần Việc (app.py)

File [app.py](file:///d:/Gomoku_MinMax/app.py) đóng vai trò là **trung tâm điều khiển (Controller)** của toàn bộ hệ thống. Nhiệm vụ chính của nó bao gồm:
1. **Thiết lập server:** Chạy một HTTP web server bằng Flask framework.
2. **Quản lý Game State (Trạng thái trò chơi):** Lưu giữ bàn cờ, lượt đi, lịch sử nước đi và trạng thái kết thúc game trên bộ nhớ RAM của server.
3. **Cung cấp RESTful API:** Nhận các yêu cầu từ giao diện người dùng (Frontend) dưới dạng JSON, xử lý và phản hồi kết quả bàn cờ mới dưới dạng JSON.
4. **Tích hợp bộ não AI:** Gọi thuật toán `iterative_deepening` từ module `minmax` khi cần AI tính nước đi.

### 1. Quản lý trạng thái (Game State Variables)
Ở phần đầu của `app.py`, trạng thái trò chơi được định nghĩa thông qua các biến toàn cục:
* `board`: Một mảng hai chiều kích thước 15x15 (`BOARD_SIZE = 15`). Mỗi ô nhận một trong các giá trị: `EMPTY` (0), `HUMAN` (1 - quân O), hoặc `AI` (2 - quân X).
* `game_over`: Biến Boolean (`True` / `False`) để chặn các nước đi khi trận đấu đã phân định thắng thua hoặc hòa.
* `current_turn`: Biến xác định lượt đi hiện tại (`HUMAN` hoặc `AI`).
* `move_history`: Mảng danh sách các tuple `(x, y, player)` dùng để lưu thứ tự nước đi, phục vụ cho chức năng **Hoàn tác (Undo)**.
* `difficulty` & `DIFFICULTY_SETTINGS`: Lưu cấu hình độ khó. Mỗi độ khó sẽ tương ứng với các tham số giới hạn tìm kiếm của AI:
  * **Easy:** Tìm kiếm tối đa độ sâu 1 tầng (`depth=1`), giới hạn thời gian phản hồi `0.5s`.
  * **Medium:** Tìm kiếm tối đa độ sâu 2 tầng (`depth=2`), giới hạn thời gian phản hồi `1.0s`.
  * **Hard:** Tìm kiếm tối đa độ sâu 6 tầng (`depth=6`), giới hạn thời gian phản hồi `3.0s`.

### 2. Chi tiết các API Endpoint (Routes)

#### 🚀 2.1 Route `/start` (POST) - Khởi tạo game mới
* **Mục đích:** Khởi động lại bàn cờ và cấu hình các cài đặt ban đầu (người đi trước, độ khó).
* **Luồng xử lý:**
  1. Nhận dữ liệu JSON gồm `first` ("human" hoặc "ai") và `difficulty` ("easy", "medium", "hard").
  2. Validate dữ liệu đầu vào. Nếu dữ liệu không hợp lệ, trả về HTTP status code `400 (Bad Request)`.
  3. Reset các biến trạng thái: `board` trống, `game_over = False`, `move_history = []`.
  4. **Trường hợp AI đi trước:** Gọi ngay bộ não AI (`iterative_deepening`) để tính nước đi đầu tiên. Đánh dấu nước đi đó lên `board`, lưu vào lịch sử, và chuyển lượt cho `HUMAN`.
  5. Trả về trạng thái `board` mới và tọa độ nước đi của AI `ai_move` (nếu có).

#### 🎯 2.2 Route `/move` (POST) - Thực hiện nước đi
* **Mục đích:** Xử lý nước đi của người chơi và kích hoạt nước đi phản công của AI.
* **Luồng xử lý:**
  1. Kiểm tra nếu `game_over == True` thì từ chối xử lý, trả về lỗi.
  2. Lấy tọa độ `x`, `y` từ request JSON của người chơi.
  3. **Kiểm tra tính hợp lệ (Validation):** Tọa độ phải nằm trong khoảng từ `0` đến `14` và ô cờ đó phải đang trống (`EMPTY`). Nếu không hợp lệ, trả về trạng thái bàn cờ hiện tại mà không thực hiện gì.
  4. **Xử lý nước đi của Human:**
     * Gán `board[x][y] = HUMAN`.
     * Lưu vào `move_history`.
     * Gọi hàm `check_winner(board, HUMAN)`. Nếu người chơi thắng, gán `game_over = True` và trả về JSON báo người chơi thắng cùng bàn cờ.
     * Kiểm tra điều kiện hòa (nếu toàn bộ 225 ô cờ đều đã được lấp đầy quân). Nếu hòa, gán `game_over = True` và trả về kết quả hòa.
  5. **Xử lý nước đi của AI (nếu game chưa kết thúc):**
     * Lấy cấu hình `depth` và `time_limit` tương ứng với mức độ khó.
     * Gọi hàm `iterative_deepening(board, depth, time_limit)` để tìm nước đi tốt nhất cho AI.
     * Đặt quân AI lên bàn cờ và lưu lịch sử.
     * Kiểm tra xem AI đã thắng chưa qua hàm `check_winner(board, AI)`. Nếu AI thắng, gán `game_over = True`.
  6. Trả về trạng thái bàn cờ mới và tọa độ nước đi của AI.

#### ⏪ 2.3 Route `/undo` (POST) - Hoàn tác nước đi
* **Mục đích:** Cho phép người chơi rút lại nước đi vừa thực hiện.
* **Luồng xử lý:**
  1. Nếu game đang ở trạng thái `game_over`, reset lại thành `False` để người dùng có thể tiếp tục chơi sau khi hoàn tác.
  2. Kiểm tra `move_history`. Vì đây là game chơi với AI, một lần nhấn "Undo" của người dùng cần rút lại **cả nước đi của AI lẫn nước đi của người chơi** (tổng cộng 2 nước đi gần nhất).
  3. **Thu hồi nước đi của AI:** Kiểm tra nếu nước đi cuối cùng trong lịch sử là của `AI`, ta pop khỏi `move_history` và gán lại ô đó thành `EMPTY`.
  4. **Thu hồi nước đi của Human:** Kiểm tra nếu nước đi cuối cùng tiếp theo là của `HUMAN`, ta tiếp tục pop khỏi lịch sử và gán lại ô đó thành `EMPTY`.
  5. Trả về bàn cờ đã cập nhật và số lượng nước đi đã hoàn tác (`undone` thường là 2).

#### 🔄 2.4 Route `/reset` (POST) - Reset bàn cờ nhanh
* **Mục đích:** Xóa bàn cờ về trạng thái trống mà không thay đổi cấu hình lượt đi hay độ khó từ `/start`.

---

## II. Kế Hoạch Học Tập Chi Tiết (5 Ngày)

Để nắm bắt kiến thức một cách khoa học, hiệu quả và không bị quá tải, bạn hãy chia quá trình chuẩn bị làm 5 ngày:

```mermaid
gantt
    title Kế hoạch học tập cho Thành viên 1
    dateFormat  YYYY-MM-DD
    section Học tập lý thuyết & thực hành
    Ngày 1: Tìm hiểu Flask & REST API           :active, day1, 2026-06-11, 1d
    Ngày 2: Quản lý Game State & Biến Global     :day2, after day1, 1d
    Ngày 3: Tích hợp AI Engine & Kết nối Module :day3, after day2, 1d
    Ngày 4: Xử lý Logic Hoàn tác (Undo)         :day4, after day3, 1d
    Ngày 5: Ôn luyện Vấn đáp & Mô phỏng bảo vệ   :day5, after day4, 1d
```

### 📅 Ngày 1: Nền tảng Flask Framework & REST API
* **Mục tiêu:** Hiểu cách Flask khởi chạy server và cách giao tiếp giữa Client (Trình duyệt) với Server qua giao thức HTTP JSON.
* **Nội dung cần học:**
  * Flask route hoạt động thế nào? (`@app.route("/", methods=["POST"])`).
  * Làm thế nào để lấy dữ liệu JSON gửi lên từ JS Frontend? (`request.json` hoặc `request.get_json()`).
  * Trả dữ liệu JSON về cho Frontend bằng cách nào? (`jsonify(...)`).
  * HTTP Status Code cơ bản: `200 OK` và `400 Bad Request` dùng khi nào trong code?
* **Thực hành tự kiểm tra:** 
  * Hãy mở terminal, chạy lệnh `python app.py` để khởi động server.
  * Thử mở trình duyệt vào địa chỉ `http://127.0.0.1:5000/` để xem giao diện web có tải thành công không.

### 📅 Ngày 2: Cơ chế quản lý Game State & Mảng hai chiều
* **Mục tiêu:** Hiểu sâu về cách lưu trữ trạng thái bàn cờ Gomoku và cách Python xử lý biến toàn cục (`global`).
* **Nội dung cần học:**
  * Tại sao bàn cờ lại được khai báo là danh sách lồng nhau (List Comprehension): `[[EMPTY for _ in range(15)] for _ in range(15)]`?
  * Ý nghĩa của từ khóa `global` trong các hàm của Python (Ví dụ: `global board, game_over`). Nếu không dùng từ khóa này khi gán giá trị mới cho biến thì chuyện gì sẽ xảy ra? (Python sẽ coi đó là biến cục bộ mới và sinh lỗi hoặc không cập nhật trạng thái chung).
  * Cách truy cập tọa độ hàng/cột: `board[x][y]` đại diện cho dòng `x`, cột `y`.
* **Thực hành tự kiểm tra:**
  * Nhìn vào hàm `move()` và giải thích cách tọa độ `x`, `y` được lấy từ request và kiểm tra điều kiện ngoài biên (`0 <= x < 15`).

### 📅 Ngày 3: Tương tác giữa API Controller với AI Engine (`minmax.py`)
* **Mục tiêu:** Nắm được cách Backend kết nối và chuyển tiếp dữ liệu đến thuật toán tìm kiếm AI.
* **Nội dung cần học:**
  * Đọc hiểu dòng import: `from minmax import iterative_deepening, BOARD_SIZE, EMPTY, AI, HUMAN, check_winner`.
  * Hiểu cách hàm `iterative_deepening(board, max_depth, time_limit)` được gọi trong `/start` và `/move`. Nhận thức được rằng Thành viên 1 truyền trạng thái `board` hiện tại sang cho AI, AI tính toán xong trả về một tuple tọa độ `(ai_x, ai_y)` hoặc `None`.
  * Xem cấu trúc `DIFFICULTY_SETTINGS`. Giải thích sự khác biệt giữa các độ khó về mặt độ sâu tính toán (`max_depth`) và giới hạn thời gian (`time_limit`).
* **Thực hành tự kiểm tra:**
  * Tại sao khi AI đi trước trong `/start`, ta lại gọi `iterative_deepening` ngay lập tức?

### 📅 Ngày 4: Giải thuật Hoàn tác (Undo) & Các trường hợp biên (Corner Cases)
* **Mục tiêu:** Hiểu cơ chế hoạt động của lịch sử nước đi (`move_history`) và các kịch bản biên trong game.
* **Nội dung cần học:**
  * Cấu trúc ngăn xếp (Stack) của `move_history`: Phần tử được thêm vào cuối bằng `.append()` và lấy ra từ cuối bằng `.pop()`.
  * Tại sao hàm `undo()` lại thực hiện lệnh `.pop()` tối đa 2 lần? (Để xóa cả nước đi của AI lẫn người chơi, đảm bảo game quay về đúng lượt của người chơi).
  * Làm thế nào để khôi phục trạng thái `game_over` về `False` khi người dùng nhấn Undo ở cuối trận đấu?
  * Trường hợp biên: Nếu bàn cờ trống không có nước đi nào (`not move_history`), hàm xử lý thế nào để không bị lỗi ứng dụng?
* **Thực hành tự kiểm tra:**
  * Tự vẽ sơ đồ các bước đi của mảng `move_history` khi: Người đi ô (0,0) → AI đi ô (1,1) → Người nhấn Undo. Mảng thay đổi thế nào?

### 📅 Ngày 5: Tổng ôn tập & Thử nghiệm mô phỏng bảo vệ
* **Mục tiêu:** Rèn luyện phản xạ thuyết trình và trả lời các câu hỏi từ hội đồng giảng viên.
* **Nội dung cần học:**
  * Đọc kỹ bộ câu hỏi vấn đáp dưới đây.
  * Tự thực hành giải thích code bằng lời nói tiếng Việt mạch lạc, rõ ràng.
  * Luyện tập phong thái tự tin, điềm tĩnh khi trả lời các điểm yếu trong kiến trúc hiện tại của dự án.

---

## III. Bộ Câu Hỏi Vấn Đáp Thường Gặp (Chuyên biệt cho Thành viên 1)

Dưới đây là các câu hỏi giảng viên rất dễ đặt ra cho thành viên phụ trách phần Backend & Game State, đi kèm gợi ý trả lời chuẩn xác nhất:

### ❓ Câu 1: Em hãy giải thích từ khóa `global` được sử dụng trong các route như `/start`, `/move` có tác dụng gì? Nếu không dùng có sao không?
* **Trả lời:**
  * Trong Python, khi một biến được khai báo ở ngoài hàm, nó là biến toàn cục. Tuy nhiên, nếu trong hàm chúng ta muốn thay đổi giá trị của biến đó (ví dụ gán lại bàn cờ mới `board = ...` hoặc gán lại trạng thái `game_over = False`), Python mặc định sẽ coi đó là việc tạo một biến cục bộ mới trùng tên trong hàm, dẫn đến biến toàn cục bên ngoài không hề bị thay đổi.
  * Việc sử dụng từ khóa `global` (ví dụ: `global board, game_over`) nhằm thông báo cho Python biết rằng chúng ta đang muốn thao tác và thay đổi giá trị của chính các biến toàn cục đã khai báo ở đầu file.
  * Nếu không dùng từ khóa này khi gán giá trị mới, hệ thống sẽ gặp lỗi logic (trạng thái game không được cập nhật trên diện rộng) hoặc lỗi biên dịch `UnboundLocalError`.

### ❓ Câu 2: Biến toàn cục (`board`, `game_over`,...) lưu trạng thái game hiện tại nằm ở đâu? Thiết kế này có nhược điểm gì khi ứng dụng có nhiều người chơi cùng lúc?
* **Trả lời:**
  * Hiện tại, trạng thái trò chơi được lưu trực tiếp trên **bộ nhớ RAM** của server dưới dạng các biến toàn cục của tiến trình Python Flask.
  * **Nhược điểm chí mạng:** Thiết kế này chỉ hỗ trợ duy nhất **1 phiên chơi (single-session)** tại một thời điểm. Nếu có 2 người dùng truy cập web từ 2 máy tính khác nhau (hoặc 2 tab trình duyệt khác nhau) và chơi cùng lúc, họ sẽ chơi chung trên cùng một bàn cờ, nước đi của người này sẽ ghi đè hoặc can thiệp vào bàn cờ của người kia (gây ra hiện tượng Race Condition / trùng lặp trạng thái).
  * **Cách khắc phục:** Để hỗ trợ đa người chơi (multi-session), chúng ta cần:
    1. Sử dụng cơ chế **Session** (ví dụ: `flask.session`) để lưu trạng thái riêng biệt cho từng client thông qua cookie.
    2. Hoặc lưu trạng thái trận đấu vào một **cơ sở dữ liệu** (như SQLite, MySQL hoặc Redis) với mỗi trận đấu có một `game_id` riêng biệt, giao diện Frontend sẽ truyền kèm `game_id` trong mỗi request API để xác định đúng bàn cờ cần cập nhật.

### ❓ Câu 3: Hãy giải thích cách em cài đặt và kiểm soát các mức độ khó "Dễ", "Trung bình", "Khó" trên Backend?
* **Trả lời:**
  * Cấu hình độ khó được lưu trữ trong từ điển `DIFFICULTY_SETTINGS` ở dòng 15 trong `app.py`.
  * Mỗi mức độ khó được định nghĩa bởi một tuple `(max_depth, time_limit)`:
    * Mức **Dễ (Easy):** `max_depth = 1`, `time_limit = 0.5` giây. AI chỉ duyệt trước 1 nước và phản hồi cực nhanh.
    * Mức **Trung bình (Medium):** `max_depth = 2`, `time_limit = 1.0` giây. AI suy nghĩ sâu hơn một chút.
    * Mức **Khó (Hard):** `max_depth = 6`, `time_limit = 3.0` giây. AI được phép duyệt cây tìm kiếm sâu đến 6 tầng và có tới tối đa 3 giây để tìm nước đi tối ưu nhất.
  * Khi client gọi route `/start`, độ khó được lưu lại vào biến toàn cục `difficulty`. Khi người dùng thực hiện nước đi tại route `/move`, backend sẽ lấy các thông số `max_depth` và `time_limit` tương ứng từ `DIFFICULTY_SETTINGS` để truyền vào hàm tính toán AI `iterative_deepening(board, max_depth, time_limit)`.

### ❓ Câu 4: Trong route `/move`, tại sao sau khi nhận nước đi của người chơi, em lại phải gọi hàm `check_winner` trước khi gọi bộ não AI?
* **Trả lời:**
  * Chúng ta cần kiểm tra xem nước đi vừa rồi của người chơi có giúp họ giành chiến thắng hay không.
  * Nếu người chơi đã thắng (`check_winner(board, HUMAN) == True`), trò chơi lập tức kết thúc. Chúng ta cần gán `game_over = True` và trả về kết quả thắng cuộc cho Frontend ngay lập tức mà không được phép gọi thuật toán AI chạy nữa (vì game đã dừng, AI không có quyền đi tiếp).
  * Việc kiểm tra này vừa đảm bảo tính đúng đắn của luật chơi, vừa tránh lãng phí tài nguyên CPU của server khi phải chạy thuật toán tìm kiếm AI vô nghĩa.

### ❓ Câu 5: Hãy giải thích thuật toán hoàn tác (`undo`) hoạt động như thế nào? Tại sao lại phải dùng hàm `pop()` của danh sách?
* **Trả lời:**
  * Lịch sử tất cả các nước đi được lưu trong mảng `move_history` theo dạng ngăn xếp (nước đi nào đi sau sẽ được thêm vào cuối danh sách).
  * Khi người dùng nhấn nút Hoàn tác, chúng ta muốn xóa các nước đi gần nhất. Phương thức `.pop()` của danh sách Python giúp lấy ra và loại bỏ phần tử cuối cùng của danh sách đó.
  * Đầu tiên, chúng ta kiểm tra phần tử cuối cùng của `move_history`. Nếu đó là nước đi của AI (`player == AI`), ta gọi `move_history.pop()` và đặt lại giá trị ô cờ đó trên bàn cờ thành trống (`EMPTY`).
  * Tiếp tục kiểm tra phần tử tiếp theo ở cuối danh sách. Nếu đó là nước đi của người chơi (`player == HUMAN`), ta tiếp tục gọi `move_history.pop()` và đặt lại ô cờ đó thành trống (`EMPTY`).
  * Việc pop 2 lần liên tiếp giúp đưa trạng thái bàn cờ quay ngược lại đúng thời điểm trước khi người chơi thực hiện nước đi cuối cùng của họ.

### ❓ Câu 6: Làm thế nào để Backend phát hiện và xử lý trường hợp bàn cờ bị hòa (hết ô trống)?
* **Trả lời:**
  * Trong route `/move`, sau khi người chơi đi và không thắng, Backend kiểm tra điều kiện bàn cờ đầy bằng biểu thức Generator:
    `all(board[i][j] != EMPTY for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))`
  * Biểu thức này sẽ duyệt qua tất cả các ô trên bàn cờ 15x15. Nếu không còn bất kỳ ô nào có giá trị `EMPTY` (tất cả các ô đều đã chứa quân `HUMAN` hoặc `AI`), hàm `all()` sẽ trả về `True`.
  * Khi đó, Backend ghi nhận trạng thái hòa bằng cách gán `game_over = True` và trả về JSON có `"winner": "draw"` để Frontend hiển thị thông báo hòa cờ.

---

Chúc bạn ôn tập tốt và đạt kết quả cao trong buổi bảo vệ đồ án!
