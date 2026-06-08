import math
import time

BOARD_SIZE = 15
EMPTY = 0
AI = 1
HUMAN = -1

# Điểm thắng/thua phải CAO HƠN mọi giá trị evaluate có thể trả về
WIN_SCORE = 5000000


# ================= CHECK WIN =================
def check_winner(board, player):
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != player:
                continue
            for dx, dy in directions:
                count = 0
                for k in range(5):
                    x = i + dx*k
                    y = j + dy*k
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                        if board[x][y] == player:
                            count += 1
                        else:
                            break
                    else:
                        break
                if count == 5:
                    return True
    return False


# ================= MOVE GENERATION =================

def is_dangerous(board, i, j):
    """Kiểm tra ô (i,j) có nằm trong chuỗi 2+ quân liên tiếp không."""
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    player = board[i][j]
    if player == EMPTY:
        return False
    for dx, dy in directions:
        count = 1
        for step in range(1, 4):
            x, y = i + dx*step, j + dy*step
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == player:
                count += 1
            else:
                break
        for step in range(1, 4):
            x, y = i - dx*step, j - dy*step
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == player:
                count += 1
            else:
                break
        if count >= 2:
            return True
    return False


def get_possible_moves(board):
    """
    Sinh nước đi ứng viên (bán kính 2, tối đa 30).
    Ưu tiên ô gần chuỗi nguy hiểm.
    """
    must_block = set()
    normal = set()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                continue
            danger = is_dangerous(board, i, j)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx == 0 and dy == 0:
                        continue
                    x, y = i + dx, j + dy
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == EMPTY:
                        if danger:
                            must_block.add((x, y))
                        else:
                            normal.add((x, y))

    # Không được cắt gọt mảng ở đây vì list(set) là ngẫu nhiên, 
    # có thể vô tình vứt bỏ các nước đi quyết định (chặn 4, tạo 5).
    # Chúng ta sẽ trả về toàn bộ, sau đó sort và cắt gọt ở hàm minimax.
    combined = list(must_block) + [m for m in normal if m not in must_block]
    return combined


# ================= MOVE ORDERING =================
def score_move_quick(board, move, player):
    """
    Đánh giá nhanh 1 nước để sắp xếp trước khi đệ quy bằng cách chỉ đánh giá 
    sự thay đổi điểm số của 4 đường thẳng đi qua ô (move[0], move[1]).
    Bắt buộc phải tính CHÊNH LỆCH (sau - trước) để nhận biết nước đi chặn
    (khi chặn, pattern nguy hiểm của đối phương biến mất -> điểm tăng).
    """
    i, j = move[0], move[1]
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    
    score_before = 0
    for dx, dy in directions:
        line = []
        for k in range(-5, 6):
            x, y = i + dx*k, j + dy*k
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                line.append(board[x][y])
        if len(line) >= 5:
            score_before += _evaluate_line(line)
            
    board[i][j] = player
    
    score_after = 0
    for dx, dy in directions:
        line = []
        for k in range(-5, 6):
            x, y = i + dx*k, j + dy*k
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                line.append(board[x][y])
        if len(line) >= 5:
            score_after += _evaluate_line(line)
            
    board[i][j] = EMPTY
    
    # Đối với AI (maximizing), score lớn hơn -> diff dương (tốt hơn)
    # Đối với HUMAN (minimizing), score nhỏ hơn -> diff âm (tốt hơn)
    # diff phản ánh MỨC ĐỘ THAY ĐỔI THEO HƯỚNG CÓ LỢI CHO AI
    diff = score_after - score_before
    
    # Nếu đang sinh nước đi cho HUMAN (player == HUMAN), 
    # nước đi càng tốt cho HUMAN thì diff CÀNG ÂM.
    # Trong minimax ta sort reverse=False cho HUMAN (lấy bé nhất trước) -> diff âm nhất sẽ lên đầu!
    # Nên ta chỉ cần return diff nguyên bản.
    return diff


# ================= EVALUATE =================
# ---- Bảng điểm Pattern ----
# Chiến lược scoring:
#   - 4 liên tiếp (open/half/broken): PHÒNG THỦ > TẤN CÔNG (phải chặn hoặc thua)
#   - 3 hở 2 đầu: PHÒNG THỦ ≈ TẤN CÔNG (rất nguy hiểm, cần phản ứng)
#   - 3 hở 1 đầu, 2 liên: TẤN CÔNG > PHÒNG THỦ (AI chủ động tạo thế)
# → AI vẫn chặn mối đe dọa trực tiếp nhưng ưu tiên tấn công ở cấp chiến thuật

