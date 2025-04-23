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

# Evaluation parameters
DOUBLED_PAWN_PENALTY = -20
ISOLATED_PAWN_PENALTY = -15
MOBILITY_BONUS = 2
TIME_LIMIT = 5  # seconds per move
