from flask import Flask, render_template, request, jsonify
from minmax import iterative_deepening, BOARD_SIZE, EMPTY, AI, HUMAN, check_winner

app = Flask(__name__)


# ==================== GAME STATE ====================
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
game_over = False
current_turn = HUMAN
move_history = []          # List of (x, y, player) tuples
difficulty = "medium"

# Difficulty → (max_depth, time_limit)
DIFFICULTY_SETTINGS = {
    "easy":   (1, 0.5),
    "medium": (2, 1.0),
    "hard":   (6, 3.0),
}


# ==================== ROUTES ====================

@app.route("/")
def index():
    return render_template("index.html")


# ===== START GAME =====
@app.route("/start", methods=["POST"])
def start():
    global board, game_over, current_turn, move_history, difficulty

    data = request.json
    first = data.get("first", "human")
    difficulty = data.get("difficulty", "medium")

    if first not in ("human", "ai"):
        return jsonify({"error": "first phải là 'human' hoặc 'ai'"}), 400
    if difficulty not in DIFFICULTY_SETTINGS:
        return jsonify({"error": "difficulty phải là 'easy', 'medium' hoặc 'hard'"}), 400

    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    game_over = False
    move_history = []
    current_turn = HUMAN if first == "human" else AI

    ai_move = None

    # Nếu AI đi trước
    if current_turn == AI:
        max_depth, time_limit = DIFFICULTY_SETTINGS[difficulty]
        move = iterative_deepening(board, max_depth=max_depth, time_limit=time_limit)
        if move:
            board[move[0]][move[1]] = AI
            move_history.append((move[0], move[1], AI))
            ai_move = [move[0], move[1]]
        current_turn = HUMAN

    return jsonify({"board": board, "ai_move": ai_move})


# ===== RESET =====
@app.route("/reset", methods=["POST"])
def reset():
    global board, game_over, move_history
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    game_over = False
    move_history = []
    return jsonify({"board": board})


# ===== MOVE =====
@app.route("/move", methods=["POST"])
def move():
    global board, game_over, current_turn

    if game_over:
        return jsonify({"error": "Game over"})

    data = request.json
    if not data or "x" not in data or "y" not in data:
        return jsonify({"board": board})

    x, y = data["x"], data["y"]

    # Toạ độ ngoài bàn hoặc ô đã có quân → bỏ qua
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return jsonify({"board": board})
    if board[x][y] != EMPTY:
        return jsonify({"board": board})

    # --- Human move ---
    board[x][y] = HUMAN
    move_history.append((x, y, HUMAN))

    if check_winner(board, HUMAN):
        game_over = True
        return jsonify({"winner": "human", "board": board})

    # Kiểm tra hoà (bàn cờ đầy)
    if all(board[i][j] != EMPTY for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
        game_over = True
        return jsonify({"winner": "draw", "board": board})

    # --- AI move ---
    max_depth, time_limit = DIFFICULTY_SETTINGS[difficulty]
    ai_move = iterative_deepening(board, max_depth=max_depth, time_limit=time_limit)

    if ai_move:
        board[ai_move[0]][ai_move[1]] = AI
        move_history.append((ai_move[0], ai_move[1], AI))

    if check_winner(board, AI):
        game_over = True
        return jsonify({"winner": "ai", "board": board, "ai_move": list(ai_move)})

    return jsonify({"board": board, "ai_move": list(ai_move) if ai_move else None})


# ===== UNDO =====
@app.route("/undo", methods=["POST"])
def undo():
    global board, game_over, move_history

    if game_over:
        game_over = False

    if not move_history:
        return jsonify({"board": board, "undone": 0})

    undone = 0

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

    return jsonify({"board": board, "undone": undone})


if __name__ == "__main__":
    app.run(debug=True)