class Board:
    """Represents a chess board with basic functionality for piece placement and movement."""
    
    def __init__(self):
        # Initialize an 8x8 board with None representing empty squares
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
    def __str__(self):
        """Returns ASCII representation of the board."""
        result = []
        # Add column labels
        result.append("   a b c d e f g h")
        result.append("   ---------------")
        
        # Add rows with row numbers
        for i in range(8):
            row = f"{8-i} |"
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    row += "."
                else:
                    row += str(piece)
                row += " "
            row = row.rstrip()  # Remove trailing space
            row += "|"
            result.append(row)
        
        result.append("   ---------------")
        result.append("   a b c d e f g h")
        
        return "\n".join(result)
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if the given position is valid on the board."""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_piece(self, row: int, col: int):
        """Get the piece at the given position."""
        if not self.is_valid_position(row, col):
            raise ValueError("Invalid board position")
        return self.board[row][col]
    
    def place_piece(self, row: int, col: int, piece):
        """Place a piece at the given position."""
        if not self.is_valid_position(row, col):
            raise ValueError("Invalid board position")
        self.board[row][col] = piece
    
    def remove_piece(self, row: int, col: int):
        """Remove and return the piece at the given position."""
        if not self.is_valid_position(row, col):
            raise ValueError("Invalid board position")
        piece = self.board[row][col]
        self.board[row][col] = None
        return piece
    
    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int):
        """Move a piece from one position to another."""
        if not (self.is_valid_position(from_row, from_col) and 
                self.is_valid_position(to_row, to_col)):
            raise ValueError("Invalid board position")
        
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            raise ValueError("No piece at source position")
        
        self.remove_piece(from_row, from_col)
        self.place_piece(to_row, to_col, piece)