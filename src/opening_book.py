"""Opening book implementation for chess engine."""

__all__ = ['OpeningBook']  # Add explicit export

class OpeningBook:
    """Manages chess opening book moves."""

    def __init__(self):
        """Initialize the opening book database."""
        self.openings = {
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1': [
                ((6, 4), (4, 4)),  # e2-e4
                ((6, 3), (4, 3)),  # d2-d4
                ((6, 2), (4, 2))   # c2-c4
            ],
            'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1': [
                ((1, 4), (3, 4)),  # e7-e5
                ((1, 2), (3, 2)),  # c7-c5
                ((1, 5), (3, 5))   # f7-f5
            ],
            'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1': [
                ((1, 4), (3, 4)),  # e7-e5
                ((1, 2), (3, 2)),  # c7-c5
                ((1, 5), (3, 5))   # f7-f5
            ],
            'rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1': [
                ((1, 4), (3, 4)),  # e7-e5
                ((1, 2), (3, 2)),  # c7-c5
                ((1, 5), (3, 5))   # f7-f5
            ]
        }

    def get_fen(self, board, current_color: str) -> str:
        """Generate FEN string for the current board position."""
        fen = []
        for row in range(8):
            empty_squares = 0
            row_fen = ''
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    if empty_squares:
                        row_fen += str(empty_squares)
                        empty_squares = 0
                    row_fen += piece.symbol
                else:
                    empty_squares += 1
            if empty_squares:
                row_fen += str(empty_squares)
            fen.append(row_fen)
        position = '/'.join(fen)
        return f"{position} {'w' if current_color == 'white' else 'b'} KQkq - 0 1"

    def get_book_move(self, board, current_color: str) -> tuple:
        """Get a book move for the current position if available."""
        fen = self.get_fen(board, current_color)
        if fen in self.openings:
            return self.openings[fen][0]
        return None
