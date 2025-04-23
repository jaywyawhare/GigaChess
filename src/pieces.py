import chess


class PieceSquareTables:
    """Contains piece-square tables for positional evaluation."""

    # Pawn position values (8x8 board)
    pawn_table = [
        0,  0,  0,  0,  0,  0,  0,  0,    # 8th rank
        50, 50, 50, 50, 50, 50, 50, 50,   # 7th rank
        10, 10, 20, 30, 30, 20, 10, 10,   # 6th rank
        5,  5,  10, 25, 25, 10, 5,  5,    # 5th rank
        0,  0,  0,  20, 20, 0,  0,  0,    # 4th rank
        5,  -5, -10, 0,  0, -10, -5, 5,   # 3rd rank
        5,  10, 10,-20,-20, 10, 10, 5,    # 2nd rank
        0,  0,  0,  0,  0,  0,  0,  0     # 1st rank
    ]

    # Knight position values (8x8 board)
    knight_table = [
        -50,-40,-30,-30,-30,-30,-40,-50,  # 8th rank
        -40,-20, 0,  0,  0,  0, -20,-40,  # 7th rank
        -30, 0,  10, 15, 15, 10, 0, -30,  # 6th rank
        -30, 5,  15, 20, 20, 15, 5, -30,  # 5th rank
        -30, 0,  15, 20, 20, 15, 0, -30,  # 4th rank
        -30, 5,  10, 15, 15, 10, 5, -30,  # 3rd rank
        -40,-20, 0,  5,  5,  0, -20,-40,  # 2nd rank
        -50,-40,-30,-30,-30,-30,-40,-50   # 1st rank
    ]

    @staticmethod
    def get_piece_value(piece_type, square, is_endgame=False):
        """Get the positional value for a piece at a given square.
        
        Args:
            piece_type: Type of the chess piece
            square: Square position (0-63)
            is_endgame: Whether the game is in endgame phase
            
        Returns:
            Position value for the given piece and square
        """
        if piece_type == chess.PAWN:
            return PieceSquareTables.pawn_table[square]
        elif piece_type == chess.KNIGHT:
            return PieceSquareTables.knight_table[square]
        return 0
