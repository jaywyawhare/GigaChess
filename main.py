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
        self.validator = MoveValidator()
        self.search = MinimaxSearch(self.evaluator.evaluate, self.validator)
        self.current_color = chess.WHITE

    def get_valid_moves(self):
        return list(self.board.legal_moves)

    def make_move(self):
        if self.board.turn != self.current_color:
            self.current_color = not self.current_color
            return None

        move = self.search.find_best_move(self.board)
        if move and self.validator.is_legal_move(self.board, move):
            self.current_color = not self.current_color
            return move
        return None


def main():
    engine = ChessEngine()
    white_to_move = True

    while not engine.board.is_game_over():
        print("\n" + str(engine.board))
        print(f"\n{'White' if white_to_move else 'Black'} to move")
        print("Current evaluation:", engine.evaluator.evaluate(engine.board))

        move = engine.make_move()
        if move:
            engine.board.push(move)
            print(f"Move made: {move}")
            white_to_move = not white_to_move
        else:
            break

    print("\nGame Over")
    print("Result:", engine.board.result())


if __name__ == "__main__":
    main()
