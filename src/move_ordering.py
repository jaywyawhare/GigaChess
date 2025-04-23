import chess
from .constants import PIECE_VALUES


class MoveOrdering:
    """Move ordering using CCA (Check, Capture, Attack) and MVV-LVA (Most Valuable Victim - Least Valuable Attacker)."""

    @staticmethod
    def score_move(board, move):
        """Score a move based on CCA (Check, Capture, Attack) and MVV-LVA."""
        score = 0

        # Check moves get highest priority
        if board.gives_check(move):
            score += 10000

        # Captures using MVV-LVA
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            if victim and attacker:
                score += PIECE_VALUES[victim.piece_type] - (
                    PIECE_VALUES[attacker.piece_type] / 100
                )

        # Attacked square penalty
        if board.is_attacked_by(not board.turn, move.to_square):
            score -= PIECE_VALUES[board.piece_at(move.from_square).piece_type] / 2

        # Attack moves (moving to squares that attack enemy pieces)
        board.push(move)
        attacked_pieces = sum(
            1
            for sq in board.attacks(move.to_square)
            if board.piece_at(sq) and board.piece_at(sq).color != board.turn
        )
        board.pop()
        score += attacked_pieces * 50

        # Bonus for promotions
        if move.promotion:
            score += PIECE_VALUES[move.promotion]

        return score

    @staticmethod
    def sort_moves(board, moves):
        """Sort moves using CCA and MVV-LVA scoring."""
        return sorted(
            moves, key=lambda move: MoveOrdering.score_move(board, move), reverse=True
        )
