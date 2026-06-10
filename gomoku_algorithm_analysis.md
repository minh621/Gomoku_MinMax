# Phân Tích Thuật Toán - Dự Án Gomoku AI (Cờ Caro Trí Tuệ Nhân Tạo)

---

## Mục Lục

1. [Tổng Quan Dự Án](#i-tổng-quan-dự-án)
2. [Thống Kê & Giải Thích Đầy Đủ Các Thuật Toán](#ii-thống-kê--giải-thích-đầy-đủ-các-thuật-toán)
3. [Xếp Hạng Độ Khó (Dễ → Khó)](#iii-xếp-hạng-độ-khó-dễ--khó)
4. [Phân Chia Công Việc Cho 6 Người](#iv-phân-chia-công-việc-cho-6-người)
5. [Góc Nhìn Giảng Viên – Các Điểm Cần Phân Tích Sâu & Câu Hỏi Vấn Đáp](#v-góc-nhìn-giảng-viên--các-điểm-cần-phân-tích-sâu--câu-hỏi-vấn-đáp)

---

## I. Tổng Quan Dự Án

**Gomoku AI** là ứng dụng web chơi cờ Caro (Gomoku) trên bàn cờ 15×15, tích hợp trí tuệ nhân tạo (AI) sử dụng thuật toán **Minimax** kết hợp **Alpha-Beta Pruning** và **Iterative Deepening**.

**Kiến trúc tổng thể:**

```
┌─────────────────┐        HTTP/JSON        ┌──────────────────────────┐
│   Frontend      │  ◄─────────────────►    │     Backend (Flask)      │
│   (HTML/JS/CSS) │                         │       app.py             │
│   game.js       │                         │          │               │
└─────────────────┘                         │          ▼               │
                                            │   ┌──────────────┐      │
                                            │   │  minmax.py   │      │
                                            │   │  (AI Core)   │      │
                                            │   └──────────────┘      │
                                            └──────────────────────────┘
```

**Danh sách các file mã nguồn chính:**

| File | Dòng code | Vai trò |
| :--- | :---: | :--- |
| [minmax.py](file:///d:/Gomoku_MinMax/minmax.py) | 380 | Bộ não AI: chứa toàn bộ thuật toán cốt lõi |
| [app.py](file:///d:/Gomoku_MinMax/app.py) | 150 | Backend server Flask, quản lý trạng thái game |
| [game.js](file:///d:/Gomoku_MinMax/static/js/game.js) | 280 | Frontend logic, tương tác UI bàn cờ |

---

## II. Thống Kê & Giải Thích Đầy Đủ Các Thuật Toán

### Thuật toán 1: Kiểm tra điều kiện thắng (Check Winner)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 14–34](file:///d:/Gomoku_MinMax/minmax.py#L14-L34) |
| **Hàm** | `check_winner(board, player)` |
| **Độ khó** | ⭐ Dễ |

**Mô tả:** Quét toàn bộ bàn cờ 15×15 theo 4 hướng (ngang, dọc, chéo chính, chéo phụ). Tại mỗi ô, kiểm tra liệu có đúng **5 quân liên tiếp** cùng màu hay không.

**Thuật toán cốt lõi:** Brute-force scan với vòng lặp ba tầng:
- Tầng 1: Duyệt tất cả 225 ô (15×15).
- Tầng 2: Tại mỗi ô, duyệt 4 hướng `[(1,0), (0,1), (1,1), (1,-1)]`.
- Tầng 3: Kiểm tra 5 ô liên tiếp theo hướng đó.

**Độ phức tạp:** O(N² × 4 × 5) = O(N²) với N = 15 → tối đa 4.500 phép kiểm tra.

---

### Thuật toán 2: Đếm mẫu chuỗi con (Pattern Counting)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 247–257](file:///d:/Gomoku_MinMax/minmax.py#L247-L257) |
| **Hàm** | `_count_pattern(s, pattern)` |
| **Độ khó** | ⭐ Dễ |

**Mô tả:** Đếm số lần một chuỗi mẫu (pattern) xuất hiện trong chuỗi `s` bằng thuật toán tìm kiếm tuần tự (Sequential Search). Cho phép các lần xuất hiện **chồng lấp (overlapping)** vì con trỏ `start` chỉ tăng 1 sau mỗi lần tìm thấy.

**Ví dụ:** `_count_pattern("_XXX_XXX_", "_XXX_")` → trả về 2.

**Vai trò:** Là hàm nền tảng phục vụ cho hàm đánh giá thế cờ (`_evaluate_line`), đếm số lần xuất hiện các pattern đe dọa (3 hở, 4 bịt, ...) trên mỗi đường thẳng.

---

### Thuật toán 3: Trích xuất tất cả đường thẳng trên bàn cờ (Line Extraction)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 203–244](file:///d:/Gomoku_MinMax/minmax.py#L203-L244) |
| **Hàm** | `_extract_all_lines(board)` |
| **Độ khó** | ⭐⭐ Trung bình – Dễ |

**Mô tả:** Trích xuất tất cả các "đường thẳng" (lines) trên bàn cờ theo 4 hướng:
1. **15 hàng ngang** (mỗi hàng 15 ô).
2. **15 cột dọc** (mỗi cột 15 ô).
3. **29 đường chéo chính** (top-left → bottom-right), chỉ giữ đường ≥ 5 ô.
4. **29 đường chéo phụ** (top-right → bottom-left), chỉ giữ đường ≥ 5 ô.

**Tổng số đường:** 15 + 15 + ~21 + ~21 = khoảng **72 đường thẳng**.

**Vai trò:** Cung cấp đầu vào cho hàm `evaluate()`. Mỗi đường thẳng chỉ được trích **đúng 1 lần** để tránh đếm trùng pattern (rất quan trọng cho tính chính xác của hàm đánh giá).

---

### Thuật toán 4: Phát hiện chuỗi nguy hiểm (Danger Detection)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 39–61](file:///d:/Gomoku_MinMax/minmax.py#L39-L61) |
| **Hàm** | `is_dangerous(board, i, j)` |
| **Độ khó** | ⭐⭐ Trung bình – Dễ |

**Mô tả:** Kiểm tra xem ô `(i, j)` (đã có quân) có nằm trong một chuỗi **≥ 2 quân liên tiếp** cùng màu theo bất kỳ hướng nào hay không. Thuật toán đếm từ ô trung tâm ra 2 phía (tiến và lùi theo mỗi hướng, tối đa 3 bước mỗi phía).

**Vai trò:** Phục vụ cho hàm `get_possible_moves()`. Các ô lân cận khu vực "nguy hiểm" sẽ được ưu tiên xét trước (must-block moves), giúp AI phản ứng nhanh với các đe dọa.

---

### Thuật toán 5: Sinh nước đi ứng viên (Move Generation)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 64–92](file:///d:/Gomoku_MinMax/minmax.py#L64-L92) |
| **Hàm** | `get_possible_moves(board)` |
| **Độ khó** | ⭐⭐ Trung bình |

**Mô tả:** Thay vì xét tất cả 225 ô trống (rất lãng phí), thuật toán chỉ **sinh các nước đi nằm trong bán kính 2 ô** xung quanh các quân cờ đã đặt. Đây là kỹ thuật **Neighborhood-based Move Generation** phổ biến trong game AI.

**Cơ chế ưu tiên:**
- **`must_block`**: Các ô nằm gần chuỗi nguy hiểm (≥ 2 quân liên tiếp) → Ưu tiên cao.
- **`normal`**: Các ô lân cận quân cờ bình thường → Ưu tiên thấp hơn.

**Kết quả:** Danh sách ứng viên `combined = must_block + normal`, thường chỉ khoảng **20–60 nước** thay vì 225.

---

### Thuật toán 6: Đánh giá thế cờ theo dòng (Line Evaluation / Heuristic Scoring)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 142–200](file:///d:/Gomoku_MinMax/minmax.py#L142-L200) |
| **Hàm** | `_evaluate_line(line)` |
| **Bảng điểm** | Dòng 150–170 |
| **Độ khó** | ⭐⭐⭐ Trung bình |

**Mô tả:** Đây là **hàm heuristic cốt lõi** của AI. Mỗi dòng (line) trên bàn cờ được chuyển thành chuỗi ký tự (`X` = AI, `O` = Human, `_` = trống), sau đó đếm số lần xuất hiện của các **mẫu đe dọa (threat patterns)** và nhân với trọng số tương ứng.

**Bảng pattern và trọng số:**

| Pattern | Ý nghĩa | Điểm AI (Tấn công) | Điểm Human (Phòng thủ) |
| :--- | :--- | ---: | ---: |
| `XXXXX` / `OOOOO` | 5 liên tiếp (Thắng) | +10.000.000 | −10.000.000 |
| `_XXXX_` / `_OOOO_` | 4 hở 2 đầu | +1.000.000 | −2.000.000 |
| `XXXX_` / `OOOO_` | 4 bịt 1 đầu | +80.000 | −1.500.000 |
| `XX_XX` / `OO_OO` | 4 gãy (broken 4) | +80.000 | −1.500.000 |
| `_XXX_` / `_OOO_` | 3 hở 2 đầu | +30.000 | −60.000 |
| `_XX_X_` / `_OO_O_` | 3 gãy (broken 3) | +25.000 | −55.000 |
| `_XX_` / `_OO_` | 2 hở | +500 | −400 |

**Chiến lược scoring đặc biệt:**
- **Phòng thủ > Tấn công ở cấp 4**: `_HU_HALF_4 = 1.500.000` > `_AI_OPEN_4 = 1.000.000`. Điều này buộc AI **chặn đe dọa 4 quân của đối thủ** trước khi tự tạo chuỗi 4 hở.
- **Tấn công > Phòng thủ ở cấp 2–3 thấp**: AI chủ động tạo thế khi không bị đe dọa trực tiếp.

---

### Thuật toán 7: Hàm đánh giá toàn cục (Global Board Evaluation)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 260–292](file:///d:/Gomoku_MinMax/minmax.py#L260-L292) |
| **Hàm** | `evaluate(board)` |
| **Độ khó** | ⭐⭐⭐ Trung bình |

**Mô tả:** Đánh giá tổng thể trạng thái toàn bàn cờ, bao gồm 3 thành phần:

1. **Pattern scoring:** Gọi `_evaluate_line()` trên tất cả ~72 đường thẳng (qua `_extract_all_lines()`).

2. **Fork detection (Phát hiện thế gọng kìm):** Đếm số đường đe dọa cấp cao (4 quân hoặc 3 hở). Nếu một bên có **≥ 2 đường đe dọa đồng thời** → cộng/trừ bonus lớn (`100.000 + count × 30.000`). Đây là kỹ thuật nhận diện **Double Threat / Fork** — thế cờ gần như không thể chặn.

3. **Center bonus (Thưởng vị trí trung tâm):** Quân nằm gần tâm bàn cờ (ô 7,7) được cộng thêm điểm theo công thức `max(0, 14 − manhattan_distance) × 5`. Đây là heuristic phổ biến trong cờ Caro: quân ở trung tâm có nhiều hướng mở rộng hơn quân ở góc/biên.

---

### Thuật toán 8: Sắp xếp nước đi (Move Ordering)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 96–139](file:///d:/Gomoku_MinMax/minmax.py#L96-L139) |
| **Hàm** | `score_move_quick(board, move, player)` |
| **Độ khó** | ⭐⭐⭐⭐ Khó |

**Mô tả:** Kỹ thuật **Move Ordering** là yếu tố quyết định hiệu quả của Alpha-Beta Pruning. Trước khi đệ quy sâu, thuật toán đánh giá nhanh (lightweight evaluation) từng nước đi bằng phương pháp **Delta Evaluation (đánh giá chênh lệch cục bộ)**:

1. Tính điểm **trước khi đặt quân** (`score_before`) bằng cách quét 4 đường thẳng đi qua ô đó (mỗi đường lấy 11 ô: từ `k = -5` đến `k = +5`).
2. **Đặt quân giả lập** vào ô đó.
3. Tính điểm **sau khi đặt quân** (`score_after`) bằng cách quét lại 4 đường thẳng đó.
4. Tính `diff = score_after − score_before`.
5. **Hoàn tác** quân (đặt lại `EMPTY`).

**Ý nghĩa `diff`:**
- `diff > 0` (lớn): Nước đi tốt cho AI (tạo pattern tấn công hoặc phá pattern đối thủ).
- `diff < 0` (nhỏ): Nước đi tốt cho Human.

**Sắp xếp trong minimax:**
- Lượt AI (maximize): `moves.sort(reverse=True)` — nước có diff lớn nhất lên đầu.
- Lượt Human (minimize): `moves.sort(reverse=False)` — nước có diff nhỏ nhất lên đầu.

---

### Thuật toán 9: Minimax với Alpha-Beta Pruning

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 300–361](file:///d:/Gomoku_MinMax/minmax.py#L300-L361) |
| **Hàm** | `minimax(board, depth, alpha, beta, maximizing, start_time, time_limit)` |
| **Độ khó** | ⭐⭐⭐⭐⭐ Rất Khó (Thuật toán trọng tâm) |

**Mô tả:** Đây là thuật toán **cốt lõi nhất** của toàn bộ dự án. Minimax là thuật toán tìm kiếm đối kháng (Adversarial Search) trong lý thuyết trò chơi, được tối ưu bởi kỹ thuật **Alpha-Beta Pruning**.

**Nguyên lý Minimax:**
- Xây dựng **cây trò chơi (Game Tree)** với 2 loại nút xen kẽ:
  - **Maximizing node (AI):** Chọn nước đi có giá trị **cao nhất**.
  - **Minimizing node (Human):** Chọn nước đi có giá trị **thấp nhất**.
- Tại lá cây (depth = 0 hoặc thắng/thua), trả về giá trị `evaluate(board)`.

**Alpha-Beta Pruning:**
- `alpha`: Giá trị **tốt nhất** mà Maximizer (AI) đã đảm bảo được.
- `beta`: Giá trị **tốt nhất** mà Minimizer (Human) đã đảm bảo được.
- **Cắt tỉa:** Khi `beta <= alpha`, không cần xét các nhánh còn lại vì chúng **không thể ảnh hưởng** đến quyết định cuối cùng. Trong trường hợp lý tưởng (move ordering hoàn hảo), Alpha-Beta giảm số nút xét từ O(b^d) xuống **O(b^(d/2))**, tức gấp đôi độ sâu tìm kiếm.

**Các kỹ thuật tối ưu bổ sung trong cài đặt:**
1. **Depth-adjusted win score:** `WIN_SCORE + depth * 1000` — Ưu tiên thắng nhanh hơn (thắng ở depth sâu hơn có giá trị cao hơn vì depth lớn = gần gốc hơn).
2. **Move pruning:** Cắt gọt chỉ giữ **20 nước đi tốt nhất** (`moves = moves[:20]`) sau khi sắp xếp, giảm branching factor đáng kể.
3. **Timeout check:** Kiểm tra hết thời gian tại mỗi node, ném `TimeoutException` để thoát sớm.

---

### Thuật toán 10: Iterative Deepening (Tìm kiếm sâu dần)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **File** | [minmax.py — dòng 364–380](file:///d:/Gomoku_MinMax/minmax.py#L364-L380) |
| **Hàm** | `iterative_deepening(board, max_depth, time_limit)` |
| **Độ khó** | ⭐⭐⭐⭐ Khó |

**Mô tả:** Thay vì gọi Minimax trực tiếp ở độ sâu tối đa (có thể mất rất lâu hoặc không kịp giới hạn thời gian), Iterative Deepening chạy Minimax **lặp đi lặp lại** với depth tăng dần: 1, 2, 3, ..., `max_depth`.

**Cơ chế hoạt động:**
```
depth = 1 -> Minimax(depth=1) -> lưu best_move_1
depth = 2 -> Minimax(depth=2) -> lưu best_move_2 (tốt hơn)
depth = 3 -> Minimax(depth=3) -> hết thời gian giữa chừng!
-> Trả về best_move_2 (kết quả tốt nhất hoàn chỉnh)
```

**Ưu điểm:**
1. **Anytime Algorithm:** Luôn có kết quả hợp lệ bất kỳ lúc nào bị dừng.
2. **Tận dụng tối đa thời gian:** AI suy nghĩ sâu nhất có thể trong giới hạn thời gian (Easy: 0.5s, Medium: 1s, Hard: 3s).
3. **Không lãng phí:** Dù chạy nhiều lần, tổng số node xét thực tế chỉ lớn hơn ~11% so với chạy 1 lần ở depth cuối cùng (do tính chất hàm mũ).

---

## III. Xếp Hạng Độ Khó (Dễ → Khó)

| Hạng | Thuật toán | Độ khó | Lý do |
| :---: | :--- | :---: | :--- |
| 1 | Check Winner (Kiểm tra thắng) | ⭐ | Vòng lặp đơn giản, dễ hiểu |
| 2 | Pattern Counting (Đếm mẫu) | ⭐ | Tìm kiếm chuỗi con cơ bản |
| 3 | Line Extraction (Trích xuất đường) | ⭐⭐ | Xử lý toạ độ đường chéo hơi phức tạp |
| 4 | Danger Detection (Phát hiện nguy hiểm) | ⭐⭐ | Quét 2 chiều theo 4 hướng |
| 5 | Move Generation (Sinh nước đi) | ⭐⭐ | Bán kính lân cận + phân loại ưu tiên |
| 6 | Line Evaluation (Đánh giá theo dòng) | ⭐⭐⭐ | Hệ thống pattern + trọng số phức tạp |
| 7 | Global Evaluation (Đánh giá toàn cục) | ⭐⭐⭐ | Tích hợp 3 thành phần: pattern + fork + center |
| 8 | Move Ordering (Sắp xếp nước đi) | ⭐⭐⭐⭐ | Delta evaluation + hiểu rõ Minimax |
| 9 | Iterative Deepening (Sâu dần) | ⭐⭐⭐⭐ | Quản lý thời gian + exception flow |
| 10 | Minimax + Alpha-Beta Pruning | ⭐⭐⭐⭐⭐ | Đệ quy đối kháng + cắt tỉa + tối ưu nhiều tầng |

---

## IV. Phân Chia Công Việc Cho 6 Người

> Nguyên tắc: Mỗi người phụ trách **1–2 thuật toán + phần code/UI liên quan**, đảm bảo khối lượng và độ khó tương đương nhau.

### Thành viên 1 — Kiến trúc Backend & Game State

| Hạng mục | Chi tiết |
| :--- | :--- |
| **Thuật toán** | Không có thuật toán AI riêng |
| **File phụ trách** | [app.py](file:///d:/Gomoku_MinMax/app.py) (toàn bộ 150 dòng) |
| **Nội dung công việc** | Thiết kế RESTful API (`/start`, `/move`, `/undo`, `/reset`), quản lý Game State (board, move_history, game_over), tích hợp gọi AI engine, xử lý validation đầu vào, cấu hình 3 mức độ khó (depth + time_limit) |
| **Khối lượng ước tính** | ★★★☆☆ (Trung bình — nhiều logic quản lý trạng thái) |

---

### Thành viên 2 — Kiểm Tra Thắng & Sinh Nước Đi

| Hạng mục | Chi tiết |
| :--- | :--- |
| **Thuật toán** | (1) Check Winner, (4) Danger Detection, (5) Move Generation |
| **File phụ trách** | [minmax.py — dòng 13–92](file:///d:/Gomoku_MinMax/minmax.py#L13-L92) |
| **Nội dung công việc** | Cài đặt `check_winner()`, `is_dangerous()`, `get_possible_moves()`. Giải thích cơ chế quét 4 hướng, bán kính 2 ô, và phân loại must_block vs normal |
| **Khối lượng ước tính** | ★★★☆☆ (Trung bình — 3 hàm, logic rõ ràng) |

---

### Thành viên 3 — Hàm Đánh Giá Thế Cờ (Heuristic)

| Hạng mục | Chi tiết |
| :--- | :--- |
| **Thuật toán** | (2) Pattern Counting, (3) Line Extraction, (6) Line Evaluation |
| **File phụ trách** | [minmax.py — dòng 142–257](file:///d:/Gomoku_MinMax/minmax.py#L142-L257) |
| **Nội dung công việc** | Cài đặt `_count_pattern()`, `_extract_all_lines()`, `_evaluate_line()`. Thiết kế bảng pattern và trọng số. Giải thích chiến lược "Phòng thủ > Tấn công ở cấp 4" |
| **Khối lượng ước tính** | ★★★★☆ (Khó — bảng trọng số phức tạp, cần hiểu chiến thuật cờ Caro) |

---

### Thành viên 4 — Đánh Giá Toàn Cục & Move Ordering

| Hạng mục | Chi tiết |
| :--- | :--- |
| **Thuật toán** | (7) Global Evaluation, (8) Move Ordering |
| **File phụ trách** | [minmax.py — dòng 96–139 và 260–292](file:///d:/Gomoku_MinMax/minmax.py#L96-L139) |
| **Nội dung công việc** | Cài đặt `evaluate()` (fork detection + center bonus), `score_move_quick()` (delta evaluation). Giải thích tại sao move ordering cải thiện Alpha-Beta |
| **Khối lượng ước tính** | ★★★★☆ (Khó — cần hiểu sâu về cách diff ảnh hưởng tới sort order) |

---

### Thành viên 5 — Minimax, Alpha-Beta & Iterative Deepening

| Hạng mục | Chi tiết |
| :--- | :--- |
| **Thuật toán** | (9) Iterative Deepening, (10) Minimax + Alpha-Beta Pruning |
| **File phụ trách** | [minmax.py — dòng 295–380](file:///d:/Gomoku_MinMax/minmax.py#L295-L380) |
| **Nội dung công việc** | Cài đặt `minimax()`, `iterative_deepening()`, `TimeoutException`. Giải thích cây trò chơi, cắt tỉa alpha-beta, depth-adjusted win score, timeout mechanism |
| **Khối lượng ước tính** | ★★★★★ (Rất khó — thuật toán trọng tâm của toàn bộ dự án) |

---

### Thành viên 6 — Frontend, UI/UX & Tích Hợp

| Hạng mục | Chi tiết |
| :--- | :--- |
| **Thuật toán** | Không có thuật toán AI riêng |
| **File phụ trách** | [game.js](file:///d:/Gomoku_MinMax/static/js/game.js) (280 dòng), [index.html](file:///d:/Gomoku_MinMax/templates/index.html), [style.css](file:///d:/Gomoku_MinMax/static/css/style.css) |
| **Nội dung công việc** | Thiết kế giao diện Glassmorphism/Dark Theme, render bàn cờ 15x15, xử lý sự kiện click, optimistic update (hiện quân O ngay trước khi server phản hồi), quản lý trạng thái UI (isProcessing, gameActive), hiển thị modal kết quả, hiệu ứng "AI đang suy nghĩ" |
| **Khối lượng ước tính** | ★★★☆☆ (Trung bình — nhiều file nhưng logic UI không quá phức tạp) |

---

### Tổng hợp phân công:

| Thành viên | Số thuật toán | Độ khó tổng | File chính |
| :---: | :---: | :---: | :--- |
| 1 | 0 | ★★★☆☆ | app.py |
| 2 | 3 | ★★★☆☆ | minmax.py (L13–92) |
| 3 | 3 | ★★★★☆ | minmax.py (L142–257) |
| 4 | 2 | ★★★★☆ | minmax.py (L96–139, L260–292) |
| 5 | 2 | ★★★★★ | minmax.py (L295–380) |
| 6 | 0 | ★★★☆☆ | game.js, HTML, CSS |

---

## V. Góc Nhìn Giảng Viên – Các Điểm Cần Phân Tích Sâu & Câu Hỏi Vấn Đáp

> Phần này mô phỏng góc nhìn của **giảng viên phản biện** trong buổi bảo vệ đồ án AI. Dưới đây là các điểm sẽ được hỏi sâu, kèm gợi ý trả lời.

---

### Điểm 1 (Trọng tâm): Tại sao chọn Minimax thay vì Monte Carlo Tree Search (MCTS)?

**Phân tích:** Đây gần như chắc chắn sẽ là câu hỏi đầu tiên của hội đồng. Cần trả lời rõ ràng:

- **Minimax + Alpha-Beta** phù hợp khi có thể xây dựng **hàm đánh giá heuristic chất lượng cao** — đúng với Gomoku vì hệ thống pattern (3 hở, 4 bịt, fork...) đã được nghiên cứu kỹ và có thể lượng hoá chính xác.
- **MCTS** phù hợp hơn cho các trò chơi mà hàm đánh giá khó xây dựng (như Go 19x19 có quá nhiều biến thể).
- Với bàn 15x15 và giới hạn thời gian 3s, Minimax + Alpha-Beta đạt depth 4–6 đủ để chơi cực mạnh. MCTS sẽ cần hàng nghìn simulation mới đạt chất lượng tương đương.

---

### Điểm 2 (Trọng tâm): Giải thích cơ chế Alpha-Beta Pruning bằng ví dụ cụ thể

**Phân tích:** Giảng viên sẽ yêu cầu vẽ cây và giải thích khi nào cắt tỉa xảy ra. Chuẩn bị sẵn ví dụ:

```
         MAX (AI)
        /        \
    MIN (H)     MIN (H)
    /    \        /   \
  [3]   [5]    [2]   [?]  <-- Không cần xét vì 2 < 3 (alpha=3)
```

- Node MAX đã biết nhánh trái cho giá trị >= 3 (alpha = 3).
- Node MIN bên phải tìm được giá trị 2 -> vì 2 < 3 (beta <= alpha), MAX sẽ **không bao giờ chọn** nhánh phải -> cắt tỉa `[?]`.

---

### Điểm 3 (Trọng tâm): Bảng trọng số pattern — cơ sở lý thuyết hay thực nghiệm?

**Phân tích:** Đây là điểm dễ bị hỏi vặn. Câu trả lời trung thực:

- Bảng trọng số được xây dựng dựa trên **kinh nghiệm chiến thuật Gomoku** (các sách dạy cờ, bài nghiên cứu AI cờ Caro) kết hợp **hiệu chỉnh thực nghiệm** (chạy AI tự đấu với nhau, điều chỉnh cho đến khi AI phòng thủ tốt).
- Quyết định thiết kế quan trọng nhất: **`_HU_HALF_4 = 1.500.000 > _AI_OPEN_4 = 1.000.000`** — buộc AI phải chặn trước khi tấn công. Nếu đảo ngược, AI sẽ "tham" tấn công và thua trong các tình huống đối thủ có 4 bịt 1 đầu.

---

### Điểm 4: Move Ordering ảnh hưởng bao nhiêu % hiệu năng?

**Phân tích:** Không có move ordering, Alpha-Beta hoạt động như Minimax thuần (worst case O(b^d)). Với move ordering tốt, đạt **O(b^(d/2))** (best case). Trong thực tế:

- Move ordering tốt giúp cắt tỉa **70–90%** các nhánh.
- Thể hiện qua việc AI có thể đạt depth 6 trong 3 giây, trong khi không có move ordering chỉ đạt depth 3–4.

---

### Điểm 5: Tại sao cắt gọt ở 20 nước (`moves[:20]`) mà không phải 10 hay 30?

**Phân tích:** Đây là trade-off giữa **chất lượng** và **tốc độ**:

- **10 nước:** Quá ít, có thể bỏ sót nước đi quyết định (đặc biệt nước chặn).
- **30 nước:** Quá nhiều, branching factor lớn, depth giảm.
- **20 nước:** Giá trị thực nghiệm (empirical), đảm bảo bao phủ đủ các nước tấn công + phòng thủ quan trọng nhất mà vẫn cho phép search depth 4–6 trong 3 giây.

---

### Điểm 6: `depth * 1000` trong WIN_SCORE có ý nghĩa gì?

**Phân tích:** Kỹ thuật **Depth-adjusted Win Score** giải quyết 2 vấn đề:

1. **Ưu tiên thắng nhanh:** `WIN_SCORE + depth * 1000` — depth lớn hơn (gần gốc cây hơn) -> giá trị lớn hơn -> AI chọn con đường thắng ngắn nhất.
2. **Trì hoãn thua:** `-WIN_SCORE - depth * 1000` — khi thua là tất yếu, AI chọn con đường thua chậm nhất (depth nhỏ nhất), tạo cơ hội cho đối thủ mắc sai lầm.

---

### Điểm 7: Fork Detection — Tại sao phải xử lý riêng?

**Phân tích:** Fork (thế gọng kìm) xảy ra khi AI/Human tạo được **>= 2 đường đe dọa cấp cao đồng thời** (ví dụ: 2 chuỗi 3 hở cùng lúc). Đối thủ chỉ chặn được 1 đường -> thua.

Pattern scoring đơn thuần **không nhận diện được mối quan hệ giữa các đường thẳng**. Fork bonus bù đắp thiếu sót này bằng cách cộng thêm `100.000 + count * 30.000` khi có >= 2 threats.

---

### Điểm 8: Iterative Deepening có lãng phí không khi chạy lại depth 1, 2, 3... mỗi lần?

**Phân tích:** **Không đáng kể.** Với branching factor b và max depth d:
- Tổng nodes của tất cả depth 1..d: `b^1 + b^2 + ... + b^d ~ b^d * b/(b-1)`
- Chỉ nodes của depth d: `b^d`
- Overhead: `b/(b-1)` khoảng 1.05–1.11 (chỉ thêm 5–11%)

Đổi lại, ta được **anytime behavior** (luôn có kết quả) và **time management** (không bao giờ vượt giới hạn thời gian).

---

### Điểm 9: Hệ thống có xử lý race condition trên backend không?

**Phân tích:** **Không.** `app.py` sử dụng biến global `board`, `game_over`, `move_history`. Flask mặc định chạy single-threaded nên không có race condition với 1 người chơi. Tuy nhiên, nếu 2 tab trình duyệt cùng gửi request `/move`, dữ liệu sẽ bị lỗi. Đây là **điểm yếu thiết kế** — nên sử dụng session-based game state hoặc database.

---

### Điểm 10: Optimistic Update trong Frontend (game.js) là gì?

**Phân tích:** Tại dòng 161 trong [game.js](file:///d:/Gomoku_MinMax/static/js/game.js#L161):

```javascript
cell.classList.add("human");  // Hiện quân O ngay lập tức
showThinking();                // Hiển thị "AI đang suy nghĩ..."
```

Quân O được vẽ **ngay trước khi server phản hồi**. Nếu server từ chối (ô đã có quân), giao diện sẽ được render lại đúng từ `data.board`. Kỹ thuật này cải thiện **perceived latency** (cảm giác phản hồi nhanh) cho người dùng.

---

### Điểm 11: Có thể cải tiến AI thêm bằng cách nào?

**Phân tích:** Các kỹ thuật nâng cao có thể áp dụng:

1. **Transposition Table (Zobrist Hashing):** Cache lại kết quả evaluate của các trạng thái bàn cờ đã xét, tránh tính toán lặp.
2. **Killer Move Heuristic:** Lưu nước đi gây cắt tỉa ở depth trước, ưu tiên xét ở depth hiện tại.
3. **Aspiration Window:** Thu hẹp cửa sổ alpha-beta dựa trên kết quả của depth trước trong Iterative Deepening.
4. **Threat-space Search (TSS):** Tìm kiếm chuyên biệt cho chuỗi nước tấn công liên tục (VCF/VCT).

---

### Điểm 12: Giải thích tại sao pattern overlapping (`start = idx + 1`) thay vì non-overlapping (`start = idx + len(pattern)`)?

**Phân tích:** Trong Gomoku, các pattern có thể chồng lấp trên bàn cờ thật. Ví dụ chuỗi `_XXX_XXX_` chứa 2 pattern `_XXX_` chồng nhau. Nếu dùng non-overlapping, sẽ bỏ sót 1 pattern -> đánh giá sai mức độ nguy hiểm. Dùng overlapping đảm bảo đếm đúng số lượng đe dọa thực tế.

---

### Điểm 13: Tại sao `get_possible_moves()` dùng bán kính 2 mà không phải bán kính 1 hay 3?

**Phân tích:**
- **Bán kính 1:** Quá hẹp, bỏ sót các nước đi tạo khoảng cách chiến thuật (ví dụ: `X_X` — 2 quân cách 1 ô, pattern broken).
- **Bán kính 3:** Quá rộng, sinh quá nhiều nước đi -> branching factor lớn -> depth giảm.
- **Bán kính 2:** Bao phủ đủ các pattern broken (cách 1 ô) và các nước đi phòng thủ gần, đồng thời giữ số lượng ứng viên ở mức hợp lý (20–60 nước).

---

### Điểm 14: Center Bonus dùng Manhattan Distance — tại sao không dùng Euclidean?

**Phân tích:** Manhattan Distance (`|x1-x2| + |y1-y2|`) phù hợp hơn Euclidean cho bàn cờ lưới vuông vì:
- Quân cờ di chuyển theo **hàng, cột, chéo** (không phải đường thẳng tùy ý).
- Manhattan phản ánh chính xác hơn "khoảng cách ảnh hưởng" trên lưới.
- Chi phí tính toán thấp hơn (không cần sqrt).

---

### Điểm 15: TimeoutException — Tại sao dùng Exception thay vì flag kiểm tra?

**Phân tích:** Sử dụng Exception (`raise TimeoutException`) thay vì kiểm tra flag `if timeout: return` vì:
- Minimax là hàm **đệ quy sâu nhiều tầng**. Nếu dùng flag, mỗi tầng đệ quy phải kiểm tra flag và truyền kết quả "bỏ cuộc" ngược lên — code rất phức tạp.
- Exception **thoát trực tiếp** qua tất cả các tầng đệ quy về `iterative_deepening()`, nơi nó được bắt (`except TimeoutException`) một cách sạch sẽ. Kết quả best_move của depth hoàn chỉnh trước đó vẫn được giữ nguyên.

---

*Tài liệu được biên soạn ngày 10/06/2026 phục vụ buổi bảo vệ đồ án AI — Gomoku MinMax.*
