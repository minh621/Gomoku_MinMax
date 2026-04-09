import math
import copy

BOARD_SIZE = 15
EMPTY = 0
AI = 1
HUMAN = -1

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


# ================= MOVE GEN =================
# Sinh nước ứng viên theo 2 nhóm ưu tiên:
#   - must_block: ô gần chuỗi nguy hiểm (3+ quân liên tiếp) → luôn giữ lại
#   - normal: ô gần quân bình thường → bổ sung cho đủ 25
def is_dangerous(board, i, j):
    """Kiểm tra ô (i,j) có nằm trong/gần chuỗi 3+ quân liên tiếp không."""
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
        if count >= 3:
            return True
    return False


def get_possible_moves(board):
    must_block = set()
    normal = set()
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                continue
            danger = is_dangerous(board, i, j)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    x, y = i + dx, j + dy
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == EMPTY:
                        if danger:
                            must_block.add((x, y))
                        else:
                            normal.add((x, y))
 
    if not must_block and not normal:
        return [(7, 7)]
 
    # Luôn giữ must_block, bổ sung normal cho đủ 25
    combined = list(must_block) + [m for m in normal if m not in must_block]
    return combined[:25]


# ================= MOVE ORDERING =================
def score_move_quick(board, move, player):
    # Đánh giá nhanh 1 nước để sắp xếp trước khi đệ quy
    # → alpha-beta cắt được nhiều nhánh hơn
    board[move[0]][move[1]] = player
    s = evaluate(board)
    board[move[0]][move[1]] = EMPTY
    return s



# ================= EVALUATE =================
def evaluate(board):

    def score_line(line):
        score = 0

        # chuyển sang string để dễ match
        s = ''.join(['X' if x == AI else 'O' if x == HUMAN else '_' for x in line])

         # Tấn công (AI = X): điểm tăng dần theo mức độ nguy hiểm
        patterns = [
            ("XXXXX", 1000000), #thắng ngay
            ("_XXXX_", 100000), #chắn chắn thắng
            ("XXXX_", 50000),
            ("_XXXX", 50000),
            ("XX_XX",    40000),  # broken four → gần bằng 4 hở 1
            ("_XXX_",    10000),  # 3 hở 2 đầu
            ("_XX_X_",   10000),  # broken three hở 2 đầu
            ("_X_XX_",   10000),  # broken three hở 2 đầu
            ("XXX__", 500),
            ("__XXX", 500),
            ("_XX_", 200),
        ]

        for pattern, value in patterns:
            if pattern in s:
                score += value

        # trừ điểm nếu là HUMAN
        patterns_opponent = [
            ("OOOOO", -1000000),
            ("_OOOO_", -120000), #Tập trung thủ 4 hở 2 đầu hơn
            ("OOOO_", -60000),
            ("_OOOO", -60000),
            ("OO_OO",  -50000),  # broken four
            ("_OOO_",  -12000),  # 3 hở 2 đầu
            ("_OO_O_", -12000),  # broken three hở 2 đầu
            ("_O_OO_", -12000),  # broken three hở 2 đầu
            ("OOO__", -500),
            ("__OOO", -500),
            ("_OO_", -200),
        ]

        for pattern, value in patterns_opponent:
            if pattern in s:
                score += value

        return score

    #Quét toàn bộ  ô theo 4 hướng
    total_score = 0
    ai_threats = 0
    human_threats = 0
    ai_threat_pats    = ["_XXX_", "_XX_X_", "_X_XX_", "_XXXX_", "XXXX_", "_XXXX", "XX_XX"]
    human_threat_pats = ["_OOO_", "_OO_O_", "_O_OO_", "_OOOO_", "OOOO_", "_OOOO", "OO_OO"]

    # duyệt tất cả hướng
    directions = [(1,0), (0,1), (1,1), (1,-1)]

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for dx, dy in directions:
                line = []
                for k in range(7):  # lấy đoạn dài 7
                    x = i + dx*k
                    y = j + dy*k
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                        line.append(board[x][y])
                    else:
                        break

                if len(line) >= 6:
                    total_score += score_line(line)
                    s = ''.join(['X' if v == AI else 'O' if v == HUMAN else '_' for v in line])
                    for pat in ai_threat_pats:
                        if pat in s:
                            ai_threats += 1
                    for pat in human_threat_pats:
                        if pat in s:
                            human_threats += 1
    
    #fork detection
    #Nếu 1 bên có >= 2 mối đe dọa cùng lúc
    if ai_threats >= 2:
        total_score += ai_threats * 8000
    if human_threats >= 2:
        total_score -= human_threats * 8000

    return total_score


# ================= MINIMAX =================
def minimax(board, depth, alpha, beta, maximizing):

    if check_winner(board, AI):
        return 100000, None
    if check_winner(board, HUMAN):
        return -100000, None

    if depth == 0:
        return evaluate(board), None

    moves = get_possible_moves(board)
    # Sắp xếp: nước tốt cho bên đang đi được xét trước
    player = AI if maximizing else HUMAN
    moves.sort(key=lambda m: score_move_quick(board, m, player), reverse=maximizing)
    best_move = None

    if maximizing:
        max_eval = -math.inf

        for move in moves:
            # --- make ---
            board[move[0]][move[1]] = AI
            eval, _ = minimax(board, depth-1, alpha, beta, False)
            # --- unmake ---
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
            eval, _ = minimax(board, depth-1, alpha, beta, True)
            board[move[0]][move[1]] = EMPTY

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval, best_move
    


# ================= ITERATIVE DEEPENING =================
# Tìm kiếm lần lượt depth=1,2,3,4:
#   - Kết quả từ depth trước dùng để sắp xếp nước đi cho depth sau
#   - Nếu hết time_limit thì trả về kết quả tốt nhất đã tìm được
#   - Luôn có kết quả trả về dù bị timeout (an toàn hơn gọi depth=4 thẳng)
def iterative_deepening(board, max_depth=4, time_limit=1.5):
    import time
    best_move = None
    start = time.time()
 
    for depth in range(1, max_depth + 1):
        if time.time() - start > time_limit:
            break
        _, move = minimax(board, depth, -math.inf, math.inf, True)
        if move:
            best_move = move
 
    return best_move