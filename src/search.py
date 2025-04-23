import chess


class SearchAlgorithm:
    """Base class for chess search algorithms."""

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def find_best_move(self, board):
        raise NotImplementedError


class MinimaxSearch(SearchAlgorithm):
    """Minimax search with alpha-beta pruning."""

    def __init__(self, evaluator, depth=2):
        super().__init__(evaluator)
        self.depth = depth

    def find_best_move(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        best_move = None
        best_score = float("-inf")

        for move in legal_moves:
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
        if depth == 0 or board.is_game_over():
            return self.evaluator(board)

        if maximizing_player:
            max_eval = float("-inf")
            for move in board.legal_moves:
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
            for move in board.legal_moves:
                board.push(move)
                eval = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