# AI (X) — Tấn công
_AI_FIVE      = 10000000   # Win now (10M)
_AI_OPEN_4    =  1000000   # Guaranteed win next turn (1M)
_AI_HALF_4    =    80000   # Forces opponent to block
_AI_BROKEN_4  =    80000   # Forces opponent to block
_AI_OPEN_3    =    30000   # Threatens open 4
_AI_BROKEN_3  =    25000   # Threatens broken 4
_AI_HALF_3    =     1000   # Low threat
_AI_OPEN_2    =      500
_AI_BROKEN_2  =      200

# HUMAN (O) — Phòng thủ
_HU_FIVE      = 10000000   # Opponent wins
_HU_OPEN_4    =  2000000   # Opponent has guaranteed win (must block/delay)
_HU_HALF_4    =  1500000   # Opponent is 1 move from win (MUST BLOCK, > AI_OPEN_4)
_HU_BROKEN_4  =  1500000   # Opponent is 1 move from win (MUST BLOCK)
_HU_OPEN_3    =    60000   # Opponent threatens open 4 (must block, but < AI_HALF_4)
_HU_BROKEN_3  =    55000   # Opponent threatens broken 4
_HU_HALF_3    =      800
_HU_OPEN_2    =      400
_HU_BROKEN_2  =      150


def _evaluate_line(line):
    """Tính điểm cho một dòng (dài bất kỳ)."""
    total = 0
    s = ''.join(['X' if v == AI else 'O' if v == HUMAN else '_' for v in line])

    # ---- TẤN CÔNG (AI = X) ----
    if 'XXXXX' in s: total += _AI_FIVE
    total += _count_pattern(s, '_XXXX_') * _AI_OPEN_4
    total += (_count_pattern(s, 'XXXX_') + _count_pattern(s, '_XXXX')) * _AI_HALF_4
    total += (_count_pattern(s, 'XX_XX') + _count_pattern(s, 'XXX_X') + _count_pattern(s, 'X_XXX')) * _AI_BROKEN_4
    total += _count_pattern(s, '_XXX_') * _AI_OPEN_3
    total += (_count_pattern(s, '_XX_X_') + _count_pattern(s, '_X_XX_')) * _AI_BROKEN_3
    total += (_count_pattern(s, 'XXX__') + _count_pattern(s, '__XXX')) * _AI_HALF_3
    total += _count_pattern(s, '_XX_') * _AI_OPEN_2
    total += _count_pattern(s, '_X_X_') * _AI_BROKEN_2

    # ---- PHÒNG THỦ (HUMAN = O) ----
    if 'OOOOO' in s: total -= _HU_FIVE
    total -= _count_pattern(s, '_OOOO_') * _HU_OPEN_4
    total -= (_count_pattern(s, 'OOOO_') + _count_pattern(s, '_OOOO')) * _HU_HALF_4
    total -= (_count_pattern(s, 'OO_OO') + _count_pattern(s, 'OOO_O') + _count_pattern(s, 'O_OOO')) * _HU_BROKEN_4
    total -= _count_pattern(s, '_OOO_') * _HU_OPEN_3
    total -= (_count_pattern(s, '_OO_O_') + _count_pattern(s, '_O_OO_')) * _HU_BROKEN_3
    total -= (_count_pattern(s, 'OOO__') + _count_pattern(s, '__OOO')) * _HU_HALF_3
    total -= _count_pattern(s, '_OO_') * _HU_OPEN_2
    total -= _count_pattern(s, '_O_O_') * _HU_BROKEN_2

    return total


def _extract_all_lines(board):
    """
    Trích xuất tất cả các dòng (hàng, cột, chéo) trên bàn cờ.
    Mỗi dòng chỉ được trích 1 lần → tránh đếm trùng pattern.
    """
    lines = []

    # Hàng ngang
    for i in range(BOARD_SIZE):
        line = []
        for j in range(BOARD_SIZE):
            line.append(board[i][j])
        lines.append(line)

    # Cột dọc
    for j in range(BOARD_SIZE):
        line = []
        for i in range(BOARD_SIZE):
            line.append(board[i][j])
        lines.append(line)

    # Đường chéo chính (top-left → bottom-right)
    for start in range(-(BOARD_SIZE - 1), BOARD_SIZE):
        line = []
        for k in range(BOARD_SIZE):
            i, j = k, k - start
            if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
                line.append(board[i][j])
        if len(line) >= 5:
            lines.append(line)

    # Đường chéo phụ (top-right → bottom-left)
    for start in range(0, 2 * BOARD_SIZE - 1):
        line = []
        for k in range(BOARD_SIZE):
            i, j = k, start - k
            if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
                line.append(board[i][j])
        if len(line) >= 5:
            lines.append(line)

    return lines


