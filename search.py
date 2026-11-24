import chess #python-chess library


# uses alpha and beta for score keeping, but that only applies to Alpha-beta pruning, can change later
# This function recursively tests each legal move that can be made, until depth == 0, or game is over
# it returns a score for the move
def minMax(board, depth, maxNode):

    # base case where we stop searching
    if depth == 0 or board.is_game_over():
        return evaluate_board(board) # get and return the score of the move

    # max node turn
    if maxNode:
        alpha = float("-inf")

        for i in board.legal_moves:
            board.push(i)

            score = minMax(board, depth-1, False)
            board.pop() # undo move to try next one

            best_score = max(alpha ,score)

        return best_score
    
    else: # minNode turn
        beta = float("inf")

        for i in board.legal_moves:
            board.push(i)

            score = minMax(board, depth-1, True)
            board.pop()
            best_score = min(beta, score)

        return best_score


# takes move scores from minMax, returns the score that the current node prefers
def find_best_move(board, depth):
    best_move = None

    maxNode = board.turn == chess.WHITE 

    if maxNode:
        alpha = float("-inf")
    else:
        beta = float("inf")

    for i in board.legal_moves:
        board.push(i)

        score = minMax(board, depth-1, not maxNode)

        board.pop()

        if maxNode:
            if score > alpha:
                alpha = score
                best_move = i
        else:
            if score < beta:
                beta = score
                best_move = i
    return best_move

def evaluate_board(board): # heuristc function for material peices only. Doesn't evaluate checkmate, or promotion

    values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}

    score = 0
    for i in board.piece_map().values():
        value = values[i.piece_type]

        if i.color == chess.WHITE:
            score += value
        else:
            score -= value

    return score
