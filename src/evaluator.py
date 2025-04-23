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

        # Add king safety evaluation
        score += self._evaluate_king_safety(board, chess.WHITE)
        score -= self._evaluate_king_safety(board, chess.BLACK)

        # Add pawn structure evaluation
        score += self._evaluate_pawn_structure(board, chess.WHITE)
        score -= self._evaluate_pawn_structure(board, chess.BLACK)

        # Add piece mobility
        score += self._evaluate_mobility(board, chess.WHITE)
        score -= self._evaluate_mobility(board, chess.BLACK)

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

    def _evaluate_king_safety(self, board, color):
        """Evaluate king safety based on pawn shield and attacking pieces."""
        king_square = board.king(color)
        if king_square is None:
            return 0

        score = 0

        # Pawn shield
        pawn_shield_score = 0
        relative_squares = [-8, -7, -9] if color == chess.WHITE else [8, 7, 9]
        for offset in relative_squares:
            shield_square = king_square + offset
            if 0 <= shield_square < 64:
                if board.piece_at(shield_square) == chess.Piece(chess.PAWN, color):
                    pawn_shield_score += 10

        # Attacking pieces
        attacking_pieces = len(
            [
                sq
                for sq in board.attacks(king_square)
                if board.piece_at(sq) and board.piece_at(sq).color != color
            ]
        )
        attack_score = -15 * attacking_pieces

        return pawn_shield_score + attack_score

    def _evaluate_pawn_structure(self, board, color):
        """Evaluate pawn structure for given color."""
        score = 0
        pawns = board.pieces(chess.PAWN, color)

        # Evaluate doubled pawns
        files = [0] * 8
        for pawn in pawns:
            files[chess.square_file(pawn)] += 1
        doubled_pawns = sum(f - 1 for f in files if f > 1)
        score -= doubled_pawns * 20

        # Evaluate isolated pawns
        for pawn in pawns:
            file = chess.square_file(pawn)
            isolated = True
            for adj_file in [file - 1, file + 1]:
                if 0 <= adj_file < 8:
                    if any(chess.square_file(p) == adj_file for p in pawns):
                        isolated = False
                        break
            if isolated:
                score -= 15

        return score

    def _evaluate_mobility(self, board, color):
        """Evaluate piece mobility for given color."""
        score = 0
        saved_turn = board.turn
        board.turn = color

        # Count legal moves for each piece
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            pieces = board.pieces(piece_type, color)
            for piece_square in pieces:
                moves = len(
                    [
                        move
                        for move in board.legal_moves
                        if move.from_square == piece_square
                    ]
                )
                score += moves * 2  # 2 points per legal move

        board.turn = saved_turn
        return score
