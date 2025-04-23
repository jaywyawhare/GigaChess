import chess
import time
from .move_ordering import MoveOrdering
from .cache import TranspositionTable


class SearchAlgorithm:
    """Base class for chess search algorithms."""

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def find_best_move(self, board):
        raise NotImplementedError


class MinimaxSearch(SearchAlgorithm):
    """Minimax search with alpha-beta pruning and quiescence."""

    def __init__(self, evaluator, max_depth=4):  # Updated to include max_depth
        super().__init__(evaluator)
        self.max_depth = max_depth
        self.time_limit = 5  # 5 seconds per move
        self.depth = 3  # Default depth
        self.MAX_QUIESCENCE_DEPTH = 5  # Limit quiescence search depth
        self.move_ordering = MoveOrdering()
        self.tt = TranspositionTable()
        self.LMR_THRESHOLD = 3  # depth threshold for late move reduction
        self.FULL_DEPTH_MOVES = 4  # number of moves to search at full depth

    def find_best_move(self, board):
        start_time = time.time()
        best_move = None

        # Iterative deepening
        for depth in range(1, self.max_depth + 1):
            if time.time() - start_time > self.time_limit:
                break

            current_move = self._find_move_at_depth(board, depth)
            if current_move:
                best_move = current_move

        return best_move

    def _find_move_at_depth(self, board, depth):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        best_move = None
        best_score = float("-inf") if board.turn == chess.WHITE else float("inf")

        for move in legal_moves:
            board.push(move)
            # White maximizes, Black minimizes
            score = self._minimax(
                board,
                depth - 1,
                float("-inf"),
                float("inf"),
                board.turn == chess.WHITE,
            )
            board.pop()

            if board.turn == chess.WHITE:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move

    def _minimax(self, board, depth, alpha, beta, maximizing_player):
        # Try transposition table lookup
        tt_entry = self.tt.lookup(board)
        if tt_entry and tt_entry["depth"] >= depth:
            return tt_entry["score"]

        if depth == 0 or board.is_game_over():
            return self._quiescence(
                board, alpha, beta, maximizing_player, self.MAX_QUIESCENCE_DEPTH
            )

        best_move = None
        moves = list(board.legal_moves)
        moves = MoveOrdering.sort_moves(board, moves)

        if maximizing_player:
            max_eval = float("-inf")
            for i, move in enumerate(moves):
                board.push(move)

                # Late Move Reduction
                if (
                    depth >= self.LMR_THRESHOLD
                    and i >= self.FULL_DEPTH_MOVES
                    and not board.is_check()
                ):
                    eval = -self._minimax(board, depth - 2, -beta, -alpha, False)
                    if eval > alpha:  # Re-search if promising
                        eval = -self._minimax(board, depth - 1, -beta, -alpha, False)
                else:
                    eval = -self._minimax(board, depth - 1, -beta, -alpha, False)

                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if eval > max_eval:
                    best_move = move
                if beta <= alpha:
                    break

            # Store position in transposition table
            self.tt.store(board, depth, max_eval, "exact", best_move)
            return max_eval
        else:
            min_eval = float("inf")
            for move in moves:
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
