from flask import Flask, send_from_directory, jsonify, request
import os

app = Flask(__name__)

# Path to the root directory
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def is_winner(board, player):
    win_conditions = [(0,1,2),(3,4,5),(6,7,8),
                      (0,3,6),(1,4,7),(2,5,8),
                      (0,4,8),(2,4,6)]
    return any(board[i]==board[j]==board[k]==player for i,j,k in win_conditions)

def minimax(board, depth, is_maximizing, alpha, beta):
    if is_winner(board, 'O'):
        return 1
    if is_winner(board, 'X'):
        return -1
    if ' ' not in board:
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth+1, False, alpha, beta)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth+1, True, alpha, beta)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def best_move(board):
    best_val = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            move_val = minimax(board, 0, False, -float('inf'), float('inf'))
            board[i] = ' '
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

@app.route('/')
def home():
    return send_from_directory(ROOT_DIR, 'index.html')

@app.route('/move', methods=['POST'])
def move():
    board = request.json['board']
    ai_move = best_move(board)
    return jsonify({'move': ai_move})

if __name__ == '__main__':
    app.run(debug=True)
