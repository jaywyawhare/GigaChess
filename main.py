import chess
import random
import os
from src.pieces import PieceSquareTables

# Add assets folder constant
ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), "assets")


class ChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.piece_squares = PieceSquareTables()

    def get_valid_moves(self):
        return list(self.board.legal_moves)

    def make_move(self):
        legal_moves = self.get_valid_moves()
        if not legal_moves:
            return None

        best_move = None
        best_score = float("-inf")

        for move in legal_moves:
            self.board.push(move)
            score = -self.minimax(2, float("-inf"), float("inf"), False)
            self.board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_position()

        if maximizing_player:
            max_eval = float("-inf")
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_position(self):
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000,
        }

        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if not piece:
                continue

            value = piece_values[piece.piece_type]
            if piece.piece_type == chess.PAWN:
                value += self.piece_squares.pawn_table[square]
            elif piece.piece_type == chess.KNIGHT:
                value += self.piece_squares.knight_table[square]

            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

        return score


def main():
    engine = ChessEngine()

    while not engine.board.is_game_over():
        print(engine.board)
        print("\nCurrent evaluation:", engine.evaluate_position())

        move = engine.make_move()
        if move:
            engine.board.push(move)
            print(f"Move made: {move}")
        else:
            break

    print("\nGame Over")
    print("Result:", engine.board.result())


if __name__ == "__main__":
    main()
