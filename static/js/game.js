/* ============================================================
   GOMOKU (CỜ CARO) — Game Client Logic
   Manages board rendering, user interactions, and server API
   ============================================================ */

const BOARD_SIZE = 15;


// ==================== STATE ====================
let currentDifficulty = "medium";
let gameActive = false;
let isProcessing = false;
let lastAiMove = null;


// ==================== DOM REFERENCES ====================
const boardEl      = document.getElementById("board");
const statusEl     = document.getElementById("status");
const statusBar    = document.querySelector(".status-bar");
const modalOverlay = document.getElementById("resultModal");
const resultEmoji  = document.getElementById("resultEmoji");
const resultTitle  = document.getElementById("resultTitle");
const resultText   = document.getElementById("resultText");


// ==================== BOARD SETUP ====================

/**
 * Tạo lưới ô 15×15 cho bàn cờ Caro.
 */
function initBoard() {
    boardEl.innerHTML = "";
    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = 0; j < BOARD_SIZE; j++) {
            const cell = document.createElement("div");
            cell.className = "cell";
            cell.dataset.x = i;
            cell.dataset.y = j;
            cell.addEventListener("click", () => makeMove(i, j));
            boardEl.appendChild(cell);
        }
    }
}


// ==================== RENDERING ====================

/**
 * Cập nhật giao diện bàn cờ từ dữ liệu server.
 * @param {number[][]} board - Ma trận 15×15 (1 = AI/X, -1 = Human/O, 0 = Empty)
 */
function render(board) {
    const cells = boardEl.querySelectorAll(".cell");
    let index = 0;

    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = 0; j < BOARD_SIZE; j++) {
            const cell = cells[index];
            cell.className = "cell";

            // Piece
            if (board[i][j] === 1)       cell.classList.add("ai");
            else if (board[i][j] === -1)  cell.classList.add("human");

            // Last AI move highlight
            if (lastAiMove && lastAiMove[0] === i && lastAiMove[1] === j) {
                cell.classList.add("last-move");
            }

            index++;
        }
    }
}


// ==================== STATUS ====================

function setStatus(html, active = true) {
    statusEl.innerHTML = html;
    statusBar.classList.toggle("active", active);
}

function showThinking() {
    setStatus(
        `<span class="thinking-indicator">
            AI đang suy nghĩ
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </span>`
    );
}


// ==================== DIFFICULTY ====================

function setDifficulty(level) {
    if (isProcessing) return;
    currentDifficulty = level;

    document.querySelectorAll(".diff-btn").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.level === level);
    });
}

// Gắn sự kiện click cho các nút difficulty
document.querySelectorAll(".diff-btn").forEach(btn => {
    btn.addEventListener("click", () => setDifficulty(btn.dataset.level));
});


// ==================== GAME ACTIONS ====================

/**
 * Bắt đầu ván mới. Gửi lượt đi đầu và mức độ khó tới server.
 */
async function startGame(first) {
    if (isProcessing) return;
    isProcessing = true;
    gameActive = true;
    lastAiMove = null;

    hideResult();
    setStatus("Đang khởi tạo...");

    try {
        const res = await fetch("/start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ first, difficulty: currentDifficulty }),
        });
        const data = await res.json();

        if (data.ai_move) {
            lastAiMove = data.ai_move;
        }

        render(data.board);
        setStatus(first === "human" ? "Lượt của bạn — đánh O" : "AI đã đi — lượt của bạn");
    } catch {
        setStatus("Lỗi kết nối!", false);
    }

    isProcessing = false;
}


/**
 * Người chơi đặt quân O tại ô (x, y).
 */
async function makeMove(x, y) {
    if (!gameActive || isProcessing) return;

    // Kiểm tra ô trống
    const cell = boardEl.querySelector(`[data-x="${x}"][data-y="${y}"]`);
    if (cell.classList.contains("human") || cell.classList.contains("ai")) return;

    isProcessing = true;

    // Hiện quân O ngay (optimistic update)
    cell.classList.add("human");
    showThinking();
    boardEl.parentElement.classList.add("thinking");

    try {
        const res = await fetch("/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ x, y }),
        });
        const data = await res.json();

        boardEl.parentElement.classList.remove("thinking");

        if (data.ai_move) {
            lastAiMove = data.ai_move;
        }

        render(data.board);

        if (data.winner) {
            gameActive = false;
            showResult(data.winner);
        } else {
            setStatus("Lượt của bạn");
        }
    } catch {
        boardEl.parentElement.classList.remove("thinking");
        setStatus("Lỗi kết nối!", false);
    }

    isProcessing = false;
}


/**
 * Hoàn tác nước đi cuối (cả quân O người chơi + quân X AI phản hồi).
 */
async function undoMove() {
    if (isProcessing) return;
    isProcessing = true;

    try {
        const res = await fetch("/undo", { method: "POST" });
        const data = await res.json();

        lastAiMove = null;
        hideResult();
        gameActive = true;
        render(data.board);

        if (data.undone === 0) {
            setStatus("Không có nước đi để hoàn tác", false);
        } else {
            setStatus("Đã hoàn tác — lượt của bạn");
        }
    } catch {
        setStatus("Lỗi kết nối!", false);
    }

    isProcessing = false;
}


/**
 * Reset bàn cờ về trạng thái trống.
 */
async function resetGame() {
    if (isProcessing) return;
    isProcessing = true;

    try {
        const res = await fetch("/reset", { method: "POST" });
        const data = await res.json();

        lastAiMove = null;
        gameActive = false;
        hideResult();
        render(data.board);
        setStatus("Chọn mức độ khó và nhấn bắt đầu", false);
    } catch {
        setStatus("Lỗi kết nối!", false);
    }

    isProcessing = false;
}


// ==================== RESULT MODAL ====================

function showResult(winner) {
    const config = {
        human: { emoji: "🎉", title: "Bạn thắng!",  text: "Xuất sắc! Bạn đã đánh bại AI." },
        ai:    { emoji: "🤖", title: "AI thắng!",    text: "AI đã chiến thắng. Thử lại nhé!" },
        draw:  { emoji: "🤝", title: "Hoà!",         text: "Không ai thắng — trận đấu kết thúc hoà." },
    };

    const c = config[winner] || config.draw;

    resultEmoji.textContent = c.emoji;
    resultTitle.textContent = c.title;
    resultText.textContent  = c.text;

    setStatus(c.title);
    modalOverlay.classList.add("show");
}

function hideResult() {
    modalOverlay.classList.remove("show");
}

// Đóng modal khi click ngoài card
modalOverlay.addEventListener("click", (e) => {
    if (e.target === modalOverlay) hideResult();
});


// ==================== INIT ====================
initBoard();
