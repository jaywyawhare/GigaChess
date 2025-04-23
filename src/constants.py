import chess

# Piece values used across the engine
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

# Search parameters
MAX_QUIESCENCE_DEPTH = 5
DEFAULT_SEARCH_DEPTH = 3
