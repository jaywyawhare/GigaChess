import chess
from .constants import PIECE_VALUES


class MoveOrdering:
    """Move ordering using MVV-LVA (Most Valuable Victim - Least Valuable Attacker)."""

    @staticmethod
    def score_move(board, move):
        """Score a move based on MVV-LVA."""
        score = 0

        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            if victim and attacker:
                # MVV-LVA score = Victim value - Attacker value/100
                score = PIECE_VALUES[victim.piece_type] - (
                    PIECE_VALUES[attacker.piece_type] / 100
                )

        # Bonus for promotions
        if move.promotion:
            score += PIECE_VALUES[move.promotion]

        return score

    @staticmethod
    def sort_moves(board, moves):
        """Sort moves using MVV-LVA scoring."""
        return sorted(
            moves, key=lambda move: MoveOrdering.score_move(board, move), reverse=True
        )
