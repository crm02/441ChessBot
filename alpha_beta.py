import chess
from search import evaluate_board
# A large value so checkmate is always better than gaining pieces.
MATE_SCORE = 100000
def alpha_beta(board, depth, alpha, beta, maxNode):
    """Return the best score using minimax with alpha-beta pruning."""
    # Checkmate and draws need to be checked before evaluating material.
    if board.is_checkmate():
        # The player whose turn it is has been checkmated.
        return -MATE_SCORE - depth if board.turn == chess.WHITE else MATE_SCORE + depth
    if board.is_game_over(claim_draw=True):
        return 0
    if depth <= 0:
        return evaluate_board(board)
    if maxNode:  # White tries to get the highest score.
        best = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            try:
                score = alpha_beta(board, depth - 1, alpha, beta, False)
            finally:
                board.pop()
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # Remaining moves cannot improve this result.
        return best
    else:  # Black tries to get the lowest score.
        best = float("inf")
        for move in board.legal_moves:
            board.push(move)
            try:
                score = alpha_beta(board, depth - 1, alpha, beta, True)
            finally:
                board.pop()
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best
def find_best_move_alpha_beta(board, depth):
    """Choose and return a legal chess.Move for the current player."""
    if depth < 1:
        raise ValueError("Depth must be at least 1.")
    if board.is_game_over(claim_draw=True):
        return None
    best_move = None
    maxNode = board.turn == chess.WHITE
    alpha = float("-inf")
    beta = float("inf")
    best = alpha if maxNode else beta
    for move in board.legal_moves:
        board.push(move)
        try:
            score = alpha_beta(board, depth - 1, alpha, beta, not maxNode)
        finally:
            board.pop()
        if best_move is None or (maxNode and score > best) or (not maxNode and score < best):
            best = score
            best_move = move
        if maxNode:
            alpha = max(alpha, best)
        else:
            beta = min(beta, best)
    return best_move
# Optional alias if the group prefers camelCase names like minMax.
alphaBeta = alpha_beta
