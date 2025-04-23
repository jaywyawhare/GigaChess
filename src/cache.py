import chess


class TranspositionTable:
    """Cache for storing evaluated positions."""

    def __init__(self, size=1000000):
        self.size = size
        self.table = {}

    def store(self, board, depth, score, flag, best_move=None):
        """Store position evaluation."""
        key = board.fen()
        if len(self.table) >= self.size:
            self.table.clear()  # Simple cleanup when full
        self.table[key] = {
            "depth": depth,
            "score": score,
            "flag": flag,
            "best_move": best_move,
        }

    def lookup(self, board):
        """Retrieve cached position if available."""
        return self.table.get(board.fen())
