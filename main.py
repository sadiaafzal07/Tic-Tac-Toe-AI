from flask import Flask, render_template, request, jsonify
import copy

app = Flask(__name__)

# Initialize the board
board = [""] * 9

# Minimax with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif "" not in board:
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ""
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ""
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_score

def get_best_move():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False, -float("inf"), float("inf"))
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

def check_winner(brd):
    win_combinations = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for (i, j, k) in win_combinations:
        if brd[i] != "" and brd[i] == brd[j] and brd[j] == brd[k]:
            return brd[i]
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global board
    data = request.get_json()
    position = data["position"]
    board[position] = "X"

    if check_winner(board) or "" not in board:
        return jsonify(board=board, status=check_winner(board) or "Draw")

    ai_move = get_best_move()
    board[ai_move] = "O"

    result = check_winner(board)
    status = result if result else "Continue"
    if "" not in board and result is None:
        status = "Draw"

    return jsonify(board=board, status=status)

@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = [""] * 9
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
