import chess


class MoveValidator:
    """Validates chess moves and provides helper methods for move checking."""

    @staticmethod
    def is_valid_uci(uci_str):
        """Check if a string is a valid UCI move format."""
        try:
            move = chess.Move.from_uci(uci_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_legal_move(board, move):
        """Check if a move is legal in the current position."""
        return move in board.legal_moves

    @staticmethod
    def get_move_from_uci(uci_str):
        """Convert UCI string to chess.Move object. Returns None if invalid."""
        try:
            return chess.Move.from_uci(uci_str)
        except ValueError:
            return None

    @staticmethod
    def get_attacked_squares(board, color):
        """Get all squares attacked by a given color."""
        return [
            square for square in chess.SQUARES if board.is_attacked_by(color, square)
        ]

    @staticmethod
    def is_king_in_danger(board):
        """Check if the current side's king is in check or checkmate."""
        return board.is_check() or board.is_checkmate()

    @staticmethod
    def is_square_safe(board, square, color):
        """Check if a square is safe from enemy attacks."""
        return not board.is_attacked_by(not color, square)

    @staticmethod
    def get_safe_moves(board):
        """Get moves that don't move pieces to attacked squares unless capturing."""
        safe_moves = []
        for move in board.legal_moves:
            # Always allow captures
            if board.is_capture(move):
                safe_moves.append(move)
                continue

            # Check if destination square is safe
            if not board.is_attacked_by(not board.turn, move.to_square):
                safe_moves.append(move)

        return safe_moves
