from pieces import Pawn, Knight, Bishop, Rook, Queen, King

class AIEngine:
    """Chess AI engine implementing minimax algorithm."""
    
    # Basic piece values for evaluation
    PIECE_VALUES = {
        Pawn: 1,
        Knight: 3,
        Bishop: 3,
        Rook: 5,
        Queen: 9,
        King: 0  # King's value isn't used in material counting
    }
    
    # Piece square tables for positional evaluation
    PAWN_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]

    KNIGHT_TABLE = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    BISHOP_TABLE = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    ROOK_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ]
    
    def __init__(self, game_controller, color: str):
        self.game = game_controller
        self.color = color
        self.max_depth = 2  # Initial simple depth for minimax
    
    def get_best_move(self) -> tuple:
        """Find the best move using minimax algorithm."""
        best_score = float('-inf')
        best_move = None
        board = self.game.board
        
        # Get all possible moves for AI's pieces
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == self.color:
                    moves = piece.get_possible_moves(row, col, board)
                    for move in moves:
                        possible_moves.append(((row, col), move))
        
        # Evaluate each move
        for from_pos, to_pos in possible_moves:
            # Make move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            captured_piece = board.get_piece(to_row, to_col)
            piece = board.get_piece(from_row, from_col)
            
            board.move_piece(from_row, from_col, to_row, to_col)
            
            # Get score for this move
            score = -self._minimax(self.max_depth - 1, float('-inf'), float('inf'), False)
            
            # Undo move
            board.move_piece(to_row, to_col, from_row, from_col)
            if captured_piece:
                board.place_piece(to_row, to_col, captured_piece)
            
            # Update best move if necessary
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
        
        return best_move
    
    def _minimax(self, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0:
            return self._evaluate_position()
        
        board = self.game.board
        moves = []
        
        # Get all possible moves
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == (self.color if is_maximizing else self._opponent_color()):
                    piece_moves = piece.get_possible_moves(row, col, board)
                    for move in piece_moves:
                        moves.append(((row, col), move))
        
        if is_maximizing:
            max_eval = float('-inf')
            for from_pos, to_pos in moves:
                from_row, from_col = from_pos
                to_row, to_col = to_pos
                captured_piece = board.get_piece(to_row, to_col)
                piece = board.get_piece(from_row, from_col)
                
                board.move_piece(from_row, from_col, to_row, to_col)
                eval = self._minimax(depth - 1, alpha, beta, False)
                board.move_piece(to_row, to_col, from_row, from_col)
                if captured_piece:
                    board.place_piece(to_row, to_col, captured_piece)
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for from_pos, to_pos in moves:
                from_row, from_col = from_pos
                to_row, to_col = to_pos
                captured_piece = board.get_piece(to_row, to_col)
                piece = board.get_piece(from_row, from_col)
                
                board.move_piece(from_row, from_col, to_row, to_col)
                eval = self._minimax(depth - 1, alpha, beta, True)
                board.move_piece(to_row, to_col, from_row, from_col)
                if captured_piece:
                    board.place_piece(to_row, to_col, captured_piece)
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def _evaluate_position(self) -> float:
        """
        Enhanced position evaluation based on:
        1. Material count
        2. Piece positioning using piece-square tables
        3. Check status
        Positive score favors AI, negative score favors opponent.
        """
        score = 0
        board = self.game.board
        
        # Count material and evaluate piece positions
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    # Base material value
                    value = self.PIECE_VALUES[type(piece)]
                    
                    # Add positional value based on piece-square tables
                    pos_value = 0
                    piece_row = row if piece.color == 'black' else 7 - row  # Flip table for black pieces
                    
                    if isinstance(piece, Pawn):
                        pos_value = self.PAWN_TABLE[piece_row][col]
                    elif isinstance(piece, Knight):
                        pos_value = self.KNIGHT_TABLE[piece_row][col]
                    elif isinstance(piece, Bishop):
                        pos_value = self.BISHOP_TABLE[piece_row][col]
                    elif isinstance(piece, Rook):
                        pos_value = self.ROOK_TABLE[piece_row][col]
                    
                    # Apply values based on piece color
                    if piece.color == self.color:
                        score += value + (pos_value * 0.1)  # Positional value is 10% of material value
                    else:
                        score -= value + (pos_value * 0.1)
        
        # Check status
        if self.game.is_check(self.color):
            score -= 2  # Being in check is bad
        if self.game.is_check(self._opponent_color()):
            score += 2  # Putting opponent in check is good
        
        return score
    
    def _opponent_color(self) -> str:
        """Get opponent's color."""
        return 'black' if self.color == 'white' else 'white'