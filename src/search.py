import chess
from .move_ordering import MoveOrdering


class SearchAlgorithm:
    """Base class for chess search algorithms."""

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def find_best_move(self, board):
        raise NotImplementedError


class MinimaxSearch(SearchAlgorithm):
    """Minimax search with alpha-beta pruning and quiescence."""

    def __init__(self, evaluator, depth=3):  # Increased default depth
        super().__init__(evaluator)
        self.depth = depth
        self.MAX_QUIESCENCE_DEPTH = 5  # Limit quiescence search depth
        self.move_ordering = MoveOrdering()

    def find_best_move(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        best_move = None
        best_score = float("-inf")

        # Sort moves before searching
        ordered_moves = MoveOrdering.sort_moves(board, legal_moves)

        for move in ordered_moves:
            board.push(move)
            score = -self._minimax(
                board, self.depth - 1, float("-inf"), float("inf"), False
            )
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self._quiescence(
                board, alpha, beta, maximizing_player, self.MAX_QUIESCENCE_DEPTH
            )

        ordered_moves = MoveOrdering.sort_moves(board, board.legal_moves)

        if maximizing_player:
            max_eval = float("-inf")
            for move in ordered_moves:
                board.push(move)
                eval = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in ordered_moves:
                board.push(move)
                eval = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _quiescence(self, board, alpha, beta, maximizing_player, depth):
        """Quiescence search to evaluate only capture moves."""
        stand_pat = self.evaluator(board)

        if depth == 0:
            return stand_pat

        if maximizing_player:
            max_eval = stand_pat
            if max_eval >= beta:
                return max_eval
            alpha = max(alpha, max_eval)
        else:
            min_eval = stand_pat
            if min_eval <= alpha:
                return min_eval
            beta = min(beta, min_eval)

        # Only look at capture moves
        captures = [move for move in board.legal_moves if board.is_capture(move)]
        ordered_captures = MoveOrdering.sort_moves(board, captures)

        if not captures:
            return stand_pat

        if maximizing_player:
            for move in ordered_captures:
                board.push(move)
                eval = self._quiescence(board, alpha, beta, False, depth - 1)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            for move in ordered_captures:
                board.push(move)
                eval = self._quiescence(board, alpha, beta, True, depth - 1)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
