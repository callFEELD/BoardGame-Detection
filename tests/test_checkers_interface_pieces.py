import unittest
from src.checkers_interface import Piece,\
    InvalidPlayer, InvalidPiecePosition


class TestPieceInterface(unittest.TestCase):

    def test_set_correct_position(self):
        position = 5
        piece = Piece()
        piece.set_position(position)

        self.assertEqual(piece.get_position(), position)

    def test_set_wrong_position1(self):
        position = 0
        piece = Piece()
        self.assertRaises(InvalidPiecePosition, piece.set_position, position)

    def test_set_wrong_position2(self):
        position = 33
        piece = Piece()
        self.assertRaises(InvalidPiecePosition, piece.set_position, position)

    def test_set_correct_player(self):
        player = 2
        piece = Piece()
        piece.set_player(player)

        self.assertEqual(piece.get_player(), player)

    def test_set_wrong_player1(self):
        player = 0
        piece = Piece()
        self.assertRaises(InvalidPlayer, piece.set_player, player)

    def test_set_wrong_player2(self):
        player = 3
        piece = Piece()
        self.assertRaises(InvalidPlayer, piece.set_player, player)

    def test_set_king(self):
        king = True
        piece = Piece()
        piece.set_king(king)
        self.assertEqual(piece.is_king(), king)

    def test_set_everything_correct(self):
        position = 25
        player = 2
        king = True
        piece = Piece(position=position, player=player, king=king)

        self.assertEqual(piece.get_player(), player)
        self.assertEqual(piece.get_position(), position)
        self.assertEqual(piece.is_king(), king)


if __name__ == "__main__":
    unittest.main()
