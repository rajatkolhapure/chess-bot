from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class GameController:
    """Controls the chess game flow and manages game state."""
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'
        self.white_king_pos = (7, 4)  # Track king positions for check detection
        self.black_king_pos = (0, 4)
        self.last_move = None  # Track last move for en passant
        self.ai_player = None  # Color that AI plays as ('white', 'black', or None for human vs human)
        self.ai_engine = None
        self._setup_initial_board()
    
    def set_ai_player(self, color: str, ai_engine) -> None:
        """Set up AI player and its engine."""
        self.ai_player = color
        self.ai_engine = ai_engine

    def _can_castle(self, king, side: str) -> bool:
        """Check if castling is legal for the given king and side."""
        if king.has_moved:
            return False

        row = 7 if king.color == 'white' else 0
        rook_col = 0 if side == 'queenside' else 7
        rook = self.board.get_piece(row, rook_col)

        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        # Check if path is clear
        start_col = 1 if side == 'queenside' else 5
        end_col = 4 if side == 'queenside' else 7
        step = 1 if side == 'queenside' else -1

        # Check squares between king and rook are empty
        for col in range(start_col, end_col, step):
            if self.board.get_piece(row, col) is not None:
                return False

        # Check if king passes through check
        king_path = range(4, 2 if side == 'queenside' else 6, -1 if side == 'queenside' else 1)
        for col in king_path:
            # Temporarily move king
            original_pos = (row, 4)
            self.board.move_piece(row, 4, row, col)
            if king.color == 'white':
                self.white_king_pos = (row, col)
            else:
                self.black_king_pos = (row, col)

            # Check if position is safe
            in_check = self.is_check(king.color)

            # Move king back
            self.board.move_piece(row, col, *original_pos)
            if king.color == 'white':
                self.white_king_pos = original_pos
            else:
                self.black_king_pos = original_pos

            if in_check:
                return False

        return True

    def _handle_castling(self, king, from_pos: tuple, to_pos: tuple) -> bool:
        """Handle castling move if valid."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Check if it's a castling move
        if abs(to_col - from_col) == 2:
            side = 'queenside' if to_col < from_col else 'kingside'
            if not self._can_castle(king, side):
                return False

            # Move rook
            rook_from_col = 0 if side == 'queenside' else 7
            rook_to_col = 3 if side == 'queenside' else 5
            rook = self.board.get_piece(from_row, rook_from_col)
            self.board.move_piece(from_row, rook_from_col, from_row, rook_to_col)
            rook.has_moved = True

            return True

        return False

    def _handle_promotion(self, piece, to_pos: tuple) -> None:
        """Handle pawn promotion."""
        to_row, to_col = to_pos
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and to_row == 0) or (piece.color == 'black' and to_row == 7):
                # Automatically promote to Queen for now
                self.board.place_piece(to_row, to_col, Queen(piece.color))
    
    def _setup_initial_board(self):
        """Setup the initial board with all pieces."""
        # Place white pieces
        self.board.place_piece(7, 0, Rook('white'))    # Left Rook
        self.board.place_piece(7, 1, Knight('white'))  # Left Knight
        self.board.place_piece(7, 2, Bishop('white'))  # Left Bishop
        self.board.place_piece(7, 3, Queen('white'))   # Queen
        self.board.place_piece(7, 4, King('white'))    # King
        self.board.place_piece(7, 5, Bishop('white'))  # Right Bishop
        self.board.place_piece(7, 6, Knight('white'))  # Right Knight
        self.board.place_piece(7, 7, Rook('white'))    # Right Rook
        
        # Place white pawns
        for i in range(8):
            self.board.place_piece(6, i, Pawn('white'))
        
        # Place black pieces
        self.board.place_piece(0, 0, Rook('black'))    # Left Rook
        self.board.place_piece(0, 1, Knight('black'))  # Left Knight
        self.board.place_piece(0, 2, Bishop('black'))  # Left Bishop
        self.board.place_piece(0, 3, Queen('black'))   # Queen
        self.board.place_piece(0, 4, King('black'))    # King
        self.board.place_piece(0, 5, Bishop('black'))  # Right Bishop
        self.board.place_piece(0, 6, Knight('black'))  # Right Knight
        self.board.place_piece(0, 7, Rook('black'))    # Right Rook
        
        # Place black pawns
        for i in range(8):
            self.board.place_piece(1, i, Pawn('black'))
    
    def is_check(self, color: str) -> bool:
        """Check if the specified color's king is in check."""
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        opponent_color = 'black' if color == 'white' else 'white'
        
        # Check all opponent's pieces for possible attacks on the king
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    moves = piece.get_possible_moves(row, col, self.board)
                    if king_pos in moves:
                        return True
        return False
    
    def get_board_str(self) -> str:
        """Get string representation of the current board."""
        return str(self.board)
    
    def _parse_position(self, pos: str) -> tuple:
        """Convert chess notation (e.g., 'e2') to board indices."""
        if len(pos) != 2:
            raise ValueError("Invalid position format")
        
        col = ord(pos[0].lower()) - ord('a')
        row = 8 - int(pos[1])
        
        if not (0 <= row <= 7 and 0 <= col <= 7):
            raise ValueError("Invalid position")
        
        return row, col
    
    def make_move(self, from_pos: str, to_pos: str) -> bool:
        """
        Make a move using chess notation (e.g., 'e2 e4').
        Returns True if move was successful, False otherwise.
        """
        try:
            from_row, from_col = self._parse_position(from_pos)
            to_row, to_col = self._parse_position(to_pos)
            from_pos_tuple = (from_row, from_col)
            to_pos_tuple = (to_row, to_col)
            
            # Get the piece at the starting position
            piece = self.board.get_piece(from_row, from_col)
            
            if piece is None:
                print("No piece at the starting position")
                return False
            
            if piece.color != self.current_turn:
                print(f"It's {self.current_turn}'s turn")
                return False
            
            # Get possible moves for the piece
            possible_moves = piece.get_possible_moves(from_row, from_col, self.board)
            
            # Check if the move is valid
            if to_pos_tuple not in possible_moves:
                print("Invalid move for this piece")
                return False
            
            # Handle castling for king
            if isinstance(piece, King):
                if self._handle_castling(piece, from_pos_tuple, to_pos_tuple):
                    piece.has_moved = True
                if piece.color == 'white':
                    self.white_king_pos = to_pos_tuple
                else:
                    self.black_king_pos = to_pos_tuple
            
            # Reset en passant vulnerability for all pawns of the current color
            for r in range(8):
                for c in range(8):
                    p = self.board.get_piece(r, c)
                    if isinstance(p, Pawn) and p.color == self.current_turn:
                        p.en_passant_vulnerable = False
            
            # Make the move
            self.board.move_piece(from_row, from_col, to_row, to_col)
            
            # Handle pawn special moves
            if isinstance(piece, Pawn):
                # Handle en passant effects
                piece.move_effects(from_pos_tuple, to_pos_tuple, self.board)
                # Handle promotion
                self._handle_promotion(piece, to_pos_tuple)
            
            # Update piece move status
            if isinstance(piece, (King, Rook)):
                piece.has_moved = True
            
            # Check if the move puts the player in check (invalid move)
            if self.is_check(self.current_turn):
                # Undo the move
                self.board.move_piece(to_row, to_col, from_row, from_col)
                if isinstance(piece, King):  # Restore king position if it was a king move
                    if piece.color == 'white':
                        self.white_king_pos = from_pos_tuple
                    else:
                        self.black_king_pos = from_pos_tuple
                print("Invalid move: Would put you in check")
                return False
            
            # Store last move for en passant
            self.last_move = (piece, from_pos_tuple, to_pos_tuple)
            
            # Switch turns
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            
            # Check if the opponent is in check
            if self.is_check(self.current_turn):
                print(f"{self.current_turn.capitalize()} is in check!")
            
            return True
            
        except ValueError as e:
            print(f"Error: {e}")
            return False
    
    def get_current_turn(self) -> str:
        """Get the color of the player whose turn it is."""
        return self.current_turn

    def _get_all_valid_moves(self) -> list:
        """Get all valid moves for the current player."""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == self.current_turn:
                    moves = piece.get_possible_moves(row, col, self.board)
                    for move in moves:
                        # Test if move is legal (doesn't put king in check)
                        to_row, to_col = move
                        captured_piece = self.board.get_piece(to_row, to_col)
                        
                        # Make move
                        self.board.move_piece(row, col, to_row, to_col)
                        
                        # Check if move is legal
                        is_legal = not self.is_check(self.current_turn)
                        
                        # Undo move
                        self.board.move_piece(to_row, to_col, row, col)
                        if captured_piece:
                            self.board.place_piece(to_row, to_col, captured_piece)
                        
                        if is_legal:
                            valid_moves.append(((row, col), move))
        
        return valid_moves

    def is_ai_turn(self) -> bool:
        """Check if it's AI's turn to move."""
        return self.ai_player and self.current_turn == self.ai_player
    
    def make_ai_move(self) -> bool:
        """Make AI's move if it's AI's turn."""
        if not self.is_ai_turn():
            return False
            
        best_move = self.ai_engine.get_best_move()
        if not best_move:
            return False
            
        (from_row, from_col), (to_row, to_col) = best_move
        
        # Convert coordinates to chess notation
        from_pos = chr(from_col + ord('a')) + str(8 - from_row)
        to_pos = chr(to_col + ord('a')) + str(8 - to_row)
        
        # Make the move
        success = self.make_move(from_pos, to_pos)
        if success:
            print(f"AI moves: {from_pos} {to_pos}")
        return success