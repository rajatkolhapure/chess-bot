"""Tests for the opening book implementation."""

import unittest
from src.board import Board
from src.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from src.opening_book import OpeningBook

class TestOpeningBook(unittest.TestCase):
    """Test cases for OpeningBook class."""
    
    def setUp(self):
        """Set up test environment."""
        self.board = Board()
        self.book = OpeningBook()
    
    def test_initial_position_fen(self):
        """Test FEN generation for initial position."""
        # Set up initial position
        self.board.setup_initial_position()
        fen = self.book.get_fen(self.board, 'white')
        expected_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.assertEqual(fen, expected_fen)
    
    def test_after_e4_fen(self):
        """Test FEN generation after 1. e4."""
        # Set up initial position
        self.board.setup_initial_position()
        # Move e2-e4
        self.board.move_piece(6, 4, 4, 4)
        fen = self.book.get_fen(self.board, 'black')
        expected_fen = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
        self.assertEqual(fen, expected_fen)
    
    def test_get_book_move_initial(self):
        """Test getting book move from initial position."""
        # Set up initial position
        self.board.setup_initial_position()
        move = self.book.get_book_move(self.board, 'white')
        # Should return one of the main opening moves (e4, d4, or c4)
        self.assertIn(move, [
            ((6, 4), (4, 4)),  # e2-e4
            ((6, 3), (4, 3)),  # d2-d4
            ((6, 2), (4, 2))   # c2-c4
        ])
    
    def test_get_book_move_after_e4(self):
        """Test getting book move after 1. e4."""
        # Set up position after e4
        self.board.setup_initial_position()
        self.board.move_piece(6, 4, 4, 4)  # e2-e4
        move = self.book.get_book_move(self.board, 'black')
        # Should return one of the main responses
        self.assertIn(move, [
            ((1, 4), (3, 4)),  # e7-e5
            ((1, 2), (3, 2)),  # c7-c5
            ((1, 5), (3, 5))   # f7-f5
        ])
    
    def test_get_book_move_unknown_position(self):
        """Test getting book move from position not in book."""
        # Set up a random position
        self.board.setup_initial_position()
        self.board.move_piece(6, 4, 4, 4)  # e2-e4
        self.board.move_piece(1, 4, 3, 4)  # e7-e5
        self.board.move_piece(7, 6, 5, 5)  # Nf3
        move = self.book.get_book_move(self.board, 'black')
        self.assertIsNone(move)

if __name__ == '__main__':
    unittest.main()