def _count_pattern(s, pattern):
    """Đếm số lần pattern xuất hiện (không overlap) trong chuỗi s."""
    count = 0
    start = 0
    while True:
        idx = s.find(pattern, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


def evaluate(board):
    """Đánh giá toàn bộ bàn cờ sử dụng _evaluate_line."""
    total = 0
    ai_threats = 0
    human_threats = 0

    for line in _extract_all_lines(board):
        total += _evaluate_line(line)
        
        # Đếm fork
        s = ''.join(['X' if x == AI else 'O' if x == HUMAN else '_' for x in line])
        ai_threats += _count_pattern(s, '_XXXX_') + _count_pattern(s, 'XXXX_') + _count_pattern(s, '_XXXX') + _count_pattern(s, 'XX_XX') + _count_pattern(s, 'XXX_X') + _count_pattern(s, 'X_XXX') + _count_pattern(s, '_XXX_')
        human_threats += _count_pattern(s, '_OOOO_') + _count_pattern(s, 'OOOO_') + _count_pattern(s, '_OOOO') + _count_pattern(s, 'OO_OO') + _count_pattern(s, 'OOO_O') + _count_pattern(s, 'O_OOO') + _count_pattern(s, '_OOO_')

    # ---- Fork bonus ----
    if ai_threats >= 2:
        total += 100000 + ai_threats * 30000
    if human_threats >= 2:
        total -= 100000 + human_threats * 30000

    # ---- Thưởng vị trí trung tâm ----
    center = BOARD_SIZE // 2
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != EMPTY:
                dist = abs(i - center) + abs(j - center)
                bonus = max(0, 14 - dist) * 5
                if board[i][j] == AI:
                    total += bonus
                else:
                    total -= bonus

    return total


# Exception dùng để thoát sớm khi hết thời gian
class TimeoutException(Exception):
    pass


# ================= MINIMAX =================
def minimax(board, depth, alpha, beta, maximizing, start_time, time_limit):
    # Kiểm tra timeout ở mỗi node
    if time.time() - start_time > time_limit:
        raise TimeoutException()

    if check_winner(board, AI):
        return WIN_SCORE + depth * 1000, None
    if check_winner(board, HUMAN):
        return -WIN_SCORE - depth * 1000, None

    if depth == 0:
        return evaluate(board), None

    moves = get_possible_moves(board)
    if not moves:
        moves = [(BOARD_SIZE//2, BOARD_SIZE//2)]
        
    player = AI if maximizing else HUMAN
    
    # Sort moves
    # player = AI (maximize) -> sort reverse=True
    # player = HUMAN (minimize) -> sort reverse=False
    # Điểm score_move_quick dương (lớn) tốt cho AI, âm (nhỏ) tốt cho HUMAN
    moves.sort(key=lambda m: score_move_quick(board, m, player), reverse=maximizing)
    
    # CẮT GỌT: Chỉ giữ lại 20 nước đi tiềm năng nhất để search sâu (tối ưu tốc độ)
    moves = moves[:20]
    
    best_move = None

    if maximizing:
        max_eval = -math.inf
        for move in moves:
            board[move[0]][move[1]] = AI
            try:
                eval, _ = minimax(board, depth-1, alpha, beta, False, start_time, time_limit)
            finally:
                board[move[0]][move[1]] = EMPTY
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = math.inf
        for move in moves:
            board[move[0]][move[1]] = HUMAN
            try:
                eval, _ = minimax(board, depth-1, alpha, beta, True, start_time, time_limit)
            finally:
                board[move[0]][move[1]] = EMPTY
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


# ================= ITERATIVE DEEPENING =================
def iterative_deepening(board, max_depth=4, time_limit=1.5):
    best_move = None
    start = time.time()

    for depth in range(1, max_depth + 1):
        if time.time() - start > time_limit:
            break
        try:
            _, move = minimax(board, depth, -math.inf, math.inf, True, start, time_limit)
            if move:
                best_move = move
        except TimeoutException:
            # Hết giờ giữa chừng depth này, giữ nguyên best_move của depth trước và thoát
            break

    return best_move