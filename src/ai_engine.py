from pieces import Pawn, Knight, Bishop, Rook, Queen, King
import time

class AIEngine:
    """Chess AI engine implementing minimax algorithm with advanced features."""
    
    # Basic piece values for evaluation
    PIECE_VALUES = {
        Pawn: 100,
        Knight: 320,
        Bishop: 330,
        Rook: 500,
        Queen: 900,
        King: 20000  # High value to prioritize king safety
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
        self.max_time = 5.0  # Maximum time in seconds for a move
        self.start_time = None
        self.nodes_searched = 0
        self.killer_moves = {}  # Store good moves that caused beta cutoffs
        self.history_table = {}  # Store move history scores
    
    def get_best_move(self) -> tuple:
        """Find the best move using iterative deepening."""
        self.start_time = time.time()
        self.nodes_searched = 0
        best_move = None
        best_score = float('-inf')
        max_depth = 1
        
        # Initialize history table for move ordering
        self.history_table = {}
        
        try:
            # Iterative deepening
            while time.time() - self.start_time < self.max_time:
                score, move = self._iterative_deepening(max_depth)
                if move:  # Only update if we found a valid move
                    best_move = move
                    best_score = score
                max_depth += 1
                
                # Print search statistics
                elapsed = time.time() - self.start_time
                print(f"Depth {max_depth-1}: Score {best_score:.2f}, "
                      f"Nodes: {self.nodes_searched}, Time: {elapsed:.2f}s")
        except TimeoutError:
            pass
        
        return best_move
    
    def _iterative_deepening(self, depth: int) -> tuple:
        """Perform iterative deepening search to the specified depth."""
        board = self.game.board
        best_move = None
        best_score = float('-inf')
        
        # Get all possible moves for AI's pieces
        possible_moves = self._get_ordered_moves(board)
        
        # Search each move
        for from_pos, to_pos in possible_moves:
            if time.time() - self.start_time >= self.max_time:
                raise TimeoutError
            
            # Make move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            captured_piece = board.get_piece(to_row, to_col)
            piece = board.get_piece(from_row, from_col)
            
            board.move_piece(from_row, from_col, to_row, to_col)
            
            # Get score for this move
            try:
                score = -self._negamax(depth - 1, float('-inf'), float('inf'), -1)
            except TimeoutError:
                board.move_piece(to_row, to_col, from_row, from_col)
                if captured_piece:
                    board.place_piece(to_row, to_col, captured_piece)
                raise
            
            # Undo move
            board.move_piece(to_row, to_col, from_row, from_col)
            if captured_piece:
                board.place_piece(to_row, to_col, captured_piece)
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
                
            # Update history table
            move_key = (from_pos, to_pos)
            self.history_table[move_key] = self.history_table.get(move_key, 0) + 2 ** depth
        
        return best_score, best_move
    
    def _negamax(self, depth: int, alpha: float, beta: float, color: int) -> float:
        """Negamax algorithm with alpha-beta pruning."""
        self.nodes_searched += 1
        
        if time.time() - self.start_time >= self.max_time:
            raise TimeoutError
        
        # Check if we should enter quiescence search
        if depth == 0:
            return color * self._quiescence(alpha, beta, color, 4)  # Max 4 ply quiescence
        
        board = self.game.board
        possible_moves = self._get_ordered_moves(board)
        
        if not possible_moves:  # No legal moves
            if self.game.is_check(self.color if color == 1 else self._opponent_color()):
                return -20000  # Checkmate
            return 0  # Stalemate
        
        max_score = float('-inf')
        for from_pos, to_pos in possible_moves:
            # Make move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            captured_piece = board.get_piece(to_row, to_col)
            piece = board.get_piece(from_row, from_col)
            
            board.move_piece(from_row, from_col, to_row, to_col)
            
            score = -self._negamax(depth - 1, -beta, -alpha, -color)
            
            # Undo move
            board.move_piece(to_row, to_col, from_row, from_col)
            if captured_piece:
                board.place_piece(to_row, to_col, captured_piece)
            
            # Update best score
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            
            # Beta cutoff
            if alpha >= beta:
                # Store killer move
                if not captured_piece:
                    self.killer_moves[depth] = (from_pos, to_pos)
                break
        
        return max_score
    
    def _quiescence(self, alpha: float, beta: float, color: int, depth: int) -> float:
        """Quiescence search to evaluate tactical positions."""
        if depth == 0:
            return color * self._evaluate_position()
        
        stand_pat = color * self._evaluate_position()
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
        
        # Get capturing moves only
        captures = self._get_capturing_moves(self.game.board)
        
        for from_pos, to_pos in captures:
            # Make capture
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            captured_piece = self.game.board.get_piece(to_row, to_col)
            piece = self.game.board.get_piece(from_row, from_col)
            
            self.game.board.move_piece(from_row, from_col, to_row, to_col)
            
            score = -self._quiescence(-beta, -alpha, -color, depth - 1)
            
            # Undo capture
            self.game.board.move_piece(to_row, to_col, from_row, from_col)
            self.game.board.place_piece(to_row, to_col, captured_piece)
            
            if score >= beta:
                return beta
            alpha = max(alpha, score)
        
        return alpha
    
    def _get_ordered_moves(self, board) -> list:
        """Get moves ordered by likelihood of being good."""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == self.color:
                    piece_moves = piece.get_possible_moves(row, col, board)
                    for move in piece_moves:
                        moves.append(((row, col), move))
        
        # Score moves for ordering
        scored_moves = []
        for from_pos, to_pos in moves:
            score = 0
            to_row, to_col = to_pos
            moving_piece = board.get_piece(from_pos[0], from_pos[1])
            captured_piece = board.get_piece(to_row, to_col)
            
            # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
            if captured_piece:
                score += (self.PIECE_VALUES[type(captured_piece)] - 
                         self.PIECE_VALUES[type(moving_piece)] / 100)
            
            # Killer move bonus
            if (from_pos, to_pos) in self.killer_moves.values():
                score += 9
            
            # History heuristic
            move_key = (from_pos, to_pos)
            score += self.history_table.get(move_key, 0) / 10000
            
            scored_moves.append((score, (from_pos, to_pos)))
        
        # Sort moves by score
        scored_moves.sort(reverse=True)
        return [move for score, move in scored_moves]
    
    def _get_capturing_moves(self, board) -> list:
        """Get only moves that capture pieces."""
        captures = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == self.color:
                    moves = piece.get_possible_moves(row, col, board)
                    for move in moves:
                        to_row, to_col = move
                        if board.get_piece(to_row, to_col) is not None:
                            captures.append(((row, col), move))
        return captures
    
    def _evaluate_position(self) -> float:
        """
        Enhanced position evaluation based on:
        1. Material count with refined values
        2. Piece positioning using piece-square tables
        3. King safety
        4. Check status
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
                        score += value + pos_value
                    else:
                        score -= value + pos_value
        
        # King safety: penalize exposed king
        king_safety = self._evaluate_king_safety(self.color) - self._evaluate_king_safety(self._opponent_color())
        score += king_safety * 50  # Weight king safety heavily
        
        # Check status
        if self.game.is_check(self.color):
            score -= 50  # Being in check is bad
        if self.game.is_check(self._opponent_color()):
            score += 50  # Putting opponent in check is good
        
        return score
    
    def _evaluate_king_safety(self, color: str) -> float:
        """Evaluate king safety for the given color."""
        king_pos = self.game.white_king_pos if color == 'white' else self.game.black_king_pos
        row, col = king_pos
        safety = 0
        
        # Check pawn shield
        pawn_directions = [-1, 0, 1]  # Check files left, same, and right of king
        rank_offset = -1 if color == 'white' else 1  # Check rank in front of king
        
        for file_offset in pawn_directions:
            new_col = col + file_offset
            new_row = row + rank_offset
            if (0 <= new_row <= 7 and 0 <= new_col <= 7):
                piece = self.game.board.get_piece(new_row, new_col)
                if isinstance(piece, Pawn) and piece.color == color:
                    safety += 1  # Point for each protecting pawn
        
        # Penalize for open files near king
        for file_offset in [-1, 0, 1]:
            new_col = col + file_offset
            if 0 <= new_col <= 7:
                has_friendly_piece = False
                for r in range(8):
                    piece = self.game.board.get_piece(r, new_col)
                    if piece and piece.color == color:
                        has_friendly_piece = True
                        break
                if not has_friendly_piece:
                    safety -= 1  # Penalty for each open file
        
        return safety
    
    def _opponent_color(self) -> str:
        """Get opponent's color."""
        return 'black' if self.color == 'white' else 'white'