import chess
from .constants import PIECE_VALUES


class Evaluator:
    """Chess position evaluator."""

    def __init__(self, piece_squares):
        self.piece_squares = piece_squares

    def evaluate(self, board):
        """Evaluate the current position."""
        # Detect endgame
        is_endgame = self._is_endgame(board)

        score = 0
        # Calculate material and position scores
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue

            value = PIECE_VALUES[piece.piece_type]
            # Add position value
            value += self.piece_squares.get_piece_value(
                piece.piece_type, square, piece.color, is_endgame
            )

            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

        return score

    def _is_endgame(self, board):
        """Check if the position is in endgame phase."""
        queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(
            board.pieces(chess.QUEEN, chess.BLACK)
        )
        material = self._get_material_count(
            board, chess.WHITE
        ) + self._get_material_count(board, chess.BLACK)
        return (
            queens == 0 or material <= 2600
        )  # 2600 = 2 rooks + 1 minor piece per side

    def _get_material_count(self, board, color):
        """Calculate total material value for given color."""
        material = 0
        for piece_type, value in PIECE_VALUES.items():
            if piece_type != chess.KING:  # Exclude king from material count
                material += len(board.pieces(piece_type, color)) * value
        return material
