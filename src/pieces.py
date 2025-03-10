from abc import ABC, abstractmethod

class Piece(ABC):
    """Abstract base class for chess pieces."""
    
    def __init__(self, color: str):
        """Initialize piece with color ('white' or 'black')."""
        if color not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")
        self.color = color
    
    @abstractmethod
    def __str__(self):
        """Return string representation of the piece."""
        pass
    
    @abstractmethod
    def get_possible_moves(self, row: int, col: int, board) -> list:
        """Return list of possible moves for the piece."""
        pass

class Pawn(Piece):
    """Represents a pawn chess piece."""
    
    def __init__(self, color: str):
        super().__init__(color)
        self.moved = False
        self.en_passant_vulnerable = False
    
    def __str__(self):
        """Unicode representation of the pawn."""
        return '♙' if self.color == 'white' else '♟'
    
    def get_possible_moves(self, row: int, col: int, board) -> list:
        """Get all possible moves for the pawn."""
        moves = []
        direction = -1 if self.color == 'white' else 1  # White pawns move up, black pawns move down
        
        # Forward move
        if board.is_valid_position(row + direction, col):
            if board.get_piece(row + direction, col) is None:
                moves.append((row + direction, col))
                
                # Initial two-square move
                if not self.moved:
                    if board.get_piece(row + 2 * direction, col) is None:
                        moves.append((row + 2 * direction, col))
        
        # Capture moves (diagonal)
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            new_row = row + direction
            
            if board.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                # Regular capture
                if target and target.color != self.color:
                    moves.append((new_row, new_col))
                # En passant capture
                elif (board.is_valid_position(row, new_col) and
                      isinstance(board.get_piece(row, new_col), Pawn) and
                      board.get_piece(row, new_col).en_passant_vulnerable):
                    moves.append((new_row, new_col))
        
        return moves
    
    def move_effects(self, from_pos: tuple, to_pos: tuple, board):
        """Handle special pawn move effects (en passant vulnerability, capture)."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check for two-square move (en passant vulnerability)
        if abs(to_row - from_row) == 2:
            self.en_passant_vulnerable = True
        else:
            self.en_passant_vulnerable = False
        
        # Handle en passant capture
        if abs(to_col - from_col) == 1 and board.get_piece(to_row, to_col) is None:
            # Remove the captured pawn
            board.remove_piece(from_row, to_col)
        
        self.moved = True

class Knight(Piece):
    """Represents a knight chess piece."""
    
    def __str__(self):
        """Unicode representation of the knight."""
        return '♘' if self.color == 'white' else '♞'
    
    def get_possible_moves(self, row: int, col: int, board) -> list:
        """Get all possible moves for the knight."""
        moves = []
        # All possible L-shaped moves
        knight_moves = [
            (-2, -1), (-2, 1),  # Two up, one left/right
            (2, -1), (2, 1),    # Two down, one left/right
            (-1, -2), (1, -2),  # One up/down, two left
            (-1, 2), (1, 2)     # One up/down, two right
        ]
        
        for move_row, move_col in knight_moves:
            new_row, new_col = row + move_row, col + move_col
            if board.is_valid_position(new_row, new_col):
                target_piece = board.get_piece(new_row, new_col)
                if target_piece is None or target_piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves

class Bishop(Piece):
    """Represents a bishop chess piece."""
    
    def __str__(self):
        """Unicode representation of the bishop."""
        return '♗' if self.color == 'white' else '♝'
    
    def get_possible_moves(self, row: int, col: int, board) -> list:
        """Get all possible moves for the bishop."""
        moves = []
        # Diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dir_row, dir_col in directions:
            current_row, current_col = row + dir_row, col + dir_col
            while board.is_valid_position(current_row, current_col):
                target_piece = board.get_piece(current_row, current_col)
                if target_piece is None:
                    moves.append((current_row, current_col))
                elif target_piece.color != self.color:
                    moves.append((current_row, current_col))
                    break
                else:
                    break
                current_row += dir_row
                current_col += dir_col
        
        return moves

class Queen(Piece):
    """Represents a queen chess piece."""
    
    def __str__(self):
        """Unicode representation of the queen."""
        return '♕' if self.color == 'white' else '♛'
    
    def get_possible_moves(self, row: int, col: int, board) -> list:
        """Get all possible moves for the queen (combination of rook and bishop moves)."""
        moves = []
        # All eight directions
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dir_row, dir_col in directions:
            current_row, current_col = row + dir_row, col + dir_col
            while board.is_valid_position(current_row, current_col):
                target_piece = board.get_piece(current_row, current_col)
                if target_piece is None:
                    moves.append((current_row, current_col))
                elif target_piece.color != self.color:
                    moves.append((current_row, current_col))
                    break
                else:
                    break
                current_row += dir_row
                current_col += dir_col
        
        return moves

class King(Piece):
    """Represents a king chess piece."""
    
    def __init__(self, color: str):
        super().__init__(color)
        self.has_moved = False  # For castling
    
    def __str__(self):
        """Unicode representation of the king."""
        return '♔' if self.color == 'white' else '♚'
    
    def get_possible_moves(self, row: int, col: int, board) -> list:
        """Get all possible moves for the king."""
        moves = []
        # All eight directions, one square at a time
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dir_row, dir_col in directions:
            new_row, new_col = row + dir_row, col + dir_col
            if board.is_valid_position(new_row, new_col):
                target_piece = board.get_piece(new_row, new_col)
                if target_piece is None or target_piece.color != self.color:
                    moves.append((new_row, new_col))
        
        # TODO: Add castling moves
        return moves

class Rook(Piece):
    """Represents a rook chess piece."""
    
    def __init__(self, color: str):
        super().__init__(color)
        self.has_moved = False  # For castling
    
    def __str__(self):
        """Unicode representation of the rook."""
        return '♖' if self.color == 'white' else '♜'
    
    def get_possible_moves(self, row: int, col: int, board) -> list:
        """Get all possible moves for the rook."""
        moves = []
        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dir_row, dir_col in directions:
            current_row, current_col = row + dir_row, col + dir_col
            while board.is_valid_position(current_row, current_col):
                target_piece = board.get_piece(current_row, current_col)
                if target_piece is None:
                    moves.append((current_row, current_col))
                elif target_piece.color != self.color:
                    moves.append((current_row, current_col))
                    break
                else:
                    break
                current_row += dir_row
                current_col += dir_col
        
        return moves