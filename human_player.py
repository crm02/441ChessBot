import chess

HELP_TEXT = """
Enter moves like e4, Nf3, O-O or e2e4
Commands: moves, board, undo, help, quit
"""


def parse_move(board, text):
    text = text.strip()
    try:
        return board.parse_san(text)
    except ValueError:
        pass
    try:
        move = chess.Move.from_uci(text.lower())
        if move in board.legal_moves:
            return move
    except ValueError:
        pass
    return None


def get_human_move(board):
    while True:
        side = "White" if board.turn == chess.WHITE else "Black"
        text = input(f"{side} to move: ").strip()
        if not text:
            continue
        cmd = text.lower()

        if cmd in ("quit", "exit", "q"):
            return None
        if cmd == "help":
            print(HELP_TEXT)
            continue
        if cmd == "board":
            print(board, "\n")
            continue
        if cmd == "moves":
            print(", ".join(board.san(m) for m in board.legal_moves), "\n")
            continue
        if cmd == "undo":
            # undo both the AI move and the player move
            if len(board.move_stack) >= 2:
                board.pop()
                board.pop()
                print(board, "\n")
            else:
                print("Nothing to undo.\n")
            continue

        move = parse_move(board, text)
        if move is None:
            print(f"{text} is not a legal move\n")
            continue
        return move


def choose_color():
    while True:
        c = input("Play as white or black? (w/b): ").strip().lower()
        if c in ("w", "white"):
            return chess.WHITE
        if c in ("b", "black"):
            return chess.BLACK


def play_game(ai_move_fn, depth=3):
    board = chess.Board()
    human = choose_color()
    print(HELP_TEXT)

    while not board.is_game_over():
        print(board, "\n")
        if board.turn == human:
            move = get_human_move(board)
            if move is None:
                return
            print(f"You played {board.san(move)}\n")
            board.push(move)
        else:
            move = ai_move_fn(board, depth)
            print(f"AI plays {board.san(move)}\n")
            board.push(move)

    print(board)
    print("Game over:", board.result())


if __name__ == "__main__":
    from alpha_beta import find_best_move_alpha_beta
    play_game(find_best_move_alpha_beta, depth=3)