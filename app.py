from flask import Flask, render_template, request, jsonify
from minmax import iterative_deepening,  BOARD_SIZE, EMPTY, AI, HUMAN, check_winner

app = Flask(__name__)

board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
game_over = False
current_turn = HUMAN

@app.route("/")
def index():
    return render_template("index.html")


# ===== START GAME =====
@app.route("/start", methods=["POST"])
def start():
    global board, game_over, current_turn

    data = request.json
    first = data["first"]

    if first not in ("human", "ai"):
        return jsonify({"error": "first phải là 'human' hoặc 'ai'"}), 400

    board = [[EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
    game_over = False

    current_turn = HUMAN if first == "human" else AI

    # nếu AI đi trước
    if current_turn == AI:
        move = iterative_deepening(board, max_depth=4, time_limit=1.5)
        if move:
            board[move[0]][move[1]] = AI
        current_turn = HUMAN
 
    return jsonify({"board": board})


# ===== RESET =====
@app.route("/reset", methods=["POST"])
def reset():
    global board, game_over
    board = [[EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
    game_over = False
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

    # Toạ độ ngoài bàn hoặc ô đã có quân → im lặng, không làm gì
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return jsonify({"board": board})
 
    if board[x][y] != EMPTY:
        return jsonify({"board": board})

    # HUMAN MOVE
    board[x][y] = HUMAN

    if check_winner(board, HUMAN):
        game_over = True
        return jsonify({"winner": "human", "board": board})
    

    # Kiểm tra hoà (bàn cờ đầy)
    if all(board[i][j] != EMPTY for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
        game_over = True
        return jsonify({"winner": "draw", "board": board})

    # AI MOVE
    ai_move = iterative_deepening(board, max_depth=4, time_limit=1.5)

    if ai_move:
        board[ai_move[0]][ai_move[1]] = AI

    if check_winner(board, AI):
        game_over = True
        return jsonify({"winner": "ai", "board": board})

    return jsonify({"board": board})


if __name__ == "__main__":
    app.run(debug=True)