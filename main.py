import chess
import os
from src.pieces import PieceSquareTables
from src.search import MinimaxSearch
from src.validator import MoveValidator
from src.evaluator import Evaluator

ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), "assets")


class ChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.piece_squares = PieceSquareTables()
        self.evaluator = Evaluator(self.piece_squares)
        self.search = MinimaxSearch(self.evaluator.evaluate)
        self.validator = MoveValidator()

    def get_valid_moves(self):
        return list(self.board.legal_moves)

    def make_move(self):
        move = self.search.find_best_move(self.board)
        if move and self.validator.is_legal_move(self.board, move):
            return move
        return None


def main():
    engine = ChessEngine()

    while not engine.board.is_game_over():
        print(engine.board)
        print("\nCurrent evaluation:", engine.evaluator.evaluate(engine.board))

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
