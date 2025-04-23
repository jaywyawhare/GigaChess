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

    # Bishop position values (8x8 board)
    bishop_table = [
        -20,-10,-10,-10,-10,-10,-10,-20,  # 8th rank
        -10,  0,  0,  0,  0,  0,  0,-10,  # 7th rank
        -10,  0,  5, 10, 10,  5,  0,-10,  # 6th rank
        -10,  5,  5, 10, 10,  5,  5,-10,  # 5th rank
        -10,  0, 10, 10, 10, 10,  0,-10,  # 4th rank
        -10, 10, 10, 10, 10, 10, 10,-10,  # 3rd rank
        -10,  5,  0,  0,  0,  0,  5,-10,  # 2nd rank
        -20,-10,-10,-10,-10,-10,-10,-20   # 1st rank
    ]

    # Rook position values (8x8 board)
    rook_table = [
        0,  0,  0,  0,  0,  0,  0,  0,    # 8th rank
        5,  10, 10, 10, 10, 10, 10, 5,    # 7th rank
        -5,  0,  0,  0,  0,  0,  0, -5,   # 6th rank
        -5,  0,  0,  0,  0,  0,  0, -5,   # 5th rank
        -5,  0,  0,  0,  0,  0,  0, -5,   # 4th rank
        -5,  0,  0,  0,  0,  0,  0, -5,   # 3rd rank
        -5,  0,  0,  0,  0,  0,  0, -5,   # 2nd rank
        0,  0,  0,  5,  5,  0,  0,  0     # 1st rank
    ]

    # Queen position values (8x8 board)
    queen_table = [
        -20,-10,-10, -5, -5,-10,-10,-20,  # 8th rank
        -10,  0,  0,  0,  0,  0,  0,-10,  # 7th rank
        -10,  0,  5,  5,  5,  5,  0,-10,  # 6th rank
        -5,   0,  5,  5,  5,  5,  0, -5,  # 5th rank
        0,    0,  5,  5,  5,  5,  0, -5,  # 4th rank
        -10,  5,  5,  5,  5,  5,  0,-10,  # 3rd rank
        -10,  0,  5,  0,  0,  0,  0,-10,  # 2nd rank
        -20,-10,-10, -5, -5,-10,-10,-20   # 1st rank
    ]

    # King position values (middle game, 8x8 board)
    king_middle_table = [
        -30,-40,-40,-50,-50,-40,-40,-30,  # 8th rank
        -30,-40,-40,-50,-50,-40,-40,-30,  # 7th rank
        -30,-40,-40,-50,-50,-40,-40,-30,  # 6th rank
        -30,-40,-40,-50,-50,-40,-40,-30,  # 5th rank
        -20,-30,-30,-40,-40,-30,-30,-20,  # 4th rank
        -10,-20,-20,-20,-20,-20,-20,-10,  # 3rd rank
        20,  20,   0,  0,  0,  0, 20, 20, # 2nd rank
        20,  30,  10,  0,  0, 10, 30, 20  # 1st rank
    ]

    # King position values (endgame, 8x8 board)
    king_endgame_table = [
        -50,-40,-30,-20,-20,-30,-40,-50,  # 8th rank
        -30,-20,-10,  0,  0,-10,-20,-30,  # 7th rank
        -30,-10, 20, 30, 30, 20,-10,-30,  # 6th rank
        -30,-10, 30, 40, 40, 30,-10,-30,  # 5th rank
        -30,-10, 30, 40, 40, 30,-10,-30,  # 4th rank
        -30,-10, 20, 30, 30, 20,-10,-30,  # 3rd rank
        -30,-30,  0,  0,  0,  0,-30,-30,  # 2nd rank
        -50,-30,-30,-30,-30,-30,-30,-50   # 1st rank
    ]

    # Piece table lookup dictionary
    tables = {
        chess.PAWN: pawn_table,
        chess.KNIGHT: knight_table,
        chess.BISHOP: bishop_table,
        chess.ROOK: rook_table,
        chess.QUEEN: queen_table,
        chess.KING: king_middle_table,  # Default to middle game
    }

    @staticmethod
    def get_piece_value(piece_type, square, color, is_endgame=False):
        """Get the positional value for a piece at a given square.
        
        Args:
            piece_type: Type of the chess piece
            square: Square position (0-63)
            color: Color of the piece (chess.WHITE or chess.BLACK)
            is_endgame: Whether the game is in endgame phase
            
        Returns:
            Position value for the given piece and square
        """
        # Get the appropriate table
        if piece_type == chess.KING and is_endgame:
            table = PieceSquareTables.king_endgame_table
        else:
            table = PieceSquareTables.tables.get(piece_type)
        
        if table is None:
            return 0

        # Flip square for black pieces
        if color == chess.BLACK:
            square = 63 - square
            
        return table[square]
